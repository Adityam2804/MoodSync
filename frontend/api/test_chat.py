from sentence_transformers import SentenceTransformer, util
import numpy as np
import matplotlib.pyplot as plt
import requests

def plot_similarity_scores(inputs, expected_tones, detected_tones, similarity_scores):
    # Ensure the length of all lists are the same
    assert len(inputs) == len(expected_tones) == len(detected_tones) == len(similarity_scores), "All input lists must have the same length."

    # Prepare data for plotting
    y_positions = np.arange(len(inputs))
    
    # Create the plot
    plt.figure(figsize=(10, 8))
    plt.barh(y_positions, similarity_scores, color='skyblue', edgecolor='black')
    plt.yticks(y_positions, [f"Input: {inp}\n  Output:{det}" for inp, exp, det in zip(inputs, expected_tones, detected_tones)])
    
    plt.xlabel('Similarity Score')
    plt.ylabel('Chat Inputs and Outputs')
    plt.title('Chat Detection Similarity Scores')
    plt.grid(True)
    plt.gca().invert_yaxis()  # Invert the y-axis so the highest scores are on top
    plt.show()

def fetch_responses_from_chatbot(api_url, inputs):
    generated_responses = []
    for input_text in inputs:
        try:
            # Send request to chatbot API
            response = requests.post(api_url, json={"chat": input_text})
            response.raise_for_status()
            chatbot_response = response.json().get("response", "No response")
            generated_responses.append(chatbot_response)
        except Exception as e:
            print(f"Error fetching response for input '{input_text}': {e}")
            generated_responses.append("Error fetching response")
    return generated_responses

def main():
    # Initialize the model
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Define chat inputs and expected responses
    chatbot_inputs = [
        "I feel sad today.",
        "I just got a new job!",
        "I'm really tired of all this rain.",
        "My team lost the game last night.",
        "I can't find my favorite book.",
        "I had a great workout session today!",
        "I am not feeling well.",
        "Today is my birthday.",
        "I just finished a big project.",
        "It's really cold outside."
    ]

    expected_responses = [
        "I'm sorry to hear that. Let's play something to cheer you up.",
        "Congratulations! That's awesome!",
        "Rainy days can be tough. How about some music to lift your spirits?",
        "That's disappointing. Some motivational music might help.",
        "Let's find a relaxing song while you look for it.",
        "That's great! Some energetic music would match your mood.",
        "I hope you feel better soon. Here's a song to help you relax.",
        "Happy Birthday! Here's a special song for your special day.",
        "Well done! Let's enjoy some celebratory music.",
        "Stay warm! I'll play some cozy songs for you."
    ]

    # Define the chatbot API URL
    chatbot_api_url = "http://127.0.0.1:4000/api/chat"  # Replace with your chatbot API URL

    # Fetch responses from the chatbot dynamically
    generated_responses = fetch_responses_from_chatbot(chatbot_api_url, chatbot_inputs)

    # Calculate embeddings and similarities
    reference_embeddings = model.encode(expected_responses)
    generated_embeddings = model.encode(generated_responses)
    similarities = util.pytorch_cos_sim(generated_embeddings, reference_embeddings)

    # Display similarity scores
    similarity_scores = similarities.diag().numpy()
    for i, score in enumerate(similarity_scores):
        print(f"Input: {chatbot_inputs[i]}")
        print(f"Expected Response: {expected_responses[i]}")
        print(f"Generated Response: {generated_responses[i]}")
        print(f"Similarity Score: {score:.2f}")
        print("-----------")
    
    # Plot the similarity scores
    plot_similarity_scores(chatbot_inputs, expected_responses, generated_responses, similarity_scores)

if __name__ == "__main__":
    main()
