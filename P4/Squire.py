from crccheck.crc import Crc16
from datetime import datetime as dt

class Squire(object):
    
    def __init__(self):
        self.eop = (420).to_bytes(4,byteorder="big")    
    
    def makePackage(self, header, payload):
        package = header + payload + self.eop
        return package

    def makeAnswer(self, type, ids, index=0):
        ans = self.makePackage(bytes([type,ids["sensorID"],ids["serverID"],0,0,0,index,0,0,0]),b"")
        return ans
        
    def readHeader(self, header):
        '''
            h0 = type
            h1 = sensorID
            h2 = serverID
            h3 = nPacks
            h4 = packIndex
            h5 = fileID/payloadSize
            h6 = errorIndex
            h7 = lastIndex
            h8/h9 = CRC
        '''
        headDict = {
            "type" : header[0],
            "sensorID" : header[1],
            "serverID" : header[2],
            "nPacks" : header[3],
            "packIndex" : header[4],
            "plSize" : header[5],
            "errorIndex" : header[6],
            "lastIndex" : header[7],
            "CRC" : ((header[8:10]).hex()).upper()
        }
        

        return headDict

    def makePayload(self, file, start, size):
        payload = b""
        payload = file[start:start+size]
      
        return payload
        
    def fragment(self, file, desc):
        plSize = 114
        nBytes = len(file)

        nPacks = nBytes//plSize
        payloads = []
        packages = []
        
        if nPacks < 1:
            payloads.append(file)
        
        else:
            exPackSize = nBytes%plSize
            startPoint = 0
            for pack in range(0,nPacks):
                payload = self.makePayload(file,startPoint,plSize)
                payloads.append(payload)
                startPoint += 114
            payloads.append(self.makePayload(file,startPoint,exPackSize))
        
        for index in range(len(payloads)):
            
            # Header structure []
            pl = payloads[index]

            packSize = len(payloads)
            header = bytes([desc["type"], desc["sensorID"], desc["serverID"], packSize, index, len(pl), 0])
            if(index==0):
                header += bytes([index])
            else:
                header += bytes([index-1])

            header += Crc16.calc(pl).to_bytes(2, "big")

            package = self.makePackage(header,pl)
            packages.append(package)

        return packages

    def logging(self, log, action, data):
        head = self.readHeader(data)
        if action == "s":
            action = "sent "
        elif action == "r":
            action = "rcvd "
        else:
            action = "wtf "
        
        line = (f"{dt.now()} / " ) + action + "/ "
        line += (f"{head['type']} / {len(data)}")

        
        if head["type"] == 3:
            line += (f" / {head['packIndex']+1} / {head['nPacks']} / {head['CRC']}\n")

        else:
            line += "\n"

        log.write(line)


    