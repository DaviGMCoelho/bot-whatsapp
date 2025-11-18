import os

import flask
import datetime

from dotenv import load_dotenv

from src.services.message_service import EvolutionAPI
from src.services.gemini_service import GeminiService

load_dotenv()
evolution = EvolutionAPI(str(os.getenv("AUTHENTICATION_API_KEY")))
gemini = GeminiService(
    api_key=os.getenv("GOOGLE_API_KEY"),
    document=r'data\base_dados.csv',
    temperature=0
)

app = flask.Flask(
    __name__,
    template_folder=r'views\templates',
    static_folder=r'views\static'
)

def get_user_message(message_data: dict):
    msg_type = message_data.get('messageType')
    if msg_type == 'conversation' or 'conversation' in message_data:
        return message_data.get('conversation')
    elif msg_type == 'extendedTextMessage' or 'extendedTextMessage' in message_data:
        return message_data.get('extendedTextMessage').get('text')
    else:
        print("tipo não reconhecido:", msg_type, message_data)
        return None

def log_error(e):
    if not os.path.exists("logs"):
        os.mkdir('logs')
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f'logs/{type(e).__name__}-{timestamp}.txt'

    with open(filename, 'a', encoding='utf-8') as file:
        file.write(str(e))

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = flask.request.json
        instance = data['instance']
        remote_jid = data['data']['key']['remoteJid']

        user_message = get_user_message(data['data']['message'])
        if not user_message:
            return "No valid text message", 400

        message = gemini.generate_message(user_message)
        evolution.send_message(instance, remote_jid.split('@')[0], message)
        return flask.jsonify(message)

    except Exception as e:
        log_error(e)
        return flask.jsonify({"error": str(e)}), 500

@app.route('/manager')
def manager():
    return flask.render_template('manager.html', titulo='Configurações')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

