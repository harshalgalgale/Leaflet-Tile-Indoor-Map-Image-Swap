#!/usr/bin/env python
# Will Tanna 11/6/2014

# name.py and runTile.sh
# This script takes the tiles created by GDAL and swaps their names with the runTile.sh script
# The reason this has to be done is because the output of the tiles comes out backwards with
# the command line program to convert images to tiles. Therefore if we have pictures from
# 0 to 15, 15 should actually be 0 and 0 should be 15 when it runs through leaflet. 

# This script can be run independently but it should be run with ./runTile.sh. What they do
# is go through your current dirctory, so ./tiles, goes into the images directory and goes
# through each of the .png's and make tiles for those images. Once that is done, the next step will occur which is the
# name.py script, where it goes through all the sub directories of thise image tiles and copies
# the file as well as change the name to what it should be within it's current sub directory.
#
# That extra folder that has the same name as the parent is the fixed tile names. Once the script 
# goes through all the directories it then moves that second sub directory (so the second uw1) and 
# moves them to a folder called compiledTiles. We then do one last loop to remove all the folders except for images and
# compiledTiles!! You can now drop the folders in compiledTiles into your leafet/images folder
# and call that folder in the javascript to load the map with your image tiles!!
#
# Requirements:
# - You will need to have GDAL and GDAL-Python installed. If you on a mac you can
# 	brew install GDAL and pip install GDAL-Python within your virtualenv
# - Python 2.7 (But did work on Python 3)

import os
import subprocess
import sys
import time
import re
from subprocess import check_call

# Regex to get the first set of characters in between two forward slashes
# So ./lib-1/0 would just return lib-1
parent = re.compile(r"^(?:\\.|[^/\\])*/((?:\\.|[^/\\])*)")


child = re.compile(r"(./[^/\\]*/[^/]*)")


# Essentially a file. It has the file name and it's directory as well as it's full path
class fileName:
	def __init__(self, dpath, fname, fullPath, childDir):
		self.dpath = dpath
		self.fname = fname
		self.fullPath = fullPath
		self.childDir = childDir
	
	def __repr__(self):
		return 'Full: %r, Dir: %r, child: %r,  FileName: %r' % (self.fullPath, self.dpath, self.childDir, self.fname)
	
	
	def compare(self, fileNameObject):
		if self.dpath == fileNameObject.dpath:
			return True
		else:
			return False

# The main function to swap and copy the files
def copyFiles(dirName):
	# Regex to compare where we are in the file structure
	middlePat = re.compile(r"^(?:\\.|[^/\\])*/((?:\\.|[^/\\])*)/")
	endPat = re.compile(r"^.*\/([^/]*)$")

	# The arrays for the different directories
	zero = []
	one = []
	two = []
	three = []
	four = []
	five = []
	six = []
	seven = []
	eight = []
	nine = []
	ten = []
	eleven = []
	twelve = []
	thirteen = []
	fourteen = []
	fifteen = []

	# One big list of lists
	megaList = [zero, one, two, three, four, five, six, seven, eight, nine, ten, eleven, twelve, thirteen, fourteen, fifteen]

	# Dictionary to call the different arrays
	number = {
		'0': zero,
		'1': one,
		'2': two,
		'3': three,
		'4': four,
		'5': five,
		'6': six,
		'7': seven,
		'8': eight,
		'9': nine,
		'10': ten,
		'11': eleven,
		'12': twelve,
		'13': thirteen,
		'14': fourteen,
		'15': fifteen,}

	# This loops through the directory passed in from the file arguements
	# It looks at the files iwth .png (the image maps) checks if the path of
	# the file matches the directory we are looking in, if so then it appends
	# that child directory number in the array's listed above by looking into
	# the number directionary and appending to that list in the dict.
	for dpath, dnames, fnames in os.walk(dirName):
		for i, fname in enumerate(fnames):
			fullPath = os.path.join(dpath, fname)
			if fname.endswith(".png"):
				if dpath != dirName:
					if endPat.match(dpath):
						childDir = endPat.match(dpath).group(1)
						number[childDir].append(fileName(dpath, fname, fullPath, childDir))


	# Create directories for easier copying for the flask server stuff so it renders properly
	for miniList in megaList:
		for x in miniList:
			# Create a new directory string
			dir =  "%s/%s" % (dirName,x.dpath)
			# if the directory does not exist create it
			if not os.path.exists(dir):
				os.makedirs(dir)
		# Now put the files in that directory!
		for x, y in zip(miniList, miniList[::-1]):
			command =  "cp %s %s/%s" % (x.fullPath, dirName, y.fullPath)
			print(command)
			process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
			output = process.communicate()[0]

# moves the directories with the new files to one location
def moveDir(dirName):
	# This goes through the new file structure with the changes made above
	# It goes through each directory looking for a folder that matches the parent name
	# If it does match then it appends it to a list only once so there are no duplicate
	# folders being moved
	dirList = []
	for dpath, dnames, fnames in os.walk(dirName):
		if len(dnames) != 0 and dnames[0] != 'images' and dnames[0] != 'Library' and dpath != '.':
				if parent.match(dpath):
					newDpath = parent.match(dpath).group(1)
				else:
					print("There was an error")
					sys.exit()
				if newDpath in dnames[-1]:
					# This just gives us the main directory we need to work with
					if child.match(dpath):
						newMvdpath = child.match(dpath).group(1)
					else:
						print("There was an error")
						sys.exit()
					if len(dirList) == 0:
						# If's it's empty, start the list
						dirList.append(newMvdpath)
						# And save the dir we are in, in the 'global' string
					elif newMvdpath not in dirList:
						# If the dir is not in the list put it in there!
						dirList.append(newMvdpath)
					# the dir is already in there so don't put a duplicate in tere

	# Let's make sure that the directory we are putting these into exists:
	folderForTiles = 'compiledTiles'
	if not os.path.exists(folderForTiles):
		os.makedirs(folderForTiles)

	# Once we have a list of the directories we want to move we create a bash move command with the
	# paths in the directory list as well as folder we want to put the other folders into
	for x in dirList:
		# Just grab the important bits like "uw-1-0"
		if parent.match(x):
			dirString = parent.match(x).group(1)
		else:
			print("There was an error")
			sys.exit()
		#print x,dirString
		# Save the full path of where the folder is that, that we want to move
		fullDirPath =  x + "/" + dirString
		# Save a destination for where the folder content will be moved too
		folderCheck = "compiledTiles/%s" % dirString
		# Check to see if the directory we are moving to exists, if not then make one
		if not os.path.exists(folderCheck):
			os.makedirs(folderCheck)
		# Create the move command string with the paths
		mvCommand = "mv %s/* %s" % (fullDirPath, folderCheck)
		# print it to console to the user can see
		print(mvCommand)
		# Check the command to make sure it can be run by shell
		check_call(mvCommand, shell=True)

if __name__ == '__main__':
	# if a 1 is passed as the second argument then copy the files
	if sys.argv[2] == '1':
		copyFiles(sys.argv[1])
	# if a 2 is passed as the second argument then move the directories
	elif sys.argv[2] == '2':
		moveDir(sys.argv[1])
	else:
		# Else just exit the script
		sys.exit()
	
