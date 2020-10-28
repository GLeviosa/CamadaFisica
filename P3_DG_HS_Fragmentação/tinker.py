from enlace import *
from packManager import *
import time

class tinker(object):

    def __init__(self, serialPort):
        self.portName = serialPort
        self.comPort = enlace(self.portName)
        self.comPort.enable()
        self.eop = (420).to_bytes(4,byteorder="big")
        self.fullArchive = b""
        self.header = b""
        self.payload = b""
        self.eopReceived = b""

    def sendPackage(self, package):
        self.comPort.sendData(package)
        time.sleep(0.5)

    def sendHandShake(self, string):
        packM = packManager()
        packM.makePackage((string).encode("utf-8"),1,False)
        self.comPort.sendData(packM.package)
        time.sleep(0.5)


    def getPackage(self):
        self.header, self.lenHeader = self.comPort.getData(10)
        self.hList = packManager().readHeader(self.header)
        self.nPacks = self.hList[0]
        self.packIndex = self.hList[1]
        self.payloadSize = self.hList[2]
        self.isError = self.hList[3]
        self.errorIndex = self.hList[4]

        self.payload, self.lenPayload = self.comPort.getData(self.payloadSize)
        self.eopReceived, self.lenEopReceived = self.comPort.getData(4)

    def eopCheck(self):
        if self.eop == self.eopReceived:
            return True
        else:
            return False
            
    def finnish(self):
        self.comPort.disable()

    def addPayload(self):
        self.fullArchive += self.payload





    


