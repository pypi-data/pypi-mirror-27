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

colours = {
            'end'        :'\033[0m',
            # 'word'         :'\033[31m',
            'notes'    :'\033[32m',
            'gold'   :'\033[33m',
            'blue' :'\033[34m',
            # 'examples_even':'\033[35m',
        }

cdxDir = '{}/.cdx'.format(homedir)

if sys.version[0]== '2':
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
cdx -s bookmark [dirpath|url|note1 note2 ..] # save the CURRENT dirpath or some notes as bookmark (also --save)
cdx bookmark                                 # cdx to a location or retuan notes by bookmark
cdx -l                                       # dispaly the saved bookmarks(also --list)
cdx -m old_bookmark new_bookmark             # modify a bookmark name (also --modify)
cdx -d bookmark1 bookmark2 ...               # delete a bookmark (also --delete)""")


    def version(self):
        return 'cdx version 1.1.2 ,  Dec 6 2017'

    def save(self, bookmark, apath=None):
        "save the bookmark"
        self._data = shelve.open(dbFile)
        if not apath:
            self._data[bookmark] = os.path.abspath(os.getcwd())
            self._data.close()
            print('cdx {0} >>> {1}'.format(bookmark,os.getcwd()))
        elif len(apath)==1:
            if apath[0].startswith('~'):
                tpath = apath[0].replace(apath[0][0],homedir)
                if os.path.exists(tpath):
                    self._data[bookmark] = os.path.abspath(tpath)
                    self._data.close()
                    print('cdx {0} >>> {1}'.format(bookmark,tpath))
            if os.path.exists(apath[0]):
                self._data[bookmark] = os.path.abspath(apath[0])
                self._data.close()
                print('cdx {0} >>> {1}'.format(bookmark,apath[0]))
            else:
                self._data[bookmark] =  apath[0]
                self._data.close()
                if len(apath[0]) < 46:
                    print("cdx {0} >>> {1}".format(bookmark, apath[0]))
                else:
                    print("cdx {0} >>> {1}...".format(bookmark, apath[0][:46]))
        elif len(apath)>1:
            notes = ' '.join(apath)
            self._data[bookmark] = notes
            self._data.close()
            if len(notes) < 46:
                print("cdx {0} >>> {1}".format(bookmark, notes))
            else:
                print("cdx {0} >>> {1}...".format(bookmark, notes[:46]))


    def list_bookmarks(self):
        "display the paths marked"
        self._data = shelve.open(dbFile)
        print("-"*70)
        print("{:15}    {:15}".format("Bookmarks", "Locations"))
        print("-"*70)
        if not self._data:
            print("-"*70)
            print("Empty bookmark! 'cdx -s bookmark [dirpath]' to save a bookmark.")
        for k, v in self._data.items():
            if platform == 'linux':
                if len(v) <= 45:
                    print('{0}{1:15}{2}    {3}{4}{5}'.format(colours['gold'], k, colours['end'], colours['blue'], v, colours['end']))
                else:
                    print('{0}{1:15}{2}    {3}{4}...{5}'.format(colours['gold'], k, colours['end'], colours['blue'], v[:48], colours['end']))
            else:
                if len(v) <= 45:
                    print('{0:15}    {1}'.format(k, v))
                else:
                    print('{0:15}    {1}...'.format(k, v[48]))
            print("-"*70)
        self._data.close()

    def cdx(self, bookmark):
        "cd to the location path marked"
        self._data = shelve.open(dbFile)

        if bookmark in self._data.keys():
            if not self._data[bookmark].startswith('http'):
                if os.path.exists(self._data[bookmark]):
                    os.chdir(self._data[bookmark])
                    self._data.close()
                    os.system(shell)
                else:
                    print(self._data[bookmark])
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

    def dalete(self, bookmarks):
        "delete bookmark"
        self._data = shelve.open(dbFile)
        for bk in bookmarks:
            if bk in self._data:
                del self._data[bk]
                print("cdx: '{}' was removed.".format(bk))
            else:
                print("cdx: fail to delete '{}'.".format(bk))
        Cdx.list_bookmarks(self)

    def truncate(self):
        "clear the data."
        print("Do you want to truncate the datafile?")
        if sys.version[0] == '3':
            warning = input("y or n ? >  ")
        else:
            warning = raw_input("y or n ? >  ")
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
        opts, args = getopt.getopt(sys.argv[1:], "hvls:dm:t", ["help", 'version', 'list',\
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
                    cdx_go.save(value, args)
            if name == '--save':
                if value and not args:
                    cdx_go.save(value)
                elif value and args:
                    cdx_go.save(value, args)
            sys.exit(0)
        elif name in ('-l', '--list'):
            cdx_go.list_bookmarks()
            sys.exit(0)
        elif name in ('-d'):
            if args:
                    cdx_go.dalete(args)
                    sys.exit(0)
            else:
                print('Enter bookmarks to delete.')
                print('cdx -d bookmark_1 bookmark_2 bookmark_3 ...')
                sys.exit(1)

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
