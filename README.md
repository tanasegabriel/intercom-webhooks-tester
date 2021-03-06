# Intercom webhooks tester

A small CLI tool for quickly setting up and testing Intercom webhooks, powered by [ngrok](https://ngrok.com/).

### Installation:
 
1. Download the [latest release](https://github.com/tanasegabriel/intercom-webhooks-tester/releases) and unzip it.
2. Run with the `--setup` argument and provide your access token when prompted. 
3. Grab the public URL and set up [your Intercom webhook subscription](https://app.intercom.com/developers/_/webhooks).

<p align="center">
  <img src="https://user-images.githubusercontent.com/20187768/40028598-b821d618-57d7-11e8-9029-91327a9cdfb6.gif">
</p>

You'll need extended scopes on your token. Once the webhook subscription is set up, the setup process will finish automatically if you're setting a new subscription. If you're editing an already existing one, make sure to trigger a ping at the end.
From now on, your subscription will get updated with the ngrok public URL everytime the tool is started. 
The subscription's topics can be changed, but if you do delete your subscription or you rotate your Access Token, you'll need to run the setup process again.

The JSON payload of each notification will be printed on your terminal, but you can also use ngrok's built in webgui by accessing `http://localhost:4040`

#### Usage:

```
intercom-webhooks-tester [-h] [-s] [-p]

optional arguments:
  -h, --help      show this help message and exit
  -s, --setup     setup
  -p, --prettify  prettify the JSON payload of the notifications
```


### Development:
1. Create a folder called `tunnel` in the root of the project. Download the [latest ngrok binary](https://ngrok.com/download) and place it in this folder
2. Run `pip -r install requirements.txt` preferably in a virtualenv and you're good to go!

#### New releases:
1. Package the file using `pyinstaller` - you'll find the result of this in the `dist` folder.
2. While creating a new zip file for a new release, make sure to include the `tunnel` directory containing the `ngrok` binary file.

```bash
$ pyinstaller -D -n 'intercom-webooks-tester' tester.py
$ mkdir tunnel && cd tunnel
$ wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-darwin-amd64.zip #downloading ngrok for OS X
$ unzip ngrok-stable-darwin-amd64.zip && rm -rf ngrok-stable-darwin-amd64.zip #unziping and removing the archive
$ cd ../..
$ zip -r intercom-webhooks-tester_v0.2_osx.zip intercom-webooks-tester/ #creating a new zip file to be released
```


### Mentions:
This tool should be used only for testing purposes, so use [your Intercom test app](https://docs.intercom.com/configure-intercom-for-your-product-or-site/create-a-test-version-of-intercom/create-a-test-version-of-intercom) for this. The access token is passed through a cipher for scrambling purposes, but an encrypted version of it will still lay in an `.env` file located right next to the main binary.

The webhooks are not being checked for their hub signature either, as validating if a webhook should be handled or not is outside of the scope of this tool.

Also, Flask's internal web server is used. This tool is not asynchronous nor it provides WSGI.
