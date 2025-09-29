pip install -r requirements.txt

ESP32 Setup
Open either .ino file in the Arduino IDE.

Go to Tools > Board and select your ESP32 model.

Go to Tools > Port and select the correct serial port.

Update the WiFi credentials (ssid and password) and the HOST_URL in the firmware to match your network and the IP address of the computer running the server.

Upload the firmware to your ESP32.

Usage
Option A: Running the Direct PC Reporter
This is the most efficient way to monitor your PC's network ports. The ESP32 is not used.

1. Start the Receiver Server
In your first terminal, run the Flask server:

Bash
python3 receiver_server.py

The server will start and listen for reports.

2. Start the PC Reporter Script
In a second terminal, run the direct reporter script.
Note: On macOS and Linux, sudo is required for psutil to access network connection details.

Bash
sudo python3 pc_reporter_direct.py

You will now see reports about your PC's listening ports appearing in the server terminal every 10 seconds.

Option B: Running the ESP32 as a Standalone Sensor
This turns your ESP32 into an independent IoT device.

1. Start the Receiver Server
In a terminal, run the Flask server:
Bash
python3 receiver_server.py

2. Power on the ESP32
Power your ESP32 (flashed with esp32_sensor_reporter.ino) via USB or another power source. Once it connects to your WiFi, it will begin sending its WiFi signal strength to the server every 10 seconds. You will see these reports appear in the server terminal.

