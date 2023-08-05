# cdx

* Introduction
 * change derectory fast by 'cdx bookmark'.
 
 
* Features
 * bookmark saved for dirpath or url
 * cdx a directory by bookmark fast
 * modify, dispaly, delete bookmarks

### version
    cdx 1.0.1 , Dec 5 2017
 
### setup
    sudo pip install cdx
    
    
### Usage
"""
usage: cdx [option] [arg] ..
Options and arguments:
cdx -s bookmark [dirpath]                # save the CURRENT location or a [dirpath] as bookmark (also --save)
cdx bookmark                              # cdx to a location by bookmark or open url with default web broswer
cdx -l                                        # dispaly the saved bookmarks(also --list)
cdx -m old_bookmark new_bookmark  # modify a bookmark name (also --modify)
cdx -d bookmark                           # delete a bookmark (also --delete)
"""

### Example
    # save the current dirpath as 'py'
    js@py:~/Documents/pycodes$ cdx -s py
    py >>> /home/js/Documents/pycodes
    
    # save a directory path as 'pj'
    js@py:~/Documents/pycodes$ cdx -s pj ./projects/
    pj >>> ./projects/
    
    # save 'google' website as 'gg'
    js@py:~/Documents/pycodes$ cdx -s gg 'http://www.google.com'
    
    # display the bookmarks saved
    js@py:~/Documents/pycodes$ cdx -l
    --------------------------------------------------
    Bookmarks                 Locations 
    --------------------------------------------------
    gg                 http://www.google.com
    pj                 /home/js/Documents/pycodes/projects
    py                 /home/js/Documents/pycodes
    --------------------------------------------------
    
    # modify the bookmark 'gg' to 'g'
    js@py:~/Documents/pycodes$ cdx -m gg g
    Done!
    g >>> http://www.google.com
    
    # save a directory path as 'doc'
    js@py:~/Documents/pycodes$ cdx -s doc /home/js/Documents/
    doc >>> /home/js/Documents/
    
    # use the bookmark 'doc'
    js@py:~/Documents/pycodes$ cdx doc
    js@py:~/Documents$ 


