auth_token = "ODFHIR NFF6i0KrXrxDkZHt/VzkmZEaUWOjnQX2z"  # replace with your actual token
import requests
import json

def get_appointments(start_date, end_date):
    url = "https://api.opendental.com/api/v1/appointments"
    headers = {
        "Authorization": auth_token,
    }
    params = {
        "dateStart": start_date,
        "dateEnd": end_date,
    }
    response = requests.get(url, headers=headers, params=params).json()
    return response

def get_appointments_patient(pat_num):
    url = "https://api.opendental.com/api/v1/appointments"
    headers = {
        "Authorization": auth_token,
    }
    params = {
        "PatNum": pat_num, 
    }
    response = requests.get(url, headers=headers, params=params).json()
    return response

def get_patients():
    url = "https://api.opendental.com/api/v1/patients"
    headers = {
        "Authorization": auth_token,
    }
    params = {
        "hideInactive": "true",
    }
    response = requests.get(url, headers=headers, params=params).json()
    return response

def get_patient(patient_id):
    url = f"https://api.opendental.com/api/v1/patients/{patient_id}"
    headers = {
        "Authorization": auth_token,
    }
    response = requests.get(url, headers=headers).json()
    clinic_number = response['ClinicNum']
    provider_number = response['PriProv']
    prov = get_provider(clinic_number, provider_number)
    ins = get_insurance(patient_id)
    combined_data = ins
    combined_data.update(prov)
    combined_data.update(response)
    return combined_data

def get_provider(clinic_number, provider_id):
    url = f"https://api.opendental.com/api/v1/providers/?ClinicNum={clinic_number}"
    headers = {
        "Authorization": auth_token,
    }
    response = requests.get(url, headers=headers).json()
    for prov in response:
        if(prov["ProvNum"] == provider_id):
            return prov
    return response[0]

def get_insurance(patient_id):
    url = f"https://api.opendental.com/api/v1/familymodules/{patient_id}/Insurance"
    headers = {
        "Authorization": auth_token,
    }
    response = requests.get(url, headers=headers).json()
    return response[0]
