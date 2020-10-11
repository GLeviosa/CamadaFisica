from enlace import *
from Squire import *
import time

class Tinker(object):

    def __init__(self, serialPort):
        self.portName = serialPort
        self.comPort = enlace(self.portName)
        self.comPort.enable()
        self.pacman = Squire()
        self.eop = (420).to_bytes(4,byteorder="big")
        self.allPayloads = {}
        self.fullArchive = b""
        self.header = b""
        self.payload = b""
        self.eopReceived = b""

    def sendPackage(self, package):
        self.comPort.sendData(package)
        time.sleep(0.5)

    def sendHandShake(self,serverID,nPacks):
        self.handshake = self.pacman.makePackage(bytes([1,0,serverID,nPacks,0,0,0,0,1,2]), b"")
        self.comPort.sendData(self.handshake)
        time.sleep(0.5)

    def getPackage(self,header):
        self.header = header
        self.hDict = self.pacman.readHeader(self.header)
        self.payload = self.comPort.getData(self.hDict["plSize"])
        self.eopReceived = self.comPort.getData(4)
        self.pack = self.header + self.payload + self.eopReceived
    
    def getAnswer(self):
        ans = self.comPort.getData(14)
        headDesc = self.pacman.readHeader(ans)
        return ans, headDesc
        
    def eopCheck(self):
        if self.eop == self.eopReceived:
            return True
        else:
            return False
    
    def isEmpty(self):
        isIt = self.comPort.rx.getIsEmpty()
        return isIt

    def finnish(self):
        self.comPort.disable()

    def addPayload(self, pack):
        packHeader = self.pacman.readHeader(pack)
        self.allPayloads[packHeader["packIndex"]] = pack[10:10+packHeader["plSize"]]

    def assembleData(self):
        archive = b""
        for i, e in self.allPayloads.items():
            archive += e
        
        self.fullArchive = archive
            
    # def wait(self)





    


