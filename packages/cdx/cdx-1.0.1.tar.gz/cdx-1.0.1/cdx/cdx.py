# -*- coding:utf-8 -*-

"cdx --- cd a directory with bookmark."

import os
import sys
import getopt
import shelve
import webbrowser 
import locale

homedir = ''
shell = ''
if 'HOME' in os.environ:
    homedir = os.environ['HOME']
    shell = os.environ['SHELL']
elif 'USERPROFILE' in os.environ:
    homedir = os.environ['USERPROFILE']
    shell = os.environ['COMSPEC']
else:
    print("Home directory was not found.")
    exit(-1)

platform = sys.platform

locale_encoding = locale.getpreferredencoding()



cdxDir = '{}/.cdx'.format(homedir)

if sys.version[0]== '2':
    print(sys.version)
    dbFile = '{}/database'.format(cdxDir).decode(locale_encoding)
if sys.version[0] == '3':
    dbFile = '{}/database'.format(cdxDir)

def init_db():
    if not os.path.exists(cdxDir):
        try:
            os.mkdir(cdxDir)
        except:
            print("cdx: can not create data file.")
            sys.exit(-1)
    else:
        pass

class Cdx(object):
    "cdx"

    def usage(self):
        print("""usage: cdx [option] [arg] ..
Options and arguments:
cdx -s bookmark [dirpath]          # save the CURRENT location or a [dirpath] as bookmark (also --save)
cdx bookmark                       # cdx to a location by bookmark
cdx -l                             # dispaly the saved bookmarks(also --list)
cdx -m old_bookmark new_bookmark   # modify a bookmark name (also --modify)
cdx -d bookmark                    # delete a bookmark (also --delete)""")


    def version(self):
        return 'cdx version 1.0.1 ,  Dec 5 2017'

    def save(self, bookmark, apath=None):
        "save the bookmark"
        self._data = shelve.open(dbFile)
        if not apath:
            self._data[bookmark] = os.path.abspath(os.getcwd())
            self._data.close()
            print('cdx {0} >>> {1}'.format(bookmark,os.getcwd()))
        else:
            if apath.startswith('~'):
                tpath = apath.replace(apath[0],homedir)
                if os.path.exists(tpath):
                    self._data[bookmark] = os.path.abspath(tpath)
                    self._data.close()
                    print('cdx {0} >>> {1}'.format(bookmark,tpath))
            elif os.path.exists(apath):
                self._data[bookmark] = os.path.abspath(apath)
                self._data.close()
                print('cdx {0} >>> {1}'.format(bookmark,apath))
            elif 'http://' or 'https://' in apath:  # url
                self._data[bookmark] =  apath
                self._data.close()
            else:
                print("cdx: no such file or directory: {}".format(apath))


    def list_bookmarks(self):
        "display the paths marked"
        self._data = shelve.open(dbFile)
        print("-"*70)
        print("{:^15}    {:^30}".format("Bookmarks", "Locations"))
        print("-"*70)
        if not self._data:
            print("-"*70)
            print("Empty! use 'cdx -s bookmark [dirpath]' to save a bookmark.")
        for k, v in self._data.items():
            print('{:15}    {}'.format(k, v))
        print("-"*70)
        self._data.close()

    def cdx(self, bookmark):
        "cd to the location path marked"
        self._data = shelve.open(dbFile)

        if bookmark in self._data.keys():
            if not self._data[bookmark].startswith('http'):
                os.chdir(self._data[bookmark])
                self._data.close()
                os.system(shell)
            else:
                webbrowser.open(self._data[bookmark])
                self._data.close()
                if platform == 'linux':
                    os.system(shell) 
        else:
            if os.path.exists(bookmark):
                os.chdir(bookmark)
                self._data.close()
                os.system(shell)
            elif bookmark.startswith('http'):
                webbrowser.open(bookmark)
                self._data.close()
                if platform == 'linux':
                    os.system(shell)
            else:
                self._data.close()
                print("cdx: '{}' is not in the bookmarks or the location does not exist.\
                \nusing 'cdx -s bookmark [dirpath]' to save a bookmark.".format(bookmark))
                Cdx.list_bookmarks(self)
                    


    def modify(self, old_bookmark, new_bookmark):
        "modify bookmarks"
        self._data = shelve.open(dbFile)
        try:
            self._data[new_bookmark] = self._data[old_bookmark]
            del self._data[old_bookmark]
            print("cdx {0} >>> {1}".format(new_bookmark, self._data[new_bookmark]))
            self._data.close()
        except:
            Cdx.list_bookmarks(self)

    def dalete(self, bookmark):
        "delete bookmark"
        self._data = shelve.open(dbFile)
        try:
            del self._data[bookmark]
            self._data.close()
            print("cdx: '{}' bookmark was removed.".format(bookmark))
        except:
            print("Can't find the bookmark '{}' to delete.".format(bookmark))
            Cdx.list_bookmarks(self)

    def truncate(self):
        "clear the data."
        print("Do you want to truncate the datafile?")
        if sys.version[0] == '3':
            warning = input("y or n > ")
        else:
            warning = raw_input("y or n > ")
        if warning == 'y':
            os.remove(dbFile)
            self._data = shelve.open(dbFile)
            self._data.clear()
            self._data.close()
            print("Data is empty.\nUsing 'cdx -s bookmark [dirpath]' to save a bookmark.")
        else:
            sys.exit(0)


def main():
    "get options and arguments from command."
    init_db()
    cdx_go = Cdx()
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hvls:d:m:t", ["help", 'version', 'list',\
        'save=', 'delete=', 'modify=', 'truncate'])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)

    for name, value in opts:
        if name in ("-h", "--help"):
            cdx_go.usage()
            sys.exit(0)
        elif name in ('-s', '--save'):
            if name == '-s':
                if not args:
                    cdx_go.save(value)
                else:
                    for arg in args:
                        cdx_go.save(value, arg)
            if name == '--save':
                if value and not args:
                    cdx_go.save(value)
                elif value and len(args) == 1:
                    print('here')
                    cdx_go.save(value, args[0])
            sys.exit(0)
        elif name in ('-l', '--list'):
            cdx_go.list_bookmarks()
            sys.exit(0)
        elif name in ('-d'):
            cdx_go.dalete(value)
            sys.exit(0)
        elif name in ('-v', '--version'):
            print(cdx_go.version())
            sys.exit(0)
        elif name in ('-m', '--modify'):
            cdx_go.modify(value, args[0])
            sys.exit(0)
        elif name in ('-t','--truncate'):
            cdx_go.truncate()
            sys.exit(0)
        else:
            assert False, "unhandled option"

    if len(args) == 1:
        for x in args:
            cdx_go.cdx(x)
    else:
        # os.chdir(homedir)
        cdx_go.usage()
        cdx_go.list_bookmarks()
        # os.system(shell)



if __name__ == "__main__":
    sys.exit(main())
