==============================
Keycloak Token Tracer Program 
==============================

1.0 Overview
-------------------

This program sniffs for HTTP packets which are requests and responses 
to and from the token endpoint of the Keycloak authorization server 
used to server application servers.

The program contains two types of packet filter-parser pairs:

1. One filters and parsers packets that send token requests to the endpoint
2. One filters and parsers packets that are responses to requests to the token endpoint

There are two principal cases in which tokens are transmitted 
using packets for the OpenID Connect Authentication procedure:

1. Authorization code request
2. Refresh token request 

The Authorization code request occurs once a user has logged 
into the server through a login screen.

The refresh token request occurs when the user refreshes the webpage 
after having logged in provided that:

1. The Access Token is expired
2. The Refresh Token is not expired

After the refresh token has expired, the user will be forced 
to log into the server again using the login page. 
The refresh token generally has a longer expiry than the access token.

1.1 Requirements
-------------------

- Python 2.7+
- tshark
- pyshark

To install the program, one also needs:

- pip
- git (if installing locally or running the module directly)

1.2 Usage
--------------------

The token tracer program is invoked as an ordinary python program:

::

    python tokenTracer.py

Invoking the token tracer with no command line arguments will cause 
the program to sniff live on the ethernet interface for all HTTP packets 
and print them to stdout. 
The program will only output packets that satisfy its filters. 
There are two types of packets that it will print:

1. HTTP POST requests made to the token endpoint
2. HTTP responses containing the access token 

1.3 Command Line Arguments
----------------------------

+----------------+-------------+-----------------+---------------------------------------------------------------------+
| Variable       | Short Form  | Default         | Description                                                         | 
+================+=============+=================+=====================================================================+
| --interface    | -i          | eth0            | Set the network interface on which the packet sniffer should sniff  |
+----------------+-------------+-----------------+---------------------------------------------------------------------+
| --input-file   | -f          | None            | Set an input packet capture (.pcap) file to read packets from       |
+----------------+-------------+-----------------+---------------------------------------------------------------------+
| --json         | -j          | False           | Output to stdout in JSON format                                     |
+----------------+-------------+-----------------+---------------------------------------------------------------------+
| --all          | -a          | False           | Print all HTTP packets intercepted                                  |
+----------------+-------------+-----------------+---------------------------------------------------------------------+

1.4 Installation
-----------------------------

There are three options:

1. Installation through pip remotely (Recommended)
2. Installation through pip locally
3. Run the token tracer module directly

The first option is the simplest option and is most appropriate 
for end-users. The later options are more suitable for 
development and testing.

1.4.1 Remote Pip Installation
================================

1. Install Python and pip. Your system will likely already have 
these installed. On Debian/Ubuntu enter:

::

    apt-get install python python-pip -y

2. Install tshark. On Debian/Ubuntu enter:

::

    apt-get install tshark -y

3. Install pyshark via pip:

::

    pip install pyshark

4. Install the program through pip remotely:

::

    pip install tokenTracer

The token tracer program will then be installed.

To check that the installation worked, type:

::

    tokenTracer -h

A help menu should display:

::

    usage: tokenTracer.py [-h] [-i INTERFACE] [-a] [-f IFILE] [-j]

    Traces HTTP requests and responses for authorization tokens from Keycloak for
    the CanDIG GA4GH server

    optional arguments:
      -h, --help            show this help message and exit
      -i INTERFACE, --interface INTERFACE
                            Set the interface on which to sniff packets
      -a, --all             Output all HTTP packets captured
      -f IFILE, --file IFILE
                            Read from .pcap input file IFILE
      -j, --json            Output in JSON format

  
1.4.2 Local Pip Installation
=============================

1. Install Python, pip, and git. Your system will likely already have 
these installed. On Debian/Ubuntu enter:

::

    apt-get install python python-pip git -y

2. Install tshark. On Debian/Ubuntu enter:

::

    apt-get install tshark -y 

3. Install pyshark via pip:

::

    pip install pyshark

4. Change directory (``cd``) into the folder which will containing 
the folder for the git repository.
You may wish to create new folders with ``mkdir``.

