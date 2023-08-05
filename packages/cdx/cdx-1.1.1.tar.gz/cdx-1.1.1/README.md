# cdx

* Introduction
 * change derectory fast by 'cdx bookmark'.
 
 
* Features
 * bookmark saved for dirpath or url
 * cdx a directory by bookmark fast
 * modify, dispaly, delete bookmarks

### version
    cdx 1.1.1 , Dec 6 2017
 
### setup
    sudo pip install cdx
    
    
### Usage
"""
usage: cdx [option] [arg] 
Options and arguments:
cdx -s bookmark [dirpath|url|note1 note2 ..] # save the CURRENT dirpath or some notes as bookmark (also --save)
cdx bookmark                                 # cdx to a location or retuan notes by bookmark
cdx -l                                       # dispaly the saved bookmarks(also --list)
cdx -m old_bookmark new_bookmark             # modify a bookmark name (also --modify)
cdx -d bookmark1 bookmark2 ...               # delete a bookmark (also --delete)
"""

### Example
    # save the current dirpath as a bookmark 
    js@machine:~/Documents/pycodes/myprojects$ cdx -s cdx
    cdx cdx >>> /home/js/Documents/pycodes/myprojects
    
    # add a website
    js@machine:~/Documents/pycodes/myprojects$ cdx -s gh https://github.com/ZhangLijuncn/cdx
    notes gh >>> https://github.com/ZhangLijuncn/cdx

    # notes some infomation 
    js@machine:~/Documents/pycodes/myprojects$ cdx -s version v1.1.1 Dec,6,2017
    cdx version >>> v1.1.1 Dec,6,2017

    # mark a dirpath
    js@machine:~/Documents/pycodes/myprojects$ cdx -s doc ~/Documents/
    cdx doc >>> /home/js/Documents/

    # modify a bookmark
    js@machine:~/Documents/pycodes/myprojects$ cdx -m version v
    cdx v >>> v1.1.1 Dec,6,2017

    # display all the bookmarks
    js@machine:~/Documents/pycodes/myprojects$ cdx -l
    ----------------------------------------------------------------------
    Bookmarks          Locations      
    ----------------------------------------------------------------------
    doc                /home/js/Documents
    v                   v1.1.1 Dec,6,2017
    cdx                /home/js/Documents/pycodes/myprojects
    gh                 https://github.com/ZhangLijuncn/cdx
    ----------------------------------------------------------------------

    # change a diretory by bookmark
    js@machine:~/Documents/pycodes/myprojects$ cdx doc
    js@machine:~/Documents$ 

    # open a url in the default web browser
    js@machine:~/Documents$ cdx gh

    # delete some bookmarks
    js@machine:~/Documents$ cdx -d doc v cdx 
    cdx: 'doc' was removed.
    cdx: 'v' was removed.
    cdx: 'cdx' was removed.
    ----------------------------------------------------------------------
    Bookmarks          Locations      
    ----------------------------------------------------------------------
    gh                 https://github.com/ZhangLijuncn/cdx
    ----------------------------------------------------------------------
