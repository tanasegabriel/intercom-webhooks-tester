#!/usr/bin/env python3
import os
from pathlib import Path
from dotenv import load_dotenv, set_key, unset_key

env_path = Path('.') / '.env'
if not env_path.is_file():
  env_file = open(str(env_path), 'w+')
  env_file.close()

def load():
  load_dotenv(dotenv_path=env_path, verbose=False)

def set(key, value):
  if os.getenv(key):
    unset_key(str(env_path), key)
  set_key(str(env_path), key, value)
