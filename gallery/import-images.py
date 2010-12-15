#!/usr/bin/python

import fnmatch
import os

print 'Purging existing images ...'
os.system('sudo rm -f images/*')
os.system('sudo rm -f imagethumbs/*')

rootPath = '/home/rpradeep/Pictures/Photos'
pattern = '*.JPG'

XML = open('gallery.xml', 'w');

XML.write( '<simpleviewerGallery maxImageHeight="1024" maxImageWidth="1024" \
textColor="0xFFFFFF" frameColor="0xffffff" frameWidth="20" stagePadding="40" \
thumbnailColumns="3" thumbnailRows="3" navPosition="left" title="Madeira" \
enableRightClickOpen="true" backgroundImagePath="" thumbPath="thumbs/" \
imagePath="images/" >\n' )


print "Copying new images ..."
for root, dirs, files in os.walk(rootPath):
    for filename in fnmatch.filter(files, pattern):
        if root.endswith('.extra'):
        # ignore images in the .extra directories
            continue
        else:
            # generate thumbnails and links
            absFileName = os.path.join(root, filename)
            print absFileName
            os.system('sudo cp -l ' + absFileName + ' images/' + filename)
            os.system('sudo convert ' + absFileName + ' -resize 5% thumbs/' + filename)
            
            #generate xml content
            XML.write( '<image>\n' )
            XML.write( '    <filename>' + filename + '</filename>\n' )
            XML.write( '</image>\n')

print 'Finished generating gallery.xml'
XML.write( '</simpleviewerGallery>\n' )
