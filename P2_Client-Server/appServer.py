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
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)


# se fosse apenas o arduino, uma porta de comunicaçã seria suficiente, estamos usando duas pq o software de emular recebe um uma porta e envia em outra
serialName1 = "COM2"
serialName2 = "COM6"                 # Windows(variacao de)
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
        print("-------------------------")
        print("Port enabled")
        print("-------------------------")
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        
       
        # imageR = "./imageB.png"
        #  # Endereco da imagem a ser salva

        # Log
        print("-------------------------")
        print("Initializing communication")
        print("Port: {}".format(com.fisica.name))
        print("-------------------------")

        # A camada enlace possui uma camada inferior, TX possui um método para conhecermos o status da transmissão
        # Tente entender como esse método funciona e o que ele retorna
        # time.sleep(0.5) #sem o time o getStatus retorna zero, pois nao deu tempo de enviar
        # txSize = com.tx.getStatus()
        # print('tamanho do que enviou {}' .format(txSize))
        #Uma outra forma de saber o tamanho da lista enviada é apenas fazendo:
        # txSize = len(txBuffer) #modo alternativo... mais simples, mas se nem todos os bytes foram realmente enviados, havera problemas

        # print("-------------------------")
        # print(txSize)
        # print("-------------------------")
        
        #Agora vamos iniciar a recepção dos dados. Se algo chegou ao RX, deve estar automaticamente guardado
        #Observe o que faz a rotina dentro do thread RX
        #print um aviso de que a recepção vai começar.
        #Será que todos os bytes enviados estão realmente guardadas? Será que conseguimos verificar?
        #Veja o que faz a funcao do enlaceRX  getBufferLen
        #acesso aos bytes recebidos
        
        
        #IMPORTANTE: se voce obteve o tamnho do txBuffer com o getStatus, tem que transformar o tamanho em int para poder usar no getData. (A funcao getStatus retorna em float)
        #int(txSize)...

        sizeReceived, lenSizeReceived = com.getData(4)

        print("-------------------------")
        print("Size received: {0}".format(lenSizeReceived))
        print("-------------------------")
    
        sizeReceivedInt = int.from_bytes(sizeReceived, byteorder = "big")
        imgReceived, lenImgReceived = com.getData(sizeReceivedInt)

        print("-------------------------")
        print("Size from received image: {0}".format(lenImgReceived))
        print("-------------------------")    
    
        # Salva imagem recebida em arquivo
        imageW = "./imgs/imgReceived.png"
        print("-------------------------")
        print ("Saving in directory:")
        print (" - {}".format(imageW))
        f = open(imageW, 'wb')
        f.write(imgReceived)

        # Fecha arquivo de imagem
        f.close()   

        print("Image saved!")

        # Sending size from received image
        lenImgReceivedBytes = lenImgReceived.to_bytes(4,byteorder = "big")
        com2.sendData(lenImgReceivedBytes)
        time.sleep(4)

        print("-------------------------")
        print("Size received sent to Client")
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


# Para fazer esse projeto foram feitas alterações no loopback, e na montagem dos arduínos. Foi necessário
# conectar os pinos tx de um com o rx do outro e vice-versa. Como o tamanho da imagem não era conhecido
# o client envia, primeiro, o tamanho da imagem em 4 bytes. Como esse número é conhecido pelo server esse
# não tem problemas para lê-lo e em seguida, sabendo agora o tamanho do arquivo, consegue receber a imagem.
# Em seguida, o server verifica o tamanho da imagem recebida e envia (também no formato de 4 bytes). Dessa,
# forma o client pode ter certeza se o arquivo foi enviado por completo.