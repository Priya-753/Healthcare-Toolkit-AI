import base64
from openai import OpenAI
import os

# Set your OpenAI API key
api_key = 'sk-W1I2vqmJwzDiz_3DHwGvDxpP3RiV0mYLg3qB553OdjT3BlbkFJbXMsqTYHYHkZY7la3Cu18vcHTtdmWwvMoJHm-ChQ0A'
os.environ['OPENAI_API_KEY'] = api_key

client = OpenAI()

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def get_image_summarization(image_path):
    # Getting the base64 string
    base64_image = encode_image(image_path)

    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": """Can you give a dental overview of this image in 100 words? Similar to This is a panoramic dental X-ray (OPG), providing a comprehensive view of the entire mouth, including the teeth, jaws, and surrounding structures. Here’s an overview of key observations based on what is visible:

    1. Restorations and Fillings:
    Several teeth on both the upper and lower arches have visible dental fillings or crowns (appearing as bright white areas).
    Notably, there are two filled molars on the lower jaw, one on each side, which appear to be restored with metal-based materials.
    2. Missing Teeth:
    Gaps are visible in certain areas, suggesting missing teeth in both the upper and lower arches.
    Specifically, some premolars or molars are absent, likely removed (possibly due to extraction or decay).
    3. Root Canal Treatment:
    One tooth near the center (likely a front tooth) has a root canal filling that extends through the length of the root. This appears as a white, linear filling material in the center of the tooth.
    4. Third Molars (Wisdom Teeth):
    The lower right wisdom tooth appears impacted or possibly tilted, with its root extending in an angular direction, which might cause issues if it is not already symptomatic.
    The other wisdom teeth either seem absent or are not visible clearly, suggesting they may have been removed or are not present.
    5. Bone Density and Jaw Health:
    The jawbone appears reasonably intact, though bone loss might need further assessment with closer clinical examination.
    There are no obvious signs of severe bone lesions or fractures, but the condyles (jaw joints) are slightly distorted due to panoramic projection limitations.
    6. Periodontal Health:
    Some spacing between the roots and the surrounding bone is visible, which could indicate mild to moderate bone loss or periodontal issues, especially around the molars.
    Summary and Recommendations:
    Restorative work is present (fillings, root canal, crowns) and some teeth are missing.
    Wisdom tooth on the lower right might require attention if causing discomfort or crowding.
    It’s recommended to assess further:
    Check periodontal health to evaluate any bone loss.
    Monitor impacted wisdom tooth for potential future issues.
    A more detailed clinical examination by a dentist may be required to confirm any hidden infections or minor issues.
    
    Another example:
    This image is a panoramic (orthopantomogram, OPG) dental X-ray, which provides a comprehensive view of the upper and lower jaws, teeth, and supporting structures. Below is a general dental overview of what I observe:

Teeth alignment and crowding:
There appears to be some overlapping or crowding in the anterior (front) teeth, especially in the lower jaw (mandibular region).
Molars seem aligned in general, but there could be mild spacing or alignment issues.
Presence of Restorations:
Several teeth, particularly the molars on both the left and right side, contain metallic restorations (likely amalgam fillings or crowns), which show up as bright white areas on the X-ray.
Wisdom teeth:
On the lower jaw, both left and right sides show third molars (wisdom teeth). These appear fully developed but slightly inclined.
There is a possibility of impaction or limited eruption on the lower right side (near the back). This could be a potential site of concern for impaction or crowding.
Periodontal Bone Levels:
Bone levels appear reasonably intact, although a closer examination may be needed to assess for early signs of bone loss or periodontal disease, especially in regions with restorations.
In some anterior teeth, the bone margins appear slightly reduced, suggesting mild periodontal concerns.
Maxillary Sinus:
The sinuses (visible above the upper molars) seem generally clear, though further examination by a specialist would confirm if there are any subtle irregularities.
Possible Impacted Tooth:
The lower wisdom teeth, especially on the left, appear to be inclined and could suggest partial impaction, which might require clinical evaluation for removal.
Clinical Concerns:
Potential Wisdom Tooth Extraction: Given the position of the lower third molars (wisdom teeth), an oral surgeon may recommend extraction, particularly if there is limited space or risk of infection.
Restorative Care Maintenance: Multiple fillings are present, and their condition needs to be monitored for decay or leakage.
Periodontal Health Monitoring: Mild signs of possible bone loss around certain areas indicate the importance of good oral hygiene and routine check-ups.

Another example:
This is a panoramic dental X-ray (also known as an orthopantomogram or OPG). It provides a broad view of the upper and lower jaws, teeth, sinuses, and surrounding structures. Here's a detailed overview of the key findings and components visible in this X-ray:

Observations:
Teeth:
Partially missing teeth: There are several areas where teeth appear to be missing, such as gaps in the upper and lower arches.
Restorative work: Two crowns or large dental fillings (likely metal-based) are visible on the lower left and right molars.
Root remnants / possible extractions: There are some areas with root structures but no visible crown portions, suggesting previous extractions or severe decay (e.g., in the upper jaw).
Bone Structure:
The overall bone quality around the jaws appears uneven, with some regions showing areas of resorption, possibly due to missing teeth.
No obvious signs of fractures, but there could be minor bone loss or changes associated with periodontal issues.
Possible Pathology:
Sinus cavities: The upper sinuses (maxillary sinuses) are partially visible but seem cloudy or less defined on the left side. This could suggest sinus congestion or chronic sinusitis.
Cyst or radiolucency: There is a rounded radiolucent area (dark spot) near the lower left side, possibly indicating a cyst, abscess, or lesion. This would need further investigation.
Alignment / Bite Issues:
There might be malalignment or shifting of teeth, particularly in areas with missing teeth, which could result in improper bite (malocclusion).
Some lower incisors appear elongated, potentially indicating bone loss or early periodontal disease.
Wisdom Teeth:
The third molars (wisdom teeth) are not clearly visible, suggesting they may have been extracted previously.""",
            },
            {
            "type": "image_url",
            "image_url": {
                "url":  f"data:image/jpeg;base64,{base64_image}"
            },
            },
        ],
        }
    ],
    )

    return(response.choices[0].message.content)