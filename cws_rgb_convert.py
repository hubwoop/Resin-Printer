#!/usr/bin/python3
#

import zipfile

import sys
import os
import re

def yes_or_no(question):
    while "the answer is invalid":
        reply = str(input(question+' (y/n): ')).lower().strip()
        if reply[0] == 'y':
            return True
        if reply[0] == 'n':
            return False

try:
	infile = sys.argv[1]
except:
	print ("Usage: " + sys.argv[0] + " <inFile>")
	exit(1)

tempdir = infile+ "_temp"

changename = infile.split(".")[0]
print(changename)

# Entpacken
with zipfile.ZipFile(infile, 'r') as zip_ref:
    zip_ref.extractall(tempdir)

# Preview entfernen und Namen ändern
for f in os.listdir(tempdir):
    #print(f)
    filestring = str(f)
    isdeleted = False
    if re.match('preview', f):
    	print("Removing preview image: " + f)
    	os.remove("./"+tempdir+"/"+f)
    	isdeleted = True
    if filestring.endswith('.gcode'):
        print("Renaming G-Code File " + f + " to " + changename + ".gcode")
        try:
            os.rename("./"+tempdir+"/"+f,"./"+tempdir+"/"+ changename + ".gcode")
        except:
        	print("Error renaming file")
    if filestring.endswith('.png') and not isdeleted:
        newpngfile = str(f).replace("slice", changename)
        print("Renaming PNG File " + f + " to " + newpngfile)
        try:
            os.rename("./"+tempdir+"/"+f,"./"+tempdir+"/"+ newpngfile)
        except:
        	print("Error renaming file")        
        #os.rename("./"+tempdir+"/"+f,"./"+tempdir+"/"+ changename + ".gcode")

print("Iteration 1 END")

if yes_or_no("Do RGB Conversion?"):
    # RGB Conversion
    for f in os.listdir(tempdir):
        #print(f)
        filestring = str(f)
        isdeleted = False
        if filestring.endswith('.png'):
            outfile = "./"+tempdir+"/"+f
            infile = "./"+tempdir+"/"+f
            print("RGB-Conversion for image: " + infile + ". Output to: " + outfile)
            os.system("python monoMSLAConvert.py " + infile + " " + outfile)
     

# ZIP erstellen

zip_file = zipfile.ZipFile(changename+".zip", 'w')
for f in os.listdir(tempdir):
    zip_file.write("./"+tempdir+"/"+f,f, compress_type=zipfile.ZIP_DEFLATED)
zip_file.close()

# Remove temp dir
print("Deleting Temp dir: " + tempdir)
for f in os.listdir(tempdir):
    #print(f)
    os.remove("./"+tempdir+"/"+f)

os.rmdir("./"+tempdir)