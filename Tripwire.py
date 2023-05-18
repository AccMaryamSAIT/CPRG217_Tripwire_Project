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