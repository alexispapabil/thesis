#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import time
import subprocess

def makeqfile():
        p = subprocess.Popen(['python', 'generator.py', '50'])
        time.sleep(5)
        return p
