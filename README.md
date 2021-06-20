# LifeSaver-USB-LogicalDisks_auto_backup

Note: Windows Only for now

LifeSaver automatically, periodically saves USB flash drive data into the PC. Theoriticaly it will work with any any connected drive ex - Hard Disk ,SSD ... But, can't handle Backing up multipatition drives. I can guess, but cannot be sure of, how it will react to multipartiton system.

I basically made it for my father. Being a boomer and him doing all his work in a flash drive. Many instances arose where his data got corrupt or some other mishap.

This is in alpha release. It's not thoroughly tested, but worked fine in all my testings.
A release is attached to github, you can download it from there.

How it works:-

So, basically it stores PNPDeviceId and stores it in config_file. This makes the backing up independent of drive letters, which tend to change for any connected device, based on how many or at which port they are connected.

Some Precautions:-

* 1.Windows Denfender doesn't seem to like exe created by Pyinstaller. It will mark files as trojan.
* 2.Disable windows defender real time protection before extracting the zip.3
* 3.Put the zip in drivepa/rtition, of which you don't want bakup of, add this folder to Defender's trust list.
* 4.And don't move the extracted folder anywhere else, without unconfiguring the auto backup task using the program.
* 5.Follow the instructions, show by the program.
