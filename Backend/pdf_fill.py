import fitz  # PyMuPDF
import ast
import google.generativeai as genai

genai.configure(api_key="AIzaSyDwZKCIoIXv0WNZe5IxH9HqUK9Mf0_jxo4")

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  generation_config=generation_config,
)

chat_session = model.start_chat()

def fill_form(pdf_path, output_pdf, transcript, patientInformation, cdtCodes):
    pdf = fitz.open(pdf_path)

    # Extract form fields
    form_fields = {}
    field_names = []
    text = ""
    for page in pdf:
        text += page.get_text()
        for widget in page.widgets():
            if widget.field_name:
                form_fields[widget.field_name] = widget  # Store each field with its widget object
                field_names.append(widget.field_name)
    pdf.close()
    response = chat_session.send_message(f"""You're an expert in analysing medical transcripts, CDT billing codes, employer information and filling data for pre-authorisation claims. You must analyse the data I give you and return a python dictionary of the relevant variables asked of you. You must return all data possible and not hallucinate. Combine data from the transcript, provided procedures performed and examples that I've provided to return the fields I need as a python dictionary. I want only relevant form details to be filled in and its paramount you fill in and return as python dictionary. do not include any comments since the data you return will be used in a future code task that cannot take prompts. Remember all descriptions and codes must be processed since a wrong pre-authorisation can lead to loss of money or increase in time. IMPORTANT: if you don't find data to fill for certain variables you DON'T need to include it in the python dictionary. IMPORTANT: the key or value pairs must always be in string format


    Transcript:
    {transcript}

    Patient Information:
    {patientInformation}

    CDT billing codes of the various procedures performed which must all be included:
    {cdtCodes}

    Here's how a sample row should be filled in for the billing code in the variables provided below:
    "Tooth  or letterFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY": "12",
    "Surfaces or QuadFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY": "2",
    "DESCRIPTION OF SERVICE Including XRays Prophylaxis Materials Used etcFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY": "Exam, Cleaning, Filling",
    "Date Service PerformedFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY": "2023-12-28",
    "Procedure NumberFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY": "12345",
    "FeeFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY": "350.00",
    "FeeFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_2": None,
    "AllowanceFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY": "300.00"

    The fields that i want filled in are the following:
    {field_names}""")

    data_new = ast.literal_eval(response.text[7:-4])

    # Open the PDF with PyMuPDF
    pdf = fitz.open(pdf_path)

    # Iterate through pages and update form fields
    for page_num in range(len(pdf)):
        page = pdf[page_num]
        for field in page.widgets():  # Get form fields
            field_name = field.field_name
            if field_name in data_new:
                field_text = data_new[field_name]
                field.field_value = field_text  # Set the value for the form field
                field.update()  # Apply the change

    # Save the filled form as a new PDF
    pdf.save(output_pdf)
    pdf.close()