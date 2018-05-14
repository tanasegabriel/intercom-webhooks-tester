#!/usr/bin/env python3
import os
import sys
import getpass
import secrets
from modules import cipher, prompt, webserver, environment, api_caller

def isCompleted():
  for item in ['intercom_at', 'webhook_id', 'key']:
    if not os.getenv(item):
      return False
  return True

def run():
  environment.load()
  token = getpass.getpass('Access Token: ')
  if not api_caller.isExtended(token):
    prompt.prints('This token is incorrect or it lacks Extended Scopes!', 'warning')
    sys.exit(1)
  prompt.prints('Access Token check passed!', 'success')

  tunnel = webserver.createTunnel()
  key = secrets.token_urlsafe(32)
  intercom_at = cipher.AESCipher(key=key).encrypt(token)
  prompt.printStats(tunnel)

  for item in ['intercom_at', 'key']:
    environment.set(item, eval(item))

  prompt.prints('Please configure your webhook susbscription and save it', 'standard')
  prompt.prints('\nWaiting to receive ping..', 'important_message')
  webserver.start('pingTest', setenv=True)
  prompt.prints('Setup complete.', 'status')
  sys.exit(0)
