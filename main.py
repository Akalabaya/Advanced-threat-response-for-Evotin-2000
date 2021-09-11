""" Program to generate report for a executable for analyse"""

###Importing modules###
import os,pathlib
import time
import subprocess
import time
from subprocess import Popen, PIPE
import pathlib
import shutil
import psutil
###Class for running and controling the sandbox.###
class run_sandbox:
    def __init__(self,sandbox_path):
        self.sandbox_path = '"' + sandbox_path + '"'
    def run(self,filename,wait=""):
            cmd = self.sandbox_path + " /nosbiectrl  /silent  /elevate "+wait+" " + filename
            Popen(cmd)
       
            
    def get_output(self,sandbox_path):
        folder = sandbox_path+"/drive/C/analyse/files/"
        files = os.listdir(folder)
        for file in files:        
            if "network" in file:
                pass
            else:
                if "WinDump" in file:
                    os.remove(folder+file)
                else:
                    shutil.copyfile(folder+file,"analyse/files/"+file)
                    os.remove(folder+file)

folder = 'D:/Users/AKALABAYA PAL/source/repos/Akap Internet Security/Akap Internet Security/bin/Debug/.SND_BOX_LOCALS/Start.exe'
sandbox_folder = "C:/Sandbox/Akalabaya_Pal/DefaultBox/"

sandbox_controller = run_sandbox(folder)

#Creating files for analyse
print("[*] Creating folders for analyse...")
try:
    os.mkdir("analyse/")
    os.mkdir("analyse/files")
    os.mkdir("analyse/network")
    os.mkdir("analyse/psr")
    os.mkdir("analyse/procmon")
except:
    pass
try:
    #Creating folder for an analyse folder
    os.mkdir(sandbox_folder+"drive/C/analyse/")
    os.mkdir(sandbox_folder+"drive/C/analyse/files")
    os.mkdir(sandbox_folder+"drive/C/analyse/network")
except:
    pass


print("[*] Starting windump network...")
sandbox_controller.run("WinDump.exe -w C:/analyse/netwok.log")

print("[*] Starting procmon...")
os.system("start /min Procmon.exe /AcceptEula /Quiet /Minimized /backingfile logs/capture.pml")



sandbox_controller.run("malware/a.exe")
#Sleeping for 10 seconds
time.sleep(15)

print("[*] Terminating Windump...")
sandbox_controller.run('taskkill /IM WinDump.exe /F')

print("[*] Terminating Procmon...")
os.system("Procmon.exe /AcceptEula /Terminate")


time.sleep(5)

print("[*] Saving file as csv...")
os.system("Procmon.exe /AcceptEula /OpenLog logs\capture.pml /SaveAs analyse/procmon/capture.csv")

print("[*] Writing windump log..")
shutil.copy(sandbox_folder+"drive/C/analyse/netwok.log","analyse/network/network.log")


