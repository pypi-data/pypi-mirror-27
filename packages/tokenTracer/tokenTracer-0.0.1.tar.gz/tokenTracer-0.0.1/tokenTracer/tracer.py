'''
This python program iterates through all the packets in a pcap capture file
If a packet containing an access token is found, the information on that packet is printed
'''
import pyshark
import logging
import sys

# set logging level to CRITICAL to surpress logger
# set logging level to DEBUG to view debug statements
# in production, the logger MUST be set to CRITICAL
#logLevel = logging.CRITICAL
logLevel = logging.DEBUG
#logLevel = logging.INFO

logging.basicConfig(level=logLevel)
logger = logging.getLogger()

import cmdparse
import assembler
import display
       
class sniffer:            
    '''
    The frontend class establishes the command line parser and contains the packet capturer

    The frontend prepares a packetDict object that is loaded with packets

    +--------------------------------------------+
    |sniffer                                     |
    |             +------------------+ ------->  | -----------> +---------------+
    |             |sniff             |           |              | cmdLineParser | 
    |             +------------------+ <-------  | <-- args <-- +---------------+
    |                      |                     |
    |         -------------+----------+          |-----------------------------------------------+
    |         |           XOR         |          |                                               |  args
    |         \/                      \/         |                                               \/
    | +-----------------+    +--------------+    |                 +------------+            +---------+
    | |interfaceCapturer|    | fileCapturer |    | --> packet -->  | assembler  | -> dict -> | display | --> stdout
    | +-----------------+    +--------------+    |                 +------------+            +---------+
    +--------------------------------------------+ 
             /\                      /\
    eth0     |                     +-----+
    +--      |                     |.pcap|
    |--------+                     |     |
    +--   packets                  +-----+
    '''

    def start(self):
        '''
        Initializes the command-line arguments parser 

        Loads the sniffing process with the command line arguments

        Parameters: None
        
        Returns: None
        '''        
        parser = cmdparse.cmdparse()
        args = parser.argParse(sys.argv[1:])
        self.sniff(args)


    def sniff(self, args):    
        '''
        Configures the packet sniffer based on the command line arguments args

        Decides based on args whether the sniff live or from a file
        Creates the base pDict object based on args

        Parameters: 

        argObject args - The object containing the command line arguments as attributes mapped with their values

        Returns: None
        '''
        self.assembler = assembler.assembler()
        self.display = display.display(args.allPackets, args.jsonFormat)

        # either read from a packet capture file
        # or capture packets live from a network interface
        # the network interface is given by args.interface
        if args.iFile:
            self.fileCap(args)
        else:
            self.liveCap(args)
        exit


    def fileCap(self, args):
        '''
        Captures from an input packet capture (pcap) file

        Parameters:

        argObject args - The object containing the command line arguments as attributes mapped with their values 

        Returns: None       
        '''
        capture = pyshark.FileCapture(args.iFile, display_filter=args.protocol)
        # iterate through all the packets in the capture file
        for packet in capture:
            self.processPacket(packet)


    def liveCap(self, args):
        '''
        Captures from a live network interface

        Parameters:

        argObject args - The object containing the command line arguments as attributes mapped with their values 

        Returns: None
        '''
        capture = pyshark.LiveCapture(interface=args.interface, display_filter=args.protocol)
        try:
            for packet in capture.sniff_continuously():
                self.processPacket(packet)
        except RuntimeError:
            # exit gracefully upon a CTRL+C signal being given
            return

    def processPacket(self, packet):
        #logger.debug(packet)
        pDict = self.assembler.assembleDict(packet)
        self.display.output(pDict)

def main():
    # create the frontend
    iSniff = sniffer()
    # start the packet sniffing process
    iSniff.start()

# if the module is run directly 
# as a script (not imported)
if __name__ == "__main__":
    main()
