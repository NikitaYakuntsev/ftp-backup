"""
The MIT License (MIT)

Copyright (c) 2016 Nikita Yakuntsev

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import ConfigParser
from common import FTP_SECT_PREF, FTP_HOST, FTP_USER, FTP_PASS, CONF_FILE_PATH, SYNC_FILE_PATH
from common import DIR_SECT_PREF, DIR_MASK, DIR_PATH, DIR_PERIOD_DAYS, DIR_FTP_LIFETIME, DIR_FTP_PATH, DIR_ONLY_CHANGED
import random

config = ConfigParser.RawConfigParser()
if False:
    for i in range(1, 5):
        section = "{} {}".format(FTP_SECT_PREF, i)
        config.add_section(section)
        config.set(section, FTP_HOST, "localhost")
        config.set(section, FTP_USER, "root")
        config.set(section, FTP_PASS, "passwd")


        #for i in range(1, 4):
    section = "{} #{}".format(DIR_SECT_PREF, i)
    config.add_section(section)
    config.set(section, DIR_PATH, "/home/nikitayakuntsev")
    config.set(section, DIR_MASK, "*.*")
    config.set(section, DIR_PERIOD_DAYS, random.randint(1, 14))
    config.set(section, DIR_FTP_LIFETIME, 7)
    config.set(section, DIR_ONLY_CHANGED, False)
    config.set(section, DIR_FTP_PATH, "160314_Test")

with open(CONF_FILE_PATH, 'wb') as conffile:
    config.write(conffile)

with open(SYNC_FILE_PATH, 'wb') as fl:
    fl.write("0")
