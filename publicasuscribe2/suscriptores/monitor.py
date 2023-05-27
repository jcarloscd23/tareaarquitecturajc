import json, time, stomp, sys

class Mensaje_monitor(stomp.ConnectionListener):
    def on_message(self, body):
        data = json.loads(body.body)
        print("ADVERTENCIA!!!")
        print(f"[{data['wearable']['date']}]: asistir al paciente {data['name']} {data['last_name']}... con wearable {data['wearable']['id']}")
        print(f"ssn: {data['ssn']}, edad: {data['age']}, temperatura: {round(data['wearable']['temperature'], 1)}, ritmo cardiaco: {data['wearable']['heart_rate']}, presión arterial: {data['wearable']['blood_pressure']}, dispositivo: {data['wearable']['id']}")
        print()
        time.sleep(1)

class Monitor:

    def __init__(self):
        self.topic = "monitor"

    def suscribe(self):
        print("Inicio de monitoreo de signos vitales...")
        print()
        self.consume(queue=self.topic)

    def consume(self, queue):
        try:
            conn = stomp.Connection(host_and_ports=[('localhost', 61613)])
            conn.set_listener('callback',Mensaje_monitor())
            conn.connect(wait=True)
            conn.subscribe(destination=queue, id=1)
            while True:
                time.sleep(1)

        except (KeyboardInterrupt, SystemExit):
            conn.disconnect()
            sys.exit("Conexión finalizada...")

if __name__ == '__main__':
    monitor = Monitor()
    monitor.suscribe()
    