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

import datetime, os, re, sqlite3, time, urllib
from Tkinter import Tk

r = Tk()

path = os.path.expanduser('~/My Documents/DayZ')
user = urllib.quote(os.environ.get('USERNAME')).replace('.', '%2e')
profile = '%s/%s.DayZProfile' % (path, user)

addressPattern = re.compile('^\s*lastMPServer\s*=\s*"([\d\.]+):(\d+)"\s*;?\s*$')
namePattern = re.compile('^\s*lastMPServerName\s*=\s*"(.*)"\s*;?\s*$')

db = sqlite3.connect('dayz-tools.db')

cursor = db.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS server_log (date REAL, name TEXT, address TEXT, port INT, PRIMARY KEY(address, port))')
db.commit()

cursor.execute('SELECT MAX(date) FROM server_log')
t0 = cursor.fetchone()[0] or 0.0

print 'Server history:'
cursor.execute('SELECT * FROM server_log ORDER BY date')
for record in cursor.fetchall():
    date, name, address, port = record
    date = datetime.datetime.fromtimestamp(date)
    print '%s: "%s", %s:%d' % (date, name, address, port)
print ''

def getlastserver(profile):
    name = ''
    address = ''
    port = 0

    with open(profile) as fin:
        for line in fin.xreadlines():
            if line.startswith('lastMPServer='):
                match = addressPattern.match(line)
                if match is not None:
                    address = match.group(1)
                    port = int(match.group(2))
            elif line.startswith('lastMPServerName='):
                match = namePattern.match(line)
                if match is not None:
                    name = match.group(1)

    return (name, address, port)

print 'Monitoring server changes...'
while 1:
    t1 = os.stat(profile).st_mtime
    if t1 > t0:
        t0 = t1
        date = datetime.datetime.fromtimestamp(t0)
        name, address, port = getlastserver(profile)
        print '%s: "%s", %s:%d' % (date, name, address, port)
        cursor.execute('INSERT OR REPLACE INTO server_log VALUES (?,?,?,?)', (t0, name, address, port))
        db.commit()

    time.sleep(1.0)

