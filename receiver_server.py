# receiver_server.py
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/report', methods=['POST'])
def receive_report():
    # Check if the incoming request has JSON data
    if not request.is_json:
        print("Received non-JSON data")
        return jsonify({"status": "error", "message": "Request must be JSON"}), 400

    # Get the JSON data from the request
    data = request.get_json()

    # Print the data to the console so you can see it
    print("\n--- ✅ Report received from ESP32 ---")
    print(data)
    print("--------------------------------------\n")

    # Send a success response back to the ESP32
    return jsonify({"status": "success", "message": "Data received"}), 200

if __name__ == '__main__':
    # Run the server, accessible on your local network
    # The host '0.0.0.0' makes it available to other devices on the network
    print("Receiver server is running...")
    print("Listening for reports at http://<YOUR_PC_IP>:5000/report")
    app.run(host='0.0.0.0', port=5000, debug=True)