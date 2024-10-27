import fitz  # PyMuPDF

pdf_path = "./claimform_deltacare.pdf"
pdf = fitz.open(pdf_path)
import ast

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

data = {
    "1 Patient Name": "Vrinda Narayan",
    "2 Birthdate": "31 August 2000",
    "3 Relation to Subscriber": "Mother",
    "School": "DPS Dwarka"
}
data_new = {
  "DENTISTS PRETREATMENT ESTIMATE OF CHARGES": "PRE-TREATMENT ESTIMATE",
  "DENTISTS STATEMENT OF ACTUAL CHARGES": "ACTUAL CHARGES",
  "RESUBMITTAL": None,
  "undefined": None,
  "XRAYS OR MODELS ENCLOSED HOW MANY": "2",
  "1 Patient Name": "Allen Allowed",
  "2 Birthdate": "06 June 1980",
  "3 Relation to Subscriber": "Self",
  "School": "N/A",
  "School City": "N/A",
  "School State": "N/A",
  "5 Subscribers Name": "Allen Allowed",
  "6 Subscribers ID Number": "1234567890",
  "Dual Coverage Yes": True,
  "Dual Coverage No": False,
  "Date": "2023-12-28",
  "7 Subscribers Mailing Address": "266 Jamaica Street\nForbes, CT 21598",
  "8 Subscribers Phone": "(253)687-9654",
  "15 ID Number": "9876543210",
  "Check": "12345",
  "9 City State Zip": "Forbes, CT 21598",
  "16 Union Local": "123",
  "13 Policy Number": "POLICY12345",
  "Date_2": "2023-12-27",
  "10 Employer Name": "Tech Company Inc.",
  "11 GroupPlan Number": "GROUPPLAN789",
  "17 Name and Address of Other Insurance": "Secondary Insurance Co.\n456 Elm Street\nAnytown, CA 54321",
  "12 Spouse's Name": "Jane Allowed",
  "13 Spouses Employer": "Retail Company",
  "Signature of above insured": "Allen Allowed (Signature)",
  "19 Dentist Name": "Dr. Smith",
  "Facility No": "FACILITY123",
  "23 Date Treatment Series Began": "2023-12-01",
  "Initial Placement No": True,
  "20 Dentists Address": "123 Main Street\nForbes, CT 21598",
  "If no reason for replacement": "N/A",
  "21 City State Zip": "Forbes, CT 21598",
  "25 Date of prior placement": "N/A",
  "Treatment result of accident Yes": False,
  "Treatment result of accident No": True,
  "Tax ID to be used for Tax reporting": "12-3456789",
  "License No": "DENTAL12345",
  "22 Phone": "(555) 123-4567",
  "Result of occupational injury Yes": False,
  "Result of occupational injury No": True,
  "Orthodontic purposes Yes": False,
  "Orthodontic purposes No": True,
  "29 IF FOR ORTHODONTIC REASONS": "N/A",
  "Initial Treatment Date": "2023-12-01",
  "Total Fee": "500.00",
  "Down Payment": "100.00",
  "Date_3": "2023-12-28",
  "Monthly Payment Amt": "50.00",
  "Number of Months": "8",
  "Date of First Billing": "2024-01-28",
  "Retainer Fee": "50.00",
  "Tooth  or letterFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY": "12",
  "Surfaces or QuadFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY": "2",
  "DESCRIPTION OF SERVICE Including XRays Prophylaxis Materials Used etcFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY": "Exam, Cleaning, Filling",
  "Date Service PerformedFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY": "2023-12-28",
  "Procedure NumberFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY": "12345",
  "FeeFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY": "350.00",
  "FeeFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_2": None,
  "AllowanceFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY": "300.00",
  "Tooth  or letterFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_2": None,
  "Surfaces or QuadFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_2": None,
  "DESCRIPTION OF SERVICE Including XRays Prophylaxis Materials Used etcFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_2": None,
  "Date Service PerformedFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_2": None,
  "Procedure NumberFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_2": None,
  "FeeFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_3": None,
  "FeeFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_4": None,
  "AllowanceFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_2": None,
  "Tooth  or letterFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_3": None,
  "Surfaces or QuadFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_3": None,
  "DESCRIPTION OF SERVICE Including XRays Prophylaxis Materials Used etcFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_3": None,
  "Date Service PerformedFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_3": None,
  "Procedure NumberFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_3": None,
  "FeeFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_5": None,
  "FeeFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_6": None,
  "AllowanceFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_3": None,
  "Tooth  or letterFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_4": None,
  "Surfaces or QuadFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_4": None,
  "DESCRIPTION OF SERVICE Including XRays Prophylaxis Materials Used etcFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_4": None,
  "Date Service PerformedFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_4": None,
  "Procedure NumberFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_4": None,
  "FeeFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_7": None,
  "FeeFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_8": None,
  "AllowanceFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_4": None,
  "Tooth  or letterFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_5": None,
  "Surfaces or QuadFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_5": None,
  "DESCRIPTION OF SERVICE Including XRays Prophylaxis Materials Used etcFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_5": None,
  "Date Service PerformedFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_5": None,
  "Procedure NumberFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_5": None,
  "FeeFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_9": None,
  "FeeFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_10": None,
  "AllowanceFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_5": None,
  "Tooth  or letterFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_6": None,
  "Surfaces or QuadFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_6": None,
  "DESCRIPTION OF SERVICE Including XRays Prophylaxis Materials Used etcFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_6": None,
  "Date Service PerformedFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_6": None,
  "Procedure NumberFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_6": None,
  "FeeFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_11": None,
  "FeeFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_12": None,
  "AllowanceFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_6": None,
  "Tooth  or letterFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_7": None,
  "Surfaces or QuadFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_7": None,
  "DESCRIPTION OF SERVICE Including XRays Prophylaxis Materials Used etcFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_7": None,
  "Date Service PerformedFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_7": None,
  "Procedure NumberFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_7": None,
  "FeeFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_13": None,
  "FeeFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_14": None,
  "AllowanceFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_7": None,
  "Tooth  or letterFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_8": None,
  "Surfaces or QuadFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_8": None,
  "DESCRIPTION OF SERVICE Including XRays Prophylaxis Materials Used etcFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_8": None,
  "Date Service PerformedFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_8": None,
  "Procedure NumberFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_8": None,
  "FeeFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_15": None,
  "FeeFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_16": None,
  "AllowanceFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_8": None,
  "Tooth  or letterFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_9": None,
  "Surfaces or QuadFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_9": None,
  "DESCRIPTION OF SERVICE Including XRays Prophylaxis Materials Used etcFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_9": None,
  "Date Service PerformedFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_9": None,
  "Procedure NumberFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_9": None,
  "FeeFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_17": None,
  "FeeFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_18": None,
  "AllowanceFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_9": None,
  "Tooth  or letterFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_10": None,
  "Surfaces or QuadFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_10": None,
  "DESCRIPTION OF SERVICE Including XRays Prophylaxis Materials Used etcFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_10": None,
  "Date Service PerformedFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_10": None,
  "Procedure NumberFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_10": None,
  "FeeFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_19": None,
  "FeeFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_20": None,
  "AllowanceFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_10": None,
  "Tooth  or letterFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_11": None,
  "Surfaces or QuadFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_11": None,
  "DESCRIPTION OF SERVICE Including XRays Prophylaxis Materials Used etcFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_11": None,
  "Date Service PerformedFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_11": None,
  "Procedure NumberFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_11": None,
  "FeeFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_21": None,
  "FeeFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_22": None,
  "AllowanceFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_11": None,
  "Tooth  or letterFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_12": None,
  "Surfaces or QuadFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_12": None,
  "DESCRIPTION OF SERVICE Including XRays Prophylaxis Materials Used etcFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_12": None,
  "Date Service PerformedFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_12": None,
  "Procedure NumberFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_12": None,
  "FeeFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_23": None,
  "FeeFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_24": None,
  "AllowanceFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_12": None,
  "Tooth  or letterFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_13": None,
  "Surfaces or QuadFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_13": None,
  "DESCRIPTION OF SERVICE Including XRays Prophylaxis Materials Used etcFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_13": None,
  "Date Service PerformedFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_13": None,
  "Procedure NumberFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_13": None,
  "FeeFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_25": None,
  "FeeFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_26": None,
  "AllowanceFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_13": None,
  "Tooth  or letterFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_14": None,
  "Surfaces or QuadFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_14": None,
  "DESCRIPTION OF SERVICE Including XRays Prophylaxis Materials Used etcFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_14": None,
  "Date Service PerformedFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_14": None,
  "Procedure NumberFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_14": None,
  "FeeFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_27": None,
  "FeeFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_28": None,
  "AllowanceFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_14": None,
  "Tooth  or letterFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_15": None,
  "Surfaces or QuadFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_15": None,
  "DESCRIPTION OF SERVICE Including XRays Prophylaxis Materials Used etcFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_15": None,
  "Date Service PerformedFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_15": None,
  "Procedure NumberFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_15": None,
  "FeeFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_29": None,
  "FeeFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_30": None,
  "AllowanceFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_15": None,
  "Total Fee Charged": "350.00",
  "AllowanceTotal Fee Charged": "300.00",
  "CoInsurance": "50.00",
  "fill_151": None,
  "Subscriber's Signature": "Allen Allowed (Signature)",
  "Date 4": "2023-12-28",
  "Insurance Pays": "300.00",
  "Dentist's Signature": "Dr. Smith (Signature)",
  "Date 5": "2023-12-28",
  "Patient Pays": "50.00"
}

