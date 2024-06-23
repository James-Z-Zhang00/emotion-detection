import requests
import json

def _get_dominant_emotion(inputJson):
    max_key = max(inputJson, key=inputJson.get)
    return max_key

def emotion_detector(text_to_analyse):
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    inputJson = { "raw_document": { "text": text_to_analyse } }
    Headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    response = requests.post(url, json = inputJson, headers = Headers)
    formatted_response = json.loads(response.text)

    if response.status_code == 400 or response.status_code == 304:
        for f in formatted_response:
            formatted_response[f] = None
        formatted_response['dominant_emotion'] = None
        return formatted_response
        
    emotions = formatted_response['emotionPredictions'][0]['emotion']
    dominant_emotion = _get_dominant_emotion(emotions)
    emotions['dominant_emotion'] = str(dominant_emotion)
    return emotions



    
    # if response.status_code == 200:
    #     label = formatted_response['documentSentiment']['label']
    #     score = formatted_response['documentSentiment']['score']
    # elif response.status_code == 500:
    #     label = None
    #     score = None
    # return {'label': label, 'score': score}