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
from archive import *
from packManager import *
from tinker import *

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



def main():
    try:
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        tinkeroo = tinker(serialName)
        packM = packManager()
    
        print("-------------------------")
        print("Port enabled")
        print("-------------------------")
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        
        # Log
        print("-------------------------")
        print("Initializing communication")
        print("Port: {}".format(tinkeroo.comPort.fisica.name))
        print("-------------------------")
              
        print("-------------------------")
        print("Receiving {}º package...".format(1))
        print("-------------------------")

        tinkeroo.getPackage()
        nPacks = tinkeroo.nPacks
        print(nPacks)

        # header0, lenHeader0 = com.getData(10)

        # headerList[quantidade, index, tamanho, erro, qualErro]
        # headerList0 = .readHeader(header0)
        # payload0, lenPayload0 = com.getData(headerList0[2])
        # eop0, lenEop0 = com.getData(4)
        # eopINT0 = int.from_bytes(eop0, byteorder = "big")
        print("-------------------------")
        print("{}º package received".format(1))
        print("-------------------------")
        if tinkeroo.eopCheck():
            tinkeroo.addPayload()
            confirm = ("1º package has been received without any problems").encode("utf-8")
            packM.makePackage(confirm,1,False)
            tinkeroo.sendPackage(packM.package)

            for i in range(1,nPacks):
                print("{} PACOTES RESTANTES".format(nPacks-i))
                print("-------------------------")
                print("Receiving {}º package...".format(i+1))
                print("-------------------------")

                tinkeroo.getPackage()
                # header, lenHeader = com.getData(10)
                # headerList = pf.readHeader(header)
                # print("Payload Size: {}".format(headerList[2]))
                # payload, lenPayload = com.getData(headerList[2])
                # eop, lenEop = com.getData(4)
                # eopINT = int.from_bytes(eop, byteorder = "big")
                # print("EOP: {}".format(eopINT))
                print("-------------------------")
                print("-------------------------")
                print("{}º package received!".format(i+1))
                print("-------------------------")

                check = tinkeroo.eopCheck()
                
                if not check:
                    print("check")
                    msg = ("ERROR [420]").encode("utf-8") 
                    packM.makePackage(msg,tinkeroo.packIndex,True)
                    tinkeroo.sendPackage(packM.package)
                    break
                else:
                    confirm = ("CHECK").encode("utf-8")
                    packM.makePackage(confirm,tinkeroo.packIndex,False)
                    tinkeroo.sendPackage(packM.package)

        else:
            msg = ("ERROR [420]").encode("utf-8")
            packM.makePackage(msg,tinkeroo.packIndex,True)
            tinkeroo.sendPackage(packM.package)


         
        # print("-------------------------")
        # print("Size received: {0}".format(lenSizeReceived))
        # print("-------------------------")
    
        # sizeReceivedInt = int.from_bytes(sizeReceived, byteorder = "big")
        # imgReceived, lenImgReceived = com.getData(sizeReceivedInt)

        # print("-------------------------")
        # print("Size from received image: {0}".format(lenImgReceived))
        # print("-------------------------")    
    
        # Salva imagem recebida em arquivo
        imageW = "./imgReceived.png"
        print("-------------------------")
        print ("Saving in directory:")
        print (" - {}".format(imageW))
        f = open(imageW, 'wb')
        f.write(tinkeroo.fullArchive)

        # Fecha arquivo de imagem
        f.close()   

        print("Image saved!")

        # Sending size from received image
        # lenImgReceivedBytes = lenImgReceived.to_bytes(4,byteorder = "big")
        checkEnd = ("All packages were received without any issues!").encode("utf-8")
        packM.makePackage(checkEnd,1,False)
        tinkeroo.sendPackage(packM.package)

        print("-------------------------")
        print("End check sent to Client")
        print("-------------------------")
        
    
        # Encerra comunicação
        print("-------------------------")
        print("Communication finnish.")
        print("-------------------------")
        tinkeroo.finnish()
    except:
        print("ops! :-\\")
        tinkeroo.finnish()

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()


# Para fazer esse projeto foram feitas alterações no loopback, e na montagem dos arduínos. Foi necessário
# conectar os pinos tx de um com o rx do outro e vice-versa. Como o tamanho da imagem não era conhecido
# o client envia, primeiro, o tamanho da imagem em 4 bytes. Como esse número é conhecido pelo server esse
# não tem problemas para lê-lo e em seguida, sabendo agora o tamanho do arquivo, consegue receber a imagem.
# Em seguida, o server verifica o tamanho da imagem recebida e envia (também no formato de 4 bytes). Dessa,
# forma o client pode ter certeza se o arquivo foi enviado por completo.