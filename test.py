#!/usr/bin/python

import cgitb; cgitb.enable()
import os
import sys
import inspect

def make_table(header, dictionary):
    return ('''
    <h2>{}</h2>
    <table>
    <tr>
        <th>KEY</th><th>VALUE</th>
    </tr>
    {}
    </table>'''.format(header, 
                    '\n'.join([f'\t<tr>\n\t<td>{k}</td>\n\t<td>{v}</td>\n\t</tr>' for k, v in dictionary.items()]))
    )
    
print('Content-type: text/html\n\n')
print('''<html>
<head>
    <style>
        h1, h2 {font-family: Menlo; margin: 5% 0% 3% 0%; font-weight: normal;}
        table {border: none; font-family: Menlo; font-size: 10pt}
        td {border: 1px solid grey; margin: 0; padding: 10; background-color: #eee; vertical-align: top}
        td:nth-child(odd) {font-weight: bold; background-color: #ffffff;}
    </style>
</head>
<body>''')

print('<h1>HALLOW, IT\'S PYTHON CGI</h1>')

sys_vars = {'version': sys.version.replace('\n', '<br>'),
            'copyrignt': sys.copyright.replace('\n', '<br>'),
            'workdir': sys.exec_prefix,
            'executable': sys.executable,
            'encoding': sys.getdefaultencoding(),
            'filesystem_encoding': sys.getfilesystemencoding(),
            'platform': sys.platform
           }
print (make_table('SYSTEM INFO', sys_vars))

dictionary = dict([n \
                    for n in inspect.getmembers(os.uname()) \
                        if (not n[0].startswith('__') and \
                            not str(n[1]).startswith('<')
                           )
                ])
print (make_table('OS.UNAME', dictionary))
print (make_table('OS.ENVIRON', dict(os.environ)))

print('</body></html>')
