from packManager import *

class archive(object):

    def __init__(self, dir):
        self.file = open(dir, "rb").read()
        self.packs = self.fragment(self.file)
        self.nPacks = len(self.packs)

    def makePayload(self, file, start, size):
        payload = b""

        for byte in range(start,start+size):
            payload += file[byte].to_bytes(1, byteorder="big")
        
        return payload

    def fragment(self, file):
        plSize = 114
        lenArq = len(file)

        nPacks = lenArq//plSize
        payloads = []
        packages = []

        if nPacks < 1:
            payloads.append(file)
        
        else:
            exPackSize = lenArq%plSize
            startPoint = 0
            for pack in range(0,nPacks):
                payload = self.makePayload(file,startPoint,plSize)
                payloads.append(payload)
                startPoint += 114
            payloads.append(self.makePayload(file,startPoint,exPackSize))

        for index in range(0,len(payloads)):
            # Header structure [packSize, pQ, pQ, packIndex, pI, pI, payloadSize, is_error, what_error, -]
            pl = payloads[index]
            packM = packManager()
            packM.makePackage(pl,index,False)
            packages.append(packM.package)

        return packages


    # def readHeader(self, package):
    #     nPacks = int.from_bytes(package[0:3], byteorder = "big")
    #     packIndex = int.from_bytes(package[3:6], byteorder = "big")
    #     packSize = package[6]
    #     if package[7] == 0:
    #         isError = False
    #     else:
    #         isError = True
        
    #     errorIndex = package[8]

    #     headerList = []
    #     headerList.append(nPacks)
    #     headerList.append(packIndex)
    #     headerList.append(packSize)
    #     headerList.append(isError)
    #     headerList.append(errorIndex)

    #     return headerList
    

a = b"\x14\xf6"
diretorio = "./img.png"
teste = open(diretorio, 'rb').read()

file = archive(diretorio)
packs = file.packs
inteiro = int.from_bytes(packs[0][0:3], byteorder = "big")

print(file.nPacks)



