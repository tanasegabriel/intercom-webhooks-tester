#!/usr/bin/env python3
import os
import sys
import time
from termcolor import colored, cprint

def yesOrNo(question, default="yes"):
  valid = {"yes": True, "y": True, "ye": True,
           "no": False, "n": False}
  if default is None:
    prompt = " [y/n] "
  elif default == "yes":
    prompt = " [Y/n] "
  elif default == "no":
    prompt = " [y/N] "
  else:
    raise ValueError("invalid default answer: '%s'" % default)
  while True:
    sys.stdout.write(question + prompt)
    choice = input().lower()
    if default is not None and choice == '':
      return valid[default]
    elif choice in valid:
      return valid[choice]
    else:
      sys.stdout.write("Please respond with 'yes' or 'no' "

                       "(or 'y' or 'n').\n")

def countdown(t, msg, end_msg):
  while t:
    print(msg + str(t), end='\r')
    time.sleep(1)
    t -= 1
  prints(end_msg, 'standard')

def clear():
  os.system('clear')

def printStats(public_url, webhook_id=False):
  prints('The public URL is: ' + public_url, 'status')
  if webhook_id:
    prints('The webhook ID is: ' + os.environ['webhook_id'], 'status')

def prints(string, type=None):
  s = {'colour': None, 'on_colour': None}
  a = ['bold']

  if type == 'warning':
    s['colour'] = 'red'

  elif type == 'success':
    s['colour'] = 'green'

  elif type == 'standard':
    s['colour'] = 'cyan'

  elif type == 'status':
    s['colour'] = 'yellow'

  elif type == 'important_message':
    s['colour'] = 'white'
    s['on_colour'] = 'on_red'

  elif type == 'new_webhook':
    s['colour'] = 'white'
    s['on_colour'] = 'on_blue'

  cprint(string, s['colour'], s['on_colour'], attrs=a)
