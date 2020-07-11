from GUI import adminPanel
from GUI import mainWindow
from GUI import loadingWindow

from tkinter import Tk

import argparse
import sys


from Model import getfromserver
from Model import hashpasswordInit



parser=argparse.ArgumentParser()
parser.add_argument('-u','--username',help='inserer le username')
parser.add_argument('-p','--password',help='inserer le password')
args=parser.parse_args()


if args.username and args.password:#admin window
    username=hashpasswordInit(args.username)['key']
    password=hashpasswordInit(args.password)['key']
   
    data=getfromserver(username,password)
    
    if data==[]:#username/pass incorrect
        
        print('Error')
        
    else:#redirect
        
        root=Tk()
        adminPanel(root,data)
        root.mainloop()
        
else:#main window
    root=Tk()
    loadingWindow(root)
    root.mainloop()

    root=Tk()
    mainWindow(root)
    root.mainloop()
