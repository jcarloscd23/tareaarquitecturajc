'''
name bot: SMAMBot
username: SMAM_Mensajebot
'''

import json, time, stomp, sys, telepot

class Mensaje_alerta(stomp.ConnectionListener):

    def __init__(self,token,chat_id):
        self.token = token
        self.chat_id = chat_id

    def on_message(self, body):
        print("enviando notificación de signos vitales...")
        if self.token and self.chat_id:
            print("\tMENSAJE ENVIADO", end="\n")
            data = json.loads(body.body)
            message = f"ADVERTENCIA!!!\n[{data['wearable']['date']}]: asistir al paciente {data['name']} {data['last_name']}...\nssn: {data['ssn']}, edad: {data['age']}, temperatura: {round(data['wearable']['temperature'], 1)}, ritmo cardiaco: {data['wearable']['heart_rate']}, presión arterial: {data['wearable']['blood_pressure']}, dispositivo: {data['wearable']['id']}"
            bot = telepot.Bot(self.token)
            print(bot.getMe())
            bot.sendMessage(self.chat_id, message)
        else:
            print("\tMENSAJE NO ENVIADO", end="\n")
        time.sleep(5)

class Notifier:
    
    def __init__(self):
        self.topic = "notifier"
        self.token = '6123823618:AAHyUAjkloJePnXt9Na-HRCZfk86_oiNRc0'
        self.chat_id = "5813006283," #El chat_id es diferente para cada usuario

    def suscribe(self):
        print("Inicio de gestión de notificaciones...")
        print()
        self.consume(queue=self.topic)

    def consume(self, queue):
        try:
            conn = stomp.Connection(host_and_ports=[('localhost', 61613)])
            conn.set_listener('callback', Mensaje_alerta(self.token,self.chat_id))
            conn.connect(wait=True)
            conn.subscribe(destination=queue, id=1)
            while True:
                time.sleep(1)
        
        except (KeyboardInterrupt, SystemExit):
            conn.disconnect()
            sys.exit("Conexión finalizada...")

if __name__ == '__main__':
    notifier = Notifier()
    notifier.suscribe()
