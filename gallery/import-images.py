#!/usr/bin/python

import fnmatch
import os

print 'Purging existing images ...'
os.system('sudo rm -f images/*')
os.system('sudo rm -f imagethumbs/*')

rootPath = '/home/rpradeep/Pictures/Photos'
pattern = '*.JPG'
 
print "Copying new images ...sudo r"
for root, dirs, files in os.walk(rootPath):
    for filename in fnmatch.filter(files, pattern):
        if root.endswith('.extra'):
        # ignore images in the .extra directories
            continue
        else:
            absFileName = os.path.join(root, filename)
            print absFileName
            os.system('sudo convert ' + absFileName + ' -resize 40% images/' + filename)
            os.system('sudo convert ' + absFileName + ' -resize 5% imagethumbs/' + filename)

print 'Done'