5. Clone the git repository. A folder called ``tokenTracer`` will be 
created in the current directory that will contain the tokenTracer 
program files.

::

    git clone https://github.com/Bio-Core/tokenTracer.git

6. Change directory into the git repository:


::

    cd tokenTracer

7. Install via pip inside the directory:

::

    pip install .

The token tracer should be installed onto the computer. 

You can verify the installation with:

::

    tokenTracer -h

A help menu should display:

::

    usage: tokenTracer.py [-h] [-i INTERFACE] [-a] [-f IFILE] [-j]

    Traces HTTP requests and responses for authorization tokens from Keycloak for
    the CanDIG GA4GH server

    optional arguments:
      -h, --help            show this help message and exit
      -i INTERFACE, --interface INTERFACE
                            Set the interface on which to sniff packets
      -a, --all             Output all HTTP packets captured
      -f IFILE, --file IFILE
                            Read from .pcap input file IFILE
      -j, --json            Output in JSON format


1.4.3 Running the module directly
=====================================

1. Install Python, pip, and git. Your system will likely already have 
these installed. On Debian/Ubuntu enter:

::

    apt-get install python python-pip git -y

2. Install tshark. On Debian/Ubuntu enter:

::

    apt-get install tshark -y

3. Install pyshark via pip:

::

    pip install pyshark

4. Change directory (``cd``) into the folder which will containing 
the folder for the git repository.
You may wish to create new folders with ``mkdir``.

5. Clone the git repository. A folder called tokenTracer will be 
created in the current directory that will contain the tokenTracer 
program files.

::

    git clone https://github.com/Bio-Core/tokenTracer.git

6. Change directory into the git repository into the tokenTracer folder:

::

    cd tokenTracer/tokenTracer

7. Run the tokenTracer module:

::

    python tokenTracer.py

The token tracer program should now be running.

1.4.4 Uninstallation
=====================

If the token tracer was installed through pip, the program may be uninstalled via pip:

::

    pip uninstall tokenTracer

1.5 Running the Program
---------------------------

To run the program, enter its name into the command-line:

::

    tokenTracer

The tokenTracer will then begin running. You will notice this 
as the terminal will not return to displaying the login 
information on the left-hand side, but will remain blank
and unresponsive. 

1.5.1 Default Configuration Behaviour
========================================

The token tracer will be running using its default configuration. 

This configuration will cause the token tracer to sniff for packets 
on the default ethernet network interface ``eth0``. 
This can be changed through the command-line arguments to listen 
on a different network interface with ``-i``  or to read 
from a packet capture file with ``-f``.

To list the available network interfaces, use a program such as ``ip`` or ``ifconfig``.
These are the only interfaces on which the token tracer can capture. Ideally,
the token tracer should be deployed on the same network interface as the Keycloak server
so that the token tracer may intercept the same packets that are sent to and from the 
Keycloak server.

1.5.2 Exiting the Program
=============================

To exit the program, enter ``CTRL+C`` together. The program will abort from sniffing from a live interface. When reading from a packet file, the program wil terminate automatically when it reaches the end of the file.

1.6 Examples
----------------

1.6.1 Example 1: Input Test File
==================================================

1. Run the token tracer with the --input-file command line option 
with the argument "test/test.pcap":

::

    tokenTracer -f test/testInput.pcap

2. The token tracer will output the packets that match its filters 
for token endpoint requests and response:

