# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 09:47:02 2015

@author: twagner
"""

import numpy as np
import struct

###############################################################################
class LMDReader:
    def __init__(self, filename):
        self.lmdFullfile = filename
        self.lmdFile = open(filename, 'rb')
        self.data = self.lmdFile.read()
        self.lmdFile.close()

        self.dz = self.readFloat(40, 1)
        self.radius = self.readFloat(52, 1)
        
        (Nrow, Ncol) = self.readShort(168, 2)

        Nheader = 184
        self.readHeader(Nheader)

        iStart = Nheader
        Nbyte = 4
        self.xScale = np.array(self.readFloat(iStart, Nrow))
        iStart += Nbyte * Nrow
        self.yScale = np.array(self.readFloat(iStart, Ncol))
    
        offset = Nbyte * Ncol
        iStart += offset 
        
        self.Z = self.readFloat(iStart, Nrow*Ncol).reshape((Nrow, Ncol))
        self.Z[self.Z == 0] = np.nan    

        offset = Nbyte * Nrow * Ncol
        iStart += offset
        # self.readFooter(iStart)

    def readShort(self, iStart, N):
        return self.readData(iStart, N, 2, 'h')

    def readUnsignedShort(self, iStart, N):
        return self.readData(iStart, N, 2, 'H')

    def readFloat(self, iStart, N):
        return self.readData(iStart, N, 4, 'f')

    def readInteger(self, iStart, N):
        return self.readData(iStart, N, 4, 'i')

    def readDouble(self, iStart, N):
        return self.readData(iStart, N, 8, 'd')


    def readData(self, iStart, N, Nbyte, numberFormat):
        i1 = iStart
        offset = Nbyte * N
        i2 = i1 + offset
        littleEndian = '<'
        formatString = littleEndian + str(N) + numberFormat
        valueList = struct.unpack(formatString, self.data[i1:i2])
        
        if len(valueList) == 1:
            value = valueList[0]
        else:
            value = np.array(valueList)
        
        return value


    def readAscii(self, i1, N):
        Nbytes = 1
        i2 = i1 + Nbytes * N
        formatString = '<' + str(N) + 'c'
        charValues = np.array(struct.unpack(formatString, self.data[i1:i2]))

        formatString = '<' + str(N) + 'B'

        unsignedCharValues = np.array(
                struct.unpack(formatString, self.data[i1:i2]))

        charValues[unsignedCharValues < 32] = ' '
        charValues[unsignedCharValues > 126] = ' '

        value = b''.join(list(charValues))
        
        return value


    def readHeader(self, Nbytes):
        self.analyzeData(0, Nbytes)

        
    def readFooter(self, iStart):
        Nbytes = len(self.data) - iStart

        self.analyzeData(iStart, Nbytes)


    def analyzeData(self, iStart, Nbytes):
        Nb2 = Nbytes // 2
        Nb4 = Nbytes // 4
        Nb8 = Nbytes // 8
        
        # 1 byte
        dataAscii = self.readAscii(iStart, Nbytes)
    
        # 2 bytes
        dataShort = np.array(self.readShort(iStart, Nb2))
        dataUnsignedShort = np.array(self.readUnsignedShort(iStart, Nb2))
    
        # 4 bytes
        dataInteger = np.array(self.readInteger(iStart, Nb4))
        dataFloat = np.array(self.readFloat(iStart, Nb4))

        # 8 bytes
        dataDouble = self.readDouble(iStart, Nb8)

        print('')
        print('%7s %11s %11s %10s %6s %6s %6s %6s %11s' % (
                'offset',
                'double', 'float',
                'integer', 'short', 'short', 'ushort', 'ushort', 'ascii'))
        print(82*'-')
        
        for i in range(Nb4):
            if i % 2:
                print("%07i %11s %11.4g %10i %6i %6i %6i %6i" % (
                        iStart + 4*i,
                        '',
                        dataFloat[i],
                        dataInteger[i],
                        dataShort[2*i],
                        dataShort[2*i+1],
                        dataUnsignedShort[2*i],
                        dataUnsignedShort[2*i+1]))
            else:
                j = i // 2
                print("%07i %11.4g %11.4g %10i %6i %6i %6i %6i %11s" % (
                        iStart + 4*i,
                        dataDouble[j],
                        dataFloat[i],
                        dataInteger[i],
                        dataShort[2*i],
                        dataShort[2*i+1],
                        dataUnsignedShort[2*i],
                        dataUnsignedShort[2*i+1],
                        dataAscii[4*i:4*i+8]))
            
###############################################################################
if __name__ == "__main__":
    filename = "../Data/reference.lmd"
    lmd = LMDReader(filename)
