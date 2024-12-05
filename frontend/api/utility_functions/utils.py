import requests
import json
import joblib

# Load the saved model
clf = joblib.load("tone_classifier.pkl")

def classify_tone_with_ml(score, magnitude):
    """
    Classify tone using a machine learning model.
    """
    # Predict tone
    tone = clf.predict([[score, magnitude]])[0]
    return tone

def classify_tone(score, magnitude):
    print(score,magnitude)
    if score > 0.25:
        if magnitude > 0.6:
            return 'Joy'
        else:
            return 'Confident'
    elif score < -0.25:
        if magnitude > 0.5:
            return 'Sadness'
        else:
            return 'Anger'
    else:
        if magnitude < 0.1:
            return 'Neutral'
        elif score > 0:
            return 'Tentative'
        else:
            return 'Analytical'

def analyseTone(text):
    url = "https://language.googleapis.com/v1/documents:analyzeSentiment?key=AIzaSyDVkn3cXvmgb5HaN_05ZKCgJd5xtk4_cv4"
    headers = {'Content-Type': 'application/json'}
    body = {
        'document': {
            'type': 'PLAIN_TEXT',
            'content': text
        },
        'encodingType': 'UTF8'
    }
    response = requests.post(url, headers=headers, json=body)
    result = response.json()
    score = result['documentSentiment']['score']
    magnitude = result['documentSentiment']['magnitude']
    print(score,magnitude)
    tone = classify_tone_with_ml(score, magnitude)
    return tone
