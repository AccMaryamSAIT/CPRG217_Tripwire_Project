'''
P S E U D O C O D E

This script will allow the user to check if files in a specific 
directory have been edited, removed or added as well as create the 
record file that the directory will be checked against. 

1. Read contents of tripwireDir
    a. check if file exists
    b. if not, print an error

2. Create a hash and file name pair of files in tripwireDir
    a. Create tripwireRecord
    b. Write information to tripwireRecord

3. Write a program that creates a hash of tripwireDir when excecuted
    a. Format it like tripwireRecord
    b. Write information to tripwireDir file

4. Check hash in tripwireRecord against tripwireDir
    a. Start by checking which files exist. 
    b. If no file exists, it's removed
    c. If file exists, check the hash.
    d. If hash changed, the file was edited. 
    f. If a new filename is read, it was added. 

5. Print the changes observed to terminal


C O D E 
'''
#code starts here

import sys # Use the sys module to access arguments passed through the shell
import os # Use the os module for iterating files within a directory and checking if directory passed as an arg exists
import hashlib # Use hashlib module for generating a hash value

"""
Authors: Maryam Bunama, Eric Russon, Roman Kapitoulski.
Version: 1.0
Date: May 23, 2023
Program: Tripwire.py
Description: This script serves two purposes.


First, you may use this program to create a record file for a specified directory which will contain information about
all the files in the directory. This record file will be a text file which will include the folder name chosen, the file
names where each file serves as a key to a hash-value that correlates to the content within the file associated. The
script first records the directory's absolute path as the header of the file. It then reads each of the files' binary
data, then converts this data through a chosen algorithm into a hash value. The files and hash-values are stored as
key/value pairs underneath the directory path.

To utilize the first functionality, in an OS shell and run the command "python tripwire.py tripwireDir tripwireRecord c"
The first word "python" is a command and will tell your OS to run the python program.
The second word "tripwire.py" is an argument for the python program which will then run the script.
The third word "tripwireDir" is an argument which is specified as a path of which directory to create the record in.
The forth word "tripwireRecord" is a second argument for the script which will specify the name of the record to create.
The fifth word "c" is a third argument for the script which tells it to create the record.

The format for the record (assuming there are files) should look like:
directorypath
filename hashvalue
filename2 hashvalue


Second, after a record file is created for a folder, you may run this script with the record as an argument.
This will locate the directory specified in the record, and will perform a scan of the directory's binary data to see
if files have been added, removed, or modified. For files that have been added or removed, the script simply checks
to see if the files in the present directory match with the record. To check if the files have been modified it reads
the file's binary data, runs it through the same algorithm used to create the files. It compares the hash-value
generated to the record's hash-value. Based on the results it will specify if it has been modified or not. Finally,
the script will report to the console specifying the results.

The format for the report to console should look like:
directorypath

Modified:
filename

Removed:
filename

Added:
filename

"""

### Functions

## Create function to read file content and return a hash result
def generateHash(fileContent):
    # Use hashlib.md5(data).hextdigest() hash algorithm
    hash = hashlib.md5(fileContent).hexdigest()
    # Return hash result
    return hash

def invalidArguments():
    print("""\nError. Please follow one of the following formats:
    1. To create a tripwire record enter the following arguments: tripwire.py tripwireDir tripwireRecord c
    2. To evaluate a directory for changes enter the following arguments: tripwire.py tripwireRecord\n""")

def exitProgram():
    print("Exiting program...")
    sys.exit(0)

# argv is a list of arguments passed to tripwire.py through the shell
args = sys.argv

# Variables to store values for the directory and record
directory = ""
recordName = ""
procedure = ""

validDirectory = False
validRecord = False
validProcedure = False

### 4 arguments to create the record
if len(args) == 4:
    directory = args[1]
    recordName = args[2]
    procedure = args[3]

    ## Validate arguments
    # Check if directory is valid
    if not os.path.isdir(directory):
        print(str(directory) + " is not a directory.")

    if not os.path.exists(directory):
        print(str(directory) + " does not exist.")

    # Check if record already exists
    if os.path.exists(recordName):
        correctInput = False
        print(str(recordName) + " already exists.")

        # Ask the user if they would like to overwrite the existing file
        while not correctInput:
            overwriteRecord = str(input("Do you want to overwrite this file? (Type y to overwrite. Type n to exit): "))
            if overwriteRecord.lower() == "y":
                correctInput = True
                print("Overwriting the file...")
            elif overwriteRecord.lower() == "n":
                correctInput = True
                exitProgram()
            else:
                print("Please enter a valid response")

    # Check if the procedure is valid
    if procedure != "c":
        invalidArguments()
        exitProgram()

    ## At this point in the script arguments should be valid.

    # Create the record/Overwrite the record for writing. Input to record file is "infile"
    infile = open(str(recordName), "w")

    # Write the directory path to the header of the record
    infile.write(directory + "\n")

    # Iterate through the directory to obtain a list of files
    files = os.listdir(directory)

    for file in files:
        # Ignore record file
        if (directory + file) == recordName:
            continue
        if os.path.isfile(directory + file):
            print(file + " exists")
            # Open the file
            fileContent = open(directory + file, "rb")
            # Pass the file's binary data to the generateHash function
            hash = generateHash(fileContent.read())
            # Write the key/value pair to the record file
            infile.write(file + " " + hash + "\n")

        fileContent.close()

    infile.close()

### 2 arguments to compare the directory to the record
elif len(args) == 2:
    ## Compare specified directory to record
    # Use the hash function on each file in the directory
    # Compare it with record
    # Specify any changes
    # Report to console
    print("Evaluating a directory...")

else:
    invalidArguments()
    sys.exit(0)
