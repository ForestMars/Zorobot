#! /usr/bin/env python
##
# @Description: Load environment variables using lexical analysis and run app.
# Intended to be invoked canonically with `flask run` (which -oddly- looks for app.py before run.py)
#
import os
import shlex
import subprocess


command = shlex.split("env -i bash -c 'source .env && env'")
proc = subprocess.Popen(command,
    stdout=subprocess.PIPE,
    encoding='utf8',
    universal_newlines=True
    )
for line in proc.stdout:
  (key, _, value) = line.partition("=")
  os.environ[key] = value.strip()
proc.communicate()


# N.B. app.py & run.py are reversed in this example.
# Since we're already in flask run, we run app via python. (It's all back to front, as we say.)
# subprocess.call("python run.py", shell=True)
