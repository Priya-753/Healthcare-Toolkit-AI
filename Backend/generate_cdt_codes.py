import base64
from openai import OpenAI
import os
import ast
import json

# Set your OpenAI API key
api_key = 'sk-W1I2vqmJwzDiz_3DHwGvDxpP3RiV0mYLg3qB553OdjT3BlbkFJbXMsqTYHYHkZY7la3Cu18vcHTtdmWwvMoJHm-ChQ0A'
os.environ['OPENAI_API_KEY'] = api_key

client = OpenAI()

def get_cdt_icd_codes(transcript, soap):

    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": f"""you're an expert in diagnosing ICD and CDT codes from given SOAP notes and transcripts. given a transcript and SOAP notes for a dental appointment, you will generate ICD and CDT codes. you will also keep in mind to mention the quadrant, teeth type(molar, premolar, canine), teeth number since all of this data is required in the next step of where your output will be used which is to generate pre-authorisation and insurance claims. response will be in the following json format - {{"procAndBillingCodes": {{<array of ICD diagnosis and corresponding CDT procedure where both will be objects like icd: <icdObject>, cdt: <cdtObject>>}} }}
        An object of CDT code will contain the following schema: {{codeNumber: <codeNumber>, teethNumber: <teethNumber if needed otherwise null>, quadrant: <quadrant if needed otherwise null>, teethType:  <teethType if needed otherwise null>, description: <description if needed otherwise null>}}
        An object of ICD code will contain the following schema: {{codeNumber: <codeNumber>, description: <description>}}

        Transcript:
        {transcript}

        SOAP:
        {soap}""",
                    },
        ],
        }
    ],
    )
    return(json.loads(response.choices[0].message.content[7:-4]))

transcript = """Speaker 0 (Dentist): Hi! What can I help you with today?
Speaker 1 (Patient): Hi, Doctor. I’ve been feeling some sensitivity on both sides of my mouth, mostly when I eat sweets.
Speaker 0: Okay, let’s have a look. I’ll also take some X-rays to get a clearer picture.
(The dentist takes bitewing X-rays and reviews the images.)
Speaker 0: I see some cavities in a few places. In quadrant 2, tooth 14—the upper left first molar—has a moderate cavity on the chewing surface. Tooth 15, the second molar, has a smaller cavity on the side.
Speaker 1: Oh no. Are they bad?
Speaker 0: Luckily, they’re still in the enamel layer and haven’t reached the nerve. We can treat these with fillings to stop the decay from spreading.
Speaker 1: Okay. Is that all?
Speaker 0: There’s also a small cavity on tooth 31 in quadrant 4, your lower right molar. It’s not as deep, but we should address it too.
Speaker 1: How long will all of this take?
Speaker 0: Each filling takes about 20 minutes, so we can finish all three in one visit. I’ll numb the areas before we start, and you’ll be good to go once we’re done. Just avoid eating on those sides for a few hours until the anesthesia wears off.
Speaker 1: Sounds good. Let’s take care of them today.
Speaker 0: Perfect! I’ll get everything set up."""
soap = """Subjective: The patient presents complaining of sensitivity on both sides of the mouth, primarily when eating sweets.
Objective: Bitewing radiographs reveal the following:
Tooth #14 (upper left first molar): Moderate-sized carious lesion on the occlusal surface.
Tooth #15 (upper left second molar): Small carious lesion on the interproximal surface.
Tooth #31 (lower right first molar): Small carious lesion.
All lesions appear to be confined to the enamel and have not reached the dentin or pulp.
Assessment: Dental caries affecting teeth #14, #15, and #31. The patient's sensitivity is likely due to the exposed dentin resulting from the carious lesions."""
# print(get_cdt_icd_codes(transcript, soap))