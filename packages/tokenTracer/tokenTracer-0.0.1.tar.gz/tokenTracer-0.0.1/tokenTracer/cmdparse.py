import argparse

class cmdparse:
    
    def argParse(self, cmdArgs):
        '''
        Parsers the command line for optional arguments
        
        Returns an object that holds the command line arguments as attributes

        Parameters:

        cmdArgs

        Returns:

        argObject args - The object containing the command line arguments as attributes mapped with their values
        '''
        # command line argument parser
        descLine = 'Outputs a live trace of intercepted HTTP requests and responses for Keycloak authorization tokens.'
        parser = argparse.ArgumentParser(description=descLine)

        argList = [["-i",  "--interface",   "eth0",             
                    "interface",  "store",      "Set the interface on which to sniff packets."],
                   ["-a",  "--all",         False,              
                    "allPackets", "store_true", "Output all HTTP packets captured."           ],
                   ["-f", "--file",  None,               
                    "iFile",      "store",      "Read from .pcap input file IFILE."           ],
                   ["-j",  "--json",        False,               
                    "jsonFormat", "store_true", "Output in JSON format."                      ],
                   ["-p", "--protocol", "http", 
                    "protocol", "store", "The protocols to filter for."]]

        for subList in argList:
            parser.add_argument(subList[0], subList[1], default=subList[2], dest=subList[3], action=subList[4], help=subList[5])

        # parse for the command line arguments
        args = parser.parse_args(cmdArgs)
        return args
