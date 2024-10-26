from roblox import Client
import asyncio
from datetime import datetime
import random
import subprocess
import psutil
import time

async def Log(msg, exception = False):
    if exception:
        print(f"[{datetime.now().strftime("%H:%M:%S")}][EXCEPTION] {msg}")
    else:
        print(f"[{datetime.now().strftime("%H:%M:%S")}][INFO] {msg}")

async def Main():
    cookies = await ReadOrCreateCookiesFile()
    if cookies:
        token = random.choice(cookies)
        client = await Login(token)
        if client:
            target = await GetTarget(client)
            if target:
                timeout = input("Timeout: ")
                await Loop(cookies, target, timeout)

async def ReadOrCreateCookiesFile():
    try:
        with open("cookies.txt") as cookies:
            cookies = cookies.read().splitlines()
        if cookies:
            return cookies
        else:
            await Log(f"The cookies.txt file is empty!", True)
            return None
    except Exception as ex:
        await Log(f"cookies.txt not found! Exception: {ex}", True)
        return None

async def Login(token):
    try:
        client = Client(token)
        user = await client.get_authenticated_user()
        await Log(f"Logged in as {user.name}!")
        return client
    except Exception as ex:
        await Log(f"Invalid .ROBLOSECURITY token! Exception: {ex}", True)
        return None
    
async def GetTarget(client: Client):
    try:
        target = int(input(f"Place id: "))
        place = await client.get_place(target)
        return target
    except Exception as ex:
        await Log(f"Invalid place id! Exception: {ex}", True)
        return None
    
async def Loop(cookies, target, timeout):
    while True:
        try:
            token = random.choice(cookies)
            client = await Login(token)
            if client is not None:
                response = await client.requests.session.post("https://friends.roblox.com/v1/users/1/request-friendship")
                await Log(f"X-csrf-token response headers: {response.headers}")
                client.requests.session.headers["x-csrf-token"] = response.headers["x-csrf-token"]
                response = await client.requests.session.post("https://auth.roblox.com/v1/authentication-ticket", headers={"referer": f"https://www.roblox.com/games/{target}"})
                await Log(f"Xsrf-token response headers: {response.headers}")
                xsrfToken = response.headers["rbx-authentication-ticket"]
                browserId = random.randint(100000, 1000000)
                await LaunchRoblox(xsrfToken, browserId, target)
                await SearchRoblox(timeout)
        except Exception as ex:
            await Log(f"Loop process failed! Exception: {ex}", True)

async def LaunchRoblox(xsrfToken, browserId, target):
    try:
        launchCommand = f"start roblox-player:1+launchmode:play+gameinfo:{xsrfToken}+launchtime:{browserId}+placelauncherurl:https%3A%2F%2Fassetgame.roblox.com%2Fgame%2FPlaceLauncher.ashx:%3Frequest%3DRequestGame%26browserTrackerId%3D{browserId}%26placeId%3D{target}%26isPlayTogetherGame%3Dfalse+browsertrackerid:{browserId}+robloxLocale:en_us+gameLocale:en_us+channel:"
        await Log(f"Launching Roblox! Xsrf-token: {xsrfToken}, browser id: {browserId}, place id: {target}.")
        subprocess.run(launchCommand, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as ex:
        await Log(f"Roblox launch failed! Exception: {ex}", True)

async def SearchRoblox(timeout):
    try:
        found = False
        await Log("Searching Roblox!")
        if not found:
            for process in psutil.process_iter(attrs=["processId", "processName"]):
                if "RobloxPlayerBeta.exe" in process.info["processName"]:
                    found = True
                    await Log(f"Roblox found! Process id: {process.info["processId"]}")
                    break
        if found:
            await Log("Roblox launch completed!")
            time.sleep(timeout)
            await CleanRoblox()
            found = False
    except Exception as ex:
        await Log(f"Roblox search failed! Exception: {ex}", True)

async def CleanRoblox():
    try:
        kill_commands = [
            "taskkill /IM RobloxPlayerLauncher.exe /F",
            "taskkill /IM RobloxPlayerBeta.exe /F",
            "taskkill /IM RobloxStudioLauncherBeta.exe /F"
        ]
        delete_commands = [
            "del /Q %systemdrive%\\Users\\%username%\\AppData\\LocalLow\\rbxcsettings.rbx",
            "del /Q %systemdrive%\\Users\\%username%\\AppData\\Local\\Roblox\\GlobalBasicSettings_13.xml",
            "del /Q %systemdrive%\\Users\\%username%\\AppData\\Local\\Roblox\\RobloxCookies.dat",
            "del /Q %systemdrive%\\Users\\%username%\\AppData\\Local\\Roblox\\frm.cfg",
            "del /Q %systemdrive%\\Users\\%username%\\AppData\\Local\\Roblox\\AnalysticsSettings.xml",
            "del /Q %systemdrive%\\Users\\%username%\\AppData\\Local\\Roblox\\LocalStorage\\*",
            "del /S /Q %systemdrive%\\Users\\%username%\\AppData\\Local\\Roblox\\logs\\*",
            "del /Q %temp%\\RBX-*.log",
            "del /S /Q %systemdrive%\\Windows\\Temp\\*",
            "del /S /Q %systemdrive%\\Users\\%username%\\AppData\\Local\\Microsoft\\CLR_v4.0_32\\UsageLogs\\*",
            "del /S /Q %systemdrive%\\Users\\%username%\\AppData\\Local\\Microsoft\\CLR_v4.0\\UsageLogs\\*"
        ]
        await Log("Start cleaning!")
        await Execute(kill_commands)
        await Execute(delete_commands)
    except Exception as ex:
        await Log(f"Cleaning failed! Exception: {ex}", True)

async def Execute(commands):
    for command in commands:
        try:
            subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception as ex:
            await Log(f"Unable to execute the command! Exception: {ex}", True)

asyncio.get_event_loop().run_until_complete(Main())