# Emotion Detection Web Application

A Web Application project to analyze emotions from user-provided textual data, identify dominant emotion

CRUD operations embedded with dynamic http requests

## Objectives

Develop a Python package that processes string variable with IBM Watson NLP (Natural Language Processing) Libraries, return the emotion analysis in a JSON file

Deploy the app by Python Flask framework

Create a front end UI for the user to enter text message, sent the http request and display the analysis results

Build a Python UnitTest module to test the program

Improve the program by Pylint in PEP8 Guidelines

## Emotion Analysis

The feature that get the emotion report and sent the formatted data back to the UI with IBM Watson Natural Language Processing

Get URL, user input, and header. Send them to IBM server, format the response with incorprate error handling

```python
def emotion_detector(text_to_analyse):
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    # url for using IBM Watson NLP libraries
    inputJson = { "raw_document": { "text": text_to_analyse } }
    # Create JSON file for the library to proceed analysis
    Headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    # Create the header of request before sending
    response = requests.post(url, json = inputJson, headers = Headers)
    # Send the request by POST method to the url we defined before, with the given JSON file and the header
    formatted_response = json.loads(response.text)
    # Extract the text part of the response and convert it to JSON

    if response.status_code == 400 or response.status_code == 304:
    # Error handling: if there's an error (invaild text input or page not found)
        for f in formatted_response:
            formatted_response[f] = None
        formatted_response['dominant_emotion'] = None
        # Set all attributes of the response to None and add key-value pair dominant_emotion : None
        # For the UI to know there's an invaild return
        return formatted_response
        # Return the response from here, the function will not go any further
        
    emotions = formatted_response['emotionPredictions'][0]['emotion']
    # Extract the emotion part of the response JSON
    dominant_emotion = _get_dominant_emotion(emotions)
    # Get the dominant emotion (the emotion with the highest score)
    emotions['dominant_emotion'] = str(dominant_emotion)
    # Set the dominant_emotion data
    return emotions
    # Return the response to the UI
```

The returned JSON file (analysis result) is like this:

```JavaScript
{
    'anger': anger_score,
    'disgust': disgust_score,
    'fear': fear_score,
    'joy': joy_score,
    'sadness': sadness_score,
    'dominant_emotion': '<name of the dominant emotion>'
}
```

Package the function for calling from external files: `__init__.py`

```python
from . import emotion_detection
```

Test the package from terminal

<img width="716" alt="4b_packaging_test" src="https://github.com/James-Z-Zhang00/emotion-detection-web-application/assets/144994336/cd82c135-c9a4-453d-b55b-297da6024347">

## Server Deployment

Deploy the server by Python Flask framework using decorator 

Name the server as Emotion Detection

Create 2 routes default homepage `/` and emotion detector `/emotionDetector`

Set the IP address to `0.0.0.0`, deploy at port `5000`

```python
app = Flask("Emotion Detection")

@app.route("/emotionDetector")
def sent_detector():
    """ Sent the input from user to IBM Watson Library server """
    text_to_analyze = request.args.get('textToAnalyze')
    # Extract user input string value
    response = emotion_detector(text_to_analyze)
    # Call the emotion_detector function and save the results to response
    error_message = "Invalid text! Please try again"
    if response['dominant_emotion'] is None:
    # Error handling if there's an invaild input or page not found, unable to give a dominant_emotion
        return f"<b>{error_message}!</b>"
    # Else return the refined/formatted message
    return _refine_string(response)

@app.route("/")
def render_index_page():
    """ Default homepage with index.html rendered """
    return render_template('index.html')
    # Render the index.html template for the default homepage route

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    # Run the server at IP address 0.0.0.0, port 5000
```

## Front end UI

By html web page embedded with JavaScript request sending feature

<img width="987" alt="6b_deployment_test" src="https://github.com/James-Z-Zhang00/emotion-detection-web-application/assets/144994336/5c1f8bb9-9f58-4c57-94b0-ecf4de673b93">

The JavaScript function

```JavaScript
let RunSentimentAnalysis = ()=>{
    textToAnalyze = document.getElementById("textToAnalyze").value;

    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("system_response").innerHTML = xhttp.responseText;
        }
    };
    xhttp.open("GET", "emotionDetector?textToAnalyze"+"="+textToAnalyze, true);
    xhttp.send();
}
```

## UnitTest Module

To test the program, I built a Python UnitTest module

Given certain text and check what is the dominant emotion of them

```python
from EmotionDetection.emotion_detection import emotion_detector

import unittest

class TestEmotionDetection(unittest.TestCase):
    def test_emotion_detector(self):
        result_1 = emotion_detector('I am glad this happened')
        self.assertEqual(result_1['dominant_emotion'], 'joy')
        result_2 = emotion_detector('I am really mad about this')
        self.assertEqual(result_2['dominant_emotion'], 'anger')
        result_3 = emotion_detector('I feel disgusted just hearing about this')
        self.assertEqual(result_3['dominant_emotion'], 'disgust')
        result_4 = emotion_detector('I am so sad about this')
        self.assertEqual(result_4['dominant_emotion'], 'sadness')
        result_5 = emotion_detector('I am really afraid that this will happen')
        self.assertEqual(result_5['dominant_emotion'], 'fear')

unittest.main()
```

Run the UnitTest module

<img width="907" alt="5b_unit_testing_result" src="https://github.com/James-Z-Zhang00/emotion-detection-web-application/assets/144994336/cc6631d8-838a-4bc5-9709-d36554cbd6c2">

## Pylint by PEP8 Guidelines

Pylint is a static code analysis tool for Python, it follows the style recommended by PEP 8, the Python style guide.

<img width="677" alt="8b_static_code_analysis" src="https://github.com/James-Z-Zhang00/emotion-detection-web-application/assets/144994336/61706dd5-ce10-4d99-a5cc-1cc3b10c1064">


