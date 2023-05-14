import os
import json
import datetime
from pathlib import Path


class DB:
    def __init__(self, Database, Debug=False, DatabaseMode=0):
        self.DatabasePath = os.path.join(Path.cwd(), "DB", Database)
        self.Debug = Debug
        self.SavePath = os.path.join(Path.cwd(), "DB")
        self.SettingsFile = os.path.join(Path.cwd(), "DB", "DatabaseSettings.json")
        if not os.path.exists(self.SavePath):
            os.mkdir(self.SavePath)
        if not Path(self.SettingsFile).is_file():
            with open(self.SettingsFile, "w") as outfile:
                self.Settings = {"DBsavemode": DatabaseMode}
                json.dump(self.Settings, outfile)
        else:
            with open(self.SettingsFile, 'r') as f:
                self.Settings = json.load(f)
        if not Path(self.DatabasePath).is_file():
            with open(self.DatabasePath, "w") as outfile:
                self.Database = {}
                json.dump(self.Database, outfile)
        else:
            with open(self.DatabasePath, 'r') as f:
                self.Database = json.load(f)

    def __str__(self):
        return str(f"Loaded database: {self.DatabasePath}")

    def CurrentTime(self):
        return datetime.datetime.now()

    def CheckIfExists(self, Mode: int, Table, Entry="", Key=""):
        """
        This function checks if a key exists in the database
        the different modes:
        0: check if table exists
        1: check if entry exists
        2: check if key exists
        """
        FUNC = "CheckIfExists"
        if Mode == 0:
            if Table in self.Database:
                return 1, "True"
            else:
                return 1, "False"
        if Mode == 1:
            if Table in self.Database:
                if Entry in self.Database[Table]:
                    return 1, "True"
                else:
                    return 1, "False"
            else:
                if self.Debug: print(
                    f"[Debug/Error {self.CurrentTime()}]: ({FUNC}, Mode:{Mode}) Table {Table} does not exist, can't check for entry!")
                return -4, "Error"
        if Mode == 2:
            if Table in self.Database:
                if Entry in self.Database[Table]:
                    if Key in self.Database[Table][Entry]:
                        return 1, "True"
                    else:
                        return 1, "False"
                else:
                    if self.Debug: print(
                        f"[Debug/Error {self.CurrentTime()}]: ({FUNC}, Mode:{Mode}) Entry {Entry} does not exist in table {Table}, can't check for Key!")
                    return -4, "Error"
            else:
                if self.Debug: print(
                    f"[Debug/Error {self.CurrentTime()}]: ({FUNC}, Mode:{Mode}) Table {Table} does not exist, can't check for entry!")
            return -4, "Error"
        else:
            if self.Debug: print(f"[Debug/Error {self.CurrentTime()}]: ({FUNC}) Invalid Mode {Mode}")
            return -2, "Error"

    def CreateTable(self, Table, Type=0):
        """
        This function creates a new table in the database
        Types:
        0: Dynamic table, entries don't need to have the same keys
        1: Static table, all entries must have the same keys (like SQL)
        :param Table: Table to create
        :type Table: string
        :param Type: Type of table
        :type Type: integer
        :return: 1 if successful, 0 otherwise
        """
        FUNC = "CreateTable"
        if not self.CheckIfExists(0, Table)[1] == "Error":
            if self.CheckIfExists(0, Table)[1] == "False":
                self.Database[Table] = {}
                if self.Debug: print(f"[Debug/Info {self.CurrentTime()}]: ({FUNC}) Table {Table} created in database!")
                return 1
            if self.CheckIfExists(0, Table)[1] == "True":
                if self.Debug: print(f"[Debug/Info {self.CurrentTime()}]: ({FUNC}) Table {Table} already exists!")
                return -5
        else:
            return self.CheckIfExists(0, Table)[0]

    def DeleteTable(self, Table):
        """
        This function deletes a table from the database
        :param Table: Table to delete
        :type Table: string
        :return: 1 if successful, 0 otherwise
        """
        FUNC = "DeleteTable"
        if not self.CheckIfExists(0, Table)[1] == "Error":
            if self.CheckIfExists(0, Table)[1] == "True":
                del self.Database[Table]
                if self.Debug: print(
                    f"[Debug/Info {self.CurrentTime()}]: ({FUNC}) Table {Table} deleted from database!")
                return 1
            if self.CheckIfExists(0, Table)[1] == "False":
                if self.Debug: print(f"[Debug/Info {self.CurrentTime()}]: ({FUNC}) Table {Table} doesn't exist!")
                return -4
        else:
            return self.CheckIfExists(0, Table)[0]

    def CreateEntry(self, Table, Entry, Content: dict):
        """
        This function adds a new entry to a table
        :param Table: Table to make changes to
        :type Table: string
        :param Entry: Entry to make
        :type Entry: string
        :param Content: Content to add to entry
        :type Content: dict
        :return: 1 if successful, 0 otherwise
        """
        FUNC = "CreateEntry"
        if not self.CheckIfExists(1, Table, Entry)[1] == "Error":
            if self.CheckIfExists(1, Table, Entry)[1] == "False":
                self.Database[Table][Entry] = Content
                if self.Debug: print(
                    f"[Debug/Info {self.CurrentTime()}]: ({FUNC}) Entry {Entry} added to table {Table}!")
                return 1
            if self.CheckIfExists(1, Table, Entry)[1] == "True":
                if self.Debug: print(
                    f"[Debug/Error {self.CurrentTime()}]: ({FUNC}) Entry {Entry} already exists in table {Table}!")
                return -5
        else:
            return self.CheckIfExists(1, Table, Entry)[0]

    def DeleteEntry(self, Table, Entry):
        """
        This function removes an entry from a table
        :param Table: Table to make changes to
        :type Table: string
        :param Entry: Entry to make
        :type Entry: string
        :return: 1 if successful, 0 otherwise
        """
        FUNC = "DeleteEntry"
        if not self.CheckIfExists(1, Table, Entry)[1] == "Error":
            if self.CheckIfExists(1, Table, Entry)[1] == "True":
                del self.Database[Table][Entry]
                if self.Debug: print(
                    f"[Debug/Info {self.CurrentTime()}]: ({FUNC}) Entry {Entry} removed from table {Table}!")
                return 1
            if self.CheckIfExists(1, Table, Entry)[1] == "False":
                if self.Debug: print(
                    f"[Debug/Error {self.CurrentTime()}]: ({FUNC}) Entry {Entry} doesn't exist in table {Table}!")
                return -4
        else:
            return self.CheckIfExists(1, Table, Entry)[0]

    def OverwriteEntry(self, Table, Entry, Content):
        """
        This function overwrites an entry in a table
        :param Table: Table to make changes to
        :type Table: string
        :param Entry: Entry to overwrite
        :type Entry: string
        :param Content: Content to add to entry
        :type Content: dict
        :return: 1 if successful, 0 otherwise
        """
        FUNC = "OverwriteEntry"
        if not self.CheckIfExists(1, Table, Entry)[1] == "Error":
            if self.CheckIfExists(1, Table, Entry)[1] == "True":
                self.Database[Table][Entry] = Content
                if self.Debug: print(
                    f"[Debug/Info {self.CurrentTime()}]: ({FUNC}) Entry {Entry} overwritten in table {Table}!")
                return 1
            if self.CheckIfExists(1, Table, Entry)[1] == "False":
                if self.Debug: print(
                    f"[Debug/Error {self.CurrentTime()}]: ({FUNC}) Entry {Entry} does not exist in table {Table}!")
                return -4
        else:
            return self.CheckIfExists(1, Table, Entry)[0]

    def ModifyKey(self, Table, Entry, Key, Content):
        """
        This function changes the content of a key in the database
        :param Table: Table to make changes to
        :type Table: string
        :param Entry: Entry to make changes to
        :type Entry: string
        :param Key: Key to change
        :type Key: string
        :param Content: Content to put in the key
        :type Content: any
        :return: 1 if successful, 0 otherwise
        """
        FUNC = "ModifyKey"
        if not self.CheckIfExists(2, Table, Entry, Key)[1] == "Error":
            if self.CheckIfExists(2, Table, Entry, Key)[1] == "True":
                self.Database[Table][Entry][Key] = Content
                if self.Debug: print(
                    f"[Debug/Info {self.CurrentTime()}]: ({FUNC}) Key {Key} from Entry {Entry} overwritten in table {Table}!")
                return 1
            if self.CheckIfExists(2, Table, Entry, Key)[1] == "False":
                if self.Debug: print(
                    f"[Debug/Error {self.CurrentTime()}]: ({FUNC}) Key {Key} does not exist in Entry {Entry} from table {Table}!")
                return -4
        else:
            return self.CheckIfExists(2, Table, Entry, Key)[0]

    def ReadKey(self, Table, Entry, Key):
        """
        This function reads the content of a key in the database
        :param Table: The table to read
        :type Table: string
        :param Entry: Entry to read
        :type Entry: string
        :param Key: Key to read
        :type Key: string
        :return: 1 if successful, 0 otherwise and the data of the key
        """
        FUNC = "ReadKey"
        if not self.CheckIfExists(2, Table, Entry, Key)[1] == "Error":
            if self.CheckIfExists(2, Table, Entry, Key)[1] == "True":
                if self.Debug: print(
                    f"[Debug/Info {self.CurrentTime()}]: ({FUNC}) Key {Key} from Entry {Entry} in table {Table} read!")
                return 1, self.Database[Table][Entry][Key]
            if self.CheckIfExists(2, Table, Entry, Key)[1] == "False":
                if self.Debug: print(
                    f"[Debug/Error {self.CurrentTime()}]: ({FUNC}) Key {Key} does not exist in Entry {Entry} from table {Table}!")
                return -4, None
        else:
            return self.CheckIfExists(2, Table, Entry, Key)[0]

    def MatchKey(self, Table, Entry, Key, Data):
        """
        This function checks if the key is the same as the data
        :param Table: The table to read
        :type Table: string
        :param Entry: Entry to read
        :type Entry: string
        :param Key: Key to read
        :type Key: string
        :param Data: Data to match with content of key
        :type Data: string
        :return: 1 if successful, 0 otherwise and whether the key is the same as the data
        """
        FUNC = "MatchKey"
        if not self.CheckIfExists(2, Table, Entry, Key)[1] == "Error":
            if self.CheckIfExists(2, Table, Entry, Key)[1] == "True":
                if self.Database[Table][Entry][Key] == Data:
                    if self.Debug: print(
                        f"[Debug/Info {self.CurrentTime()}]: ({FUNC}) Matched Key {Key} from Entry {Entry} with Data {Data} in table {Table}!")
                    return 1, "True"
                else:
                    if self.Debug: print(
                        f"[Debug/Info {self.CurrentTime()}]: ({FUNC}) Matched Key {Key} from Entry {Entry} with Data {Data} in table {Table}!")
                    return 1, "False"
            if self.CheckIfExists(2, Table, Entry, Key)[1] == "False":
                if self.Debug: print(
                    f"[Debug/Error {self.CurrentTime()}]: ({FUNC}) Key {Key} does not exist in Entry {Entry} from table {Table}!")
                return -4, "Error"
        else:
            return self.CheckIfExists(2, Table, Entry, Key)[0], "Error"

    def SaveDatabase(self):
        """
        This function saves the changes made to the database
        """
        FUNC = "SaveDatabase"
        with open(self.DatabasePath, "w") as outfile:
            json.dump(self.Database, outfile)
        if self.Debug: print(
            f"[Debug/Info {self.CurrentTime()}]: ({FUNC}) Database {self.DatabasePath} saved!")
        return 1

    def ParseCommands(self, commandslist):
        """
        This function parses a list of commands and executes them
        :param commandslist: a list of commands to parse and execute
        :type commandslist: list
        :return: 1 if successful, 0 otherwise and data if requested
        """
        FUNC = "ParseCommands"
        returnlist = []
        for commands in commandslist:
            if self.CheckIfRequiredArgsGiven(commands, ["command"]):
                if commands["command"] == "CurrentTime":
                    returndict = {"data": str(self.CurrentTime())}
                    returnlist.append(returndict)
                    continue

                if commands["command"] == "CheckIfExists":
                    if self.CheckIfRequiredArgsGiven(commands, ["Mode"]):
                        if commands["Mode"] == 0:
                            if self.CheckIfRequiredArgsGiven(commands, ["Table"]):
                                returncode, data = self.CheckIfExists(commands["Mode"],
                                                                      commands["Table"])
                        else:
                            if commands["Mode"] == 1:
                                if self.CheckIfRequiredArgsGiven(commands, ["Table", "Entry"]):
                                    returncode, data = self.CheckIfExists(commands["Mode"],
                                                                          commands["Table"],
                                                                          commands["Entry"])
                            else:
                                if commands["Mode"] == 2:
                                    if self.CheckIfRequiredArgsGiven(commands, ["Table", "Entry", "Key"]):
                                        returncode, data = self.CheckIfExists(commands["Mode"],
                                                                              commands["Table"],
                                                                              commands["Entry"],
                                                                              commands["Key"])
                                else:
                                    returncode = -2
                                    data = None
                    else:
                        returncode = -1
                        data = None
                    returndict = {"data": data, "returncode": returncode}
                    returnlist.append(returndict)
                    continue

                if commands["command"] == "CreateTable":
                    if self.CheckIfRequiredArgsGiven(commands, ["Table"]):
                        if not "Type" in commands:
                            returncode = self.CreateTable(commands["Table"])
                        else:
                            returncode = self.CreateTable(commands["Table"],
                                                          commands["Type"])
                    else:
                        returncode = -1
                    returndict = {"returncode": returncode}
                    returnlist.append(returndict)
                    continue

                if commands["command"] == "DeleteTable":
                    if self.CheckIfRequiredArgsGiven(commands, ["Table"]):
                        returncode = self.DeleteTable(commands["Table"])
                    else:
                        returncode = -1
                    returndict = {"returncode": returncode}
                    returnlist.append(returndict)
                    continue

                if commands["command"] == "CreateEntry":
                    if self.CheckIfRequiredArgsGiven(commands, ["Table", "Entry", "Content"]):
                        returncode = self.CreateEntry(commands["Table"],
                                                      commands["Entry"],
                                                      commands["Content"])
                    else:
                        returncode = -1
                    returndict = {"returncode": returncode}
                    returnlist.append(returndict)
                    continue

                if commands["command"] == "DeleteEntry":
                    if self.CheckIfRequiredArgsGiven(commands, ["Table", "Entry"]):
                        returncode = self.DeleteEntry(commands["Table"],
                                                      commands["Entry"])
                    else:
                        returncode = -1
                    returndict = {"returncode": returncode}
                    returnlist.append(returndict)
                    continue

                if commands["command"] == "OverwriteEntry":
                    if self.CheckIfRequiredArgsGiven(commands, ["Table", "Entry", "Content"]):
                        returncode = self.OverwriteEntry(commands["Table"],
                                                         commands["Entry"],
                                                         commands["Content"])
                    else:
                        returncode = -1
                    returndict = {"returncode": returncode}
                    returnlist.append(returndict)
                    continue

                if commands["command"] == "ModifyKey":
                    if self.CheckIfRequiredArgsGiven(commands, ["Table", "Entry", "Key", "Content"]):
                        returncode = self.ModifyKey(commands["Table"],
                                                    commands["Entry"],
                                                    commands["Key"],
                                                    commands["Content"])
                    else:
                        returncode = -1
                    returndict = {"returncode": returncode}
                    returnlist.append(returndict)
                    continue

                if commands["command"] == "ReadKey":
                    if self.CheckIfRequiredArgsGiven(commands, ["Table", "Entry", "Key"]):
                        returncode, data = self.ReadKey(commands["Table"],
                                                        commands["Entry"],
                                                        commands["Key"])
                    else:
                        returncode = -1
                    returndict = {"returncode": returncode, "data": data}
                    returnlist.append(returndict)
                    continue

                if commands["command"] == "MatchKey":
                    if self.CheckIfRequiredArgsGiven(commands, ["Table", "Entry", "Key", "Data"]):
                        returncode, data = self.MatchKey(commands["Table"],
                                                         commands["Entry"],
                                                         commands["Key"],
                                                         commands["Data"])
                    else:
                        returncode = -1
                    returndict = {"returncode": returncode, "data": data}
                    returnlist.append(returndict)
                    continue
            else:
                returncode = -3
                returndict = {"returncode": returncode}
                returnlist.append(returndict)
                continue
        self.SaveDatabase()
        if self.Debug: print(
            f"[Debug/Info {self.CurrentTime()}]: ({FUNC}) Executed commandslist {commandslist}!")
        print(returnlist)
        return returnlist

    def CheckIfRequiredArgsGiven(self, command: dict, requiredargs: list):
        """
        Checks if the command has the required arguments
        :param command: the command to check
        :type command: dict
        :param requiredargs: a list with the arguments the command needs
        :type requiredargs: list
        :return: returns true or false
        """
        FUNC = "CheckIfRequiredArgsGiven"
        for arg in requiredargs:
            if not arg in command:
                if self.Debug: print(f"[Debug/Info {self.CurrentTime()}]: ({FUNC}) Args missing for command {command}!")
                return False
        return True


