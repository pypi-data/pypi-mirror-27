import os
import locale

homedir = ''
shell = ''
if 'HOME' in os.environ:
    homedir = os.environ['HOME']
    shell = os.environ['SHELL']
elif 'USERPROFILE' in os.environ:
    homedir = os.environ['USERPROFILE']
    shell = os.environ['SHELL']
else:
    print("Home directory was not found.")
    exit(-1)


locale_encoding = locale.getpreferredencoding()
