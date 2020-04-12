# -*- coding: utf-8 -*-
import sys
import requests
import json
import argparse
from pathlib import Path
import re

class vidDownload():
	def __init__(self, vid_url, session = None):
		video_id = vid_url.split('/')[5].split('?')[0]
		if not session:
			self.session = requests.Session()
		else:
			self.session = session
		
		def get_guest_token(self, id):
			request = self.session.get('https://twitter.com/i/videos/tweet/'+id)
			bearer_file = re.findall('src="(.*js)',request.text) if request.status_code == 200 else False
			headers = {
				'User-agent' : 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0',
				'accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
				'accept-language' : 'es-419,es;q=0.9,es-ES;q=0.8,en;q=0.7,en-GB;q=0.6,en-US;q=0.5'
			}
			if (bearer_file):
				file_content = self.session.get(str(bearer_file[0])).text
				bearer_token_pattern = re.compile('Bearer ([a-zA-Z0-9%-])+')
				bearer_token = bearer_token_pattern.search(file_content)
				bearer_token = bearer_token.group(0)
				headers['authorization'] = bearer_token
				# end bearer
				# start activation
				req2 = self.session.post('https://api.twitter.com/1.1/guest/activate.json',headers=headers)
				headers['x-guest-token'] = json.loads(req2.text)['guest_token']
				return headers

		def downloader(self):
			getid_api = 'https://api.twitter.com/1.1/statuses/show.json?id=' + video_id
			headers = get_guest_token(self, video_id)
			get_url = self.session.get(getid_api, headers=headers)
			get_json =  json.loads(get_url.text)
			media = get_json['extended_entities']['media'][0]
			videos = media['video_info']['variants']
            		bitrate = 0
			for vid in videos:
				if vid['content_type'] == 'video/mp4':
					if vid['bitrate'] > bitrate:
						bitrate = vid['bitrate']
						hq_video_url = vid['url'] 
			return hq_video_url
		self.url = downloader(self)
