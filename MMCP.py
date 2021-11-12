#!/usr/bin/env python3
# This script is intended to push commands to a mass amount of devices.
# Version: 0.2.4

import fnmatch
import re
import os
import tkinter as Tk
import tkinter.messagebox
import tkinter.simpledialog
from tkinter import filedialog
from paramiko import *
import paramiko

# Variables
infile_check, loop, loop2 = 0, 0, 0
targetList = []
dir = os.path.dirname(__file__)
icon = os.path.join(dir, 'mikrotik-icon.png')
bannerPhoto = os.path.join(dir, 'mikrotik-banner.png')
helptext = os.path.join(dir, "help.txt")
blank, stdout_content, cmd, user, match, ssh, infile = '', '', '', '', '', '', ''
logstring = str(':log warning "User ran commands via MikrotikMCP"')


def debug():
    print(commands.get("1.0", "end"))


def connect(host, user, password, loop):
    global ssh
    port = int(sshport.get("1.0", "end"))
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, username=user, password=password, port=port)
    except AuthenticationException:
        output.configure(state='normal')
        output.insert("1.0", str(loop) + "." + str(loop2) + ": ERROR: Authentication failed.\n")
        output.configure(state='disabled')


def execute(*args):
    global stdout_content, cmd, ssh
    for a in args:
        ssh.exec_command(a)
    stdin, stdout, stderr = ssh.exec_command(cmd)
    stdout_content = stdout.readlines()


def chkPing():
    global cmd, match
    pattern = "ping*"
    match = fnmatch.fnmatch(cmd, pattern)
    if match:
        cmd = cmd[:-1] + " count=3"


def chkOutput():
    global loop2, stdout_content
    print(loop2)
    print(stdout_content)
    pattern2 = "*expected end of command*"
    pattern3 = "*bad command name*"
    chk2 = ['\r\n']

    if len(stdout_content) >= 3:
        index = len(stdout_content) - 2
        output.insert("end", str(loop) + "." + str(loop2) + ": " + stdout_content[index])
        return
    if len(stdout_content) == 0:
        output.insert("end", str(loop) + "." + str(loop2) + ": Success.\n")
    for x in stdout_content:
        match2 = fnmatch.fnmatch(str(stdout_content[loop2]), pattern2)
        match3 = fnmatch.fnmatch(str(stdout_content[loop2]), pattern3)
        print(match2)
        if match2:
            if match:
                output.insert("end", str(loop) + "." + str(loop2) + ": ERROR: Default ping is limited 3\n"
                                                                    "Please remove ping 'count' argument")
            else:
                output.insert("end", str(loop) + "." + str(loop2) + ": ERROR: Expected end of command\n")
        if match3:
            output.insert("end", str(loop) + "." + str(loop2) + ": ERROR: Command unavailable\n")
        if stdout_content[loop2] == chk2[0]:
            output.insert("1.0", str(loop) + "." + str(loop2) + ": Command was sent but status is unknown.\n")
        loop2 += 1
    if loop == len(targetList):
        output.configure(state="disabled")


def submit():
    global user, targetList, infile_check, loop, cmd, loop2
    loop = 0
    output.configure(state="normal")
    output.delete("1.0", "end")
    cmd = commands.get("1.0", "end")
    print(cmd)
    if user == "":
        user = tkinter.simpledialog.askstring("Username", "Please enter username:")
    password = tkinter.simpledialog.askstring("Password", "Please enter password for user: " + user, show='*')
    if infile_check == 0:
        targets = target.get("1.0", "end")
        print(targets)
        trgtlst = re.split(",|;| |\n", targets)
        targetList = trgtlst[:-1]
    for i in targetList:
        loop2 = 0
        loop += 1
        host = str(i)
        chkPing()
        connect(host, user, password, loop)
        execute(logstring, "quit")
        chkOutput()
        # if AuthenticationException:
        #     continue


def browseFiles():
    global infile
    infile = filedialog.askopenfilename(initialdir="~/",
                                        title="Select a File",
                                        filetypes=(("Text files",
                                                    "*.txt*"),
                                                   ("all files",
                                                    "*.*")))


def openfile():
    global infile_check, targetList
    trgtlst = []
    browseFiles()
    loop_check = 1
    with open(infile) as targetFile:
        targets = targetFile.readlines()
        infile_check += 1
        target.delete("1.0", "end")
        target.config(fg="black")
        for line in targets:
            loop_check += 1
            if loop_check < len(targets):
                trgt = line[:-1]
            else:
                trgt = line
            target.insert("end", str(trgt) + "\n")
            trgtlst.append(trgt)
        targetList = trgtlst


# def clearSampleText(field):
#     if field.cget("fg") == 'grey':
#         field.delete("1.0", "end")  # delete all the text in the field
#         field.insert('1.0', '')  # Insert blank for user input
#         field.config(fg='black')


