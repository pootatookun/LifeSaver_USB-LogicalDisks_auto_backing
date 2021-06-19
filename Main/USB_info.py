import wmi
from time import sleep

c = wmi.WMI()

PNPDeviceId_main = {"Name": [], "PNPDeviceId": [], "Disk Letter": []}

#Pulling drive letter, using PNPDeviceId
def Drive_letter():
    for PNPDeviceId in PNPDeviceId_main["PNPDeviceId"]:
        for physical_disk in c.Win32_DiskDrive():
            if physical_disk.PNPDeviceId == PNPDeviceId:
                for partition in physical_disk.associators ("Win32_DiskDriveToDiskPartition"):
                    for logical_disk in partition.associators ("Win32_LogicalDiskToPartition"):
                        PNPDeviceId_main["Disk Letter"].append(logical_disk.Caption)

#store letter to prompt user, where to store for each device
#stores prompt letter in disk letter, removes any other letter in it
def prompt_letter():
    length = len(PNPDeviceId_main["Disk Letter"])
    for physical_disk in c.Win32_DiskDrive():
        for partition in physical_disk.associators ("Win32_DiskDriveToDiskPartition"):
            for logical_disk in partition.associators ("Win32_LogicalDiskToPartition"):
                if logical_disk.caption not in PNPDeviceId_main["Disk Letter"]:
                    PNPDeviceId_main["Disk Letter"].insert(0, logical_disk.Caption)
    
    for i in range(length):
        PNPDeviceId_main["Disk Letter"].pop()

def get_USB_Info():

    while True:
        PNPDeviceId = {"PNPDeviceId": []}
        print("Remove the usb drive/s from PC,if already aren't, you want to make backup of")
        input("Press Enter to Continue...")
        sleep(1)

        #Store current PNPDeviceId/s of disks connected.
        for USB_info in c.Win32_DiskDrive():
            PNPDeviceId["PNPDeviceId"].append(USB_info.PNPDeviceID)
        print("All the connected disk drives captured")
        sleep(1)
        print("Now, insert the usb drive/s")
        input("Press Enter to Continue...")
        sleep(1)

        #Checks if their is any change in PNPDeviceIds.If, their is anythin new, add store it
        for USB_info in c.Win32_DiskDrive():
            if USB_info.PNPDeviceId not in PNPDeviceId["PNPDeviceId"]:
                PNPDeviceId_main["PNPDeviceId"].append(USB_info.PNPDeviceID)                
        
        #if no new Disk is added, PNPDeviceId_main["PNPDeviceId"] will be empty.
        #display error message and restart the loop
        if not PNPDeviceId_main["PNPDeviceId"]:
            print("Error: No new mass storage detected  (￣□￣;)")
            sleep(1.5)
            print("                     Are you sure you added one?  (•ิ_•ิ)?")
            sleep(1)            
            print("Anywayssss..")
            sleep(1)
            print("Restarting.................")
            sleep(0.9)
            print('-------------------------------------')
            sleep(0.7)
            print('-------------------------------------')
            sleep(0.5)
            print('----------------------------- (ー_ー)!!')   
            sleep(2)         
            continue
        else:
            #take out drive letters for PNPDeviceId/s
            Drive_letter()
            print('You want to backup',len(PNPDeviceId_main["Disk Letter"]),'usb drive/s?')
            sleep(0.8)
            print('And the drive letter associated is/are',PNPDeviceId_main["Disk Letter"])
            sleep(0.8)
            while True:
                a = input('Enter y to confirm: ')
                if a in 'yY':
                    prompt_letter()
                    return 1
                elif a in 'nN':
                    break
                else:
                    continue
                    



#Just another(Hardcore) way to take out drive letter
'''
#Pulling drive letter, using PNPDeviceId
def Drive_letter():
    
    for PNPDeviceId in PNPDeviceId_main["PNPDeviceId"]:
        for disk_lable in c.Win32_DiskDrive():
            if disk_lable.PNPDeviceId == PNPDeviceId:
                PNPDeviceId_main["Name"].append(disk_lable.Name)
    
    associators = []
    for i in c.Win32_DiskPartition():
        associators.append(i.associators())

    for i in associators:
        ii = str(i)
        if "PHYSICALDRIVE2" in ii:
            disk_name = re.compile('DeviceID="[a-zA-Z]:"').search(ii).group()
            PNPDeviceId_main["Disk Letter"].append(re.compile('[a-zA-Z]:').search(disk_name).group())
'''




