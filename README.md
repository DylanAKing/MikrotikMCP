# MikrotikMCP
A gui application that uses python to send commands to a mass amount routerOS devices

![Main-Window](https://user-images.githubusercontent.com/49817441/139592073-8cbd95e1-324d-4b52-b38e-84a02b586436.png)

This application takes commands and targets and runs the command(s) against all the targets.
Targets can either be enter manually, seperated by commas (ex: 172.0.0.1,172.0.0.2,...,),
or targets can be loaded from a text file, with one target per line. 

![command+target](https://user-images.githubusercontent.com/49817441/139592836-baadeabe-a785-4a69-9e60-bc3ffd2e415c.png)

It then prompts the for a username and password to login to the targets with.

![username-prompt](https://user-images.githubusercontent.com/49817441/139592843-9c67bb5d-5399-476a-9e05-6b0e625ee0ed.png) ![password-prompt](https://user-images.githubusercontent.com/49817441/139592846-85da2095-d38f-4461-9586-26fcfc3a0abf.png)

Finally displays some general output 
from each system letting you know if the command(s) ran correcctly.

![output](https://user-images.githubusercontent.com/49817441/139592879-a7b6cb71-9419-457b-8b83-58f68127cc78.png)

Additonally it adds a log entry to RouterOS devices informing the user this tool was ran

![routerOS-log](https://user-images.githubusercontent.com/49817441/139593029-20c6b73d-1d38-483b-a972-cb0774add6a0.png)

### Dependencies:
#### - python3.9
#### - python-tk (Tkinter)
#### - paramiko

To run this application open a terminal and type:

    python3 /path/to/MMCP.py


# Bugs may be encountered at this stage in development
