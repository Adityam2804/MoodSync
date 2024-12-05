import requests
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Define the Google Natural Language API URL and API key
API_URL = "https://language.googleapis.com/v1/documents:analyzeSentiment?key=AIzaSyDVkn3cXvmgb5HaN_05ZKCgJd5xtk4_cv4"

# Benchmark data
benchmark_data = [
    # Positive Sentiments
    {"chat": "I'm so happy today!", "expected_tone": "Joy"},
    {"chat": "This is the best day of my life!", "expected_tone": "Joy"},
    {"chat": "I can't wait for the weekend!", "expected_tone": "Joy"},
    {"chat": "You did an amazing job on this project!", "expected_tone": "Confident"},
    {"chat": "I'm thrilled with the results!", "expected_tone": "Joy"},
    {"chat": "Thank you for your help, it means so much!", "expected_tone": "Joy"},
    {"chat": "Great work! I'm proud of you.", "expected_tone": "Confident"},
    {"chat": "This is exactly what I wanted. Perfect!", "expected_tone": "Joy"},

    # Negative Sentiments
    {"chat": "I feel sad and lonely.", "expected_tone": "Sadness"},
    {"chat": "I'm so disappointed in myself.", "expected_tone": "Sadness"},
    {"chat": "Why does everything have to go wrong?", "expected_tone": "Sadness"},
    {"chat": "I can't believe you did that!", "expected_tone": "Anger"},
    {"chat": "You're the worst!", "expected_tone": "Anger"},
    {"chat": "This is completely unacceptable.", "expected_tone": "Anger"},
    {"chat": "I hate how things are going.", "expected_tone": "Sadness"},
    {"chat": "I feel betrayed by everyone.", "expected_tone": "Sadness"},

    # Neutral Sentiments
    {"chat": "It's a sunny day outside.", "expected_tone": "Neutral"},
    {"chat": "I'll see you at 5 PM.", "expected_tone": "Neutral"},
    {"chat": "There are 24 hours in a day.", "expected_tone": "Neutral"},
    {"chat": "This is a statement with no emotion.", "expected_tone": "Neutral"},
    {"chat": "I went to the store to buy groceries.", "expected_tone": "Neutral"},
    {"chat": "Today is Thursday.", "expected_tone": "Neutral"},
    {"chat": "I have a meeting at 3 PM.", "expected_tone": "Neutral"},
    {"chat": "The car is parked outside.", "expected_tone": "Neutral"},

    # Tentative/Analytical Sentiments
    {"chat": "I'm not sure if this will work.", "expected_tone": "Tentative"},
    {"chat": "This data suggests a strong correlation.", "expected_tone": "Analytical"},
    {"chat": "Let's try a different approach to solve this.", "expected_tone": "Tentative"},
    {"chat": "The results seem inconclusive so far.", "expected_tone": "Analytical"},
    {"chat": "Maybe we can figure this out together.", "expected_tone": "Tentative"},
    {"chat": "I'm analyzing the situation carefully.", "expected_tone": "Analytical"},
    {"chat": "We should evaluate all possible options.", "expected_tone": "Analytical"},
    {"chat": "This might work, but I have doubts.", "expected_tone": "Tentative"},

    # Sensitive Topics
    {"chat": "Men are better at math.", "expected_tone": "Neutral"},
    {"chat": "Women are always emotional.", "expected_tone": "Neutral"},
    {"chat": "Diversity in the workplace is a strength.", "expected_tone": "Confident"},
    {"chat": "I believe in equal rights for everyone.", "expected_tone": "Confident"},
    {"chat": "Everyone deserves an equal opportunity.", "expected_tone": "Confident"},
    {"chat": "Gender equality is a fundamental right.", "expected_tone": "Confident"},
    {"chat": "Racial discrimination has no place in society.", "expected_tone": "Confident"},
    {"chat": "Fair treatment for all is essential.", "expected_tone": "Confident"},

    # Multilingual Inputs
    {"chat": "Estoy muy feliz hoy.", "expected_tone": "Joy"},  # Spanish: "I'm very happy today."
    {"chat": "Je suis triste aujourd'hui.", "expected_tone": "Sadness"},  # French: "I'm sad today."
    {"chat": "Das ist ein schöner Tag.", "expected_tone": "Neutral"},  # German: "It's a beautiful day."
    {"chat": "これは美しい日です。", "expected_tone": "Neutral"},  # Japanese: "It's a beautiful day."
    {"chat": "Estoy agradecido por todo.", "expected_tone": "Joy"},  # Spanish: "I'm grateful for everything."
    {"chat": "Ce projet est très intéressant.", "expected_tone": "Analytical"},  # French: "This project is very interesting."
    {"chat": "Das ist ein sehr interessantes Thema.", "expected_tone": "Analytical"},  # German: "This is a very interesting topic."
    {"chat": "今日はとても良いです。", "expected_tone": "Joy"},  # Japanese: "Today is very good."

    # Ambiguous Inputs
    {"chat": "I don't know how I feel about this.", "expected_tone": "Tentative"},
    {"chat": "It's okay, I guess.", "expected_tone": "Neutral"},
    {"chat": "Well, that could have gone better.", "expected_tone": "Sadness"},
    {"chat": "Hmm, interesting perspective.", "expected_tone": "Analytical"},
    {"chat": "I think this might be worth exploring.", "expected_tone": "Tentative"},
    {"chat": "This is not bad, but it's not great either.", "expected_tone": "Neutral"},
    {"chat": "I need more information to decide.", "expected_tone": "Analytical"},
    {"chat": "It's hard to say at this point.", "expected_tone": "Tentative"}
]

# Function to analyze sentiment using Google API
def get_sentiment(text):
    """
    Analyze sentiment for the given text using Google NLP API.
    """
    headers = {"Content-Type": "application/json"}
    body = {
        "document": {
            "type": "PLAIN_TEXT",
            "content": text
        },
        "encodingType": "UTF8"
    }
    response = requests.post(API_URL, headers=headers, json=body)
    if response.status_code == 200:
        result = response.json()
        score = result.get("documentSentiment", {}).get("score", 0)
        magnitude = result.get("documentSentiment", {}).get("magnitude", 0)
        return score, magnitude
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None, None

# Transform benchmark data
transformed_data = []

for item in benchmark_data:
    chat_text = item["chat"]
    expected_tone = item["expected_tone"]

    # Get sentiment analysis
    score, magnitude = get_sentiment(chat_text)
    
    if score is not None and magnitude is not None:
        transformed_data.append({
            "score": score,
            "magnitude": magnitude,
            "tone": expected_tone
        })

# Save transformed data to CSV
df = pd.DataFrame(transformed_data)
df.to_csv("tone_classification_data.csv", index=False)
print("Transformed data saved to tone_classification_data.csv.")

# Train a model
X = df[["score", "magnitude"]]  # Features
y = df["tone"]  # Labels

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

clf = RandomForestClassifier(random_state=42)
clf.fit(X_train, y_train)

# Save the trained model to a .pkl file
joblib.dump(clf, "tone_classifier.pkl")
print("Trained model saved to tone_classifier.pkl.")
