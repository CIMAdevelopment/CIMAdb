# CIMA: Project Database

## W.I.P. json database written in python

The detailled instructions will be written, after the code has been completed.

## To-Do:
+ Rewrite to save table data in Union var instead of dict (will make data easier to access and more like a traditional database)

## Current commands

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

## ParseCommands

Allows you to execute multiple commands at once by giving it a list containing dicts which contain the commands

## CheckIfRequiredArgsGiven:
Checks if the commands contain the required arguments.

## Return codes:

+ -5: Table/Entry/Key Already exists

+ -4: Table/Entry/Key Doesn't exists

+ -3: Missing command

+ -2: Argument is invalid

+ -1: Missing arguments

+ 0: Error that aint really bad

+ 1: Command was succesfull
