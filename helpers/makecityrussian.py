#—————————————————————————————————————————————,
# С Д Е Л А Т Ь   Г О Р О Д   Р У С С К И М ! |
#—————————————————————————————————————————————`
#
# BASIC USAGE:
# import makecityrussian
# makecityrussian.now()

import locale
import io
import sys

def set_locale():
    '''Set local env. variables to russian, f.e. days of week for strftime'''
    locale.setlocale(locale.LC_TIME, ('ru_RU', 'UTF-8'))        # Time and date locals
    locale.setlocale(locale.LC_COLLATE, ('ru_RU', 'UTF-8'))     # Sorting strings locals
    locale.setlocale(locale.LC_MESSAGES, ('ru_RU', 'UTF-8'))    # OS messages locals (may not work in different platforms)

def set_utf8():
    '''Fix problems with console I/O at ascii-based environments'''
    sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')
    sys.stdin = sys.stdin.detach()

def now():
    set_locale()
    set_utf8()

if __name__ == "__main__":
    print ('\n'.join([f'{k} : {v}' for k, v in locale.localeconv().items()]))
    now()
    print ('\n'.join([f'{k} : {v}' for k, v in locale.localeconv().items()]))
