#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Script per sincronizzare i file di un progetto su chiave USB e
# in via opzionale su macchina remota. La sincronizzazione avviene
# con l'utente configurato nella variabile USERNAME, usando lo stesso
# percorso relativo rispetto alla sua HOME.
#
# Creato: 20141008
#
__author__ = 'brunato'

import os
import re
import sys

### Configurazione ###
USERNAME = 'brunato'
######################

HOME = os.path.expanduser('~%s' % USERNAME)
PROJECT_PATH = os.getcwd()
RSYNC_COMMAND = u'rsync -rlptvd --delete {0} "{1}/" {2}"{3}"'

# Lo script sincronizza solo la directory base in cui viene collocato, per ridurre
# il rischio di cancellazioni accidentati di dati.
if __file__ not in [os.path.basename(__file__), (u'./%s' % os.path.basename(__file__))]:
    print("Lo script di sincronizzazione può essere eseguito solo chiamandolo "
          "dalla sua directory base!")
    sys.exit(1)

# Controlla che il path da sincronizzare appartenga alla home dell'utente.
if not PROJECT_PATH.startswith(HOME):
    print("Si possono sincronizzare solo progetti contenuti in una sottodirectory "
        "della home dell'utente!")
    sys.exit(1)

# Estrae l'argomento opzionale, se non c'è assume che non
# si vuole sincronizzare su host remoto.
try:
    host = sys.argv[1]
except IndexError:
    host = None

df = os.popen('mount -l -t vfat 2>/dev/null', 'r')
df.readline() # skip first line
for line in df.readlines():
    line = line.strip()
    match = re.search(u'\S+\s+on\s+(/run/media/.+)\s+type vfat', line)
    if match is not None:
        usbpath = match.group(1)
        if "USB" in usbpath.upper() or "KINGSTON" in usbpath.upper():
            break
else:
    usbpath = None
df.close()

if usbpath is None and host is None:
    print("Nessuna chiave USB rilevata e nessun nome host in argomento! Esco ...")

if usbpath is not None:
    usbpath += PROJECT_PATH[len(HOME):]
    options = u'--exclude-from=exclude-list.txt'
    command = RSYNC_COMMAND.format(options, PROJECT_PATH, '', usbpath)
    print(u'\n*** Sync to USB Key ***')
    print(u'# %s' % command)
    os.system(command)

if host is not None:
    remote = u'{0}@{1}:'.format(USERNAME, host)
    options = u"--exclude-from=exclude-list.txt -e 'ssh'"
    command = RSYNC_COMMAND.format(options, PROJECT_PATH, remote, PROJECT_PATH[len(HOME)+1:])
    print(u'\n*** Sync to remote host "%s" ***' % host)
    print(u'# %s' % command)
    os.system(command)
