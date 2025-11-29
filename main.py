import os
import datetime
import traceback

import flask

from dotenv import load_dotenv

from src.controllers.message_controller import MessageController

load_dotenv()
message = MessageController()

app = flask.Flask(
    __name__,
    template_folder=r'src\views\templates',
    static_folder=r'src\views\static'
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
    print(e)
    #if not os.path.exists("src/data/logs"):
    #    os.mkdir('src/data/logs')
    #timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    #filename = f'{type(e).__name__}-{timestamp}.txt'

    #with open(filename, 'a', encoding='utf-8') as file:
    #    file.write(str(e))

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = flask.request.json
        instance = data['instance']
        remote_jid = data['data']['key']['remoteJid']

        user_message = get_user_message(data['data']['message'])
        if not user_message:
            return flask.jsonify({"error": "No valid text message"}), 400

        message.process_data(instance, remote_jid, user_message)
        return flask.jsonify({"status": 'sucess'}), 200

    except Exception as e:
        log_error(traceback.format_exc())
        return flask.jsonify({"error": str(e)}), 500

@app.route('/manager')
def manager():
    return flask.render_template('manager.html', titulo='Configurações')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
