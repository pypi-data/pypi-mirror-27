from tracer import logger
import json

class display:

    def __init__(self, printAll, jsonFormat):
        '''
        Initializes the attributes of the packetDict object

        Starts the packet dict with an empty dictionary

        The constructor for the packetDict class
        takes a packet object and a fieldName 
        The field name is the first line of the header
        which details the HTTP method and URL

        Parameters:

        boolean printAll - If True, print all intercepted HTTP packets
        boolean jsonFormat - If True, print to stdout in newline-separated JSON objects 
                             If False, print to stdout in pretty-printed format
                             Pretty-printed format uses newline-separated key-value pairs
                             whose keys are separated from their values by a colon and whitespace.

        Returns: packetDict
        '''
        self.printAll = printAll
        self.json = jsonFormat

        access_token         = 'access_token'
        access_token_expiry  = 'expires_in'
        refresh_token        = 'refresh_token'
        refresh_token_expiry = 'refresh_expires_in'
        token_type           = 'token_type'
        id_token             = 'id_token'
        not_before_policy    = 'not-before-policy'
        session_state        = 'session_state'

        packetSize           = 'packetSize'
        sourceIP             = 'sourceIP'
        destIP               = 'destIP'
        destPort             = 'destPort'
        sourcePort           = 'sourcePort'
        clientSecret         = 'clientSecret'
        grantType            = 'grantType'
        clientId             = 'clientId'
        httpHeader           = 'httpHeader'
        refreshToken         = 'refreshToken'
        authorizationCode    = 'authorizationCode'
        redirectUri          = 'redirectUri'
        scope                = 'scope'
        accessToken          = 'accessToken'
        accessTokenExpiry    = 'accessTokenExpiry'
        refreshToken         = 'refreshToken'
        refreshTokenExpiry   = 'refreshTokenExpiry'
        tokenType            = 'tokenType'
        idToken              = 'idToken'
        timestamp            = 'timestamp'

        # printList defines the default sequence to print
        # printList is a list of doubles
        # the first entry of a double is the pretty-printed name
        # and the second entry is the key to access the pDict for the value
        # keys that dont have entries are ignored in the pDict
        self.printList = [("Timestamp", timestamp), 
                          ("Transmission Time", "http_time"), 
                          ("Packet Size", packetSize), 
                          ("Date", "http_date"),
                          ("Cookie", "http_cookie"),
                          ("User Agent", "http_user_agent"),
                          ("Connection", "http_connection"),
                          ("Request Full URI", "http_request_full_uri"),
                          ("Request Method", "http_request_method"),
                          ("Accept Language", "http_accept_language"),
                          ("Chat", "http_chat"),
                          ("Content Type", "content_type"), 
                          ("Response Code", "response_code"), 
                          ("Response Phrase", "response_phrase"), 
                          ("Source IP", sourceIP),
                          ("Source Port", sourcePort), 
                          ("Destination IP", destIP), 
                          ("Destination Port", destPort), 
                          ("Server", "server"),
                          ("Client Secret", clientSecret), 
                          ("Client Id", clientId), 
                          ("Grant Type", grantType), 
                          ("Authorization Code", authorizationCode), 
                          ("Redirect Uri", redirectUri), 
                          ("Scope", scope), 
                          ("Access Token", accessToken), 
                          ("Access Token Expiry", accessTokenExpiry), 
                          ("Refresh Token", refreshToken), 
                          ("Refresh Token Expiry", refreshTokenExpiry), 
                          ("Token Type", tokenType),
                          ("Id Token", idToken)]
        # ("File Data", "file_data")

        # a filter is a lambda
        # that takes parameter x which is a pDict 
        # that when evaluated to True will cause
        # the display class to output the packet 

        # filterToken is a predicate lambda that evaluates to True
        # only for packets that are responses containing tokens
        # or are requests for tokens
        self.filterToken = lambda x : self.index(x, refreshToken) or self.index(x, grantType) or self.index(x, accessToken) or self.index(x, idToken)

        # filterNone performs no filtering
        # and prints all (http) packets
        self.filterNone = lambda x : True

        # sets the filter to use
        # printAll switches the filter to print all (http) packets
        # the default is the token filter
        if self.printAll:
            self.filterCurrent = self.filterNone
        else:
            self.filterCurrent = self.filterToken


    def index(self, iDict, iKey):
        """
        Determines if iDict contains an entry for key iKey

        Parameters:

        dict iDict - a python dictionary
        str iKey - the key to index into iDict

        Returns True if dict iDict contains a value for key iKey
        Returns False on KeyError
        """
        try:
            iDict[iKey]
        except KeyError:
            return False
        return True


    def outPrint(self, pDict, fieldName, key):
        """
        Output function that prints the entry in pDict
        with key "key" with pretty-printed name "fieldName"

        Parameters:

        dict pDict
        str fieldName
        str key

        Returns:

        data
        """
        try:
            data = pDict[key]
        except KeyError:
            #logger.debug("KeyError on key {0}".format(key))
            return None
        print("{0:21}{1}".format(fieldName + ":", data))
        return data

    def prettyPrint(self, pDict):
        '''
        Pretty-prints the packet data to stdout

        Tightly coupled to the packetDict object

        Parameters:

        dict pDict - the dictionary representing the flattened packet data

        Returns: None
        '''        
        logger.debug('Pretty-printing...')
        # printList is the sequence to print
        for item in self.printList:
            self.outPrint(pDict, item[0], item[1])
        print('')
                                       
    def jsonWrite(self, pDict):
        """
        Outputs JSON format to stdout

        Parameters: 

        dict pDict - the dictionary representing the flattened packet data

        Returns: None
        """
        logger.debug('Outputting JSON')
        jsonString = json.JSONEncoder().encode(pDict)
        print(jsonString)

    def output(self, pDict):
        '''
        Main logging function

        Decides which format to print to stdout

        Parameters: None

        Returns: None
        '''
        logger.debug('Preparing to output...')
        packetTest = self.filterCurrent

        # if packetTest evaluates to True over the pDict
        # then output the packet
        if packetTest(pDict):
            if self.json:
                self.jsonWrite(pDict)
            else:
                self.prettyPrint(pDict)
