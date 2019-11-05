#Importa as bibliotecas necessarias
from time import sleep
from datetime import datetime
import paho.mqtt.client as mqtt

#INICIA O MQTT
client = mqtt.Client()
client.connect("localhost",1883,60)
client.loop_start()

#MQTT SUBSCRIBE
#Atualiza Temp e Comida a cada 30 segundos
def switching(m):
    #Se segundos for igual a 0
    if (m==0):
        #Subscribe no topico temp
        client.subscribe(esp+"/temp")
        #Se tiver mensagem chama a função on_message_temp
        client.on_message = on_message_temp
    else:
        #Se não Unsubscribe no topico temp
        client.unsubscribe(esp+"/temp")
    #Se segundos for igual a 30
    if (m==30):
        #Subscribe no topico comid
        client.subscribe(esp+"/comid")
        #Se tiver mensagem chama a função on_message_comid
        client.on_message = on_message_comid
    else:
        #Se não Unsubscribe no topico comid
        client.unsubscribe(esp+"/comid")

#Função para decodificar a mensagem
def on_message_temp(client, userdata, msg):
    #Salva a mensagem do topico na variavel dados_temp
    dados_temp = msg.payload.decode()
    #Printa o dado para conferencia
    print('A temperatura é: ', dados_temp[0:5])

def on_message_comid(client, userdata, msg):
    #Salva a mensagem do topico na variavel dados_comid
    dados_comid = msg.payload.decode()
    #Printa o dado para conferencia
    print('A comida está em: ', dados_comid[0:5], '%')

#Variaveis de controle geral
i = 0
x = 0
y = 0
numesp = 2
tk = "tk"

#Variaveis de controle das ESP's
horai = [600*60, 601*60]
horaf = [660*60, 661*60]
numali = [10, 5]
tempoali = [60 , 60]
#reservatorio = []
tempototalali = [0, 0]
intervaloali = [0, 0]
margemerro = [10, 10]
horareset = horai
motor = [0, 0]
controlali = [0, 0]
hdesl = [0, 0]
while x < numesp:
    if horai[x] > horaf[x]:
        tempototalali[x] = (horaf[x]-horai[x]) + 86400
    else:
        tempototalali[x] = horaf[x]-horai[x]
    intervaloali[x] = tempototalali[x]/numali[x]
    margemerro[x] = horai[x]+10
    x += 1

#Desliga para começar desligado por padrão
while y < numesp:
    placa = "tk%s"%(y)
    client.publish(placa+"/onoff", "D");
    y += 1
#Void Loop :)
while True:
    #Obtem o horario atual
    t = datetime.now()
    #Converte as horario atual para segundos
    hora = (((t.hour*60)+t.minute)*60)+t.second
    print(t.hour, ':', t.minute, ':', t.second)
    while i < numesp:
        esp = "tk%s"%(i)
        #  Obtem os dados da ESP8266 Temperatura e Comida
        switching(t.second)
        #Logica de Ligar o Motor
        if hora>=horai[i] and hora<=margemerro[i] and motor[i]==0:
            motor[i] = 1
            #Manda comando para a ESP8266 ligar o motor
            client.publish(esp+"/onoff", "L")
            hdesl[i] = horai[i] + tempoali[i]
            controlali[i] = controlali[i]+1
        if hora>=hdesl[i] and motor[i] == 1:
            motor[i] = 0;
            #Manda comando para a ESP8266 desligar o motor
            client.publish(esp+"/onoff", "D");
            horai[i] = horai[i] + intervaloali[i];
            margemerro[i] = horai[i]+10;
        if numali[i] == controlali[i]:
            horai = horareset;
            controlali[i] = 0;
        #Printa variavel do motor e a hora para conferir
        print(motor[i])
        i += 1
    i = 0
    #Delay de 1 segundo
    sleep(1.0)