# OnionHarvester-Server
The web application for paralleling and distributing search operations among Onion Harvester clients.

# Brief Description
Clients will connect to this server and will ask for a range of onion addresses to be scanned. Server returns them a start address, end address and time out. Clients should respond in the given time.

Addresses created by clients from start address to end address. Number of threads, TOR configuration, time out of sockets for scanning each onion are in the client configuration. Clients may join or leave the server any time.

For the client source code, go to the Onion Harvester project. [Onion Harvester Clients](https://github.com/mirsamantajbakhsh/OnionHarvester)
