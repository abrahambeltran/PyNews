# PythonProject

## COP 4521
Group# 15

Members:

    Dipanwita Chakraborty Bhattacharya  dcb22i

    Abraham Beltran                     ab19bb

![](/illustration.png)

## curl abrahambeltran.dev (domain being used)

Curl in this case works by verifying a secure socket layer (SSL) certificate with the local authorized certificate store after communicating to the server through the transport layer security (TLS) in order to initiate the handshake. In our example because the https forwarding has not been completed yet, it skips this step and immediately requests information from the server at the IP 147.182.187.44. By communicating through port 80 with TCP (in https this would be port 443 instead), curl uses the GET command to get information from the website. This then returns the html from the website to the user through the terminal.

So to summarize, when curl is run, the client sends to the server and then the server sends back to the client to confirm the message. Afterwards, the client sends its information for verification and then the server authenticates it and sends back information to the client. This happens using SSL and TLS through port 80 in this case for http and port 443 for https.

## Security

We have SSH keys implemented to limit who can access the servers in order to limit the exposure. IPs will also be whitelisted for access to the server as well in order to limit intrusion attempts. Login attempts will be managed by auto0 so although there may be possible zero day vulnerabilities, we are relying on their maintenance to keep our website secure after development.

## Updates

In order to keep the server secure, we have opted for automatic updates for all dependencies and the operating system. Although it has the risk of affecting the website functions it should be the best way to ensure that everything is safe from vulnerabilities that may arise. We did this by configuring the 'unattended-upgrades' package to allow for updates to general packages and recommended updates given by ubuntu. No changes were made to the auto-upgrade interval which is set at once a day.

Code updates or upgrades will be done after development and testing on our personal machines and then transfered through SFTP.

## Configs

Configuration files for the server can be found in the config folder. Config files on the server are held in their default locations.
