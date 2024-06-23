""" Flask server """
from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector

def _refine_string(data):
    result = "For the given statement, the system response is "
    for d in data:
        if d != 'dominant_emotion':
            result += ("'" + d + "': " + str(data[d]) + ", ")
        else:
            result += ("The dominant emotion is " + f"<b>{data[d]}.</b>")
    return result

#Initiate the flask app : TODO
app = Flask("Emotion Detection")

@app.route("/emotionDetector")
def sent_detector():
    """ Sent the input from user to IBM Watson Library server """
    text_to_analyze = request.args.get('textToAnalyze')
    response = emotion_detector(text_to_analyze)
    error_message = "Invalid text! Please try again"
    if response['dominant_emotion'] is None:
        return f"<b>{error_message}!</b>"
    return _refine_string(response)
    #return f"<b>Invalid text! Please try again!</b>"

@app.route("/")
def render_index_page():
    """ Default homepage with index.html rendered """
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
