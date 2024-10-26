import os
import time
from flask import Flask, request, jsonify
from flask_cors import CORS
from threading import Thread
from deepgram.utils import verboselogs

from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    LiveTranscriptionEvents,
    LiveOptions,
    Microphone,
)

from datetime import datetime
from werkzeug.utils import secure_filename

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

def start_recording(patient_id, appointment_time):
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
            is_finals.append(f"Speaker {speaker_id}:" + result.channel.alternatives[0].transcript)
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

@app.route('/start', methods=['POST'])
def start():
    print("Recieved start request")
    global transcript
    global patient_id
    global appointment_time
    print("Hi")
    patient_id = request.json.get('patient_id')
    print("Patient ID")
    appointment_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')  # Format current time

    if not patient_id:
        return jsonify({"error": "patient_id is required"}), 400
    
    # Clear previous transcript
    transcript = ""
    
    # Start recording in a separate thread
    Thread(target=start_recording, args=(patient_id, appointment_time), daemon=True).start()
    return jsonify({"message": "Recording started"}), 200

@app.route('/stop', methods=['POST'])
def stop():
    print("Recieved stop request")
    global is_recording
    is_recording = False
    save_transcript(patient_id, appointment_time, transcript)
    return jsonify({"message": "Recording stopped"}), 200

@app.route('/transcript', methods=['GET'])
def get_transcript():
    print("Recieved transcript request")
    global transcript
    return jsonify({"transcript": transcript}), 200

# New Endpoint to handle image uploads
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

if __name__ == '__main__':
    app.run(debug=True)
