import os
from openai import OpenAI
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get OpenAI API key from environment variables
openai_api_key = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=openai_api_key)


@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Get the message from the request body
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({'error': 'Message is required'}), 400
        
        user_message = data['message']
        
        # Create a response using the specified model
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant. Please answer the user's query."
                },
                {"role": "user", "content": user_message},
            ],
        )
        
        # Extract the output text
        answer = response.choices[0].message.content.strip()
        
        return jsonify({'response': answer}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1', port=8000)
