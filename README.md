# CIMAdb
## W.I.P. json database written in python

The detailled instructions will be written, after the code has been completed.

## current commands

+ CurrentTime
+ CheckIfExists
+ CreateTable
+ DeleteTable
+ CreateEntry
+ DeleteEntry
+ OverwriteEntry
+ ModifyKey
+ ReadKey
+ MatchKey
+ SaveDatabase

## ParseCommands

allows you to execute multiple commands at once by giving it a list containing dicts which contain the commands

## CheckIfRequiredArgsGiven:
checks if the commands contain the required arguments
return codes:

-5: Table/Entry/Key Already exists

-4: Table/Entry/Key Doesn't exists

-3: missing command

-2: argument is invalid

-1: missing arguments

0: error that aint really bad

1: command was succesfull
