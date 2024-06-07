import os
from time import sleep
import subprocess           #so I can send terminal commands
from sys import exit        #exit closes the program at any point, less if-else
import pyautogui as pg      #that's our keyboard/mouse controller, pg is alias
import win32gui
import importlib


def main():
    # help select will be a lever to decide how much help I need
    # Also allow customizing of help. I thought automating the whole game will make it boring
    # More number in help_select, more help given(assuming that level file supports it)
    # Higher number is better
    help_select = int(input('Enter the level of help you want: '))  

    #First we open up the scrcpy append
    window_name = open_scrcpy_window_name()
    print(window_name)
    all_window_names = pg.getAllTitles()
    if window_name not in all_window_names:
        print('Could not find scrcpy, connect to it and restart')
        exit()
    if not switch_to_window(window_name):
        print(f'Could not switch to {window_name}, closing')
        exit()
    level_found = find_level()
    if not (level_found is None):
        module = importlib.import_module(f'levels.{level_found}')   #Dynamically import that level file. 
        if hasattr(module, 'execute'):                              #All level files will have an execute fn
            module.execute(help_select)                             #that we invoke
    input()


def find_level():
    '''This function figures out which level are we on. Each level will have a pause screenshot, 
    that is unique to that level. If it is found, then that name is sent back. The name sent back
    is going to be the exact name of the file for that script. 
    
    Eg. Pause screenshot found in the 
    window is 'eggs.png' then eggs is sent back, and it is assumed eggs.py exists in levels folder
    
    We remove the screenshot from here to work on a file so it is not taken without needing to delete the 
    script file. Yes, scripts have special treatment.'''
    
    return 'eggs' # Lol this is too much work, TODO later


def open_scrcpy_window_name():
    #Why such a big path? Coz I remembered you could be running it in fkning UNIX
    path = os.path.join(os.path.abspath(''),     #Assuming scrcpy will be in that path, convenient. Maybe should
    'scrcpy-win64-v2.4',                       #allow a default path too
    'adb.exe')
    #val = subprocess.check_output(path)
    print(path)
    try:
        # Run adb devices to list connected devices
        result = subprocess.run([path, 'devices'], shell=True, capture_output=True, text=True)
        # Parse the output to extract device names
        device_lines = result.stdout.splitlines()[1:]
        device_names = [line.split()[0] for line in device_lines if line.endswith("device")][0]
        #print(device_names)
        result = subprocess.run([path, '-s', device_names, 'shell', 'getprop', 'ro.product.model'], shell=True, capture_output=True, text=True)
        #print(result.stdout)
        return result.stdout.strip()
    except Exception as e:
        print(f"Error running adb devices: {e}")
        return []


def switch_to_window(window_name_to_look_for):
    found = False
    for i in range(16):
        with pg.hold('alt'):
            pg.press('tab',presses=i,interval=0.8)
        sleep(1)
        if win32gui.GetWindowText (win32gui.GetForegroundWindow()) == window_name_to_look_for:
            found = True
            break
    return found


if __name__=='__main__':
    main()
