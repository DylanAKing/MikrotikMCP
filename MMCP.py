# This script is intended to push commands to a mass amount of devices.
# Version: 0.2.1


import os
import easygui
import tkinter as Tk
import tkinter.messagebox
import tkinter.simpledialog
import paramiko
from paramiko.ssh_exception import AuthenticationException

port = 22
infile_check = 0
targetList = []
user = ""
dirname = os.path.dirname(__file__)
icon = os.path.join(dirname, 'mikrotik-icon.png')
bannerPhoto = os.path.join(dirname, 'mikrotik-banner.png')
helptext = os.path.join(dirname, "help.txt")

def debug():
    print(commands.get("1.0", "end"))


def submit():

    global infile_check
    global targetList
    global user
    print(infile_check)
    output.delete("1.0", "end")
    checklist = []
    checklist2 = ['\r\n']
    loop = 0
    cmd = commands.get("1.0", "end")
    if user == "":
        user = tkinter.simpledialog.askstring("Username", "Please enter username:")
    password = tkinter.simpledialog.askstring("Password", "Please enter password for user: " + user, show='*')
    logstring = str(':log warning "User ran commands via MikrotikMCP"')

    if infile_check == 0:
        targets = target.get("1.0", "end")
        trgtlst = targets.split(",")
        targetList = trgtlst[:-1]

    for i in targetList:
        loop += 1
        host = str(i)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(host, port, username=user, password=password)
        except AuthenticationException:
            output.insert("1.0", str(loop)+": " + "ERROR: Authentication failed")
        stdin, stdout, stderr = ssh.exec_command(cmd)
        ssh.exec_command(logstring)
        ssh.exec_command("quit")
        stdout_content = stdout.readlines()
        if stdout_content == checklist:
            output.insert("1.0", str(loop) + ": " + "Success")
        elif stdout_content == checklist2:
            output.insert("1.0", str(loop)+": "+"ERROR: Function unavailable on target device")


def openfile():
    global infile_check
    global targetList
    trgtlst = []
    infile = easygui.fileopenbox()
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
            target.insert("1.0", str(trgt) + "\n")
            trgtlst.append(trgt)
        targetList = trgtlst


def clearSampleCommand(event):
    if commands.cget('fg') == 'grey':
        commands.delete("1.0", "end")  # delete all the text in the field
        commands.insert('1.0', '')  # Insert blank for user input
        commands.config(fg='black')


def clearSampleTarget(event):
    if target.cget('fg') == 'grey':
        target.delete("1.0", "end")  # delete all the text in the field
        target.insert("1.0", '')  # Insert blank for user input
        target.config(fg='black')


def help():
    with open(helptext) as help.txt:
        helpDoc = help.txt.readlines()
        tkinter.messagebox.showinfo(title="Help", message=helpDoc)


def changeUser():
    global user
    user = tkinter.simpledialog.askstring("Username", "Please enter username:")


# initial setup of GUI window
root = Tk.Tk()
root.title("Mikrotik MCP")
root.wm_minsize(350, 100)
root.wm_iconphoto(False, Tk.PhotoImage(file=icon))

# create header for command(s) input
H1 = Tk.Label(text="Commands:")
H1.grid(row=2, column=0, padx=10, pady=25)

# create input textbox for commands
commands = Tk.Text(root, bg="white", height=3, width=50)
commands.insert('1.0', "Enter commands here")
commands.grid(row=2, column=1, columnspan=3)
commands.bind('<FocusIn>', clearSampleCommand)
commands.config(fg='grey')

# create header for target(s) input
H2 = Tk.Label(text="Targets:")
H2.grid(row=3, column=0)

# create target Selection
target = Tk.Text(root, bg="white", height=3, width=50)
target.insert('1.0', "172.0.0.1,172.0.0.2,...")
target.grid(row=3, column=1, columnspan=3, pady=10)
target.bind('<FocusIn>', clearSampleTarget)
target.config(fg='grey')

# create load from file button
loadButton = Tk.Button(root, text="Load", activebackground="light grey", command=lambda: openfile())
loadButton.grid(row=3, column=4, padx=20)

# create and insert submit button
submitButton = Tk.Button(root, text="Submit", activebackground="light grey", command=lambda: debug())
submitButton.grid(row=5, column=3, pady=20)

# create and insert exit button
exitButton = Tk.Button(root, text="Quit", activebackground="light grey", command=lambda: exit())
exitButton.grid(row=5, column=4, padx=10, pady=20)

# create and insert help.txt button
helpButton = Tk.Button(root, text="Help", activebackground="light grey", command=lambda: help())
helpButton.grid(row=5, column=0, padx=10, pady=20)

# Insert graphic as application banner
bannerImage = Tk.PhotoImage(file=bannerPhoto)
banner = Tk.Label(root, image=bannerImage)
banner.grid(row=0, column=1, columnspan=3, padx=12, pady=10)

H3 = Tk.Label(text="Mass Command Pusher", font=20)
H3.grid(row=1, column=2)

H4 = Tk.Label(text="Output:")
H4.grid(row=4, column=0, pady=25)

output = Tk.Text(root, bg='white', height=5, width=50)
output.grid(row=4, column=1, columnspan=3, pady=10)

# create and insert change user button
userButton = Tk.Button(root, text="Change User", activebackground="light grey", command=lambda: changeUser())
userButton.grid(row=5, column=2, padx=10, pady=20)

root.mainloop()
