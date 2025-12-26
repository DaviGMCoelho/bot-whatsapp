import traceback
from flask import Blueprint, request, jsonify, current_app

webhook_bp = Blueprint("webhook", __name__)

def log_error(e):
    print(e)

@webhook_bp.route('/webhook', methods=['POST'])
def webhook():
    try:
        controller = current_app.container["message_controller"]
        data = request.get_json()
        from_me = data['data']['key']['fromMe']

        if not from_me:
            instance = data['instance']
            remote_jid = data['data']['key']['remoteJidAlt']
            user_message = controller.get_message_type(data['data']['message'])
            if not user_message:
                return jsonify({"error": "No valid text message"}), 400

            controller.process_data(instance, remote_jid, user_message)
            return jsonify({"status": 'sucess'}), 200
        return jsonify({"status": 'sucess'}), 200

    except Exception as e:
        log_error(traceback.format_exc())
        return jsonify({"error": str(e)}), 500
