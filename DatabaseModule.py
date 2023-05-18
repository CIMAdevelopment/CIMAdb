import os
import json
import datetime
from pathlib import Path
from typing import Union
from enum import *


class Mode(Enum):
    class ModifyList(Enum):
        """
        1: APPEND \n
        2: REMOVE
        """
        APPEND = 1
        REMOVE = 2
        # REPLACE = 3


class DB:
    def __init__(self, Database, Debug=False, DatabaseMode=0):
        self.DatabasePath = Path("DB") / Database
        self.Debug = Debug
        self.SavePath = Path("DB")
        self.SettingsFile = self.SavePath / "DatabaseSettings.json"

        self.SavePath.mkdir(parents=True, exist_ok=True)

        if not self.SettingsFile.exists():
            self.Settings = {"DBsavemode": DatabaseMode}
            with self.SettingsFile.open("w") as outfile:
                json.dump(self.Settings, outfile)
        else:
            with self.SettingsFile.open("r") as f:
                self.Settings = json.load(f)

        if not self.DatabasePath.is_file():
            self.Database = {}
            with self.DatabasePath.open("w") as outfile:
                json.dump(self.Database, outfile)
        else:
            with self.DatabasePath.open("r") as f:
                self.Database = json.load(f)

    def __str__(self):
        return str(f"Loaded database: {self.DatabasePath}")

    def CurrentTime(self):
        return datetime.datetime.now()

    def CheckIfExists(self, keys: Union[str, list]) -> tuple[int, str]:
        """
        This function checks if a key exists in the dictionary

        :param keys: a list of keys representing the path to the key or a single key
        :type keys: Union[str, list]
        :return: True if the key exists, False otherwise
        :rtype: tuple[int, str]
        """
        FUNC = "CheckIfExists"
        current_dict = self.Database
        all_keys_exist = True
        if isinstance(keys, list):
            for i, key in enumerate(keys[:-1]):
                if isinstance(current_dict, dict) and key in current_dict:
                    current_dict = current_dict[key]
                else:
                    if self.Debug:
                        print(f"[Debug {self.CurrentTime()}]: ({FUNC}) Key {key} does not exist in {current_dict}")
                    all_keys_exist = False
                    break
            if all_keys_exist and keys[-1] in current_dict:
                return 1, "True"
            else:
                if self.Debug:
                    print(f"[Debug {self.CurrentTime()}]: ({FUNC}) Key {keys[-1]} does not exist in {current_dict}")
                return -4, "False"
        else:
            if keys in current_dict:
                return 1, "True"
            else:
                if self.Debug:
                    print(f"[Debug {self.CurrentTime()}]: ({FUNC}) Key {keys} does not exist in {current_dict}")
                return -4, "False"

    def CreateTable(self, Table: str, Type: int = 0) -> int:
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
        :rtype: int
        """
        FUNC = "CreateTable"
        if not self.CheckIfExists(Table)[1] == "Error":
            if self.CheckIfExists(Table)[1] == "False":
                self.Database[Table] = {}
                if self.Debug: print(f"[Debug/Info {self.CurrentTime()}]: ({FUNC}) Table {Table} created in database!")
                return 1
            if self.CheckIfExists(Table)[1] == "True":
                if self.Debug: print(f"[Debug/Info {self.CurrentTime()}]: ({FUNC}) Table {Table} already exists!")
                return -5
        else:
            return self.CheckIfExists(Table)[0]

    def DeleteTable(self, Table: str) -> int:
        """
        This function deletes a table from the database
        :param Table: Table to delete
        :type Table: string
        :return: 1 if successful, 0 otherwise
        :rtype: int
        """
        FUNC = "DeleteTable"
        if not self.CheckIfExists(Table)[1] == "Error":
            if self.CheckIfExists(Table)[1] == "True":
                del self.Database[Table]
                if self.Debug: print(
                    f"[Debug/Info {self.CurrentTime()}]: ({FUNC}) Table {Table} deleted from database!")
                return 1
            if self.CheckIfExists(Table)[1] == "False":
                if self.Debug: print(f"[Debug/Info {self.CurrentTime()}]: ({FUNC}) Table {Table} doesn't exist!")
                return -4
        else:
            return self.CheckIfExists(Table)[0]

    def CreateEntry(self, Table: str, Entry: str, Content: dict) -> int:
        """
        This function adds a new entry to a table
        :param Table: Table to make changes to
        :type Table: str
        :param Entry: Entry to make
        :type Entry: str
        :param Content: Content to add to entry
        :type Content: dict
        :return: 1 if successful, 0 otherwise
        :rtype: int
        """
        FUNC = "CreateEntry"
        if not self.CheckIfExists([Table, Entry])[1] == "Error":
            if self.CheckIfExists([Table, Entry])[1] == "False":
                self.Database[Table][Entry] = Content
                if self.Debug: print(
                    f"[Debug/Info {self.CurrentTime()}]: ({FUNC}) Entry {Entry} added to table {Table}!")
                return 1
            if self.CheckIfExists([Table, Entry])[1] == "True":
                if self.Debug: print(
                    f"[Debug/Error {self.CurrentTime()}]: ({FUNC}) Entry {Entry} already exists in table {Table}!")
                return -5
        else:
            return self.CheckIfExists([Table, Entry])[0]

    def DeleteEntry(self, Table: str, Entry: str) -> int:
        """
        This function removes an entry from a table
        :param Table: Table to make changes to
        :type Table: str
        :param Entry: Entry to make
        :type Entry: str
        :return: 1 if successful, 0 otherwise
        :rtype: int
        """
        FUNC = "DeleteEntry"
        if not self.CheckIfExists([Table, Entry])[1] == "Error":
            if self.CheckIfExists([Table, Entry])[1] == "True":
                del self.Database[Table][Entry]
                if self.Debug: print(
                    f"[Debug/Info {self.CurrentTime()}]: ({FUNC}) Entry {Entry} removed from table {Table}!")
                return 1
            if self.CheckIfExists([Table, Entry])[1] == "False":
                if self.Debug: print(
                    f"[Debug/Error {self.CurrentTime()}]: ({FUNC}) Entry {Entry} doesn't exist in table {Table}!")
                return -4
        else:
            return self.CheckIfExists([Table, Entry])[0]

    def OverwriteEntry(self, Table: str, Entry: str, Content: dict) -> int:
        """
        This function overwrites an entry in a table or creates it
        :param Table: Table to make changes to
        :type Table: string
        :param Entry: Entry to overwrite
        :type Entry: string
        :param Content: Content to add to entry
        :type Content: dict
        :return: 1 if successful, 0 otherwise
        :rtype: int
        """
        FUNC = "OverwriteEntry"
        if not self.CheckIfExists([Table, Entry])[1] == "Error":
            self.Database[Table][Entry] = Content
            if self.Debug: print(
                f"[Debug/Info {self.CurrentTime()}]: ({FUNC}) Entry {Entry} overwritten in table {Table}!")
            return 1
        else:
            return self.CheckIfExists([Table, Entry])[0]

    def ModifyKey(self, Table: str, Entry: str, Key: Union[list, str], Content: any) -> int:
        """
        This function changes the content of a key in the database
        :param Table: Table to make changes to
        :type Table: string
        :param Entry: Entry to make changes to
        :type Entry: string
        :param Key: Key to change, use list if the key is within subkeys
        :type Key: Union[list, str]
        :param Content: Content to put in the key
        :type Content: any
        :return: 1 if successful, 0 otherwise
        :rtype: int
        """
        FUNC = "ModifyKey"
        KeyPath = [Table, Entry] + (Key if isinstance(Key, list) else [Key])
        ledict = self.Database
        if not self.CheckIfExists(KeyPath)[1] == "Error":
            for i, key in enumerate(KeyPath[:-1]):
                ledict = ledict[key]
            ledict[KeyPath[-1]] = Content
            if self.Debug: print(
                f"[Debug/Info {self.CurrentTime()}]: ({FUNC}) Key {Key} from Entry {Entry} overwritten in table {Table}!")
            return 1
        else:
            return self.CheckIfExists([KeyPath])[0]

    def CreateKey(self, Table: str, Entry: str, Key: Union[list, str], Content: any) -> int:
        """
        This function creates a key in the database
        :param Table: Table to make changes to
        :type Table: string
        :param Entry: Entry to make changes to
        :type Entry: string
        :param Key: Key to create, use list if the key is within subkeys
        :type Key: Union[list, str]
        :param Content: Content to put in the key
        :type Content: any
        :return: 1 if successful, 0 otherwise
        :rtype: int
        """
        FUNC = "CreateKey"
        KeyPath = [Table, Entry] + (Key if isinstance(Key, list) else [Key])
        ledict = self.Database
        if not self.CheckIfExists(KeyPath)[1] == "Error":
            if self.CheckIfExists(KeyPath)[1] == "False":
                for i, key in enumerate(KeyPath[:-1]):
                    if isinstance(ledict, dict) and key in ledict:
                        ledict = ledict[key]
                    else:
                        ledict[key] = {}
                        ledict = ledict[key]
                ledict[KeyPath[-1]] = Content
                if self.Debug: print(
                    f"[Debug/Info {self.CurrentTime()}]: ({FUNC}) Created Key {Key} in Entry {Entry} in table {Table}!")
                return 1
            if self.CheckIfExists(KeyPath)[1] == "True":
                if self.Debug: print(
                    f"[Debug/Error {self.CurrentTime()}]: ({FUNC}) Key {Key} already exists in Entry {Entry} from table {Table}!")
                return -5
        else:
            return self.CheckIfExists([KeyPath])[0]

    def ReadKey(self, Table: str, Entry: str, Key: Union[list, str]) -> tuple[int, any]:
        """
        This function reads the content of a key in the database
        :param Table: The table to read
        :type Table: str
        :param Entry: Entry to read
        :type Entry: str
        :param Key: Key to read
        :type Key: str
        :return: 1 if successful, 0 otherwise and the data of the key
        :rtype: tuple[int, any]
        """
        FUNC = "ReadKey"
        KeyPath = [Table, Entry] + (Key if isinstance(Key, list) else [Key])
        ledict = self.Database
        if not self.CheckIfExists(KeyPath)[1] == "Error":
            if self.CheckIfExists(KeyPath)[1] == "True":
                for i, key in enumerate(KeyPath[:-1]):
                    ledict = ledict[key]
                if self.Debug: print(
                    f"[Debug/Info {self.CurrentTime()}]: ({FUNC}) Key {Key} from Entry {Entry} in table {Table} read!")
                return 1, ledict[KeyPath[-1]]
            if self.CheckIfExists(KeyPath)[1] == "False":
                if self.Debug: print(
                    f"[Debug/Error {self.CurrentTime()}]: ({FUNC}) Key {Key} does not exist in Entry {Entry} from table {Table}!")
                return -4, None
        else:
            return self.CheckIfExists(KeyPath)[0], None

    def MatchKey(self, Table: str, Entry: str, Key: Union[list, str], Data: any) -> tuple[int, str]:
        """
        This function checks if the key is the same as the data
        :param Table: The table to read
        :type Table: str
        :param Entry: Entry to read
        :type Entry: str
        :param Key: Key to read
        :type Key: str
        :param Data: Data to match with content of key
        :type Data: any
        :return: 1 if successful, 0 otherwise and whether the key is the same as the data
        :rtype: tuple[int, bool]
        """
        FUNC = "MatchKey"
        KeyPath = [Table, Entry] + (Key if isinstance(Key, list) else [Key])
        ledict = self.Database
        if not self.CheckIfExists(KeyPath)[1] == "Error":
            if self.CheckIfExists(KeyPath)[1] == "True":
                for i, key in enumerate(KeyPath[:-1]):
                    ledict = ledict[key]
                if ledict[KeyPath[-1]] == Data:
                    if self.Debug: print(
                        f"[Debug/Info {self.CurrentTime()}]: ({FUNC}) Matched Key {Key} from Entry {Entry} with Data {Data} in table {Table}!")
                    return 1, "True"
                else:
                    if self.Debug: print(
                        f"[Debug/Info {self.CurrentTime()}]: ({FUNC}) Matched Key {Key} from Entry {Entry} with Data {Data} in table {Table}!")
                    return 1, "False"
            if self.CheckIfExists(KeyPath)[1] == "False":
                if self.Debug: print(
                    f"[Debug/Error {self.CurrentTime()}]: ({FUNC}) Key {Key} does not exist in Entry {Entry} from table {Table}!")
                return -4, "Error"
        else:
            return self.CheckIfExists(KeyPath)[0], "Error"

    def DeleteKey(self, Table: str, Entry: str, Key: Union[list, str]) -> int:
        """
        This function deletes a key from the database
        :param Table: The table to delete the key from
        :type Table: str
        :param Entry: The Entry to delete the key from
        :type Entry: str
        :param Key: Key to delete from the database
        :type Key: str
        :return: 1 if successful, 0 otherwise and the data of the key
        :rtype: int
        """
        FUNC = "DeleteKey"
        KeyPath = [Table, Entry] + (Key if isinstance(Key, list) else [Key])
        ledict = self.Database
        if not self.CheckIfExists(KeyPath)[1] == "Error":
            if self.CheckIfExists(KeyPath)[1] == "True":
                for i, key in enumerate(KeyPath[:-1]):
                    ledict = ledict[key]
                del ledict[KeyPath[-1]]
                if self.Debug: print(
                    f"[Debug/Info {self.CurrentTime()}]: ({FUNC}) Key {Key} from Entry {Entry} in table {Table} deleted!")
                return 1
            if self.CheckIfExists(KeyPath)[1] == "False":
                if self.Debug: print(
                    f"[Debug/Error {self.CurrentTime()}]: ({FUNC}) Key {Key} does not exist in Entry {Entry} from table {Table}!")
                return -4
        else:
            return self.CheckIfExists(KeyPath)[0]

    def ModifyList(self, Table: str, Entry: str, Key: Union[str, list], Data: any, mode: str) -> int:
        """
        This function allows to modify a list within an entry
        :param Table: The table to modify
        :type Table: str
        :param Entry: The entry to modify
        :type Entry: str
        :param Key: The key of the list to modify
        :type Key: Union[str, list]
        :param Data: The Data to add, replace or remove from/to the list
        :type Data: any
        :param mode: The mode of this function (APPEND, REMOVE)
        :type mode: str
        :return:
        :rtype: int
        """
        FUNC = "ModifyList"
        KeyPath = [Table, Entry] + (Key if isinstance(Key, list) else [Key])
        ledict = self.Database
        if not self.CheckIfExists(KeyPath)[1] == "Error":
            if self.CheckIfExists(KeyPath)[1] == "True":
                for i, key in enumerate(KeyPath[:-1]):
                    ledict = ledict[key]
                if isinstance(ledict[KeyPath[-1]], list):
                    if mode == "APPEND":
                        if isinstance(Data, list):
                            ledict[KeyPath[-1]].extend(Data)
                            if self.Debug: print(
                                f"[Debug/Info {self.CurrentTime()}]: ({FUNC}) Added {Data} to list {Key} from Entry {Entry} in table {Table}!")
                            return 1
                        else:
                            ledict[KeyPath[-1]].append(Data)
                            if self.Debug: print(
                                f"[Debug/Info {self.CurrentTime()}]: ({FUNC}) Added {Data} to list {Key} from Entry {Entry} in table {Table}!")
                            return 1

                    if mode == "REMOVE":
                        if isinstance(Data, list):
                            for entry in Data:
                                ledict[KeyPath[-1]].remove(entry)
                            if self.Debug: print(
                                f"[Debug/Info {self.CurrentTime()}]: ({FUNC}) Removed {Data} from list {Key} in Entry {Entry} in table {Table}!")
                            return 1
                        else:
                            ledict[KeyPath[-1]].remove(Data)
                            if self.Debug: print(
                                f"[Debug/Info {self.CurrentTime()}]: ({FUNC}) Removed {Data} from list {Key} in Entry {Entry} in table {Table}!")
                            return 1
        else:
            return self.CheckIfExists([KeyPath])[0]

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
                    if self.CheckIfRequiredArgsGiven(commands, ["Key"]):
                        returncode, data = self.CheckIfExists(commands["Key"])
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


'''
test = DB("testfile.json", True)
# test.Database = {}
print(test.Database)
test.CreateTable("Hi")
print(test.Database)
test.CreateTable("heyyy")
test.CreateEntry("heyyy", "LeOtherUser", {"key": "some text", "Anotherdict": {"hi": "hey"}})

commandslist = [{
    "command": "CurrentTime"
}, {
    "command": "CheckIfExists",
    "Mode": 0,
    "Table": "Hi"
}, {
    "command": "CheckIfExists",
    "Mode": 0,
    "Table": "wut"
}, {
    "command": "CreateTable",
    "Table": "heyyy"
}, {
    "command": "CreateTable",
    "Table": "Hi"
}, {
    "command": "DeleteTable",
    "Table": "Hi"
}, {
    "command": "DeleteTable",
    "Table": "i dont exist"
}, {
    "command": "CreateEntry",
    "Table": "heyyy",
    "Entry": "LeUser",
    "Content": {"FullName": "Henk de steen", "a number": 4, "lesubdict": {"hmmm": "k"}, "lesublist": ["hhhh"]}
}, {
    "command": "CreateEntry",
    "Table": "heyyy",
    "Entry": "LeUser",
    "Content": {"FullName": "hank"}
}, {
    "command": "DeleteEntry",
    "Table": "heyyy",
    "Entry": "LeOtherUser"
}, {
    "command": "DeleteEntry",
    "Table": "heyyy",
    "Entry": "LeOtherUser"
}, {
    "command": "OverwriteEntry",
    "Table": "heyyy",
    "Entry": "LeUser",
    "Content": {"FullName": "hank"}
}, {
    "command": "OverwriteEntry",
    "Table": "heyyy",
    "Entry": "hhhh",
    "Content": {"FullName": "hank"}
}, {
    "command": "ModifyKey",
    "Table": "heyyy",
    "Entry": "LeUser",
    "Key": "FullName",
    "Content": "hank"
}, {
    "command": "ModifyKey",
    "Table": "heyyy",
    "Entry": "LeUser",
    "Key": "i dont exist",
    "Content": "lol"
}, {
    "command": "ReadKey",
    "Table": "heyyy",
    "Entry": "LeUser",
    "Key": "FullName"
}, {
    "command": "ReadKey",
    "Table": "heyyy",
    "Entry": "LeUser",
    "Key": "i dont exist"
}, {
    "command": "MatchKey",
    "Table": "heyyy",
    "Entry": "LeUser",
    "Key": "FullName",
    "Data": "hank"
}, {
    "command": "MatchKey",
    "Table": "heyyy",
    "Entry": "LeUser",
    "Key": "FullName",
    "Data": "Jaap"
}, {
    "Mode": 0,
    "Table": "Hi"
}]

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
'''