test = DB("testfile.json", True)
# test.Database = {}
print(test.Database)
test.CreateTable("Hi")
print(test.Database)
test.CreateTable("heyyy")
test.CreateEntry("heyyy", "LeOtherUser", {"key": "some text", "Anotherdict": {"hi": "hey"}})

commandslist = []
commandslist.append({
    "command": "CurrentTime"
})

# Existing Table
commandslist.append({
    "command": "CheckIfExists",
    "Mode": 0,
    "Table": "Hi"
})

# Nonexisting Table
commandslist.append({
    "command": "CheckIfExists",
    "Mode": 0,
    "Table": "wut"
})

# New Table
commandslist.append({
    "command": "CreateTable",
    "Table": "heyyy"
})

# Existing Table
commandslist.append({
    "command": "CreateTable",
    "Table": "Hi"
})

commandslist.append({
    "command": "DeleteTable",
    "Table": "Hi"
})

commandslist.append({
    "command": "DeleteTable",
    "Table": "i dont exist"
})

commandslist.append({
    "command": "CreateEntry",
    "Table": "heyyy",
    "Entry": "LeUser",
    "Content": {"FullName": "Henk de steen", "a number": 4, "lesubdict": {"hmmm": "k"}, "lesublist": ["hhhh"]}
})

commandslist.append({
    "command": "CreateEntry",
    "Table": "heyyy",
    "Entry": "LeUser",
    "Content": {"FullName": "hank"}
})

