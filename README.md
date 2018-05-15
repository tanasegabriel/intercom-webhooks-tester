# Intercom webhooks tester

A small CLI tool for quickly setting up and testing Intercom webhooks, powered by [ngrok](https://ngrok.com/).

### Installation:
 
1. Download the [latest release](https://github.com/tanasegabriel/intercom-webhooks-tester/releases) and unzip it.
2. Run with the `--setup` argument and provide your access token when prompted. 
3. Grab the public URL and set up [your Intercom webhook subscription](https://app.intercom.com/developers/_/webhooks).

<p align="center">
  <img src="https://user-images.githubusercontent.com/20187768/40028598-b821d618-57d7-11e8-9029-91327a9cdfb6.gif">
</p>

You'll need extended scopes on your token. Once the webhook subscription is set up, the setup process will finish automatically.
From now on, your subscription will get updated with the ngrok public URL everytime the tool is started. 
The subscription's topics can be changed, but if you do delete your subscription or you rotate your Access Token, you'll need to run the setup process again.

The JSON payload of each notification will be printed on your terminal, but you can also use ngrok's built in webgui by accessing `http://localhost:4040`


### Development:
1. Create a folder called `tunnel` in the root of the project. Download the [latest ngrok binary](https://ngrok.com/download) and place it in this folder
2. Run `pip -r install requirements.txt` preferably in a virtualenv and you're good to go!

#### New releases:
1. Run `pyinstaller --onefile tester.py` for packaging. You'll find your binary file in the `dist` directory. 
2. While creating a new zip file for a new release, make sure to include the `tunnel` directory containing the `ngrok` binary file.


### Mentions:
This tool should be used only for testing purposes, so use [your Intercom test app](https://docs.intercom.com/configure-intercom-for-your-product-or-site/create-a-test-version-of-intercom/create-a-test-version-of-intercom) for this. The access token is passed through a cipher for scrambling purposes, but an encrypted version of it will still lay in an `.env` file located right next to the main binary.

The webhooks are not being checked for their hub signature either, as validating if a webhook should be handled or not is outside of the scope of this tool.

Also, Flask's internal web server is used. This tool is not asynchronous nor it provides WSGI.
