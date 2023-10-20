# ========================================================================
# USAGE:
# 1. Open Steam
# 2. Run this program.
# 3. Start Game(s) download.
# 4. Go to bed and let the program do the rest.
# NOTE: THIS SHOULD BE RAN BEFORE QUEUING ANY DOWNLOADS IN ORDER FOR THE PROGRAM TO WORK.
# ========================================================================

import psutil
import time
import os


# Adds number of handles through every iteration. Outside of loop so that index 0 can be called as a baseline.
base_handles = []
# While loop that will run until program is stopped or computer is shutdown.
while 1:
    for proc in psutil.process_iter():
        if proc.name() == "steam.exe": # Find the process with the name "Steam.exe"
            try:
                pinfo = proc.as_dict(attrs=['pid']) # Add a dictionary with the key 'pid' associated with the ID of the steam application.
            except psutil.NoSuchProcess: # If no process itll continue
                pass
            print(pinfo) # Print out the dictionary for debugging

    steamproc = psutil.Process(pinfo['pid']) # Don't need any other keys so the Process ID is taken straight out and placed in variable.
    first_collect = steamproc.num_handles() # Collects number of handles that are running before download for baseline.
    base_handles.append(first_collect) # Adds handles to the base_handles array.

    while steamproc.num_handles() >= base_handles[0] + 50: # While the handles is elevated over the baseline + 50 handles it prints this message. (Download is running)
        print("Still Downloading Please wait!")

    failSafe = 0 # Place holder for number. Failsafe is to allow time for program to be cancelled or another download to start/finish verifying files.
    while steamproc.num_handles() <= base_handles[0] + 20: # While the current handles are less than baseline handles + 20 that means there is no download.
        failSafe += 1 # Add to failsafe number on each iteration.
        time.sleep(1) # Allow for one second each iteration of loop.
        hostname = "google.com" # Defines Hostname for ping
        response = os.system("ping -n 1 " + hostname) # Uses the ping command to see if there is a response from google.
        countdown = 900 - failSafe 
        print("Shutting Down in: {} Seconds.".format(countdown)) # Message giving time left.
        if steamproc.num_handles() >= base_handles[0] + 50: # If new download is detected loop will break and program will restart.
            break
        elif response != 0: # If there is no response from google program stops and will not shutdown computer. Allows for internet to come back and download start back.
            print("Internet Connection Issues!")
            break
        elif failSafe == 900:  # 900 Seconds == 15 Minutes 
            print("Goodnight Sleepy head! Sweet Dreams <3") # Everybody needs a goodnight message.
            os.system("shutdown /s /t 1") # Command to shutdown computer. 
