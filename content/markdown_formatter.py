import os
import re
import sys

print(os.getcwd())

# path of file to modify given as command line argument
try:
    path = sys.argv[1]
except IndexError as e:
    raise Exception("Make sure you specify the path to the file " \
                    "you wish to modify") from e

# check file exists
assert os.path.exists(path), f"No file found at {path}"

# check file is a markdown document
assert path.endswith('.md'), "File must be a markdown document"

# don't try to format post which explains this function
if re.search(r'hexo-and-jupyter', path):
    print("Cannot format this file")
    raise ValueError

with open(path) as f:
    txt = f.read()

# fix syntax highlighting
txt = re.sub(r'```(.+)', r'{% codeblock lang:\1 %}', txt)
txt = re.sub('```', '{% endcodeblock %}', txt)

# add space around tag blocks
txt = re.sub(r'({%((?!end)[ a-z:])*%})', r'\n\1', txt)
txt = re.sub(r'({%[ a-z:]*end[ a-z:]*%})', r'\1\n', txt)

# add space around horizontal rule
txt = re.sub(r'<hr>', r'\n<hr>\n', txt)
txt = re.sub(r'({%[ a-z:]*end[ a-z:]*%})', r'\1\n', txt)

# fix image directories
txt = re.sub(r'\]\((.*)\_files', r'](/images/\1', txt)

# remove default captions
txt = re.sub(r'\!\[(?:png|jpeg|svg)\]', '![]', txt)

# remove options function
txt = re.sub(r'options\((?:(?!\()(?:.|\s))*?\)\s*', '', txt)

# escape underscores in inline math
txt = re.sub(r'(\s\$[^\n\r\$]+)\_([^\n\r\$]+\$)', r'\1\\_\2', txt)

# remove original dataframe styling
txt = re.sub(r"""<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>""", '\r\n', txt)

# extract tables from divs
txt = re.sub(r"""</table>
</div>""", '</table>', txt)

# split document into lines
txt_lines = txt.split('\n')

# escape asterisks in code blocks
#in_codeblock = False
#for i, l in enumerate(txt_lines):
#    if re.match(r'{% codeblock lang:.+ %}', l):
#        in_codeblock = True
#    if re.match(r'{% endcodeblock %}', l):
#        in_codeblock = False
#    if in_codeblock:
#        txt_lines[i] = re.sub('\*', '\*', l)

# escape characters in LaTeX star and bar diagrams
for i, l in enumerate(txt_lines):
    if re.match(r'^\$\$.*\$\$$', l):
        l = re.sub(r'\*', r'\*', l)
        txt_lines[i] = re.sub(r'\\(\_|,)', r'\\\\\\\1', l)

# remove table captions
for i, l in enumerate(txt_lines):
    if re.match(r'<caption>A (tibble|data|matrix)', l):
        txt_lines[i] = ''

# convert tables to datatables
tbl_cnt = 0
new_lines = txt_lines.copy()
for i, l in enumerate(txt_lines):
    if re.match(r'(<table>|<table border="1" class="dataframe">)', l):
        txt_lines[i] = re.sub(r'(<table>|<table border="1" class="dataframe">)',
                              f'<table id="table{tbl_cnt}" class="display">', l)
        txt_lines.insert(i,
                         "<script >$(document).ready( function () {$('" +
                         f"#table{tbl_cnt}" +
                         "').DataTable();} );</script>")
        if tbl_cnt == 0:
            txt_lines.insert(i,
                         '<script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>')
        tbl_cnt += 1

# add custom captions
curr_cap = None
for i, l in enumerate(txt_lines):
    cap_match = re.findall(r'@(?:caption|cap)\=\"(.+)\"', l)
    assert len(cap_match) < 2, f"More than one caption found on line {i}"
    if cap_match:
        curr_cap = cap_match[0]
    elif curr_cap:
        img_match = re.findall(r'\!\[\]', l)
        assert len(img_match) < 2, f"More than one image found on line {i}"
        if img_match:
            txt_lines[i] = l.replace('![]', f'![{curr_cap}]')
            curr_cap = None

# fix LaTeX issues
txt_lines = [re.sub(r'\\\\\s*$', r'\\\\\\\\', l) for l in txt_lines]

# recombine into a single string
txt = '\n'.join(txt_lines)

# remove code for @noecho
txt = re.sub(r'@noecho(?:.|\s)*?{% endcodeblock %}', '', txt)

# overwrite file
with open(path, 'w') as f:
    f.write(txt)
