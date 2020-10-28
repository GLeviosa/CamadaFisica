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
        tinkeroo = tinker(serialName)

        # imageR = input("Input image directory: ")
        imageR = "./img.png"
        # Log
        print("-------------------------")
        print("Initializing communication")
        print("Port: {}".format(tinkeroo.comPort.fisica.name))
        print("-------------------------")
        # Carrega imagem
        print("-------------------------")
        print ("Loading image...")
        print (" - {}".format(imageR))
        print("-------------------------")
        print ("Making packages....")
        print("-------------------------")

        file = archive(imageR)
        
        # txBuffer = open(imageR, 'rb').read()
        timeStart = time.time()
        
        index = 1
        for pack in file.packs:
            print("-------------------------")
            print("Preparing to send {}º package...".format(index))
            print("-------------------------")
            
            tinkeroo.sendPackage(pack)
            
            print("-------------------------")
            print("{}º package sent!".format(index))
            print("-------------------------")

            tinkeroo.getPackage()

            # headerConfirm, lenHeaderConfirm = com.getData(10)

            # headerC = pf.readHeader(headerConfirm)

            # confirmMsg, lenConfirmMsg = com.getData(headerC[2])
            # confirmEop, lenConfirmEop = com.getData(4)
            
            if tinkeroo.isError:
                print("-------------------------")
                print(tinkeroo.payload.decode("utf-8"))
                print("There was an error in the {}º package".format(tinkeroo.packIndex))
                print("-------------------------")

            
            index += 1

        print("-------------------------")
        print("Waiting for server's response...")
        print("-------------------------")

        # headerCheckEnd, lenHeaderCheckEnd = com.getData(10)

        # headerCE = pf.readHeader(headerCheckEnd)

        # endMsg, lenEndMsg = com.getData(headerCE[2])
        # endEop, lenEndEop = com.getData(4)

        tinkeroo.getPackage()
        print("-------------------------")
        print(tinkeroo.payload.decode("utf-8"))
        print("-------------------------")

        # # Encerra comunicação
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
