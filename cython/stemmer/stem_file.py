import os
import sys, subprocess

mypath = sys.argv[1]
files = [f for f in os.listdir(mypath) if os.path.isfile(mypath+f)]
for fil in files:
    subprocess.call("./a.out "+mypath+fil+" > "+mypath+"porter/"+fil,shell=True)
