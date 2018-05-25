#!/usr/bin/env python3
import os
import sys
import json
import requests
from modules import environment, prompt, cipher

try:
  environment.load()
  webhook_id = os.environ['webhook_id']
  sub_endpoint = 'https://api.intercom.io/subscriptions/'
  token = cipher.AESCipher(key=os.environ['key']).decrypt(os.environ['intercom_at'])
  headers = {'Accept': 'application/json', 'Authorization': 'Bearer ' + token}
except Exception as e:
  pass

def createTunnel():
  data = json.dumps({'addr': 5000, 'proto': 'http', 'name': 'webooks_tester'})
  headers = {'Content-Type': 'application/json'}
  r = requests.post('http://localhost:4040/api/tunnels', data=data, headers=headers)
  return r.json()['public_url']

def updateSubscription(url):
  try:
    # grabbing the current topics for updating the subscription
    r = requests.get(sub_endpoint + webhook_id, headers=headers).json()
    # updating the subscription with the new url
    r = requests.post(sub_endpoint + webhook_id, data=json.dumps({'topics': r['topics'], 'metadata': r['metadata'], 'url': url}), headers=headers)
    if r.status_code != 200:
      raise Exception
  except Exception as e:
    prompt.prints('An error occurred while updating the subscription', 'warning')
    prompt.prints('Check your Access Token and your webhook ID. Running setup again might fix this!', 'status')
    sys.exit(1)

def isExtended(token):
  headers = {'Accept': 'application/json', 'Authorization': 'Bearer ' + token}
  r = requests.get('https://api.intercom.io/admins', headers=headers)
  if r.status_code != 200:
    return False
  return True

def ping():
  requests.post(sub_endpoint + webhook_id + '/ping', headers=headers)
