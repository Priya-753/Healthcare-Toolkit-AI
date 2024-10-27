import os
import time
from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
from threading import Thread
from deepgram.utils import verboselogs
import glob
import os

from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    LiveTranscriptionEvents,
    LiveOptions,
    Microphone,
)

from datetime import datetime
import requests
from werkzeug.utils import secure_filename
from generate_soap_notes import get_soap_notes
from open_dental import get_appointments, get_patients, get_patient, get_appointments_patient
from summarize_xray import get_image_summarization
from generate_cdt_codes import get_cdt_icd_codes
from pdf_fill import fill_form
import json

app = Flask(__name__)
CORS(app)
transcript = ""
is_recording = False

# Load your Deepgram API key
os.environ["DEEPGRAM_API_KEY"] = "edb91923000ca8b99ef02b362391b95b56ebefc3"
deepgram = DeepgramClient()

def save_transcript(patient_id, appointment_time, final_transcript):
    """Save the final transcript in a patient-specific folder."""
    # Create directory for the patient if it doesn't exist
    patient_folder = f'./{patient_id}'
    os.makedirs(patient_folder, exist_ok=True)

    # Create a filename with the appointment time
    filename = f"{patient_folder}/transcript_{appointment_time}.txt"
    
    # Save the transcript to the file
    with open(filename, 'w') as f:
        f.write(final_transcript)

def start_recording_helper(patient_id, appointment_time):
    global transcript, is_recording
    is_recording = True
    is_finals = []
    print("Starting recording")

    def on_message(self, result, **kwargs):
        global transcript
        sentence = result.channel.alternatives[0].transcript
        if len(sentence) == 0:
            return
        try:
            # print("HEYY", result.channel.alternatives[0])
            speaker_id = result.channel.alternatives[0].words[0].speaker
        except:
            speaker_id = -1
        if result.is_final:
            is_finals.append(f"Speaker {speaker_id}: " + result.channel.alternatives[0].transcript)
            transcript = "\n".join(is_finals)
            

            # Save the final transcript when speech is finalized
            if result.speech_final:
                print(transcript)
            #     save_transcript(patient_id, appointment_time, transcript)
            #     is_finals.clear()

    dg_connection = deepgram.listen.websocket.v("1")
    dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)

    options: LiveOptions = LiveOptions(
            model="nova-2",
            language="en-US",
            # Apply smart formatting to the output
            smart_format=True,
            # Raw audio format details
            encoding="linear16",
            channels=1,
            sample_rate=16000,
            # Time in milliseconds of silence to wait for before finalizing speech
            endpointing=200,
            diarize=True,
        )
    
    addons = {
        # Prevent waiting for additional numbers
        "no_delay": "true"
    }

    if dg_connection.start(options, addons=addons) is False:
        print("Failed to connect to Deepgram")
        return
    
    print("DG Connection Started")

    microphone = Microphone(dg_connection.send)
    microphone.start()
    print("Mic Started")

    # Keep the thread alive
    while is_recording:
        time.sleep(0.1)

    microphone.finish()
    print("Mic Stopped")
    dg_connection.finish()
    print("DG Connection Stopped")

def read_transcript(patient_id, appointment_time):
    """Read the transcript file for a specific patient and appointment time."""
    patient_folder = f'./{patient_id}'
    filename = f"{patient_folder}/transcript_{appointment_time}.txt"
    
    # Check if the file exists
    if not os.path.exists(filename):
        return None
    
    # Read and return the transcript content
    with open(filename, 'r') as f:
        content = f.read()
    
    return content

@app.route('/start-recording', methods=['POST'])
def start_recording():
    print("Recieved start request")
    global transcript
    global patient_id
    global appointment_time
    print("Hi")
    patient_id = request.json.get('patient_id')
    print("Patient ID")
    appointment_time = request.json.get('appointment_time')  # Format current time

    if not patient_id:
        return jsonify({"error": "patient_id is required"}), 400
    if not appointment_time:
        appointment_time = datetime.now().strftime('%Y-%m-%d')  # Format current time
    
    # Clear previous transcript
    transcript = ""
    
    # Start recording in a separate thread
    Thread(target=start_recording_helper, args=(patient_id, appointment_time), daemon=True).start()
    return jsonify({"message": "Recording started"}), 200

@app.route('/stop-recording', methods=['POST'])
def stop_recording():
    print("Recieved stop request")
    global is_recording
    is_recording = False
    save_transcript(patient_id, appointment_time, transcript)
    return jsonify({"message": "Recording stopped"}), 200

@app.route('/is-recording', methods=['GET'])
def is_recording():
    global is_recording
    return jsonify({"is_recording": is_recording}), 200


@app.route('/get-live-transcript', methods=['GET'])
def get_transcript():
    print("Recieved transcript request")
    global transcript
    return jsonify({"transcript": transcript}), 200

@app.route('/get-soap-notes', methods=['POST'])
def get_transcript_file():
    data = request.json
    patient_id = data.get('patient_id')
    appointment_time = data.get('appointment_time')

    if not patient_id or not appointment_time:
        return jsonify({"error": "patient_id and appointment_time are required"}), 400
    
    fname = f"./{patient_id}/{appointment_time}_soapnotes"
    if os.path.exists(fname):
        with open(fname, 'r') as file:
            processed_result = ' '.join(file.readlines())
            return jsonify({"message": processed_result}), 200

    # Read the transcript content
    transcript_content = read_transcript(patient_id, appointment_time)
    
    if transcript_content is None:
        return jsonify({"error": "Transcript file not found"}), 404

    # Call a function to process the transcript
    processed_result = get_soap_notes(patient_id, appointment_time, transcript_content)
    with open(fname, 'w') as file:  # Use 'w' mode to write text files
            file.write(processed_result)
    
    return jsonify({"message": processed_result}), 200

