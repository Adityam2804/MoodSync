import requests
import json

# Define the API URL
API_URL = "http://127.0.0.1:4000/api/tone"

# Benchmark dataset
benchmark_data = [
    # Positive Sentiments
    {"chat": "I'm so happy today!", "expected_tone": "Joy"},
    {"chat": "This is the best day of my life!", "expected_tone": "Joy"},
    {"chat": "I can't wait for the weekend!", "expected_tone": "Joy"},
    {"chat": "You did an amazing job on this project!", "expected_tone": "Confident"},

    # Negative Sentiments
    {"chat": "I feel sad and lonely.", "expected_tone": "Sadness"},
    {"chat": "I'm so disappointed in myself.", "expected_tone": "Sadness"},
    {"chat": "Why does everything have to go wrong?", "expected_tone": "Sadness"},
    {"chat": "I can't believe you did that!", "expected_tone": "Anger"},
    {"chat": "You're the worst!", "expected_tone": "Anger"},

    # Neutral Sentiments
    {"chat": "It's a sunny day outside.", "expected_tone": "Neutral"},
    {"chat": "I'll see you at 5 PM.", "expected_tone": "Neutral"},
    {"chat": "There are 24 hours in a day.", "expected_tone": "Neutral"},
    {"chat": "This is a statement with no emotion.", "expected_tone": "Neutral"},

    # Tentative/Analytical Sentiments
    {"chat": "I'm not sure if this will work.", "expected_tone": "Tentative"},
    {"chat": "This data suggests a strong correlation.", "expected_tone": "Analytical"},
    {"chat": "Let's try a different approach to solve this.", "expected_tone": "Tentative"},
    {"chat": "The results seem inconclusive so far.", "expected_tone": "Analytical"},

    # Sensitive Topics
    {"chat": "Men are better at math.", "expected_tone": "Neutral"},
    {"chat": "Women are always emotional.", "expected_tone": "Neutral"},
    {"chat": "Diversity in the workplace is a strength.", "expected_tone": "Confident"},
    {"chat": "I believe in equal rights for everyone.", "expected_tone": "Confident"},


    # Ambiguous Inputs
    {"chat": "I don't know how I feel about this.", "expected_tone": "Tentative"},
    {"chat": "It's okay, I guess.", "expected_tone": "Neutral"},
    {"chat": "Well, that could have gone better.", "expected_tone": "Sadness"},
    {"chat": "Hmm, interesting perspective.", "expected_tone": "Analytical"}
]


# Test fairness
def test_fairness(api_url, benchmark_data):
    results = []
    for data in benchmark_data:
        try:
            # Send request to the API
            response = requests.post(api_url, json={"chat": data["chat"]})
            response.raise_for_status()
            detected_tone = response.json().get("tone", "Neutral")

            # Evaluate fairness
            bias = detected_tone != data["expected_tone"]
            results.append({
                "input": data["chat"],
                "expected_tone": data["expected_tone"],
                "detected_tone": detected_tone,
                "bias": bias
            })

        except Exception as e:
            print(f"Error processing input '{data['chat']}': {e}")
            results.append({
                "input": data["chat"],
                "expected_tone": data["expected_tone"],
                "detected_tone": "Error",
                "bias": True
            })

    return results

# Run the test and print results
fairness_results = test_fairness(API_URL, benchmark_data)
print(json.dumps(fairness_results, indent=2))

# Calculate and print the bias rate
bias_rate = sum(1 for result in fairness_results if result["bias"]) / len(fairness_results)
print(f"Bias Rate: {bias_rate * 100:.2f}%")
