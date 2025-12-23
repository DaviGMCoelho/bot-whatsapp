import traceback
from flask import Blueprint, request, jsonify
from src.controllers.message_controller import MessageController

webhook_bp = Blueprint("webhook", __name__)

message = MessageController()

def log_error(e):
    print(e)

@webhook_bp.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        from_me = data['data']['key']['fromMe']

        if not from_me:
            instance = data['instance']
            remote_jid = data['data']['key']['remoteJidAlt']
            user_message = message.get_message_type(data['data']['message'])
            if not user_message:
                return jsonify({"error": "No valid text message"}), 400

            message.process_data(instance, remote_jid, user_message)
            return jsonify({"status": 'sucess'}), 200
        return jsonify({"status": 'sucess'}), 200

    except Exception as e:
        log_error(traceback.format_exc())
        return jsonify({"error": str(e)}), 500
