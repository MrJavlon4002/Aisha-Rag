import requests
import os
import json
import re
import time
def stt(api_key, file_path):
    url = 'https://uzbekvoice.ai/api/v1/stt'
    headers = {
        "Authorization": api_key
    }

    files = {
        "file": ("audio.mp3", open(file_path, "rb")),
    }
    data = {
        "return_offsets": "true",
        "run_diarization": "true",
        "language": "uz",
        "blocking": "false",
    }

    try:
        response = requests.post(url, headers=headers, files=files, data=data)
        if response.status_code == 200:
            return response.json()
        else:
            return f"Request failed with status code {response.status_code}: {response.text}"
    except requests.exceptions.Timeout:
        return "Request timed out. The API response took too long to arrive."




import time
import requests

def task_polling(api_key, task_id):

    url = f'https://uzbekvoice.ai/api/v1/tasks?id={task_id}'
    headers = {
        'Authorization': api_key,
        'Content-Type': 'application/json'
    }

    while True:
        time.sleep(5)
        try:
            response = requests.get(url, headers=headers)
            return response.json()

        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e}")
            return None
            
        

def clean_json(data):
    if isinstance(data, str):
        data = json.loads(data)
    elif not isinstance(data, dict):
        print("Input must be a JSON string or a dictionary")
        return ""
    
    conversation_text = data.get('result', {}).get('conversation_text', '')
    speakers = re.split(r'(Speaker \d+:)', conversation_text)
    
    cleaned_text = ""
    for i in range(1, len(speakers), 2):
        speaker = speakers[i].strip()
        text = speakers[i + 1].strip() if i + 1 < len(speakers) else ""
        
        cleaned_speaker_text = re.sub(r'[^\w\s]', '', text)
        cleaned_speaker_text = re.sub(r'\s+', ' ', cleaned_speaker_text).strip()
        
        cleaned_text += f"{speaker} {cleaned_speaker_text}\n"
    
    return cleaned_text.strip()

# Main transcription process
def transcription(audio_file_path):
    api_key_stt = "4b4cd413-47bd-42b3-ac12-e4fa2732b5a3:1e696e95-a315-45e2-8b37-f3d64943755a"
    api_key_polling = "4b4cd413-47bd-42b3-ac12-e4fa2732b5a3:1e696e95-a315-45e2-8b37-f3d64943755a"
    result = stt(api_key_stt, audio_file_path)
    
    if isinstance(result, str):
        return None

    task_id = result['id']
    result = task_polling(api_key_polling, task_id)

    if result is None or not result.get('result'): 
        print("Failed to retrieve task results or task is still processing.")
        return None

    cleaned_text = clean_json(result)
    return cleaned_text
