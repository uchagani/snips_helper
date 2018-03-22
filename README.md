A quick helper to make re-training and downloading [Snips.ai](https://console.snips.ai) assistants easier using a headless chrome browser.

## Install

```
pip3 install snips_helper
```

The installation instructions below have been tested on a raspberry pi 3 with Raspbian Stretch Lite.  For other platforms, install the latest chrome browser and chromedriver.  See Usage at the end of this document for instructions on how to use snips_helper.  This has only been tested with python3 and as such is listed as a requirement.

## Pre-reqs
```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python3 python3-pip
sudo apt-get install libminizip1 libwebpmux2 libgtk-3-0
pip3 install selenium
```

## Download Chrome and ChromeDriver Packages
```
wget http://security.debian.org/debian-security/pool/updates/main/c/chromium-browser/chromium_63.0.3239.84-1~deb9u1_armhf.deb
wget http://security.debian.org/debian-security/pool/updates/main/c/chromium-browser/chromium-driver_63.0.3239.84-1~deb9u1_armhf.deb
```

## Install Chrome

This will error because of dependencies.  This is okay and will be fixed in the next step.
```
sudo dpkg -i chromium_63.0.3239.84-1~deb9u1_armhf.deb
```

This will install the the necessary dependencies of chromium
```
sudo apt-get install -f
```

## Install ChromeDriver
```
sudo dpkg -i chromium-driver_63.0.3239.84-1~deb9u1_armhf.deb
```

## Usage

```python
from snips_helper import ConsoleHelper

snips_helper = ConsoleHelper(chrome_driver_path='/chromedriver/path', download_dir='/assistant/download/path')

#login to the console and use the last assistant that was loaded
snips_helper.login("your@email.com", "your_p@$$word")

#you can also login to a specific assistant by passing in the assistant name.
#the name is case sensitive because the snips console is case-sensitive
snips_helper.login("your@email.com", "your_p@$$word", 'jarvis')

#or you can manually change your assitant after you login with
snips_helper.change_assistant('jarvis')

#retrain snips assistant
snips_helper.retrain_assistant()

#download snips assistant
#downloading the assistant may take a minute or so.  
snips_helper.download_assistant()
```
