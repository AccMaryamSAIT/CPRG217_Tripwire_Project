"""

PSEUDOCODE HERE 


"""

"""
Authors: Maryam Bunama, Eric Russon, Roman Kapitoulski.
Version: 1.2
Date: May 23, 2023
Program: tripwire.py
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
    filename1 hashvalue
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

import sys # Use the sys module to access arguments passed through the shell
import os # Use the os module for iterating files within a directory and checking if directory passed as an arg exists
import hashlib # Use hashlib module for generating a hash value

### FUNCTIONS

## Function to take read file content and return a hash result
def generateHash(fileContent):
    hash = hashlib.md5(fileContent).hexdigest() # Use hashlib.md5(data).hextdigest() hash algorithm
    return hash

## Function to create the tripwireRecord file
def createTripwireRecord():
    infile = open(recordName, 'w') # Create the record/Overwrite the record for writing. Input to record file is "infile"
    infile.write(os.path.join(currentDir, directory) + '\n') # Write the directory path to the header of the record
    files = os.listdir(directory) # Iterate through the directory to obtain a list of files

    for file in files:
        filePath = os.path.join(currentDir, directory, file) # Returns absolute path of file
        if (filePath) == recordName: # Ignore record file
            continue
    
        elif os.path.isfile(filePath): 
            with open(filePath, 'rb') as f:
                data = f.read()                          
                hash = generateHash(data) # Pass the file's binary data to the generateHash functions
                infile.write(f'{file} {hash}\n') # Write the key/value pair to the record file 

    infile.close()

def invalidArguments():
    print("""\nError. Please follow one of the following formats:
    1. To create a tripwire record enter the following arguments: tripwire.py tripwireDir tripwireRecord c
    2. To evaluate a directory for changes enter the following arguments: tripwire.py tripwireRecord\n""")

def exitProgram():
    print('Exiting program...')
    sys.exit(0)

args = sys.argv # argv is a list of arguments passed to tripwire.py through the shell

# Variables to store values for the directory and record
directory = ''
recordName = ''
procedure = ''

currentDir = os.getcwd() #Returns path where tripwire.py is located. It should be in the same directory as tripwireDir

### 4 arguments to create the record

if len(args) == 4:
   
    directory = args[1]
    recordName = args[2]
    procedure = args[3] 

    ## Validate arguments

    if not os.path.isdir(directory): # Check if directory is valid
        print(f'{directory} is not a directory.')

    if not os.path.exists(directory):
        print(f'{directory} does not exist.')
   
    if procedure != 'c': # Check if the procedure is valid
        invalidArguments()
        exitProgram()
  
    if os.path.exists(recordName): # Check if record already exists
        correctInput = False
        print(f'{recordName} already exists.')
       
        while not correctInput: # Ask the user if they would like to overwrite the existing file
            overwriteRecord = str(input('Do you want to overwrite this file? (Type y to overwrite. Type n to exit): '))
            if overwriteRecord.lower() == 'y':
                correctInput = True
                print('Overwriting the file...')
                createTripwireRecord()

            elif overwriteRecord.lower() == 'n':
                correctInput = True
                exitProgram()
            else:
                print('Please enter a valid response.')

    # At this point in the script arguments should be valid.
    
    infile = open(recordName, 'w') # Create the record/Overwrite the record for writing. Input to record file is "infile"
    infile.write(os.path.join(currentDir, directory) + '\n') # Write the directory path to the header of the record
    files = os.listdir(directory) # Iterate through the directory to obtain a list of files
    
    for file in files:
        createTripwireRecord()

## 2 arguments to compare the directory to the record

elif len(args) == 2: 
    recordName = args[1] # Get the record name

    # Check if record name exists
    if not os.path.exists(recordName):
        print(f'{recordName} does not exist.')
        exitProgram()

    # Create lists to store files that have been modified, added, or removed
    modified = []
    removed = []
    added = []

    # Check the record's file contents for directory location
    outfile = open(recordName, 'r')
    directory = outfile.readline().strip()

    filesInRecord = [] # Create a list to store key/value pairs

    # Append the list that holds key/value pairs
    for line in outfile:
        filesInRecord.append(line.strip())

    # Iterate through the directory and compare the hash values
    files = os.listdir(directory)
    for file in files:
        filepath = os.path.join(currentDir, directory, file) # Returns absolute path of file
      
        if (filepath) == recordName: # Ignore the record file
            continue
     
        contains = False  # Assume that the file isn't in the record
 
        for filename in filesInRecord:  # Loop through the Key/Value pairs in filesInRecord list         
            key, value = filename.split() # Split the Key/Value pair by the space between them.           
            if file == key: ## Check to see if file has been modified               
                contains = True # File is in the record
                with open(filepath, 'rb') as f: # Open file and read its binary data                   
                    hash = generateHash(f.read())               
                    if hash != value: # Compare hash values to see if the file's been modified              
                        modified.append(key) # If modified add the file to the modified list       
       
        if not contains: # Check to see if any files have been added.
            added.append(file)
    
    for filename in filesInRecord: # Loop through the Key/Value pairs in filesInRecord list      
        key, value = filename.split() # Split the Key/Value pair by the space between them.      
        if files.count(key) < 1: # Check to see if file has been removed
            removed.append(key)

    ## Report to console
    print(f'\n{directory}')
    print('\nModified:')
    for file in modified:
        print(f'{file} ')
    print('\nRemoved:')
    for file in removed:
        print(f'{file} ')
    print('\nAdded:')
    for file in added:
        print(f'{file} ')
    print('\n')

else:
    invalidArguments()
    exitProgram()