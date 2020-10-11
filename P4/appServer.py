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
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)


# se fosse apenas o arduino, uma porta de comunicaçã seria suficiente, estamos usando duas pq o software de emular recebe um uma porta e envia em outra
serialName = "/dev/cu.usbmodem14201"
# serialName2 = "COM6"                 # Windows(variacao de)
#/dev/cu.usbmodemFA131 -- Due
#/dev/cu.usbmodemFD1211 -- uno
serverID = 1

def main():
    try:
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        
        server = Tinker(serialName)
        pacman = Squire()
    
        serverLog = open("./serverLog.txt", "w")
        serverLog.write(f"{dt.now()} / Communication started!\n")
        
        IDs = {
            "sensorID" : 42,
            "serverID" : 1
        }


        timeOut = pacman.makeAnswer(5,IDs)

        running = True
        orion = True
        cont = 0
        lastIndex = 0
        
        print("-"*25)
        print("Port enabled")

        print(f"Port: {server.comPort.fisica.name}")


        print("-"*25)
        print("Waiting for Client to show up..")
        # Loooop to receive handshake
        while running:

            if orion:
                time.sleep(3)
                if server.isEmpty():
                    print("-"*25)
                    print("Buffer seems to be empty\nTrying again...")
                    time.sleep(0.5)
                    
                else:
                    handshake, thumb = server.getAnswer()
                    pacman.logging(serverLog, "r", handshake)
                    clientID = thumb["serverID"]
                    print("-"*25)
                    print("There it is!")
                    

                    # Check if the IDs are the same
                    if (clientID == IDs["serverID"]) and (thumb["type"] == 1):
                        orion = False
                        nPacks = thumb["nPacks"]
                        ans = pacman.makeAnswer(2,IDs)
                        server.sendPackage(ans)
                        pacman.logging(serverLog, "s", ans)
                        print("-"*25)
                        print("Sent it the answer!")
                    
                    else:
                        print("-"*25)
                        print("It seems like the IDs don't match :(")
                        print(f"Client's: {clientID}")
                        print(f"Server's: {IDs['serverID']}")
                        continue

                    time.sleep(1)
            
            if not orion:
                if cont < nPacks:
                    timeTryAgain = time.time() + 2
                    timeOut = time.time() + 20
                    
                    while True:
                        # if cont == 4:
                        #     time.sleep(5)
                        if not server.isEmpty() and time.time() < timeOut:
                                head = server.comPort.getData(10)
                                headDict = pacman.readHeader(head)
                                
                                if (headDict["type"] == 3):
                                    iReceived = headDict["packIndex"]
                                    # if (iReceived + 1) == headDict["nPacks"]:
                                    #     break
                                    server.getPackage(head)
                                    pacman.logging(serverLog, "r", server.pack)
                                    print("-"*25)
                                    print(f"Pack of number {iReceived+1} received")
                                    first = (iReceived == 0)
                                    theOneAfter = (iReceived - lastIndex == 1)
                                    rightEop = server.eopCheck()
                                    crcCalc = Crc16.calc(server.payload).to_bytes(2, "big").hex().upper()
                                    crcReceived = headDict["CRC"]
                                    rightCrc = crcCalc == crcReceived
                                    print(rightCrc)
                                    # rightCRC = 
                                    if (first or theOneAfter) and (rightEop):
                                        print("Its the RIGHT pack")
                                        server.addPayload(server.pack)
                                        ans = pacman.makeAnswer(4, IDs, lastIndex)
                                        server.sendPackage(ans)
                                        pacman.logging(serverLog, "s", ans)
                                        lastIndex = iReceived
                                        cont += 1

                                    else:
                                        print("Its the WRONG pack")
                                        ans = pacman.makeAnswer(6, IDs, lastIndex)
                                        cont = lastIndex + 1
                                        server.sendPackage(ans)
                                        print("Telling Client to send again..", lastIndex)
                                        pacman.logging(serverLog, "s", ans)
                                    
                                    break

                                elif (headDict["type"] == 1):
                                    print("-"*25)
                                    print("That was the handshake again!")
                                    ans = pacman.makeAnswer(2,IDs)
                                    server.sendPackage(ans)
                                    pacman.logging(serverLog, "s", ans)                                    
                                    print("You can start sending already...")

                                elif (headDict["type"] == 5):
                                    print("TimeOut!!")
                                    sys.exit()
                        else:
                            time.sleep(1)
                            if time.time() > timeOut:
                                
                                orion = True
                                ans = pacman.makeAnswer(5, IDs)
                                server.sendPackage(ans)
                                pacman.logging(serverLog, "s", ans)
                                server.finnish()
                                sys.exit()
                            
                            else:
                                if time.time() > timeTryAgain:
                                    print("#"*25)
                                    ans = pacman.makeAnswer(6,IDs,lastIndex)
                                    server.sendPackage(ans)
                                    pacman.logging(serverLog, "s", ans)

                            
                            

                else:
                    print("Holy shit, it worked!")
                    serverLog.write(f"{dt.now()} / Communication finished!")
                    serverLog.close()
                    running = False

        imageW = "./imgReceived.png"
        print("-------------------------")
        print ("Saving in directory:")
        print (" - {}".format(imageW))
        f = open(imageW, 'wb')
        print("Hello There!")
        server.assembleData()
        f.write(server.fullArchive)

        # Fecha arquivo de imagem
        f.close()  
        print("Image saved!")

        server.finnish()

    except:
        print("ops! :-\\")
        server.finnish()

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()


# Para fazer esse projeto foram feitas alterações no loopback, e na montagem dos arduínos. Foi necessário
# conectar os pinos tx de um com o rx do outro e vice-versa. Como o tamanho da imagem não era conhecido
# o client envia, primeiro, o tamanho da imagem em 4 bytes. Como esse número é conhecido pelo server esse
# não tem problemas para lê-lo e em seguida, sabendo agora o tamanho do arquivo, consegue receber a imagem.
# Em seguida, o server verifica o tamanho da imagem recebida e envia (também no formato de 4 bytes). Dessa,
# forma o client pode ter certeza se o arquivo foi enviado por completo.