commandslist.append({
    "command": "DeleteEntry",
    "Table": "heyyy",
    "Entry": "LeOtherUser"
})

commandslist.append({
    "command": "DeleteEntry",
    "Table": "heyyy",
    "Entry": "LeOtherUser"
})

commandslist.append({
    "command": "OverwriteEntry",
    "Table": "heyyy",
    "Entry": "LeUser",
    "Content": {"FullName": "hank"}
})

commandslist.append({
    "command": "OverwriteEntry",
    "Table": "heyyy",
    "Entry": "hhhh",
    "Content": {"FullName": "hank"}
})

commandslist.append({
    "command": "ModifyKey",
    "Table": "heyyy",
    "Entry": "LeUser",
    "Key": "FullName",
    "Content": "hank"
})

commandslist.append({
    "command": "ModifyKey",
    "Table": "heyyy",
    "Entry": "LeUser",
    "Key": "i dont exist",
    "Content": "lol"
})

commandslist.append({
    "command": "ReadKey",
    "Table": "heyyy",
    "Entry": "LeUser",
    "Key": "FullName"
})

commandslist.append({
    "command": "ReadKey",
    "Table": "heyyy",
    "Entry": "LeUser",
    "Key": "i dont exist"
})

commandslist.append({
    "command": "MatchKey",
    "Table": "heyyy",
    "Entry": "LeUser",
    "Key": "FullName",
    "Data": "hank"
})

commandslist.append({
    "command": "MatchKey",
    "Table": "heyyy",
    "Entry": "LeUser",
    "Key": "FullName",
    "Data": "Jaap"
})

commandslist.append({
    "Mode": 0,
    "Table": "Hi"
})
print(test.ParseCommands(commandslist))

command = {
    "command": "A test",
    "Table": "some table",
    "Entry": "some entry"
}
requiredargs = [
    "Table",
    "Entry",
    "kebab"
]
# test.CheckIfRequiredArgsGiven(command, requiredargs)

# print(test.Database)
# test.CreateTable("Hi")
# print(test.Database)
# test.CreateEntry("Hi", "There!", {"a": "test"})
# print(test.Database)
# test.DeleteTable("Hi")
# print(test.Database)
# test.SaveDatabase()
# test.CheckIfExists(0, "Hi")