::

    Timestamp:            2017-10-10 16:32:36.334519
    HTTP Protocol:        POST /auth/realms/CanDIG/protocol/openid-connect/token 
    HTTP/1.1\r\n
    Packet Size:          617
    Source:               172.17.0.3:33478
    Destination:          192.168.99.100:8080
    Client Secret:        49b0e8e6-b124-4fcd-b23d-9eee9ab71a3f
    Client Id:            ga4ghServer
    Grant Type:           authorization_code
    Authorization Code:   uss.vsUUbtcjLolLELcEK4Z0t3kJBayjdo7jkcWafDIEoDQ.909f43f0
    -848e-481d-bf42-a4d7011429d5.0135628f-70f9-43f8-9114-6c29dd0f0e76
    Redirect Uri:         http://192.168.99.100:8000/oidc_callback
    Scope:                openid email

    Timestamp:            2017-10-10 16:32:36.381584
    HTTP Protocol:        HTTP/1.1 200 OK\r\n
    Packet Size:          3583
    Source:               192.168.99.100:8080
    Destination:          172.17.0.3:33478
    Access Token:         eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJpT3R0
    bHFkZURsbFpzQU42QUhJdEkzb1lla3ZtemVkTGhWYXNuR1lRVU00In0.eyJqdGkiOiI3OTYzOTc5Yy
    02MmFhLTRjNmMtOTZmYy1jY2I4ODM2NjRlZDQiLCJleHAiOjE1MDc2Njc4NTYsIm5iZiI6MCwia...
    Access Token Expiry:  300
    Refresh Token:        eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJpT3R0
    bHFkZURsbFpzQU42QUhJdEkzb1lla3ZtemVkTGhWYXNuR1lRVU00In0.eyJqdGkiOiI1Y2YyOTU2Yi
    04OTQxLTQwNzYtODM1ZS01M2E4YzhmZWI5ZGIiLCJleHAiOjE1MDc2NjkzNTYsIm5iZiI6MCwia...
    Refresh Token Expiry: 1800
    Token Type:           bearer
    Id Token:             eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJpT3R0
    bHFkZURsbFpzQU42QUhJdEkzb1lla3ZtemVkTGhWYXNuR1lRVU00In0.eyJqdGkiOiIwM2JmMDI0ZS
    1jZGVmLTQ2MTEtOTc3Yy1kZTZkY2FmMTJhZWYiLCJleHAiOjE1MDc2Njc4NTYsIm5iZiI6MCwia...


1.6.2 Example 2: cURL HTTP Request Interception
===============================================================

1. Run the tokenTracer to intercept all HTTP packets on the loopback interface:

::

    tokenTracer -a -i lo0

2. Start a new terminal.

3. cURL the following HTTP GET request to ``localhost``:

::

    curl 127.0.0.1:80

4. Repeat this request two more times if you have an HTTP server listening on ``localhost``.
Otherwise, you will have to repeat this five times.

The request must be repeated to fill the output buffer.

5. The tokenTracer should output the three intercepted GET requests and their responses or the six GET requests:

::

    Timestamp:            2017-11-20 10:36:19.830591
    HTTP Protocol:        GET / HTTP/1.1\r\n
    Packet Size:          129
    Source:               127.0.0.1:50120
    Destination:          127.0.0.1:80

    Timestamp:            2017-11-20 10:36:19.831129
    HTTP Protocol:        HTTP/1.1 200 OK\r\n
    Packet Size:          389
    Source:               127.0.0.1:80
    Destination:          127.0.0.1:50120

    Timestamp:            2017-11-20 10:36:20.920724
    HTTP Protocol:        GET / HTTP/1.1\r\n
    Packet Size:          129
    Source:               127.0.0.1:50121
    Destination:          127.0.0.1:80

    Timestamp:            2017-11-20 10:36:20.920998
    HTTP Protocol:        HTTP/1.1 200 OK\r\n
    Packet Size:          389
    Source:               127.0.0.1:80
    Destination:          127.0.0.1:50121

    Timestamp:            2017-11-20 10:36:21.652812
    HTTP Protocol:        GET / HTTP/1.1\r\n
    Packet Size:          129
    Source:               127.0.0.1:50122
    Destination:          127.0.0.1:80

    Timestamp:            2017-11-20 10:36:21.653077
    HTTP Protocol:        HTTP/1.1 200 OK\r\n
    Packet Size:          389
    Source:               127.0.0.1:80
    Destination:          127.0.0.1:50122

As seen with this example, the output is buffered. Thus, we should not expect any output until a sufficient number of packets have been intercepted. 

1.6.3 Example 3: cURL HTTP Token Request Interception
===============================================================

We can create packets that mimic the structure of the token request packets that
the token tracer filters for.

1. Run the tokenTracer to intercept packets on the loopback interface:

::

    tokenTracer -i lo0

