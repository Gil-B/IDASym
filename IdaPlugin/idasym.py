#!/usr/bin/env python
#
# IDA libraries
import idaapi
import idautils
import idc

# Python libraries
import os

class IDASym(plugin_t):

    flags = idaapi.PLUGIN_UNL
    comment = "Export IDA symbols to file for later processing by WinDbg"
    help = "Export IDA symbols to file for later processing by WinDbg"
    wanted_name = "IDASym"
    wanted_hotkey = ""

    def init(self):  
        print("Initialized IDASym")
        return idaapi.PLUGIN_KEEP
    def run(self, arg):
        print("Running")
        PE = peutils_t()
        print("Image base is %016X" % PE.imagebase)
        print("Exporting functions...")
        filename = os.path.splitext(idc.GetIdbPath())[0] + ".sym"
        rawOffsetsFilename = os.path.splitext(idc.GetIdbPath())[0] + ".raw.sym"
        f = open(filename, 'w')
        rawOffsetsFile = open(rawOffsetsFilename, 'w')
        
        count = 0
        for address,name in Names():
            offset = address - PE.imagebase
            rawOffset = idaapi.get_fileregion_offset(address)
            if idc.GetFunctionFlags(address) != -1:
                size = idc.FindFuncEnd(address) - address
            else:
                size = 4
            
            #namesList.append((offset, name))
            count += 1
            f.write("%08X %08X;%s\n" %(offset, size, name))
            rawOffsetsFile.write("%08X %08X;%s\n" %(rawOffset, size, name))
            
        f.close()
        rawOffsetsFile.close()
        
        print("%d functions exported" %count)
        
    def term(self):
        pass        

def PLUGIN_ENTRY():
    return IDASym()

###############################################################################
# Script / Testing
###############################################################################

if __name__ == '__main__':
    pass