def clearSampleCommand(event):
    if commands.cget('fg') == 'grey':
        commands.delete("1.0", "end")  # delete all the text in the field
        commands.insert('1.0', '')  # Insert blank for user input
        commands.config(fg='black')


def clearSampleTarget(event):
    if target.cget('fg') == 'grey':
        target.delete("1.0", "end")  # delete all the text in the field
        target.config(fg='black')
        target.insert("1.0", '')  # Insert blank for user input


def clearSampleSshPort(event):
    if sshport.cget('fg') == 'grey':
        sshport.delete("1.0", "end")  # delete all the text in the field
        sshport.config(fg='black')
        sshport.insert("1.0", '')  # Insert blank for user input


def enterSampleCommand(event):
    if commands.cget('fg') == 'black':
        if len(commands.get("1.0", "end")) == 1:
            commands.config(fg='grey')
            commands.insert('end', 'Enter commands here')


def enterSampleTarget(event):
    if target.cget('fg') == 'black':
        if len(target.get("1.0", "end")) == 1:
            target.config(fg='grey')
            target.insert('end', '172.0.0.1,172.0.0.2,...')


def enterSampleSshPort(event):
    if sshport.cget('fg') == 'black':
        if len(sshport.get("1.0", "end")) == 1:
            sshport.config(fg='grey')
            sshport.insert('end', '22')


def displayHelp():
    with open(helptext) as help.txt:
        helpDoc = help.txt.readlines()
        tkinter.messagebox.showinfo(title="Help", message=helpDoc)


def changeUser():
    global user
    user = tkinter.simpledialog.askstring("Username", "Please enter username:")


def configureTextbox(name, focusInCMD, focusOutCMD, sampleString):
    name.insert('1.0', sampleString)
    name.bind('<FocusIn>', focusInCMD)
    name.bind('<FocusOut>', focusOutCMD)
    name.config(fg='grey')


# initial setup of GUI window
root = Tk.Tk()
root.title("Mikrotik MCP")
root.wm_iconphoto(False, Tk.PhotoImage(file=icon))
for row in range(2, 5):
    root.rowconfigure(row, weight=1)
for column in range(0, 5):
    root.columnconfigure(column, weight=1)

# Insert graphic as application banner
bannerImage = Tk.PhotoImage(file=bannerPhoto)
banner = Tk.Label(root, image=bannerImage)
banner.grid(row=0, column=1, columnspan=3, padx=12, pady=10)

# Labels
H1 = Tk.Label(text="Mass Command Pusher", font=20)
H1.grid(row=1, column=1, columnspan=3)

H2 = Tk.Label(text="Commands:")
H2.grid(row=2, column=0, padx=10, pady=25)

H3 = Tk.Label(text="Targets:")
H3.grid(row=3, column=0)

H4 = Tk.Label(text="Output:")
H4.grid(row=4, column=0, pady=25)

H5 = Tk.Label(text="SSH Port:")
H5.grid(row=5, column=0, pady=10)

# Textboxes
# create input textbox for commands
commands = Tk.Text(root, bg="white", height=3, width=50)
configureTextbox(commands, clearSampleCommand, enterSampleCommand, "Enter commands here")
commands.grid(row=2, column=1, columnspan=3, sticky='news', pady=10)

# create input textbox for targets
target = Tk.Text(root, bg="white", height=3, width=50)
configureTextbox(target, clearSampleTarget, enterSampleTarget, "172.0.0.1,172.0.0.2,...")
target.grid(row=3, column=1, columnspan=3, pady=10, sticky='news')

# create output textbox
output = Tk.Text(root, bg='white', height=5, width=50)
output.configure(state='disabled')
output.grid(row=4, column=1, columnspan=3, pady=10, sticky='news')

# create input textbox for ssh port
sshport = Tk.Text(root, bg='white', height=1, width=10)
configureTextbox(sshport, clearSampleSshPort, enterSampleSshPort, "22")
sshport.grid(row=5, column=1, sticky='w')

## Buttons
# create load button
loadButton = Tk.Button(root, text="Load", activebackground="light grey", command=lambda: openfile())
loadButton.grid(row=3, column=4, padx=20)

# create submit button
submitButton = Tk.Button(root, text="Submit", activebackground="light grey", command=lambda: submit())
submitButton.grid(row=6, column=3, pady=20)

# create exit button
exitButton = Tk.Button(root, text="Quit", activebackground="light grey", command=lambda: exit())
exitButton.grid(row=6, column=4, padx=10, pady=20)

# create help button
helpButton = Tk.Button(root, text="Help", activebackground="light grey", command=lambda: displayHelp())
helpButton.grid(row=6, column=0, padx=10, pady=20)

# create change user button
userButton = Tk.Button(root, text="Change User", activebackground="light grey", command=lambda: changeUser())
userButton.grid(row=6, column=2, padx=10, pady=20)

root.mainloop()
