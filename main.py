# -*- coding: utf-8 -*-
import sys
import requests
import argparse
from pathlib import Path
import re

# input: https://twitter.com/ImReeeK/status/1247980101435822088?s=09

class vidDownload():
    def __init__(self,vid_url):
        video_id = vid_url.split('/')[5].split('?')[0]
        

        def downloader():
            
        