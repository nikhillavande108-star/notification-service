import os, json, base64
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/pubsub', methods=['POST'])
def handle_pubsub():
    envelope = request.get_json()
    if not envelope or 'message' not in envelope:
        return jsonify({'error': 'invalid payload'}), 400
    raw = base64.b64decode(envelope['message']['data']).decode('utf-8')
    order = json.loads(raw)
    print(
        f"[NOTIFICATION] Sending confirmation to "
        f"{order['customer_email']} for order #{order['order_id']} "
        f"(${order['amount']})"
    )
    return jsonify({'status': 'ok'}), 200

@app.route('/health')
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