@app.route('/get-cdt-codes', methods=['POST'])
def get_cdt_file():
    data = request.json
    patient_id = data.get('patient_id')
    appointment_time = data.get('appointment_time')

    if not patient_id or not appointment_time:
        return jsonify({"error": "patient_id and appointment_time are required"}), 400
    
    ff = f"./{patient_id}/{appointment_time}_cdtcodes"
    if os.path.exists(ff):
        with open(ff, 'r') as file:
            codes = json.load(file)
            return jsonify(codes), 200
    
    fname = f"./{patient_id}/{appointment_time}_soapnotes"
    soapnotes = None
    if os.path.exists(fname):
        with open(fname, 'r') as file:
            soapnotes = ' '.join(file.readlines())

    # Read the transcript content
    transcript_content = read_transcript(patient_id, appointment_time)
    
    if transcript_content is None or soapnotes is None:
        return jsonify({"error": "Transcript or soapnotes file not found"}), 404

    # Call a function to process the transcript
    codes = get_cdt_icd_codes(transcript_content, soapnotes)
    with open(ff, 'w') as file:  # Use 'w' mode to write text files
            json.dump(codes, file)
    
    return jsonify(codes), 200

@app.route('/appointments', methods=['GET'])
def appointments():
    # Get start_date and end_date from query parameters
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    # Check if both parameters are provided
    if not start_date or not end_date:
        return jsonify({"error": "start_date and end_date are required"}), 400

    return jsonify(get_appointments(start_date, end_date))

@app.route('/appointments-patient', methods=['GET'])
def appointments_patient():
    # Get start_date and end_date from query parameters
    patient_id = request.args.get('patient_id')

    # Check if both parameters are provided
    if not patient_id:
        return jsonify({"error": "patient_id is required"}), 400

    return jsonify(get_appointments_patient(patient_id))

@app.route('/calls', methods=['GET'])
def get_calls():
    url = "https://api.vapi.ai/call"
    headers = {
        "Authorization": f"Bearer 341df6d3-14d7-46fa-8fb1-76bad94a77b5"
    }

    response = requests.get(url, headers=headers, params={})
    return jsonify(response.json())

@app.route('/patients', methods=['GET'])
def patients():
    return jsonify(get_patients())

@app.route('/one-patient', methods=['GET'])
def one_patient():
    patient_id = request.args.get('patient_id')
    if not patient_id:
        return jsonify({"error": "patient_id required"}), 400
    return jsonify(get_patient(patient_id))

@app.route('/upload-image', methods=['POST'])
def upload_image():
    patient_id = request.form.get('patient_id')
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image = request.files['image']
    if image.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if patient_id:
        # Create folder for the patient if it doesn't exist
        patient_folder = f'./{patient_id}'
        os.makedirs(patient_folder, exist_ok=True)

        # Save the image with a secure filename
        filename = secure_filename(image.filename)
        image_path = os.path.join(patient_folder, filename)
        image.save(image_path)
        return jsonify({"message": f"Image uploaded successfully for patient {patient_id}"}), 200
    else:
        return jsonify({"error": "Patient ID is required"}), 400

@app.route('/fill-claim-form', methods=['POST'])
def fill_claim():
    patient_id = request.form.get('patient_id')
    appointment_time = request.form.get('appointment_time')
    if 'pdf' not in request.files:
        return jsonify({"error": "No pdf file provided"}), 400

    pdf = request.files['pdf']
    if pdf.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if patient_id and appointment_time:
        # Create folder for the patient if it doesn't exist
        patient_folder = f'./{patient_id}'
        os.makedirs(patient_folder, exist_ok=True)

        # Save the image with a secure filename
        filename = secure_filename(pdf.filename)
        pdf_path = os.path.join(patient_folder, filename)
        pdf_output_path = pdf_path.split('.')[0] + '_output' + pdf_path.split('.')[1]
        pdf.save(pdf_path)

        ff = f"./{patient_id}/{appointment_time}_cdtcodes"
        if os.path.exists(ff):
            with open(ff, 'r') as file:
                codes = ' '.join(file.readlines())

        transcript_content = read_transcript(patient_id, appointment_time)
        fill_form(pdf_path, pdf_output_path, transcript_content, str(get_patient(patient_id)), codes)
        return send_file(pdf_output_path)
    else:
        return jsonify({"error": "Patient ID and appointment time is required"}), 400


@app.route('/images/<patientid>/<filename>')
def get_image(patientid, filename):
    return send_from_directory(f'./{patientid}', filename)


@app.route('/get-image-summary', methods=['GET'])
def get_image_summary():
    patient_id = request.args.get('patient_id')

    if not patient_id:
        return jsonify({"error": "patient_id and appointment_time are required"}), 400
    
    jpg_files = glob.glob(os.path.join(f'./{patient_id}/', "*.JPG"))
    summary = []
    url = []
    # Print list of jpg files
    for jpg_file in jpg_files:
        f = jpg_file + "_summary.txt"
        print(f)
        if os.path.exists(f):
            with open(f, 'r') as file:  # Use 'rb' mode for binary files like PDFs
                processed_result = ' '.join(file.readlines())
        else:
            processed_result = get_image_summarization(jpg_file)
            with open(f, 'w') as file:  # Use 'w' mode to write text files
                file.write(processed_result)
        summary.append(processed_result)
        # url.append(f'/images/{patient_id}/{jpg_file.split('\\')[-1]}')
        url.append(f'/images/{patient_id}/{jpg_file.split('/')[-1]}')
    
    return jsonify({"image_url": url, "summary": summary}), 200

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000, debug=True)
    app.run(host='0.0.0.0', port=8888, debug=True)
