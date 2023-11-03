import random
import subprocess, sys
import time, datetime
import requests

def log(text):
    timestamp = datetime.datetime.utcfromtimestamp(time.time()).strftime("%H:%M:%S")
    print(f"[{timestamp}] {text}")

if len(sys.argv) > 1:
    gameid = sys.argv[1]
else:
    log("Invalid arguments provided")
    exit()

log(f"Visit botting {gameid}")

try:
    with open("cookies.txt", "r") as cookies:
        cookies = cookies.read().splitlines()
except:
    log("No cookies provided")

def getName():
    try:
        return session.get('https://www.roblox.com/mobileapi/userinfo').json()["UserName"]
    except:
        log("Invalid cookie")
        return

def Clean():
    cmds = ["taskkill /IM RobloxPlayerLauncher.exe /F","taskkill /IM RobloxPlayerBeta.exe /F","taskkill /IM RobloxStudioLauncherBeta.exe /F","del /Q %systemdrive%\\Users\\%username%\\AppData\\LocalLow\\rbxcsettings.rbx","del /Q %systemdrive%\\Users\\%username%\\AppData\\Local\\Roblox\\GlobalBasicSettings_13.xml","del /Q %systemdrive%\\Users\\%username%\\AppData\\Local\\Roblox\\RobloxCookies.dat","del /Q %systemdrive%\\Users\\%username%\\AppData\\Local\\Roblox\\frm.cfg","del /Q %systemdrive%\\Users\\%username%\\AppData\\Local\\Roblox\\AnalysticsSettings.xml","del /Q %systemdrive%\\Users\\%username%\\AppData\\Local\\Roblox\\LocalStorage\\*","del /S /Q %systemdrive%\\Users\\%username%\\AppData\\Local\\Roblox\\logs\\*","del /Q %temp%\\RBX-*.log","del /S /Q %systemdrive%\\Windows\\Temp\\*","del /S /Q %systemdrive%\\Users\\%username%\\AppData\\Local\\Microsoft\\CLR_v4.0_32\\UsageLogs\\*","del /S /Q %systemdrive%\\Users\\%username%\\AppData\\Local\\Microsoft\\CLR_v4.0\\UsageLogs*"]

    for cmd in cmds:
        try:
            subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except:
            pass

    log("Roblox killed and fixed common errors")

while True:
    try:
        cookie = random.choice(cookies)
        with requests.session() as session:
            session.cookies[".ROBLOSECURITY"] = cookie
            session.headers["x-csrf-token"] = session.post("https://friends.roblox.com/v1/users/1/request-friendship").headers["x-csrf-token"]
            xsrf_token = session.post("https://auth.roblox.com/v1/authentication-ticket/", headers={"referer":f"https://www.roblox.com/games/{gameid}"}).headers["rbx-authentication-ticket"]
            browserId = random.randint(1000000, 10000000)
            subprocess.run(f"start roblox-player:1+launchmode:play+gameinfo:{xsrf_token}+launchtime:{browserId}+placelauncherurl:https%3A%2F%2Fassetgame.roblox.com%2Fgame%2FPlaceLauncher.ashx%3Frequest%3DRequestGame%26browserTrackerId%3D{browserId}%26placeId%3D{gameid}%26isPlayTogetherGame%3Dfalse+browsertrackerid:{browserId}+robloxLocale:en_us+gameLocale:en_us+channel:", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            log(f"Succesfully launched Roblox as {getName()}")
            time.sleep(20)
            Clean()
    except:
        log("Error launching Roblox. Invalid cookie?")