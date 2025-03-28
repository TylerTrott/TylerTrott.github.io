import socket
import json
import random
import time

class TrafficSensor:
    def __init__(self, sensor_id, host, port, neighbors):
        self.sensor_id = sensor_id
        self.host = host
        self.port = port
        self.neighbors = neighbors  # List of (host, port) tuples
        self.inbound = 0
        self.outbound = 0
        self.traffic_threshold = 10  # Adjust signal if traffic > threshold

    def update_traffic(self):
        """Simulate inbound and outbound traffic flow."""
        self.inbound = random.randint(0, 20)  # Simulated sensor data
        self.outbound = random.randint(0, 20)

    def optimize_traffic(self):
        """Simple rule-based traffic optimization."""
        delta_q = self.inbound - self.outbound
        if delta_q > self.traffic_threshold:
            return "Increase Green Time"
        elif delta_q < -self.traffic_threshold:
            return "Reduce Green Time"
        else:
            return "Maintain Current Signal"

    def send_update(self):
        """Send traffic data to neighboring sensors."""
        data = {
            "sensor_id": self.sensor_id,
            "inbound": self.inbound,
            "outbound": self.outbound,
            "adjustment": self.optimize_traffic()
        }
        for neighbor in self.neighbors:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect(neighbor)
                    s.sendall(json.dumps(data).encode('utf-8'))
            except Exception as e:
                print(f"Failed to send data to {neighbor}: {e}")

    def start_server(self):
        """Listen for updates from neighbors."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            print(f"Sensor {self.sensor_id} listening on {self.host}:{self.port}")
            while True:
                conn, addr = s.accept()
                with conn:
                    data = conn.recv(1024)
                    if data:
                        neighbor_data = json.loads(data.decode('utf-8'))
                        print(f"Received from {neighbor_data['sensor_id']}: {neighbor_data}")

    def run(self):
        """Main loop to update traffic and communicate."""
        while True:
            self.update_traffic()
            self.send_update()
            time.sleep(5)  # Adjust update frequency

# Example Usage
if __name__ == "__main__":
    sensor = TrafficSensor(sensor_id=1, host='127.0.0.1', port=5001, neighbors=[('127.0.0.1', 5002)])
    sensor.run()
