#!/usr/bin/env python3
import os
import sys
import argparse
from modules import setup, prompt, webserver, api_caller

# Setting up the arguments
parser = argparse.ArgumentParser(description='Intercom webhooks tester')
parser.add_argument('-s', '--setup', action="store_true", default=False, help='setup')
parser.add_argument('-p', '--prettify', action="store_true", default=False, help='prettify the JSON payload of the notifications')
options = parser.parse_args()

if options.setup:
  setup.run()
elif not setup.isCompleted():
  prompt.prints('It looks like this needs to be set up! Run with "--setup" to address this.', 'warning')
  sys.exit(1)

prompt.clear()
tunnel = webserver.createTunnel()
prompt.printStats(tunnel, os.environ['webhook_id'])

# update the webhook subscription
api_caller.updateSubscription(tunnel)

# Running ping test
webserver.pingTest()

# Starting normally
prompt.prints("\nWe're live now! You can also check the ngrok webapp at http://localhost:4040\n", 'important_message')
webserver.start(prettify=options.prettify)
