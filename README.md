# PyIoTMQTT
Controle dispositivos IoT utilizando Python e MQTT

## Projeto

Esse projeto nasceu com intuito de estudo, esse é meu primeiro projeto em python.

Antes, esse mesmo projeto de alimentador inteligente foi executado utilizando comunicação da ESP8266 com o firebase. Onde o usuário por um APP entrava com Hora inicial e Final, quantas alimentações seriam feitas nesse período e o tempo dessa alimentação. Cada ESP8266 lia seus respectivos dados, pegava a hora atual via NTP, calculava a hora que teria que acionar e ligava e desligava nos horários "automagicamente". Porém por ser um dispositivos para área rural teve a necessidade de funcionar offline.

Então peguei uma raspberry para ser um server local, ela tem um server MQTT(Mosquitto), a ESP8266 da um publish desses dados em um tópico único para cada ESP8266(exemplo tk0/temp e tk1/temp) temperatura e comida e subscreve um tópico "motor" onde se chegar "L" liga "D" desliga.

O código python se conecta ao broker MQTT local(a Rasp), Recebe as informações(Temperatura e Comida) via MQTT da ESP8266 a cada 30 segundos, recebe as variáveis para calcular a hora de acionamento da ESP8266, calcula e se for a hora correta envia o comando via MQTT para ESP8266 acionar um atuador(nesse caso um relé).

Para mim o mais importante esse código pode receber informações, calcular e atuar N placas bastando só adicionar as informações do cálculo na lista da sua respectiva variável, retirando qualquer processamento 'bruto' da ESP8266. Ou seja eu posso adicionar N placas a rede que meu código pode gerenciar isso.

Os próximos passos é criar um APP e mais para frente adicionar uma IA e ML para realmente ser um alimentador inteligente.

### Instalação
Em breve...

### Contribua
1. Fork it (<https://github.com/b00tk1ll/PyIoTMQTT/fork>)
2. Crie uma feature branch (`git checkout -b feature/branch-name`)
3. Commit suas alterações (`git commit -m 'Add some features'`)
4. Push para a branch (`git push origin feature/branch-name`)
5. Solicite um Pull Request

### Autores

* **Guilherme Silveira** - *Projeto* - [b00tk1ll](https://github.com/b00tk1ll)

Veja a lista completa de [contributors](https://github.com/b00tk1ll/samusci/contributors) que participaram desse projeto.

### License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