data_new2 = {
    "1 Patient Name": "Allen Allowed",
    "2 Birthdate": "1980-06-05",
    "10 Employer Name": "KOCH INDUSTRIES",
    "11 GroupPlan Number": "7340008",
    "19 Dentist Name": "DOC1",
    "20 Dentists Address": "266 Jamaica Street",
    "21 City State Zip": "Forbes, CT 21598",
    "22 Phone": "(253)687-9654",
    "Total Fee": "335.00",
    "DENTISTS STATEMENT OF ACTUAL CHARGES": "335.00",
    "DESCRIPTION OF SERVICE Including XRays Prophylaxis Materials Used etcFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY": "Limited Oral Evaluation and Scaling and Root Planing with Local Anesthesia",
    "Date Service PerformedFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY": "2024-08-29",
    "Procedure NumberFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY": "D0140",
    "FeeFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY": "75.00",
    "AllowanceFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY": "75.00",
    "Tooth  or letterFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_2": "23",
    "Surfaces or QuadFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_2": "LLQ",
    "DESCRIPTION OF SERVICE Including XRays Prophylaxis Materials Used etcFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_2": "Scaling and Root Planing",
    "Date Service PerformedFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_2": "2024-08-29",
    "Procedure NumberFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_2": "D4342",
    "FeeFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_2": "80.00",
    "AllowanceFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_2": "80.00",
    "Tooth  or letterFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_3": "URQ",
    "Surfaces or QuadFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_3": "URQ",
    "DESCRIPTION OF SERVICE Including XRays Prophylaxis Materials Used etcFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_3": "Scaling and Root Planing (Full Quadrant)",
    "Date Service PerformedFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_3": "2024-08-29",
    "Procedure NumberFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_3": "D4341",
    "FeeFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_3": "150.00",
    "AllowanceFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_3": "150.00",
    "DESCRIPTION OF SERVICE Including XRays Prophylaxis Materials Used etcFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_4": "Local Anesthesia",
    "Date Service PerformedFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_4": "2024-08-29",
    "Procedure NumberFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_4": "D9215",
    "FeeFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_4": "30.00",
    "AllowanceFACIAL LINGUAL LINGUAL UPPER LOWER PRIMARY_4": "30.00",
    "7 Subscribers Mailing Address": "N/A",
    "13 Policy Number": "N/A",
    "15 ID Number": "N/A",
    "Insurance Company": "DELTA DENTAL",
    "Dual Coverage No": "Yes",
    "Signature of above insured": "N/A",
    "Facility No": "N/A",
    "23 Date Treatment Series Began": "2024-08-29",
    "Tax ID to be used for Tax reporting": "N/A"
}

