

class packManager(object):
    
    def __init__(self):
        self.payload = b""
        self.header = b""
        self.package = b""
        self.eop = (420).to_bytes(4,byteorder="big")
    
    def makePackage(self, payload, index, error):
        self.payload = payload
        header = b""
        size = len(payload)
        header += size.to_bytes(3, byteorder="big")
        header += index.to_bytes(3, byteorder="big")
        header += len(payload).to_bytes(1, byteorder="big") 
        if error:
            header += int(True).to_bytes(1, byteorder="big")
            for e in range(0,2):
                header += int(False).to_bytes(1, byteorder="big")
        else:
            for e in range(0,3):
                header += int(False).to_bytes(1, byteorder="big")
        self.header = header 
        self.package = header + payload + self.eop

        
    
    def readHeader(self, package):
        nPacks = int.from_bytes(package[0:3], byteorder = "big")
        packIndex = int.from_bytes(package[3:6], byteorder = "big")
        packSize = package[6]
        if package[7] == 0:
            isError = False
        else:
            isError = True
        
        errorIndex = package[8]

        headerList = []
        headerList.append(nPacks)
        headerList.append(packIndex)
        headerList.append(packSize)
        headerList.append(isError)
        headerList.append(errorIndex)
        
        self.header = headerList

        return headerList
    
    