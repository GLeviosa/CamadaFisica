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

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
# para saber a sua porta, execute no terminal :
# python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)


# se fosse apenas o arduino, uma porta de comunicaçã seria suficiente, estamos usando duas pq o software de emular recebe um uma porta e envia em outra
serialName1 = "COM1"
serialName2 = "COM5"                 # Windows(variacao de)
#/dev/cu.usbmodemFA131 -- Due
#/dev/cu.usbmodemFD1211 -- uno



def main():
    try:
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com = enlace(serialName1)
        com2 = enlace(serialName2)
    
    
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com.enable()
        com2.enable()

        imageR = input("Input image directory: ")
        # Log
        print("-------------------------")
        print("Initializing communication")
        print("Port: {}".format(com.fisica.name))
        print("-------------------------")
       
        # Carrega imagem
        print("-------------------------")
        print ("Loading image...")
        print (" - {}".format(imageR))
        print("-------------------------")
        txBuffer = open(imageR, 'rb').read()
        timeStart = time.clock()
       
        
        # Tamanho da imagem de inteiro para bytes(4)
        lenImg = len(txBuffer)
        sizeImg = lenImg.to_bytes(4, byteorder="big")

        com.sendData(sizeImg)
        time.sleep(0.5)
        print("-------------------------")
        print("Size sent: {0}".format(len(txBuffer)))
        print("-------------------------")


        com.sendData(txBuffer)
        time.sleep(0.5)
        print("-------------------------")
        print("Image sent!")
        print("-------------------------")


        # A camada enlace possui uma camada inferior, TX possui um método para conhecermos o status da transmissão
        # Tente entender como esse método funciona e o que ele retorna
        #time.sleep(0.5) #sem o time o getStatus retorna zero, pois nao deu tempo de enviar
        #txSize = com.tx.getStatus()
        # print('tamanho do que enviou {}' .format(txSize))
        #Uma outra forma de saber o tamanho da lista enviada é apenas fazendo:
        #txSize = len(txBuffer) #modo alternativo... mais simples, mas se nem todos os bytes foram realmente enviados, havera problemas
        
        #Agora vamos iniciar a recepção dos dados. Se algo chegou ao RX, deve estar automaticamente guardado
        #Observe o que faz a rotina dentro do thread RX
        #print um aviso de que a recepção vai começar.
        #Será que todos os bytes enviados estão realmente guardadas? Será que conseguimos verificar?
        #Veja o que faz a funcao do enlaceRX  getBufferLen
        #acesso aos bytes recebidos
        
        #IMPORTANTE: se voce obteve o tamnho do txBuffer com o getStatus, tem que transformar o tamanho em int para poder usar no getData. (A funcao getStatus retorna em float)
        #int(txSize)...


        print("-------------------------")
        print("Waiting for server's response...")
        print("-------------------------")

        sizeServer, lenSizeServer = com2.getData(4)

        sizeServerInt = int.from_bytes(sizeServer, byteorder = "big")

        print("-------------------------")
        print("Response received!")
        print("Size: {0}".format(sizeServerInt))
        print("Len img: {}".format(lenImg))
        print("-------------------------")

        if sizeServerInt == lenImg:
            timeElapsed = time.clock() - timeStart
            baudRate = lenImg/timeElapsed
            print("-------------------------")
            print("Sizes match!")
            print("Baud Rate: {0}".format(baudRate))
            print("Time Elapsed: {0}".format(timeElapsed))
            print("-------------------------")
            
        else:
            print("-------------------------")
            print("Something went wrong.")
            print("Try again!")
            print("-------------------------")
        
        # Encerra comunicação
        print("-------------------------")
        print("Communication finnish.")
        print("-------------------------")
        com.disable()
        com2.disable()
    except:
        print("ops! :-\\")
        com.disable()
        com2.disable()

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