pdf_path = "./claimform_deltacare.pdf"
output_pdf = "filled_claimform_deltacare.pdf"

# Open the PDF with PyMuPDF
pdf = fitz.open(pdf_path)

# Iterate through pages and update form fields
for page_num in range(len(pdf)):
    page = pdf[page_num]
    for field in page.widgets():  # Get form fields
        field_name = field.field_name
        if field_name in data_new2:
            field_text = data_new2[field_name]
            field.field_value = field_text  # Set the value for the form field
            field.update()  # Apply the change

# Save the filled form as a new PDF
pdf.save(output_pdf)
pdf.close()

# import google.generativeai as genai

# genai.configure(api_key="AIzaSyDwZKCIoIXv0WNZe5IxH9HqUK9Mf0_jxo4")

# # Create the model
# generation_config = {
#   "temperature": 1,
#   "top_p": 0.95,
#   "top_k": 64,
#   "max_output_tokens": 8192,
#   "response_mime_type": "text/plain",
# }

# model = genai.GenerativeModel(
#   model_name="gemini-1.5-pro",
#   generation_config=generation_config,
# )

# transcript = """Speaker 0: Good morning! What brings you in today?

# Speaker 1: Good morning, Doctor. I've been having a lot of pain in one of my teeth, especially when I eat or drink something hot or cold.

