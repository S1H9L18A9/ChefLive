# print('In eggs')
import os
import pyautogui as pg      #that's our keyboard/mouse controller, pg is alias


def execute(help_select:int = 1):
    # We create an action chain for clicking on stuff. 
    script_name = os.path.basename(__file__).replace('.py','')
    print(f'{script_name}')