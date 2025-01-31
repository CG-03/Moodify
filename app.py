from flask import Flask, request, jsonify, render_template
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import logging

# Enable logging for debugging
logging.basicConfig(level=logging.DEBUG)

# Initialize Flask app
app = Flask(__name__)

# Load the DialoGPT model and tokenizer
logging.info("Loading the DialoGPT model...")
model_name = "microsoft/DialoGPT-medium"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Store conversation history for the session
conversation_history = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    global conversation_history
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()

        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        logging.debug(f"User: {user_message}")

        # Append user message to history with separator token
        conversation_history.append(f"User: {user_message}")
        chat_input = " <|endoftext|> ".join(conversation_history)  # Use endoftext token

        # Tokenize the conversation history
        inputs = tokenizer(chat_input, return_tensors="pt", truncation=True, max_length=500)

        # Generate response
        with torch.no_grad():
            outputs = model.generate(
                inputs.input_ids,
                max_length=100,
                num_return_sequences=1,
                pad_token_id=tokenizer.eos_token_id
            )

        bot_response = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
        logging.debug(f"Bot: {bot_response}")

        # Append bot response to conversation history
        conversation_history.append(f"Bot: {bot_response}")

        # Keep only the last 5 interactions to prevent bloating
        conversation_history = conversation_history[-5:]

        return jsonify({"response": bot_response}), 200

    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        return jsonify({"error": "An error occurred while processing your request."}), 500

# Start Flask app
if __name__ == '__main__':
    logging.info("Starting Flask app...")
    app.run(debug=True)
