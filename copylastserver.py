#
# Copyright (C) 2014 Judge Maygarden (dayz.jmaygarden@safersignup.com)
#
#        DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#                    Version 2, December 2004
#
# Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>
#
# Everyone is permitted to copy and distribute verbatim or modified
# copies of this license document, and changing it is allowed as long
# as the name is changed.
#
#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
#
#  0. You just DO WHAT THE FUCK YOU WANT TO.
#

import os, re, urllib
from Tkinter import Tk

r = Tk()

path = os.path.expanduser('~/My Documents/DayZ')
user = urllib.quote(os.environ.get('USERNAME')).replace('.', '%2e')
profile = '%s/%s.DayZProfile' % (path, user)
pattern = re.compile('^\s*lastMPServer\s*=\s*"([\d\.]+):\d+"\s*;?\s*$')

with open(profile) as fin:
    for line in fin.xreadlines():
        if line.startswith('lastMPServer='):
            match = pattern.match(line)
            if match is not None:
                r.withdraw()
                r.clipboard_clear()
                r.clipboard_append(match.group(1))
                r.destroy()
                break