# Speaker 0: I see. How long have you been experiencing this pain?

# Speaker 1: It started mildly a few weeks ago, but it’s been getting worse lately. Now, even brushing sometimes hurts.

# Speaker 0: That sounds uncomfortable. Let me take a look. Open wide, please.

# (The doctor examines the patient's mouth with a dental mirror and light.)

# Speaker 0: I can see a cavity on your lower left molar. It looks like decay has set in, which is likely causing the sensitivity and pain.

# Speaker 1: Oh, that doesn’t sound good. How serious is it?

# Speaker 0: Fortunately, it’s not too deep yet. We can treat it with a filling, which should stop the decay and relieve the sensitivity. But it's important to address it soon so it doesn’t reach the root, which would require a root canal treatment.

# Speaker 1: I see. What exactly is the filling procedure like?

# Speaker 0: It’s fairly simple. I’ll first numb the area to make sure you’re comfortable, then remove the decayed part of the tooth. After that, I’ll fill it with a special material to restore its shape and function. The entire process usually takes about 20-30 minutes.

# Speaker 1: That sounds manageable. Is there anything I need to avoid afterward?

# Speaker 0: After the filling, avoid eating on that side for a few hours to let it set properly. In the long term, limit sugary foods and make sure to brush and floss regularly to help prevent future cavities.

# Speaker 1: Got it. Thank you, Doctor. I appreciate the guidance.

# Speaker 0: You’re very welcome. Let’s get this scheduled soon so we can relieve that pain for you!"""

# patient_details = """{
#   "Address": "266 Jamaica Street",
#   "Address2": "",
#   "AdmitDate": "0001-01-01",
#   "BalTotal": 370.0,
#   "BillingType": "Standard Account",
#   "Birthdate": "1980-06-05",
#   "ChartNumber": "",
#   "City": "Forbes",
#   "ClinicNum": 0,
#   "DateFirstVisit": "2009-03-30",
#   "DateTStamp": "2024-08-29 10:44:54",
#   "Email": "",
#   "EstBalance": 230.0,
#   "FName": "Allen",
#   "FamFinUrgNote": "",
#   "Gender": "Male",
#   "Guarantor": 11,
#   "HmPhone": "(253)687-9654",
#   "ImageFolder": "AllowedAllen11",
#   "LName": "Allowed",
#   "Language": "",
#   "MedicaidID": "",
#   "MiddleI": "",
#   "PatNum": 11,
#   "PatStatus": "Patient",
#   "Position": "Married",
#   "PreferConfirmMethod": "None",
#   "PreferContactMethod": "None",
#   "PreferRecallMethod": "None",
#   "Preferred": "",
#   "PriProv": 1,
#   "SSN": "",
#   "SecDateEntry": "0001-01-01",
#   "SecProv": 0,
#   "State": "CT",
#   "SuperFamily": 0,
#   "TxtMsgOk": "Unknown",
#   "Ward": "",
#   "WirelessPhone": "",
#   "WkPhone": "",
#   "Zip": "21598",
#   "clinicAbbr": "",
#   "priProvAbbr": "DOC1",
#   "secProvAbbr": "",
#   "siteDesc": ""
# }"""

# chat_session = model.start_chat()
# print(f"I want to fill this form with the content: {text}. The fields I want to fill are: {field_names}, fill all fields of the form. This was the latest conversation the patient had with the doctor: {transcript}. Patient details are: {patient_details}. Only give output in json format of {data}.")
# response = chat_session.send_message(f"I want to fill this form with the content: {text}. The fields I want to fill are: {field_names}, fill all fields of the form. This was the latest conversation the patient had with the doctor: {transcript}. Patient details are: {patient_details}. Only give output in json format of {data}.")
# # print(response.text)
# # print(type(response.text))
# # print(response.text[7
# #                     :-4])
# # data_new = ast.literal_eval(response.text[7:-4])