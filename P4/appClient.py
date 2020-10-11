#####################################################
# Camada Física da Computação
#Carareto
#28/08/2020
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 
#ALGUNS ARDUINOS PRECISAM FICAR COM O BOTAO DE RESET PRESSIONADO. OU O PINO RESET ATERRADO!

from enlace import *
import time
from Squire import *
from Tinker import *
from datetime import datetime as dt
from crccheck.crc import Crc16
import sys

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
# para saber a sua porta, execute no terminal :
# python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)


# se fosse apenas o arduino, uma porta de comunicaçã seria suficiente, estamos usando duas pq o software de emular recebe um uma porta e envia em outra
serialName = "/dev/cu.usbmodem14101"
# serialName2 = "COM5"                 # Windows(variacao de)
#/dev/cu.usbmodemFA131 -- Due
#/dev/cu.usbmodemFD1211 -- uno



def main():
    try:
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.

        client = Tinker(serialName)
        pacman = Squire()
        
        clientLog = open("./clientLog.txt", "w")

        IDs = {
            "type" : 3,
            "sensorID" : 42,
            "serverID" : 1
        }
        
        timeOut = pacman.makeAnswer(5,IDs)
        # imageR = input("Input image directory: ")
        imageR = "./img.png"

        # Carrega imagem
        
        file = open(imageR, "rb").read()
        
        packs = pacman.fragment(file, IDs)
        nPacks = len(packs)
        
        print("-"*25)
        print(f"File has {nPacks*114/1000}KBytes")
        clientLog.write(f"File of {nPacks*114/1000}KBytes will be sent\n")
        clientLog.write(f"{dt.now()} / Communication started!\n")

        # Log
        print("-------------------------")
        print("Initializing communication")
        print("Port: {}".format(client.comPort.fisica.name))

        running = True
        start = False
        index = 0

        while running:
            if not start:
                print("-------------------------")
                print("Salut Server!")
                
                client.sendHandShake(IDs["serverID"],nPacks)
                pacman.logging(clientLog, "s", client.handshake)
                time.sleep(2)
                print(client.isEmpty())
                if client.isEmpty():
                    print("-"*25)
                    print("Server seems to be off.")
                    tryAgain = input("Want to try again? Y/N: ")

                    if tryAgain == "n" or tryAgain == "N":
                        sys.exit()
                    else:
                        continue

                else:
                    print("entrou aq")
                    ans, ansHead = client.getAnswer()
                    pacman.logging(clientLog, "r", ans)
                    if ansHead["type"] == 2:
                        start = True
                        print("-"*25)
                        print("Server sends its regards")
                    else:
                        print("-"*25)
                        print("Something went wrong"*25)

            if start:
                if index < nPacks: 
                    if index == 7:
                        index = 6
                    
                    pck = packs[index]
                    client.sendPackage(pck)
                    pacman.logging(clientLog, "s", pck)
                    print("-"*25)
                    print(f"{index+1} package was sent!")
                    timeResend = time.time() + 5
                    timeOut = time.time() + 20

                    print("-"*25)
                    print("Waiting for server's response")
                    while True:
                        # print(time.time() - timeResend)

                        if not client.isEmpty():
                            ans, ansHead = client.getAnswer()
                            pacman.logging(clientLog, "r", ans)

                            if ansHead["type"] == 4:
                                index += 1
                                print("Server received it well ;)")
                                break
                            
                            elif ansHead["type"] == 5:
                                print("timeout!")
                                clientLog.write(f"{dt.now()} / Timeout! Ending communication")
                                sys.exit()
                        
                        elif time.time() > timeResend:
                            client.sendPackage(pck)
                            
                            pacman.logging(clientLog, "s", pck)
                            timeResend = time.time() + 5

                            if time.time() > timeOut:
                                client.sendPackage(timeOut)
                                pacman.logging(clientLog, "r", pck)
                                client.finnish()
                                sys.exit()
                            else:
                                if not client.isEmpty():
                                    ans, ansHead = client.getAnswer()
                                    pacman.logging(clientLog, "r", ans)

                                    if ansHead["type"] == 6:
                                        index = ansHead["errorIndex"] + 1
                                        client.sendPackage(packs[index])
                                        print("-"*25)
                                        print(f"{index+1} package sent!")
                                        pacman.logging(clientLog, "s", packs[index])
                                        timeResend = time.time() + 5
                                        timeOut = time.time() + 20
                else:
                    clientLog.write(f"{dt.now()} / Communication finished!")
                    print("-"*25)
                    print("Damn, it really did work!")
                    client.finnish()
                    running = False
                                    
    except:
        print("ops! :-\\")
        client.finnish()

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
