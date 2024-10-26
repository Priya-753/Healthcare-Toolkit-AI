auth_token = "ODFHIR NFF6i0KrXrxDkZHt/VzkmZEaUWOjnQX2z"  # replace with your actual token
import requests

def get_appointments(start_date, end_date):
    url = "https://api.opendental.com/api/v1/appointments"
    headers = {
        "Authorization": auth_token,
    }
    params = {
        "dateStart": start_date,
        "dateEnd": end_date,
    }
    response = requests.get(url, headers=headers, params=params)
    return response

def get_appointments_patient(pat_num):
    url = "https://api.opendental.com/api/v1/appointments"
    headers = {
        "Authorization": auth_token,
    }
    params = {
        "PatNum": pat_num, 
    }
    response = requests.get(url, headers=headers, params=params)
    return response

def get_patients():
    url = "https://api.opendental.com/api/v1/patients"
    headers = {
        "Authorization": auth_token,
    }
    params = {
        "hideInactive": "true",
    }
    response = requests.get(url, headers=headers, params=params)
    return response

def get_patient(patient_id):
    url = f"https://api.opendental.com/api/v1/patients/{patient_id}"
    headers = {
        "Authorization": auth_token,
    }
    response = requests.get(url, headers=headers)
    return response