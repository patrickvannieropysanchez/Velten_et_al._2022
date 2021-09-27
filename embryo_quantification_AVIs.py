from ij import IJ, ImagePlus, WindowManager
from ij.io import SaveDialog as sd
from ij.gui import WaitForUserDialog
from ij.plugin import Commands, ContrastEnhancer, WindowOrganizer
from ij.plugin.filter import AVI_Writer
from ij.process import ImageProcessor
import re

chRef = 2 # Set this channel as reference for orientation
chColors = ["Blue", "Green", "Megenta"] # Set the colors for all the channels

wm = WindowManager

for img in wm.getIDList(): # For every image that is open do the following

	imp = wm.getImage(img) # Get the ImagePlus of the image
	nSlices = imp.getNSlices() # Get the amount of slices of the image stack
	imp.setZ(int(nSlices/2)) # Set the stack to the middle
	imp.setC(chRef) # Display the reference channel for orientation (motoneuronal)
	IJ.run(imp, "Grays", "") # Display the reference channel in gray
	IJ.run(imp, "Enhance Contrast", "saturated=0.35"); # Enhance contrast by having 0.35% oversaturated pixels

WindowOrganizer().run("tile") # Tile all the images on the screen for visibility
wd = WaitForUserDialog("Wait for User", "Orient the images as you like now, press 'OK' when done") # Waiting for user input, use image rotation shortcuts to speed up the process
wd.show() # Put the user dialog on top of the screen

path = sd("Where do you want to save the AVI files?", " ", "").getDirectory() # Asks where you want to save the files, leave file name empty
for img in wm.getIDList(): # For every image that is open do the following

	imp = wm.getImage(img) # Get the ImagePlus of the image stack
	title = imp.getTitle() # Get the title of the image
	title = re.sub("/", "_", title) # Replace forward slashes from to title with underscores
	nSlices = imp.getNSlices() # Get the aomunt of slices of the ImageStack
	for color in chColors: # For every color in the color list above, do the following
		c = chColors.index(color)+1 # Get the index of the color for the channel from the chColors list
		imp.setC(c) # Set the channel number
		IJ.run(imp, color, "") # Set the channel color
		IJ.run(imp, "Enhance Contrast", "saturated=0.35"); # Enhance contrast by having 0.35% oversaturated pixels
	imp.setDisplayMode(IJ.COMPOSITE) # Set image as composite
	AVI_Writer().writeImage(imp, path+"/"+title+".avi", AVI_Writer.JPEG_COMPRESSION, 7) # Write .avi to folder specified

# Tip
# Commands().closeAll() # Uncomment this line, or press Shft+W (Mac) to close all open images

print ("Finished")