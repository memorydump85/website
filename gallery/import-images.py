#!/usr/bin/python

import fnmatch
import os



def importPicture( i, o ) :
    os.system('convert ' + i + ' -auto-orient -resize x550 ' + o)


def makeThumbnail( i, o ) :
    os.system('convert ' + i + ' -auto-orient -resize x80 ' + o)


def generateXMLHeader( XML, title ) :
    XML.write( '<simpleviewerGallery maxImageHeight="550" \
        maxImageWidth="1024" \
        textColor="0xFFFFFF" \
        frameColor="0xffffff" \
        frameWidth="20" \
        stagePadding="40" \
        thumbnailColumns="5" \
        thumbnailRows="1" \
        navPosition="bottom" \
        title="' + title + '" \
        enableRightClickOpen="true" \
        backgroundImagePath="" \
        thumbPath="thumbs/" \
        imagePath="images/" >\n' )


def generateXMLEntry( XML, filename, caption ) :
    XML.write( '<image>\n' )
    XML.write( '\t<filename>' + filename + '</filename>\n' )
    XML.write( '\t<caption>' + caption + \
               '</caption>\n' )
    XML.write( '</image>\n')

def finishXML( XML ) :
    XML.write( '</simpleviewerGallery>\n' )
    
def makeAlbumCover( folder, spread ) :
    os.system(
      'convert -size 150x150 xc:none -background none ' +
              '-fill white -stroke grey60 ' +
              '-draw "rectangle 0,0 152,90" ' + folder + '/thumbs/' + spread[2] +
                    ' -geometry +5+5 -composite -rotate -10 ' +
              '-draw "rectangle 0,0 152,90" ' + folder + '/thumbs/' + spread[1] +
                    ' -geometry +5+5 -composite -rotate -10 ' +
              '-draw "rectangle 0,0 152,90" ' + folder + '/thumbs/' + spread[0] +
                    ' -geometry +5+5 -composite -rotate +5 ' +
              '-trim +repage -background none -flatten ' +
              folder + '/cover.png'
    )
    



#-------------------------------------------------------------------------------
#   Main logic
#-------------------------------------------------------------------------------

#
#   Prepare folders
#

print 'Purging existing images ...'
os.system('rm -rf content/*')
os.system('rm -rf content/*')

#
#   Pull content into folders
#

photoPath = '/home/rpradeep/Pictures/Photos'

print "Copying images ..."
for root, dirs, files in os.walk( photoPath ):
    # albums have a album.meta in them
    if not ('album.meta' in files) :
        continue

    print '\nFound ' + root
    
    # create the directory structure
    print 'importing pictures from ' + os.path.basename( root )
    albumDir = 'content/' + os.path.basename( root )
    
    os.makedirs(albumDir);
    os.makedirs(albumDir + '/images');
    os.makedirs(albumDir + '/thumbs');

    XML = open(albumDir + '/gallery.xml', 'w');

    meta = open(root + '/album.meta', 'r');
    title = meta.readline();
   
    print 'Title: ' + title
    generateXMLHeader( XML, title )
        
    for filename in fnmatch.filter(files, '*.JPG'):
        absFileName = os.path.join(root, filename)
        print absFileName
        
        # import pictures and make thumbs
        importPicture( absFileName, albumDir + '/images/' + filename )
        makeThumbnail( absFileName, albumDir + '/thumbs/' + filename )
        generateXMLEntry( XML, filename,
            os.popen('exiv2 -pc ' + absFileName).read() )

    finishXML( XML );
    XML.close()        
    spread = [meta.readline().strip(), meta.readline().strip(), meta.readline().strip()]
    makeAlbumCover( albumDir, spread)
    meta.close()

