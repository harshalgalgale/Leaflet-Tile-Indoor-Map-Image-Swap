#!/bin/bash
# Will Tanna 11/6/2014

# name.py and runTile.sh
# This script takes the tiles created by GDAL and swaps their names with the runTile.sh script
# The reason this has to be done is because the output of the tiles comes out backwards with
# the command line program to convert images to tiles. Therefore if we have pictures from
# 0 to 15, 15 should actually be 0 and 0 should be 15 when it runs through leaflet. 

# This script can be run independently but it should be run with ./runTile.sh. What they do
# is go through your current dirctory, so ./tiles, goes into the croppedPics directory and goes
# through each of the .png's and make tiles for those images. Once that is done, the next step will occur which is the
# name.py script, where it goes through all the sub directories of thise image tiles and copies
# the file as well as change the name to what it should be within it's current sub directory.
#
# That extra folder that has the same name as the parent is the fixed tile names. Once the script 
# goes through all the directories it then moves that second sub directory (so the second uw1) and 
# moves them to a folder called compiledTiles. We then do one last loop to remove all the folders except for croppedPics and
# compiledTiles!! You can now drop the folders in compiledTiles into your leafet/images folder
# and call that folder in the javascript to load the map with your image tiles!!
#
# Requirements:
# - You will need to have GDAL and GDAL-Python installed. If you on a mac you can
#   brew install GDAL and pip install GDAL-Python within your virtualenv
# - Python 2.7 (But did work on Python 3)

echo "Creating All the tiles in the croppedPics folder"
for i in $(find ./images -type f -name "*.png"); do
	gdal2tiles.py -p raster -z 0-3 -w none $i
done

echo "Swapping the Tiles around to make it work with leaflet"
for i in $(find . -maxdepth 2 -mindepth 2 -type d);  do
	var=$(echo $i | sed 's/.\///')
	python name.py $var 1
done

echo "Moving files into ./croppedPics"
python name.py "." 2

echo "Now let's clean up and get rid of all the extra folders :)"
for i in $(find . -maxdepth 1 -mindepth 1 -type d);  do
if [ "$i" != "./images" ] && [ "$i" != "./compiledTiles" ] && [ "$i" != "./.git" ]; then
	echo "rm -rf $i"
	rm -rf $i
fi
done
