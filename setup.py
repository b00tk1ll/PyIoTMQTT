#Importa as bibliotecas necessarias
from time import sleep
from datetime import datetime
import paho.mqtt.client as mqtt
import pymongo

#CONFIGURÇÕES MONGODB
#Conecta ao server do MongoDB
client = pymongo.MongoClient("mongodb://b00tk1ll:b00tk1ll22031998@peixe-shard-00-00-bt4m7.gcp.mongodb.net:27017,peixe-shard-00-01-bt4m7.gcp.mongodb.net:27017,peixe-shard-00-02-bt4m7.gcp.mongodb.net:27017/test?ssl=true&replicaSet=peixe-shard-0&authSource=admin&retryWrites=true&w=majority")
#Seleciona o banco
db = client.peixe
#Seleciona a colection HW
hw = db.hw
#Seleciona a colection APP
app = db.app

#INICIA O MQTT
client = mqtt.Client()
client.connect("localhost",1883,60)
client.loop_start()

def init_var(x=0):
    #Chama a função d_ini
    d_ini(x)
    #Atribui valores as variaveis de controle
    while x < numesp:
        motor.append(0)
        controlali.append(0)
        hdesl.append(0)
        if horai[x] > horaf[x]:
            tempototalali.append((horaf[x]-horai[x]) + 86400)
        else:
            tempototalali.append(horaf[x]-horai[x])
        intervaloali.append(tempototalali[x]/numali[x])
        margemerro.append(horai[x]+10)
        x += 1

#Obtem as variaveis do server MongoDB
def d_ini(x=0):
    while x < numesp:
        placa = "tk%s"%(x)
        dado = hw.find_one({"_id": placa})
        horai.append(dado["horai"]*60)
        horaf.append(dado["horaf"]*60)
        numali.append(dado["numali"]*60)
        tempoali.append(dado["tempoali"]*60)
        x += 1


#Manda comando para todas as ESP8266 começarem desligadas por padrão
def desl(x=0):
    while x < numesp:
        placa = "tk%s"%(x)
        client.publish(placa+"/onoff", "D");
        x += 1


#Funções para dar update nos dados ou adicionar esp ano
def update_db():
    #Recebe variavel de controle do server
    n = hw.find_one({"_id": "ctrl"})
    control = n["control"]
    #Atualiza os dados
    if(control == 1 and nesp==numesp):
        d_update()
        hw.update_one({'_id': 'ctrl'}, {'$set': {'control': 0}})
    #Se for adicionado mais uma esp
    elif(control == 1 and nesp!=numesp):
        add = nesp-numesp
        numesp = numesp+add
        init_var(nesp-add)

def d_update(x=0):
    while x < numesp:
        placa = "tk%s"%(x)
        dado = hw.find_one({"_id": placa})
        horai[x] = (dado["horai"]*60)
        horaf[x] = (dado["horaf"]*60)
        numali[x] = (dado["numali"]*60)
        tempoali[x] = (dado["tempoali"]*60)
        x += 1


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
    t_esp = msg.topic[0:3]
    #Salva a mensagem do topico na variavel dados_temp
    dados_temp = msg.payload.decode()
    #Faz o update do dado de temperatura no server
    app.update_one({'_id': t_esp}, {'$set': {'temp': float(dados_temp[0:5])}})

def on_message_comid(client, userdata, msg):
    t_esp = msg.topic[0:3]
    #Salva a mensagem do topico na variavel dados_comid
    dados_comid = msg.payload.decode()
    #Faz o update do dado de comida no server
    app.update_one({'_id': t_esp}, {'$set': {'comid': float(dados_comid[0:5])}})

#Obtem a variavel de quantas ESP8266 tem no sistema
n = hw.find_one({"_id": "numesp"})
numesp = n["numesp"]

#Variaveis de controle das ESP's
horai = []
horaf = []
numali = []
tempoali = []
tempototalali = []
intervaloali = []
margemerro = []
horareset = horai
motor = []
controlali = []
hdesl = []
i = 0

#Chama a função init_var()
init_var()

#Chama a função desl()
desl()

#Void Loop :)
while True:
    #Obtem o horario atual antes da execução do codigo
    t = datetime.now()
    #Salva em S1 os segundos e microsegundos para calcular tempo de maquina
    s1 = float(f'{t.second}.{t.microsecond}')
    #Obtem numesp para verificar se teve adicão de novas placas na rede
    e = hw.find_one({"_id": "numesp"})
    nesp = e["numesp"]
    #Chama update_db
    update_db()
    #Converte as horario atual para segundos
    hora = (((t.hour*60)+t.minute)*60)+t.second
    #Printa variavel de hora para conferencia
    print(t.hour, ':', t.minute, ':', t.second,)
    #Laço para processar os dados e atuar todas as placas
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
        i += 1
    i = 0
    #Obtem o horario atual depois da execução do codigo
    t2 = datetime.now()
    #Salva em S1 os segundos e microsegundos para calcular tempo de maquina
    s2 = float(f'{t2.second}.{t2.microsecond}')
    #Calcula o tempo de maquina
    s3 = s2-s1
    #Delay de 1 segundo menos o tempo maquina
    sleep(1.0-s3)