2. Start a new terminal.

3. cURL the following HTTP GET request to localhost:

::

    curl -X POST --data "grant_type=access_code&client_id=johnSmith&code=3142&redirect_uri=http://locahost:80&scope=global&client_secret=42" http://127.0.0.1:80

4. Repeat this three or five times.

5. The tokenTracer should output the requests:

::

    Timestamp:            2017-11-20 10:58:15.765881
    HTTP Protocol:        POST / HTTP/1.1\r\n
    Packet Size:          314
    Source:               127.0.0.1:50258
    Destination:          127.0.0.1:80
    Client Secret:        42
    Client Id:            johnSmith
    Grant Type:           access_code
    Authorization Code:   3142
    Redirect Uri:         http://locahost:80
    Scope:                global

    Timestamp:            2017-11-20 10:58:16.474243
    HTTP Protocol:        POST / HTTP/1.1\r\n
    Packet Size:          314
    Source:               127.0.0.1:50259
    Destination:          127.0.0.1:80
    Client Secret:        42
    Client Id:            johnSmith
    Grant Type:           access_code
    Authorization Code:   3142
    Redirect Uri:         http://locahost:80
    Scope:                global

    Timestamp:            2017-11-20 10:58:17.059053
    HTTP Protocol:        POST / HTTP/1.1\r\n
    Packet Size:          314
    Source:               127.0.0.1:50260
    Destination:          127.0.0.1:80
    Client Secret:        42
    Client Id:            johnSmith
    Grant Type:           access_code
    Authorization Code:   3142
    Redirect Uri:         http://locahost:80
    Scope:                global



1.6.4 Example 4: CanDIG Authorization Code Login Request
================================================================

1. Run the token tracer program:

::

    tokenTracer

2. Log into the CanDIG server using the default username and password (both ``user``).

3. The token tracer will output the authorization code request to the token endpoint and its response:

::

    $ tokenTracer 

    $ curl -L http

    HTTP Protocol:        POST /auth/realms/CanDIG/protocol/openid-connect/token HTTP/1.1\r\n
    Packet Size:          617
    Source:               172.17.0.1:56644
    Destination:          172.17.0.2:8080
    Client Secret:        250e42b8-3f41-4d0f-9b6b-e32e09fccaf7
    Client Id:            ga4ghServer
    Grant Type:           authorization_code
    Authorization Code:   uss.aanh_9Uqg0xWV6WLBioNx3Pq3h5nocT
    Redirect Uri:         http://192.168.99.100:8000/oidc_callback
    Scope:                openid email

    HTTP Protocol:        HTTP/1.1 200 OK\r\n
    Packet Size:          3582
    Source:               172.17.0.2:8080
    Destination:          172.17.0.1:56644
    Access Token:         eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJoWldPSWExUWJXczN
    Access Token Expiry:  60
    Refresh Token:        eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJoWldPSWExUWJXczN
    Refresh Token Expiry: 1800
    Token Type:           bearer
    Id Token:             eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJoWldPSWExUWJXczN



1.6.5 Example 5: CanDIG Refresh Token Request 
==================================================

1. Log into the Keycloak server as administrator using the 
default administrator username and password (both ``admin``).

2. Set the Access Token expiry time to 1 minute.

3. Run the token tracer:

::

    tokenTracer

4. Log into GA4GH Server using the default username and password:

5. Wait one minute and then refresh the webpage.

6. The token tracer will print the refresh token request made to the 
token endpoint and its response,.


1.7 Documentation
---------------------

The documentation for this program can be found under /docs.

This documentation includes:

- Detailed end-user walkthroughs
- More examples
- Command-line options
- Design documentation
- Test documentation
- Planned future changes 


1.8 External Links
---------------------

The token tracer is designed to sniff for tokens exchanged between 
application servers and Keycloak. To learn more about Keycloak visit:

http://www.keycloak.org/

This program relies on the pyshark Python sniffer capture library built 
on top of tshark. To learn more about the library, visit its 
GitHub repository:

https://github.com/KimiNewt/pyshark

To learn more about tshark and Wireshark, visit Wireshark's website:

https://www.wireshark.org/


