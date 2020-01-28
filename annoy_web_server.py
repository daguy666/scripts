#!/usr/bin/env python

import requests

URL = '<enter_url_to_annoy>'

headers = {
    'User-Agent': "I_HATE_YOUR_LOG_FILES_-AAAAA__AAAAAA-" * 50
}

r = requests.get(URL, headers=headers)

# THIS SCRIPT IS ANNOYING, I WROTE THIS TO ANNOY A TEAMMATE :) 
# DON'T USE THIS. 
