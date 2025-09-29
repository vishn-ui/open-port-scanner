# pc_port_reporter_autodetect_retry.py
import psutil, json, time, sys
import socket # ⬅️ ADD THIS LINE
import psutil, json, time, sys
try:
    import serial
    import serial.tools.list_ports as list_ports
except Exception as e:
    print("pyserial not installed. Run: python3 -m pip install --user pyserial")
    sys.exit(1)

BAUDRATE = 115200
DEFAULT_TIMEOUT = 2
OPEN_RETRIES = 30         # total attempts to open port
RETRY_DELAY_SECONDS = 1.0 # wait between attempts

def find_ports():
    return list(list_ports.comports())

def guess_port():
    ports = find_ports()
    if not ports:
        return None
    candidates = []
    for p in ports:
        desc_l = ((p.description or "") + " " + (p.manufacturer or "") + " " + (p.hwid or "")).lower()
        if any(x in desc_l for x in ["silicon", "cp210", "ch340", "ftdi", "usb serial", "wch"]):
            candidates.append(p.device)
    if len(candidates) == 1:
        return candidates[0]
    cu_ports = [p.device for p in ports if p.device.startswith("/dev/cu.")]
    if len(cu_ports) == 1:
        return cu_ports[0]
    # if ambiguous, prefer the first /dev/cu.* seen
    if cu_ports:
        return cu_ports[0]
    return None

def choose_port_interactive():
    ports = find_ports()
    if not ports:
        print("No serial ports found. Is the ESP32 plugged in?")
        sys.exit(1)
    print("Available serial ports:")
    for i, p in enumerate(ports):
        print(f"{i}: {p.device} - {p.description} - {p.hwid}")
    sel = input("Enter port index to use (or full path): ").strip()
    if sel.isdigit():
        return ports[int(sel)].device
    return sel

def get_listening_ports():
    conns = psutil.net_connections(kind='inet')
    ports = []
    for c in conns:
        if c.status == psutil.CONN_LISTEN:
            laddr = c.laddr
            port = laddr.port
            proto = 'tcp' if c.type == socket.SOCK_STREAM else 'udp'
            ports.append({"port": port, "proto": proto, "pid": c.pid})
    seen = set()
    uniq = []
    for p in sorted(ports, key=lambda x: x['port']):
        key = (p['port'], p['proto'])
        if key not in seen:
            seen.add(key)
            uniq.append(p)
    return uniq

def open_serial_with_retries(port, baud=115200, retries=OPEN_RETRIES, delay=RETRY_DELAY_SECONDS):
    import serial
    for attempt in range(1, retries+1):
        try:
            ser = serial.Serial(port, baud, timeout=DEFAULT_TIMEOUT)
            print(f"[+] Serial opened on {port}")
            return ser
        except serial.SerialException as e:
            msg = str(e)
            print(f"[{attempt}/{retries}] Cannot open {port}: {msg}")
            if "Resource busy" in msg:
                print("    -> Port is busy. Close Serial Monitor / other apps or unplug/replug the board.")
            time.sleep(delay)
    raise RuntimeError(f"Failed to open serial port {port} after {retries} attempts")

def main():
    port = guess_port()
    if not port:
        print("Couldn't auto-detect a single likely ESP32 port.")
        port = choose_port_interactive()
    print("Using serial port:", port)

    # Try opening the serial port with retries
    try:
        ser = open_serial_with_retries(port)
    except Exception as e:
        print("Fatal:", e)
        sys.exit(1)

    payload = {
        "hostname": None,
        "timestamp": int(time.time()),
        "listening_ports": get_listening_ports()
    }
    data = json.dumps(payload)
    print("Sending JSON to ESP32:", data)
    try:
        ser.write((data + "\n").encode('utf-8'))
        ser.flush()
        ser.close()
        print("Done.")
    except Exception as e:
        print("Error writing to serial:", e)

if __name__ == "__main__":
    main()
