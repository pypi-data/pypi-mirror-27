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

from tracer import logger

from urlparse import parse_qs
import json
import inspect


class assembler:
    '''
    The class for containing packet information
    represents the information stored in an individual HTTP packet
    an instance of this class exists for every HTTP packet found

    All packetDicts store:
    - the packet top level header
    - the packet size
    - the source IP address
    - the source port number
    - the destination IP address
    - the destination port number

    This information is contained inside 
    a data dictionary called data
    '''


    def accessor(self, rawData, iDict, iKey, key1, key2=None, singleKey=False):
        """
        Method for extracting data from raw packets
        and assignning them into a dict
        """
        if singleKey and type(rawData) is dict:
            try:
                result = str(rawData[key1])
            except KeyError:
                logger.debug("Key Not Found: {0}".format(key1))
                return None
        elif isinstance(key2, int):
            # index into a list if an integer
            try:
                result = str(rawData[key1][key2])
            except KeyError:
                logger.debug('Key-Index Not Found: {0}[{1}]'.format(key1, key2))
                return None                
        elif key2:
            # use as an attribute if a string
            try:
                subObject = rawData[key1]
            except KeyError:
                logger.debug('Key Not Found: {0}'.format(key1))
                return None       
            try:
                result = str(getattr(subObject, key2))
            except AttributeError:
                logger.debug('Attribute Not Found: {0}.{1}'.format(key1, key2))
                return None 
            # if key3:
            #     try:
            #         result = str(getattr(result, key3))
            #     except AttributeError:
            #         logger.debug('Attribute Not Found: {0}.{1}.{2}'.format(key1, key2, key3))
            #        return None 
        else:
            # use the first key directly as an attribute otherwise
            try:
                result = str(getattr(rawData, key1))
            except AttributeError:
                logger.debug('Attribute Not Found: {0}'.format(key1))
                return None 
        if result:
            iDict[iKey] = result
            return result

    def assembleDict(self, packet):
        '''
        Loads data from the packet into the dictionary

        Parameters:

        packet

        Returns: pDict
        '''

        # global json data fields:
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

        # we assume all packets are HTTP packets
        # as pyshark has been set to filter for HTTP
        # packets in the capturer
        # test if the HTTP packet contains a header

        if not packet:
            return 

        # create a dictionary 
        # to store the information
        pDict = dict()

        logger.debug('Processing HTTP packet...')

        logger.debug("Available fields:")
        logger.debug("Top Level")
        logger.debug(inspect.getmembers(packet))
        logger.debug("Internet Protocol Layer:")
        logger.debug(inspect.getmembers(packet["ip"]))
        logger.debug("Transmission Control Protocol Layer:")
        logger.debug(inspect.getmembers(packet["tcp"]))
        logger.debug("Hypertext Transfer Protocol Layer:")
        logger.debug(inspect.getmembers(packet["http"]))

        #print("Timestamp:")
        #print(packet.sniff_timestamp)
        #print(getattr(packet, "sniff_timestamp"))

        # load common packet information
        # all packets intecepted should contain 
        # these layers and associated fields

        # abort should the http packet be malformed
        # the packet is malformed if it is missing
        # these fields

        #self.accessor(packet, pDict, httpHeader, "http" , "")
        self.accessor(packet, pDict, "http_time", "http", "time")
        self.accessor(packet, pDict, "http_date", "http", "date")
        self.accessor(packet, pDict, "http_cookie", "http", "cookie")
        self.accessor(packet, pDict, "http_chat", "http", "chat")
        self.accessor(packet, pDict, "http_response_line", "http", "response_line")
        self.accessor(packet, pDict, "http_accept_language", "http", "accept_language")
        self.accessor(packet, pDict, "http_connection", "http", "connection")
        self.accessor(packet, pDict, "http_user_agent", "http", "user_agent")
        self.accessor(packet, pDict, "http_request_full_uri", "http", "request_full_uri")
        self.accessor(packet, pDict, "http_request_method", "http", "request_method")
        self.accessor(packet, pDict, "content_type", "http", "content_type")
        self.accessor(packet, pDict, "response_code", "http", "response_code")
        self.accessor(packet, pDict, "response_phrase", "http", "response_phrase")            
        self.accessor(packet, pDict, "server", "http", "server")
        self.accessor(packet, pDict, packetSize, "length")
        self.accessor(packet, pDict, sourceIP, "ip", "src")
        #self.accessor(packet, pDict, "ip_protocol", "ip", "proto")
        self.accessor(packet, pDict, sourcePort, "tcp", "srcport")
        self.accessor(packet, pDict, destIP, "ip", "dst")
        self.accessor(packet, pDict, destPort, "tcp", "dstport")
        self.accessor(packet, pDict, timestamp, "sniff_timestamp")        
        packetData = self.accessor(packet, pDict, "file_data", "http", "file_data")

        if packetData:
            httpQuery = parse_qs(packetData) 
            self.accessor(httpQuery, pDict, clientSecret, "client_secret", 0)
            self.accessor(httpQuery, pDict, grantType, "grant_type", 0)
            self.accessor(httpQuery, pDict, clientId, "client_id", 0)
            self.accessor(httpQuery, pDict, refreshToken, "refresh_token", 0)
            self.accessor(httpQuery, pDict, authorizationCode, "code", 0)
            self.accessor(httpQuery, pDict, redirectUri, "redirect_uri", 0)
            self.accessor(httpQuery, pDict, scope, "scope", 0)

        if packetData:
            try:
                jsonBody = json.loads(packetData)
            except ValueError:
                logger.debug('ValueError: Not JSON format')
                logger.debug('Parsing complete: Dictionary assembled:')
                logger.info(pDict)
                return pDict
            self.accessor(jsonBody, pDict, accessToken, access_token, singleKey=True)
            self.accessor(jsonBody, pDict, accessTokenExpiry, access_token_expiry, singleKey=True)
            self.accessor(jsonBody, pDict, refreshToken, refresh_token, singleKey=True)
            self.accessor(jsonBody, pDict, refreshTokenExpiry, refresh_token_expiry, singleKey=True)
            self.accessor(jsonBody, pDict, tokenType, token_type, singleKey=True)
            self.accessor(jsonBody, pDict, idToken, id_token, singleKey=True)

        logger.debug('Parsing complete: Dictionary assembled:')
        logger.info(pDict)
        return pDict
