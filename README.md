# MikrotikMCP
A gui application that uses python to send commands to a mass amount routerOS devices

## Installation

Install the required dependencies by running the following:

```bash
pip install -r requirements.txt
```

## Usage

This code is compatible only with python3. This is a executable script and can be executed by the following:

```bash
./path/to/MMCP.py
```

![Main-window](https://user-images.githubusercontent.com/49817441/140189107-85aa5b07-888a-4830-98fa-862a7c9badc6.png)

This application takes commands and targets and runs the command(s) against all the targets.
Targets can either be enter manually, seperated by commas (ex: 172.0.0.1,172.0.0.2,...,),
or targets can be loaded from a text file, with one target per line. 

![main+commands](https://user-images.githubusercontent.com/49817441/140189135-911a9b76-0c79-435d-a931-8627193d5aa7.png)

It then prompts the for a username and password to login to the targets with.

![username-prompt](https://user-images.githubusercontent.com/49817441/139592843-9c67bb5d-5399-476a-9e05-6b0e625ee0ed.png) ![password-prompt](https://user-images.githubusercontent.com/49817441/139592846-85da2095-d38f-4461-9586-26fcfc3a0abf.png)

Finally displays some general output 
from each system letting you know if the command(s) ran correcctly.

![output](https://user-images.githubusercontent.com/49817441/140189161-17d60d78-32ed-4bbd-b984-98bd38b2e1a1.png)

Additonally it adds a log entry to RouterOS devices informing the user this tool was ran

![routerOS-log](https://user-images.githubusercontent.com/49817441/139593029-20c6b73d-1d38-483b-a972-cb0774add6a0.png)




# Bugs may be encountered at this stage in development
