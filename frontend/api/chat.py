from flask import Blueprint, request, jsonify
import requests
from transformers import AutoModelForCausalLM, AutoTokenizer

chat = Blueprint('chat', __name__)

# Load DialoGPT
model_name = "microsoft/DialoGPT-medium"
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token
model = AutoModelForCausalLM.from_pretrained(model_name)

# Define CakeChat server
cakechat_server_url = "http://localhost:8080/cakechat_api/v1/actions/get_response"

# Function to query CakeChat
def get_cakechat_response(context, emotion):
    try:
        payload = {'context': context, 'emotion': emotion}
        res = requests.post(cakechat_server_url, json=payload)
        if res.status_code == 200:
            return res.json().get('response', '')
    except Exception as e:
        print(f"Error querying CakeChat: {e}")
    return None

def is_ood_input(user_input, context):
    """
    Determine if the user input is Out-of-Distribution (OOD) based on rule-based heuristics.
    """
    if not user_input.strip():  # Empty or whitespace-only input
        return True
    if len(user_input) > 100:  # Input too long
        return True
    if not any(char.isalnum() for char in user_input):  # Non-alphanumeric input
        return True
    return False


# Function to query DialoGPT
def generate_dialogpt_response(context):
    """
    Generate a response using DialoGPT while ensuring the user's input is excluded.
    """
    # Combine context with clear markers for user and bot
    dialog_input = " ".join([f"{turn}" if i % 2 == 0 else f"Bot: {turn}" for i, turn in enumerate(context)])
    
    # Tokenize the input and pass it to the model
    inputs = tokenizer(
        dialog_input + tokenizer.eos_token, 
        return_tensors="pt", 
        padding=True, 
        truncation=True
    )
    outputs = model.generate(
        inputs['input_ids'],
        max_length=100,
        num_return_sequences=1,
        pad_token_id=tokenizer.pad_token_id,
        attention_mask=inputs['attention_mask']
    )
    # Decode the output to get the bot's response
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Remove user input if it's accidentally included in the response
    response = response.replace(dialog_input, "").strip()
    return response




# Function to aggregate responses
def aggregate_responses(responses):
    if not responses:
        return "I'm sorry, I couldn't process your request."
    return max(set(responses), key=responses.count)  # Simple majority voting

@chat.route('/api/chat', methods=['POST'])
def getChatResponse():
    data = request.get_json()
    user_input = data.get('chat', '').strip()
    user_tone = data.get('tone', 'Neutral').lower()

    if not user_input:
        return jsonify({'error': 'Chat message is required'}), 400

    # Maintain context
    context = [user_input]
    if is_ood_input(user_input, context):
        return jsonify({'response': "I'm sorry, I didn't understand that. Could you rephrase?"})

    # Get responses from both models
    cakechat_response = get_cakechat_response(context, user_tone)
    dialogpt_response = generate_dialogpt_response(context)
    print(dialogpt_response)

    # Aggregate responses
    responses = [resp for resp in [cakechat_response, dialogpt_response] if resp]
    final_response = aggregate_responses(responses)

    return jsonify({'response': final_response})


