A quick helper to make using [Snips.ai]
(https://console.snips.ai) easier.

## Install

```
pip3 install snips_helper
```

The installation instructions below are only necessary if you want to use
snips_helper to download or modify your assistant.  If you only want to use
snips_helper to make parsing intents easier, the browser/driver instructions
can be skipped.

The installation instructions below have been tested on a raspberry pi 3 with
Raspbian Stretch Lite.  For other platforms, install the latest chrome browser
and chromedriver.  See Usage at the end of this document for instructions on
how to use snips_helper.  This has only been tested with python3 and as such is
 listed as a requirement.

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

## Usage (for snips console)

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


## Usage (for parsing intents)

```python
from snips_helper import IntentParser

intent = IntentParser(your_intent_data_from_mqtt_message)

intent_name = intent.name
raw_data = intent.raw_data #this is the data you passed in
parsed_data = intent.parsed_data #this is your parsed data as a json
object
session_id = intent.session_id
custom_data = intent.custom_data #no parsing is done on this (yet)
site_id = intent.site_id
input_text = intent.input_text
probability = intent.probability
slots = intent.slots #this will return an array of SlotParser objects

for slot in slots:
    raw_value = slot.raw_value
    value = slot.value
    name = slot.name
```

