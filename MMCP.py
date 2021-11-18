#!/usr/bin/env python3
# This script is intended to push commands to a mass amount of devices.
# Version: 0.2.4

import fnmatch
import re
import os
from tkinter import Label, Text, Tk, PhotoImage, Button, simpledialog, messagebox, filedialog
from paramiko import SSHClient, AuthenticationException, AutoAddPolicy


def configureTextbox(name, focusInCMD, focusOutCMD, sampleString):
    name.insert('1.0', sampleString)
    name.bind('<FocusIn>', focusInCMD)
    name.bind('<FocusOut>', focusOutCMD)
    name.config(fg='grey')


class App(Tk):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.infile_check = 0
        self.loop = 0
        self.loop2 = 0
        self.targetList = []
        self.dir = os.path.dirname(__file__)
        self.icon = os.path.join(self.dir, 'mikrotik-icon.png')
        self.bannerPhoto = os.path.join(self.dir, 'mikrotik-banner.png')
        self.helptext = os.path.join(self.dir, "help.txt")
        self.blank = ''
        self.stdout_content = ''
        self.cmd = ''
        self.user = ''
        self.match = ''
        self.ssh = SSHClient()
        self.infile = ''
        self.logstring = str(':log warning "User ran commands via MikrotikMCP"')
        self.configure_gui()

    def configure_gui(self):
        self.title("Mikrotik MCP")
        self.wm_iconphoto(False, PhotoImage(file=self.icon))
        for row in range(2, 5):
            self.rowconfigure(row, weight=1)
        for column in range(0, 5):
            self.columnconfigure(column, weight=1)
        # Insert graphic as application banner
        bannerImage = PhotoImage(file=self.bannerPhoto)
        banner = Label(self, image=bannerImage)
        banner.grid(row=0, column=1, columnspan=3, padx=12, pady=10)

        # Labels
        H1 = Label(text="Mass Command Pusher", font=20)
        H1.grid(row=1, column=1, columnspan=3)

        H2 = Label(text="Commands:")
        H2.grid(row=2, column=0, padx=10, pady=25)

        H3 = Label(text="Targets:")
        H3.grid(row=3, column=0)

        H4 = Label(text="Output:")
        H4.grid(row=4, column=0, pady=25)

        H5 = Label(text="SSH Port:")
        H5.grid(row=5, column=0, pady=10)

        # Textboxes
        # create input textbox for commands
        self.commands = Text(self, bg="white", height=3, width=50)
        configureTextbox(self.commands, self.clearSampleCommand, self.enterSampleCommand, "Enter commands here")
        self.commands.grid(row=2, column=1, columnspan=3, sticky='news', pady=10)

        # create input textbox for targets
        self.target = Text(self, bg="white", height=3, width=50)
        configureTextbox(self.target, self.clearSampleTarget, self.enterSampleTarget, "172.0.0.1,172.0.0.2,...")
        self.target.grid(row=3, column=1, columnspan=3, pady=10, sticky='news')

        # create output textbox
        self.output = Text(self, bg='white', height=5, width=50)
        self.output.configure(state='disabled')
        self.output.grid(row=4, column=1, columnspan=3, pady=10, sticky='news')

        # create input textbox for ssh port
        self.sshport = Text(self, bg='white', height=1, width=10)
        configureTextbox(self.sshport, self.clearSampleSshPort, self.enterSampleSshPort, "22")
        self.sshport.grid(row=5, column=1, sticky='w')

        ## Buttons
        # create load button
        loadButton = Button(self, text="Load", activebackground="light grey", command=self.openfile)
        loadButton.grid(row=3, column=4, padx=20)

        # create submit button
        submitButton = Button(self, text="Submit", activebackground="light grey", command=self.submit)
        submitButton.grid(row=6, column=3, pady=20)

        # create exit button
        exitButton = Button(self, text="Quit", activebackground="light grey", command=exit)
        exitButton.grid(row=6, column=4, padx=10, pady=20)

        # create help button
        helpButton = Button(self, text="Help", activebackground="light grey", command=self.displayHelp)
        helpButton.grid(row=6, column=0, padx=10, pady=20)

        # create change user button
        userButton = Button(self, text="Change User", activebackground="light grey", command=self.changeUser)
        userButton.grid(row=6, column=2, padx=10, pady=20)

    def debug(self):
        print(self.commands.get("1.0", "end"))

    def connect(self, host, user, password, loop):
        port = int(self.sshport.get("1.0", "end"))
        self.ssh.set_missing_host_key_policy(AutoAddPolicy())
        try:
            self.ssh.connect(host, username=user, password=password, port=port)
        except AuthenticationException:
            self.output.configure(state='normal')
            self.output.insert("1.0", str(self.loop) + "." + str(self.loop2) + ": ERROR: Authentication failed.\n")
            self.output.configure(state='disabled')

    def execute(self, *args):
        for a in args:
            self.ssh.exec_command(a)  # nosec
        _, stdout, stderr = self.ssh.exec_command(self.cmd)  # nosec
        print(stderr)
        self.stdout_content = stdout.readlines()

    def chkPing(self):
        pattern = "ping*"
        match = fnmatch.fnmatch(self.cmd, pattern)
        if match:
            self.cmd = self.cmd[:-1] + " count=3"

    def chkOutput(self):
        print(self.loop2)
        print(self.stdout_content)
        pattern2 = "*expected end of command*"
        pattern3 = "*bad command name*"
        chk2 = ['\r\n']

        if len(self.stdout_content) >= 3:
            index = len(self.stdout_content) - 2
            self.output.insert("end", str(self.loop) + "." + str(self.loop2) + ": " + self.stdout_content[index])
            return
        if len(self.stdout_content) == 0:
            self.output.insert("end", str(self.loop) + "." + str(self.loop2) + ": Success.\n")
        for _ in self.stdout_content:
            match2 = fnmatch.fnmatch(str(self.stdout_content[self.loop2]), pattern2)
            match3 = fnmatch.fnmatch(str(self.stdout_content[self.loop2]), pattern3)
            print(match2)
            if match2:
                if self.match:
                    self.output.insert("end", str(self.loop) + "." + str(self.loop2) + ": ERROR: Default ping is limited 3\n"
                                                                        "Please remove ping 'count' argument")
                else:
                    self.output.insert("end", str(self.loop) + "." + str(self.loop2) + ": ERROR: Expected end of command\n")
            if match3:
                self.output.insert("end", str(self.loop) + "." + str(self.loop2) + ": ERROR: Command unavailable\n")
            if self.stdout_content[self.loop2] == chk2[0]:
                self.output.insert("1.0", str(self.loop) + "." + str(self.loop2) + ": Command was sent but status is unknown.\n")
            self.loop2 += 1
        if self.loop == len(self.targetList):
            self.output.configure(state="disabled")

    def submit(self):
        loop = 0
        self.output.configure(state="normal")
        self.output.delete("1.0", "end")
        self.cmd = self.self.commands.get("1.0", "end")
        print(self.cmd)
        if self.user == "":
            self.user = simpledialog.askstring("Username", "Please enter username:")
        password = simpledialog.askstring("Password", "Please enter password for user: " + self.user, show='*')
        if self.infile_check == 0:
            targets = self.target.get("1.0", "end")
            print(targets)
            trgtlst = re.split(",|;| |\n", targets)
            self.targetList = trgtlst[:-1]
        for i in self.targetList:
            loop += 1
            host = str(i)
            self.chkPing()
            self.connect(host, self.user, password, loop)
            self.execute(self.logstring, "quit")
            self.chkOutput()

    def browseFiles(self):
        self.infile = filedialog.askopenfilename(
            initialdir="~/",
            title="Select a File",
            filetypes=(
                ("Text files", "*.txt*"),
                ("all files", "*.*")))

    def openfile(self):
        trgtlst = []
        self.browseFiles()
        self.loop_check = 1
        with open(self.infile) as targetFile:
            targets = targetFile.readlines()
            self.infile_check += 1
            self.target.delete("1.0", "end")
            self.target.config(fg="black")
            for line in targets:
                self.loop_check += 1
                if self.loop_check < len(targets):
                    trgt = line[:-1]
                else:
                    trgt = line
                self.target.insert("end", str(trgt) + "\n")
                trgtlst.append(trgt)
            self.targetList = trgtlst

    def clearSampleCommand(self, event):
        if self.commands.cget('fg') == 'grey':
            self.commands.delete("1.0", "end")  # delete all the text in the field
            self.commands.insert('1.0', '')  # Insert blank for user input
            self.commands.config(fg='black')

    def clearSampleTarget(self, event):
        if self.target.cget('fg') == 'grey':
            self.target.delete("1.0", "end")  # delete all the text in the field
            self.target.config(fg='black')
            self.target.insert("1.0", '')  # Insert blank for user input

    def clearSampleSshPort(self, event):
        if self.sshport.cget('fg') == 'grey':
            self.sshport.delete("1.0", "end")  # delete all the text in the field
            self.sshport.config(fg='black')
            self.sshport.insert("1.0", '')  # Insert blank for user input

    def enterSampleCommand(self, event):
        if self.commands.cget('fg') == 'black':
            if len(self.commands.get("1.0", "end")) == 1:
                self.commands.config(fg='grey')
                self.commands.insert('end', 'Enter commands here')

    def enterSampleTarget(self, event):
        if self.target.cget('fg') == 'black':
            if len(self.target.get("1.0", "end")) == 1:
                self.target.config(fg='grey')
                self.target.insert('end', '172.0.0.1,172.0.0.2,...')

    def enterSampleSshPort(self, event):
        if self.sshport.cget('fg') == 'black':
            if len(self.sshport.get("1.0", "end")) == 1:
                self.sshport.config(fg='grey')
                self.sshport.insert('end', '22')

    def displayHelp(self):
        with open(self.helptext) as help.txt:
            helpDoc = help.txt.readlines()
            messagebox.showinfo(title="Help", message=helpDoc)

    def changeUser(self):
        self.user = simpledialog.askstring("Username", "Please enter username:")


def main():
    app = App()
    app.mainloop()


if __name__ == '__main__':
    main()