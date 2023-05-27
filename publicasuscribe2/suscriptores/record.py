import json, time, stomp, sys, os

class Registro_paciente(stomp.ConnectionListener):
    def on_message(self, body):
        print("datos recibidos, actualizando expediente del paciente...")
        data = json.loads(body.body)
        record_file = open (f"./records/{data['ssn']}.txt",'a')
        record_file.write(f"\n[{data['wearable']['date']}]: {data['name']} {data['last_name']}... ssn: {data['ssn']}, edad: {data['age']}, temperatura: {round(data['wearable']['temperature'], 1)}, ritmo cardiaco: {data['wearable']['heart_rate']}, presión arterial: {data['wearable']['blood_pressure']}, dispositivo: {data['wearable']['id']}")
        record_file.close()
        time.sleep(1)

class Record:

    def __init__(self):
        try:
            os.mkdir('records')
        except OSError as _:
            pass
        self.topic = "record"

    def suscribe(self):
        print("Esperando datos del paciente para actualizar expediente...")
        print()
        self.consume(queue=self.topic)

    def consume(self, queue):
        try:
            conn = stomp.Connection(host_and_ports=[('localhost', 61613)])
            conn.set_listener('callback', Registro_paciente())
            conn.connect(wait=True)
            conn.subscribe(destination=queue, id=1)
            while True:
                time.sleep(1)

        except (KeyboardInterrupt, SystemExit):
            conn.disconnect()
            sys.exit("Conexión finalizada...")

if __name__ == '__main__':
    record = Record()
    record.suscribe()
