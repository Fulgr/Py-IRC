# Py-IRC
Py-IRC is a basic python IRC server and client, using the client you cannot connect to other IRC servers however you would be able to connect to toher Py-IRC servers.
## Installation
To install Py-IRC you can use git or download it as a .zip, all you need to run Py-IRC is Python and you're ready to run the client using python client.py and the server using python server.py
## How it works
### Server
The Py-IRC server creates a socket where clients can connect too, it has a list of all logged in connections and it prompts new connections to login else it would not refer it any messages or refer any of the client's messages. There are also a few basic features including /msg NickServ nick password which registers / changes the nick of the connection.
### Client
The client connects to the Py-IRC server and logs in using dummy credentials so it can see messages incoming immediately, and it continiously awaits for new messages to print and prompts the user to send their own message in a input and when that is submitted the client sends the message to the server which broadcasts the message to all other active connections.
## Planned features
- Channels
- /join & /leave command
- /list command which lists all channels
- /help command

node2.endelon-hosting.de:32995
