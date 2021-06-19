#Internal imports
from shutil import  copytree, ignore_patterns, move, rmtree
from configparser import ConfigParser
from time import  localtime, asctime
from os import listdir
from os.path import isdir, dirname
from time import sleep
from sys import exit

#Third party imports
import wmi
from win32file import CreateDirectory
#import pywintypes

#wmi object
c = wmi.WMI()

#Creating config object
config = ConfigParser()
config.read(dirname(__file__)+'\config_data.ini')

#doesn't work, will try something else in future
'''
while config['Config'].getboolean('is main running'):
    sleep(90)
'''
#List to store Drive/s Letter
Drive_letter = []
main_dir = []
dir_name = asctime(localtime())

def directory_helper():    
    i = -1 
    for device, Id in zip(config['Storage Location'], config['USB PID VID']):
        i += 1
        main_dir.append(config['Storage Location'][device][0]+config['USB PID VID'][Id].replace("\\",'!'))

        #check if their is The directory at desired location
        if not isdir(config['Storage Location'][device]+main_dir[i]): #if not create one here, and move to desired location
            try:
                CreateDirectory(main_dir[i],None)
            except:
                pass
            
            sleep(0.1)
            try:
                move(main_dir[i],config['Storage Location'][device])
            except:
                pass
        else:
            dir = listdir(config['Storage Location'][device]+main_dir[i])
            if len(dir) > 10:
                dir.sort(reverse=True)
                for i in range(len(dir)-10):
                    rmtree(
                    config['Storage Location'][device]+main_dir[i]+'\\'+dir.pop()
                    )
            
def extracting_src_dst():
    for device_id in config['USB PID VID']:
        for physical_disk in c.Win32_DiskDrive():
            if physical_disk.PNPDeviceId == config['USB PID VID'][device_id]:
                for partition in physical_disk.associators ("Win32_DiskDriveToDiskPartition"):
                    for logical_disk in partition.associators ("Win32_LogicalDiskToPartition"):
                        Drive_letter.append(logical_disk.Caption)                   

def copy_(src, dest):
    copytree(src=src, dst=dest, ignore=ignore_patterns("System Volume Information"))
    

if __name__ == '__main__':

    try:
        directory_helper()
    except:
        pass
    extracting_src_dst()

    for index,letter,dst in zip(range(len(Drive_letter)), Drive_letter, config['Storage Location']):
        copy_(letter,config['Storage Location'][dst]+main_dir[index]+'\\'+dir_name.replace(':','.'))
