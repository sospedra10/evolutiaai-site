from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS  
from utils import save_contact_data, get_agent_response, create_agent

# https://tinyurl.com/sospi-ai

app = Flask(__name__)
CORS(app) # Enable CORS for all routes (you might want to be more specific in a real application)

agent = create_agent()


@app.route('/')
def index():
    """Renders the home page."""
    return render_template('home.html')

@app.route('/translations/<lang>.json')
def translations(lang):
    return send_from_directory('translations', f'{lang}.json')

@app.route('/api/chat', methods=['POST'])
async def chat():
    if request.method == 'POST':
        try:
            data = request.get_json()
            message = data.get('message')
            history = data.get('history', [])[-6:]  # message is included in history
            # print('Message:', message)
            # print("Length of history:", len(history))
            # print('History:\n', history)
            try:
                response = await get_agent_response(agent, history)
                response = response.final_output
            except:
                print('Error in chat')
                response = "Lo siento, parece que hay un problema con el servidor. Por favor, inténtalo de nuevo más tarde."
            
            # print('Response:', response)
            
            return jsonify({'response': response}), 200
        except Exception as e:
            print(f"Error processing chat request: {e}")
            return jsonify({'error': 'Failed to process request'}), 500
    return jsonify({'error': 'Invalid request method'}), 400



@app.route('/api/submit-contact-form', methods=['POST'])
def submit_contact_form():
    if request.method == 'POST':
        try:
            print("Received a POST request")
            data = request.get_json()
            name = data.get('name')
            email = data.get('email')
            company = data.get('company')
            message = data.get('message')

            save_contact_data(name, email, company, message)

            return jsonify({'message': 'Data received and saved successfully!'}), 200
        except Exception as e:
            print(f"Error processing form submission: {e}")
            return jsonify({'error': 'Failed to save data'}), 500
    return jsonify({'error': 'Invalid request method'}), 400


@app.route('/intelligent-chatbots', methods=['GET'])
def intelligent_chatbots():
    return render_template('intelligent_chatbots.html')
    # return send_from_directory('.', 'intelligent_chatbots.html')


if __name__ == '__main__':
    app.run(debug=True) # Only use debug=True for development