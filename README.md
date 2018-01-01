# OnionHarvester-Server
The Onion Router (TOR) project aims to hide users' IP and protect their privacy related to location and Internet usage.
Beside, users are able to create hidden services which are accessible through Onion addresses.
Unlike the normal Internet, in which list of all domains are reachable through TLDs (Top Level Domains), Onion addresses can not be listed, nor TOR does not want to list them.
Onion Harvester tries to find the updated list of all Onion addresses which are accessible through TOR.

This project uses volunteer clients all over the world to list the addresses. The project is made of two main sub-projects:
- Onion Harvester Server
- Onion Harvester Clients

The client for harvesting Onion addresses is available [here](https://github.com/mirsamantajbakhsh/OnionHarvester).

## Request
Clients can send a get request to ```http(s)://server/dispatcher/generate``` and catch search options include:
1. Unique ID
2. Start and End Onion addresses
3. Scanning ports
4. Timeout

Generated options will be in JSON format like:
```
{"id": "32 characters unique id", "start": "16 characters Onion address", "end": "16 characters Onion address", "ports": ["array of ports (default is 80, 443)"], "timeout": an integer of timeout (default is 30000 milliseconds)}
```
For example:
```
{"id": "d42ae54b9b3845b48868cde7a0ccd5bc", "start": "aaaaaaaaaaaaabea", "end": "aaaaaaaaaaaaabib", "ports": ["80", "443"], "timeout": 30000}
```
## Response
Clients after harvesting the range of addresses, can send results to the server as a JSON http post request.
It must be a HTTP post request with these parameters:  
- id
- addresses
- complete

The id is a unique id that client received in request section and addresses is JSON format of valid Onion addresses. The complete parameter is used when the client has searched incompletely, so we will accept the response but that range will be kept for search again so it should have ```true``` or ```false``` value.  
The addresses parameter should be an array of addresses, ports and scanned times like below. If scan hasn't any result so do'nt send addresses parameter:
```
[["address 1", port number, "date time (format: YYYY-MM-DD HH:MM)"], ["address 2", port number, "date time (format: YYYY-MM-DD HH:MM)"]]
```
For example:  
Post ```id``` parameter:
```
d42ae54b9b3845b48868cde7a0ccd5bc
```
Post ```addresses``` parameter:
```
[["facebookcorewwwi", 80, "1991-06-22 22:22"], ["facebookcorewwwi", 443, "1991-06-22 22:22"]]
```
Post ```complete``` parameter:
```
true
```
## Install
The server has been written on Django framework and you can run below commands to install requirements:
```
git clone https://github.com/mohammadnassiri/OnionHarvester-Server.git
cd OnionHarvester-Server
pip3 install -r requirements.txt
python3 manage.py collectstatic
```

## Config
There is a ```.env ``` file contains configuration for server to be run. You can set debug mode, secret key, allowed hosts, database configurations and constants.  
For generate new secret key, you can use this oneliner code:  
```
python3 -c "import string,random; uni=string.ascii_letters+string.digits+string.punctuation; print(repr(''.join([random.SystemRandom().choice(uni) for i in range(random.randint(45,50))])))"
```

In constant section you have these options:  
 - TIMEOUT: The time that each client must response before end.
 - RANGE_LIMIT: The range of Onion addresses that each client got in each request.
 - PORTS: The ports that each client scans it on each Onion address
 
 Please be noticed that each address can have about 3 seconds of scan time so for 2 ports it will be about 6 seconds, so you must give timeout a logical number related to range limit and ports config.

# Project
This project has been run on a server and you can use it now by see: [onionharvester.com](http://onionharvester.com)

# TODO
We did'nt consider any security principle on communications between clients and server, so we will work on some simple protocle to improve this approach.  
Also template updates will be included periodically.  
This project is in beta version and any we will happy to receive any suggestions.