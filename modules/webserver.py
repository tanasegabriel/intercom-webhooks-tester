#!/usr/bin/env python
import os
import sys
import json
import psutil
import atexit
import logging
import datetime
import threading
import subprocess
from pathlib import Path
from flask import Flask, request, abort
from pygments import highlight, lexers, formatters
from modules import prompt, api_caller, environment

def start(mode=None, setenv=False, prettify=False):
  app = Flask(__name__)
  log = logging.getLogger('werkzeug')
  log.setLevel(logging.ERROR)

  @app.route('/', methods=['POST'])
  def webhook():
    if request.method == 'POST':
      if mode == 'pingTest':
        webhook_id = request.headers['Intercom-Webhook-Subscription-Id']
        if setenv:
          environment.set('webhook_id', webhook_id)
        stop()
        return '', 200

      now = str(datetime.datetime.time(datetime.datetime.now()))
      prompt.prints('\nNew webhook received at ' + now, 'new_webhook')

      if prettify:
        formatted_json = json.dumps(request.get_json(), sort_keys=True, indent=4)
        colourful_json = highlight(formatted_json, lexers.JsonLexer(), formatters.TerminalFormatter())
        print(colourful_json)
      else:
        print(request.get_json())
      return '', 200

    else:
      abort(400)
  app.run()

def stop():
  func = request.environ.get('werkzeug.server.shutdown')
  if func is None:
    raise RuntimeError('Not running with the Werkzeug Server')
  func()

def pingTest():
  thread = threading.Thread(target=start, args=('pingTest',))
  thread.start()

  # allowing the thread to start before triggering ping request
  prompt.countdown(3, 'Issuing ping request in ', 'Issuing request for triggering a ping...')
  api_caller.ping()

  # the thread should finish on its own once the ping is received
  thread.join()

  prompt.prints('The test was successful!', 'success')

def createTunnel():
  # killing other possible instances of ngrok
  for proc in psutil.process_iter():
    if proc.name() == 'ngrok':
      if prompt.yesOrNo("Found another ngrok instance running. Proceed to kill it?"):
        proc.kill()
      else:
        print("No other ngrok instance should be running. Exiting...")
        sys.exit(1)

  # starting a new tunnel
  dir_path = Path(os.path.dirname(os.path.realpath(__file__))).parent
  ngrok = subprocess.Popen([dir_path / "tunnel/ngrok", "start", "--none"], stdout=subprocess.PIPE)
  prompt.countdown(3, 'Tunnel will be up in ', 'Ngrok tunnel created! ')

  @atexit.register  # making sure the tunnel is closed when terminating
  def kill_tunnel():
    ngrok.kill()
  return api_caller.createTunnel()
