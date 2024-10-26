import fitz  # PyMuPDF
from pdfrw import PdfReader, PdfWriter, PageMerge

# Open the PDF form
# pdf_path = "./claimform_deltacare.pdf"
# pdf = fitz.open(pdf_path)

# # Extract form fields
# form_fields = {}
# for page in pdf:
#     for widget in page.widgets():
#         if widget.field_name:
#             form_fields[widget.field_name] = widget  # Store each field with its widget object

# # Print field names to verify
# for field_name in form_fields:
#     print(f"Field: {field_name}")
# pdf.close()

import fitz  # PyMuPDF

data = {
    "1 Patient Name": "Vrinda Narayan",
    "2 Birthdate": "31 August 2000",
    "3 Relation to Subscriber": "Mother",
    "School": "DPS Dwarka"
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
        print(field_name)
        if field_name in data:
            field_text = data[field_name]
            field.field_value = field_text  # Set the value for the form field
            field.update()  # Apply the change

# Save the filled form as a new PDF
pdf.save(output_pdf)
pdf.close()

