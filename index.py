import psutil
import time
import os

base_handles = []
while 1:
    for proc in psutil.process_iter():
        if proc.name() == "steam.exe":
            try:
                pinfo = proc.as_dict(attrs=['pid'])
            except psutil.NoSuchProcess:
                pass
            print(pinfo)

    steamproc = psutil.Process(pinfo['pid'])
    first_collect = steamproc.num_handles()
    base_handles.append(first_collect)

    while steamproc.num_handles() >= base_handles[0] + 50:
        print("Still Downloading Please wait!")

    failSafe = 0
    while steamproc.num_handles() <= base_handles[0] + 20:
        failSafe += 1
        time.sleep(1)
        hostname = "google.com"
        response = os.system("ping -n 1 " + hostname)
        countdown = 900 - failSafe
        print("Shutting Down in: {} Seconds.".format(countdown))
        if steamproc.num_handles() >= base_handles[0] + 50:
            break
        elif response != 0:
            print("Internet Connection Issues!")
            break
        elif failSafe == 900:  # 900 Seconds == 15 Minutes
            os.system("shutdown /s /t 1")
