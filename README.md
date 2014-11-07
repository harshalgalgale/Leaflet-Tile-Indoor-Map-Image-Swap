Indoor Map Leaflet Tile Name Swap
=======================

A script that takes the python GDAL tiles and swaps them around to work with leafletjs

If you use an app like MapTiler it leaves a watermark, but the images are in the correct order to be used with Leafletjs.

However, if you use the GDAL command line tool to make your tiles they are swapped. For example if you have images from 0-5, 5 should actually be 0, and 0 should actually be 5. But there is no watermark! (At least it did for me)

Therefore this script goes through your folders swaps the names, and puts them all in one folder called "compiledTiles".

I know this works for my data within the images folder. I have done some tests with random image names within the image directory; images with long names, and random characters and so far my regex has worked successfully. If you encounter a problem please let me know!

### Requirements:

On Mac:

```
brew install GDAL
```

Python:

```
pip install GDAL
```

### To Run:

Put images in the images folder

Then type the following in your command line

```
./runTile.sh
```

and all your images will be saved in the /compiledTiles folder with the correct ordering :)


### Constraints:

At the moment this is the GDAL command being un in runTile.sh

```
gdal2tiles.py -p raster -z 0-3 -w none $i
```

-z means zoom, meaning the image that is being processed can only be zoomed from 0 to 3. This is the highest it can go at the moment, because of my lack of wanting to implement a natural sort for the script. This script was intended for indoor maps, so we didn't need to go that deep anyway. But what happens is, when the file names are being swapped it goes

```
cp uw2-2/4/5/1.png uw2-2/4/uw2-2/4/5/8.png
cp uw2-2/4/5/10.png uw2-2/4/uw2-2/4/5/7.png
cp uw2-2/4/5/11.png uw2-2/4/uw2-2/4/5/6.png
cp uw2-2/4/5/12.png uw2-2/4/uw2-2/4/5/5.png
cp uw2-2/4/5/13.png uw2-2/4/uw2-2/4/5/4.png
cp uw2-2/4/5/14.png uw2-2/4/uw2-2/4/5/3.png
cp uw2-2/4/5/15.png uw2-2/4/uw2-2/4/5/2.png
cp uw2-2/4/5/2.png uw2-2/4/uw2-2/4/5/15.png
cp uw2-2/4/5/3.png uw2-2/4/uw2-2/4/5/14.png
cp uw2-2/4/5/4.png uw2-2/4/uw2-2/4/5/13.png
cp uw2-2/4/5/5.png uw2-2/4/uw2-2/4/5/12.png
cp uw2-2/4/5/6.png uw2-2/4/uw2-2/4/5/11.png
cp uw2-2/4/5/7.png uw2-2/4/uw2-2/4/5/10.png
cp uw2-2/4/5/8.png uw2-2/4/uw2-2/4/5/1.png
cp uw2-2/4/5/9.png uw2-2/4/uw2-2/4/5/0.png
```

as you can see it goes 1, 10, 11, not 1, 2, 3 because they are strings. Therefore you can't adjust past 3.