# Internal imports
from configparser import ConfigParser
from time import sleep
from subprocess import run
from os.path import dirname
import sys
#from signal import signal, SIGABRT, SIGFPE, SIGILL, SIGINT, SIGSEGV, SIGTERM, SIGBREAK

# Self made imports
from USB_info import get_USB_Info, PNPDeviceId_main
from reset import reset_config

# make configparser object
config = ConfigParser()
config.read(dirname(__file__)+"\config_data.ini")

#helper to get write acces via window's UAC,not using 
#inno setup for now, so diabled
'''
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

#Ask for admin rights on first run, to add write permission to config file. 
if config['Config'].getboolean('first run'):
    if is_admin():
        # Code to run
        run("PowerShell -Command icacls C:\\'Program Files (x86)'\\'My Program'\\config_data.ini /grant everyone:f")
        config['Config']['first run'] = 'False'
        with open(dirname(__file__)+'\config_data.ini', 'r+') as configfile:
            config.write(configfile)
            configfile.close()
    else:
        # Re-run the program with admin rights
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
'''        

#Create open file object
with open(dirname(__file__)+'\config_data.ini', 'r+') as configfile:
    #'True' program running pointer
    config['Config']['is main running'] = 'True'
    config.write(configfile) #Write to file 

#Disabled for now
'''
#flipping running state, running state is used by Copy.exe, at the exit signal
def change_running_state(*args):
    config['Config']['is main running'] = 'False'
    with open(dirname(__file__)+'\config_data.ini', 'r+') as configfile:
        config.write(configfile)

for sig in (SIGABRT, SIGFPE, SIGILL, SIGINT, SIGSEGV, SIGTERM, SIGBREAK):
    signal(sig, change_running_state)
'''


copy_file_name = "\Copy.exe"



print("Let's See, what do we have here.......  (?_?)")
sleep(1)


# Check if their is already a task scheduled
if not config["Config"].getboolean("backup configured"):
    
    
    #reset everything before begining
    #to prevent weird issues, from any premature termination 
    
    with open(dirname(__file__)+'\config_data.ini', 'w') as reset:
        reset_config(config)
        config.write(reset)

    print("SOOOooo Empty. Let's start the party")
    sleep(1)



    # this function gets PNPDeviceId of USB/s and stores it in a dictionary
    get_USB_Info()
    

    # Store PNPDeviceIs to config file
    for index, id in enumerate(PNPDeviceId_main["PNPDeviceId"]):
        config["USB PID VID"]["DeviceId" + str(index)] = id


    #Ask user, where to store for each device
    print("Tell me, Where to store data")
    sleep(0.7)
    print("Letters:",str(PNPDeviceId_main["Disk Letter"]))
    sleep(0.7)


    #using pid, as it tell us how many devices there are,
    #in need of backing_up, and store it in config file
    for i in range(len(PNPDeviceId_main['PNPDeviceId'])):
        while True:
            u_input = input("Enter the drive Letter, for "+str(i)+"th device: ").upper()+':'
            if u_input in PNPDeviceId_main["Disk Letter"]:
                config['Storage Location']["Device"+str(i)] = u_input
                break
    
    sleep(1)
    _time = input("Time b/w each backup task? Tell me minutes < 1439: ")
    config['duration']['duration'] = str(_time)
        
    # Schedule Backup task
    dir_path = dirname(__file__)+copy_file_name
    
    run(
        "PowerShell -Command schtasks /create /tn USB_backup /sc minute /mo "+config['duration']['duration']+" /tr "+dir_path
    )

    config["Config"] = {"backup configured": 'True', 
                        "task?": 'True',
                        "first run": 'False',
                        "is main running": 'False'}

    with open(dirname(__file__)+'\config_data.ini', 'r+') as configfile:
        config.write(configfile) 
    print("Exiting program in 3 seconds")
    sleep(3)
    sys.exit()


#if task is configured. you can either remove task or reset everything
if config["Config"].getboolean("task?"):
    print("Data is stored and automatic backup is already configured")
    sleep(0.7)
    print("You want to unconfigure automatic backup? or Reset everything?")
    sleep(0.7)
    while True:
        user_input = input("Enter '1' to unconfigure task.\nEnter '2' to Reset everything: ")
        if user_input == '1':
            run(
                "PowerShell -Command schtasks /delete /tn USB_backup"
            )
            with open(dirname(__file__)+'\config_data.ini', 'r+') as configfile:
                config['Config']['task?'] = 'False'
                config["Config"]['is main running'] = 'False'
                config.write(configfile)
            sleep(1.5)
            break

        if user_input == '2':
            print("First, let's try to remove auto backup")
            run(
                "PowerShell -Command schtasks /delete /tn USB_backup"
            )
            with open(dirname(__file__)+'\config_data.ini', 'r+') as configfile:
                config['Config']['backup configured'] = 'False'
                config["Config"]['is main running'] = 'False'
                config.write(configfile)
            print("Everything Succesfully Reseted")
            sleep(1.5)
            break

#if task is not configured. you can either remove task or reset everything
else:
    print("Their is no Backup task configured")
    sleep(0.7)
    print("Want to configure? or Reset everything?")
    sleep(0.7)
    
    while True:
        user_input = input("Enter '1' to configure task.\nEnter '2' to Reset everything: ")
        if user_input == '1':
            # Schedule Backup task
            dir_path = dirname(__file__)+copy_file_name
            run(
                "PowerShell -Command schtasks /create /tn USB_backup /sc minute /mo "+config['duration']['duration']+" /tr "+dir_path
            )
            with open(dirname(__file__)+'\config_data.ini', 'r+') as configfile:
                config['Config']['task?'] = 'True'
                config["Config"]['is main running'] = 'False'
                config.write(configfile)
            sleep(1.5)
            break

        if user_input == '2':
            with open(dirname(__file__)+'\config_data.ini', 'r+') as configfile:
                config['Config']['backup configured'] = 'False'
                config["Config"]['is main running'] = 'False'
                config.write(configfile)

            print("Everything Succesfully Reseted")
            sleep(1.5)
            break