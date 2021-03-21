import os
import re
import sys
import subprocess

# name of post
try:
    name = sys.argv[1]
except IndexError as e:
    raise Exception("Make sure you specify the name of the post " \
                    "you wish to build") from e

# check file exists
assert os.path.exists('content/' + name + '/' + name + '.ipynb'), 'Bad name'


# convert to markdown
p = subprocess.Popen('powershell.exe jupyter nbconvert --to markdown .\\content\\' +
                 name + '\\' + name + '.ipynb',
                 stdout=sys.stdout)
p.communicate()

# format markdown
p = subprocess.Popen(['python.exe',
                '.\\content\\markdown_formatter.py',
                 '.\\content\\' +  name + '\\' + name + '.md'])
p.communicate()

# move file to source
if os.path.exists('.\\source\\_posts\\' + name + '.md'):
    os.remove('.\\source\\_posts\\' + name + '.md')
os.rename('.\\content\\' +  name + '\\' + name + '.md',
          '.\\source\\_posts\\' + name + '.md')

# move images and delete folder
if os.path.exists('.\\source\\images\\' + name):
    for img in os.listdir('.\\source\\images\\' + name):
        if re.match(rf'{name}_\d+_\d+\.\w+', img):
            os.remove('.\\source\\images\\' + name + '\\' + img)
if os.path.exists('.\\content\\' +  name + '\\' + name + '_files'):
    for img in os.listdir('.\\content\\' +  name + '\\' + name + '_files'):
        os.rename('.\\content\\' +  name + '\\' + name + '_files\\' + img,
                  '.\\source\\images\\' + name + '\\' + img)
    os.rmdir('.\\content\\' +  name + '\\' + name + '_files')
