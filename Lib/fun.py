"""
This Is Fun Lib
~~~~~~~~~~~~~~~
"""
import os
with open("data/token" , "r") as i:
    token = i.read()
line = "____________________________________________________________________"

def clear():
    if os.path.isfile("../return"):
        os.system("cls")
    else:
        os.system("clear")