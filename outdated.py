# Usage:
#
# import outdated
# outdated.update()
#
# The function is a shell automation. 
# It checks outdated packages
# in a runtime environment using pip,
# then automaticaly update the found packages
# and returns the result as str.
# Requires pip (of course).

import sys
import subprocess
import ast

def update():
    outdated = ast.literal_eval( subprocess.check_output([
                sys.executable, 
                '-m', 'pip', 'list', '-o', 
                '--format=json']).decode())

    return outdated and subprocess.check_output([
                sys.executable, 
                '-m', 'pip', 'install', '-U',
                *[i['name'] for i in outdated]
                ]
            ) or 'No outdated packages found'

if __name__ == "__main__":
    print (update())
