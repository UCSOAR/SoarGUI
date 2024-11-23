from flask import Flask, jsonify
from flask_cors import CORS
import os
import platform
system = platform.uname()
print(system)
#local flask server
app = Flask(__name__)

#allowing 'GET'
cors = CORS(app, methods=['GET', 'POST'])

usb_name = "MASTER"

#lists usbs in the path provided in the parameter
def list_files_in_usb(usb_path):
    try:
        # Check if the provided path exists
        if not os.path.exists(usb_path):
            print(f"The path '{usb_path}' does not exist.")
            return

        # List all files and directories in the specified USB path
        for root, dirs, files in os.walk(usb_path):
            for file in files:
                if file == "auth.txt":
                    return file
                else:
                    continue
            else:
                print("file not found")

    except Exception as e:
        print(f"An error occurred: {e}")
   
#This function reads the file at the directory path we gave
def read_file_from_usb(usb_file_path):
    try:
        with open(usb_file_path, 'r') as file:
            content = file.readlines()  # Read all lines into a list
            return [line.strip() for line in content]  # Strip whitespace and return as a list
    except FileNotFoundError:
        print(f"File not found: {usb_file_path}")
        return None  # Return None or an empty list if the file is not found
    except Exception as e:
        print(f"An error occurred: {e}")
        return None  # Return None or an empty list on other exceptions
    
#This function encrypts the text in the usb
def encrypt(text, shift):
    encrypted_list = []   
    for word in text:
        encrypted_text = ""
        for char in word:
            if char.isalpha():
                shift_base = ord('A') if char.isupper() else ord('a')
                encrypted_char = chr((ord(char) - shift_base + shift) % 26 + shift_base)
                encrypted_text += encrypted_char
            else:
                encrypted_text += char
        encrypted_list.append(encrypted_text)
    return encrypted_list

#finds usb for WINDOWS operating systems
def find_specific_usb(volume_label):
    os_type = platform.system()
    
    if os_type == 'Windows':
        # Get all drives
        drives = [f"{chr(d)}:" for d in range(68, 91)]  # D-Z
        print(drives)
        for drive in drives:
            if os.path.exists(drive):
                # Check the volume label
                try:
                    import subprocess
                    label = subprocess.check_output(f'wmic logicaldisk where "DeviceID=\'{drive}\'" get VolumeName', shell=True).decode().strip().split("\n")[1]
                    if label.strip() == volume_label:
                        return drive
                except Exception as e:
                    print(f"Error getting volume label: {e}")
        else:
            print(f'{volume_label} is not found')

    return None
#reads file for WINDOWS operating system
def read_files_from_usb(usb_path):
    try:
        for root, dirs, files in os.walk(usb_path):
            for file in files:
                file_path = os.path.join(root, file)
                if file_path.lower().endswith('.txt'):  # Check for text files
                    print(f"\nReading file: {file_path}")
                    with open(file_path, 'r', encoding='utf-8') as f:
                        file_content = f.readlines() 
                        res =[]
                        for sub in file_content:
                            res.append(sub.replace("\n", ""))
                        return res
    except Exception as e:
        print(f"Error reading files: {e}")

#sends encrypted message to local host
@app.route('/message', methods=['GET']) 
def send():
    #This checks which os is being used by the user and calls the appropriate function
    if system[0] == "Darwin":
        #calls the files listing function
        try:
            usb_drive_path ='/Volumes/'+usb_name
            list_files_in_usb(usb_drive_path)
            usb_file_path = '/Volumes/'+ usb_name +'/' +  list_files_in_usb(usb_drive_path) # Linux/macOS example
            password = read_file_from_usb(usb_file_path)
            key = encrypt(password, 3)
            return jsonify({'permission': key[0], 'email': key[1], 'password': key[2]})
        #checks for type error,usb we searched for was not found       
        except TypeError:
            return jsonify({'message' : "usb drive not found"})
            
    #Checks which us WINDOWS is the os
    elif system[0] == "Windows":  
        usb_drive = find_specific_usb(usb_name)
        print(usb_drive)
        
        if usb_drive:
            password = read_files_from_usb(usb_drive)
            key = encrypt(password, 3)
            print(key)
            return jsonify({'permission': key[0], 'email': key[1], 'password': key[2]})
        else:
            return jsonify({'permission' : "usb drive not found"})
        
    elif system[0] == "Linux":
        try:
            usb_drive_path ='/media/soar/'+usb_name
            list_files_in_usb(usb_drive_path)
            usb_file_path = '/media/soar/'+ usb_name +'/' +  list_files_in_usb(usb_drive_path) # Linux/macOS example
            password = read_file_from_usb(usb_file_path)
            key = encrypt(password, 3)
            return jsonify({'permission': key[0], 'email': key[1], 'password': key[2]})
        #checks for type error,usb we searched for was not found       
        except TypeError:
            return jsonify({'message' : "usb drive not found"})
        
#runs flask server
if __name__ == '__main__':
   app.run()
