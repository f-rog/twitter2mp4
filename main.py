# -*- coding: utf-8 -*-
import sys
import requests
import json
import argparse
import os.path
import re
import shutil
from datetime import datetime
import logging
from colorama import init,Fore,Style

init() # colorama init

class vidDownload():
	def __init__(self, vid_url, session = None):
		video_id = vid_url.split('/')[5].split('?')[0] if 's?=' in vid_url else vid_url.split('/')[5]
		self.log = {}
		if not session:
			self.session = requests.Session()
		else:
			self.session = session

		def send_request(self,url,type_,headers):
			request = self.session.get(url,headers=headers) if type_ == 'get' else self.session.post(url,headers=headers)
			return request.text if request.status_code == 200 else False
		
		def get_guest_token(self, id):
			headers = {'User-agent' : 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0','accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9','accept-language' : 'es-419,es;q=0.9,es-ES;q=0.8,en;q=0.7,en-GB;q=0.6,en-US;q=0.5'}
			request = send_request(self,'https://twitter.com/i/videos/tweet/'+id,'get',headers)
			if (request):
				bearer_file = re.findall('src="(.*js)',request)
				file_content = send_request(self,str(bearer_file[0]),'get',headers)
				if (file_content):
					bearer_token_pattern = re.compile('Bearer ([a-zA-Z0-9%-])+')
					bearer_token = bearer_token_pattern.search(file_content)
					headers['authorization'] = bearer_token.group(0)
					self.log['bearer'] = bearer_token.group(0)
					req2 = send_request(self,'https://api.twitter.com/1.1/guest/activate.json','post',headers)
					if (req2):
						headers['x-guest-token'] = json.loads(req2)['guest_token']
						self.log['guest_token'] = json.loads(req2)['guest_token']
						return headers
			return False

		def downloader(self):
			headers = get_guest_token(self, video_id)
			self.log['full_headers'] = headers
			if (headers):
				get_url = send_request(self,'https://api.twitter.com/1.1/statuses/show.json?id='+video_id,'get',headers)
				if (get_url): 
					videos = json.loads(get_url)['extended_entities']['media'][0]['video_info']['variants']
					self.log['vid_list'] = videos 
					bitrate = 0
					for vid in videos:
						if vid['content_type'] == 'video/mp4':
							if vid['bitrate'] > bitrate:
								bitrate = vid['bitrate']
								hq_video_url = vid['url'] 
					return hq_video_url
			return False

		self.url = downloader(self)

def pretty_log(logdict):
	fn = 'log_file_twvdl-'+str(datetime.now()).replace(':','-')[:19]+'.txt'
	log_dir = os.path.join('./log/', fn)
	with open(log_dir,'w') as logfile:
		logfile.write('These are the logs for the sequence of requests, if theres an issue, please submit a report with the contents of this file.\n')
		for k,v in logdict.items():
			logfile.write('-*-*-*-*- start of '+k+'-*-*-*-*-\n'+str(v)+'\n-*-*-*-*- end of '+k+'-*-*-*-*-\n')
		print('['+Fore.RED+'+'+Style.RESET_ALL+'] '+'Log saved at /log/'+fn+'\nPlease submit a report with the content of said file.')

def save_file(url,ddir,filename):
	fn = url.split('/')[8].split('?')[0]
	if (filename):
		fn = filname if '.mp4' in filename else filename+'.mp4'
	op_dir = os.path.join(ddir, fn)
	with requests.get(url, stream=True) as r:
		with open(op_dir, 'wb') as f:
			shutil.copyfileobj(r.raw, f)

if sys.version_info[0] <= 2:
	print('['+Fore.RED+'+'+Style.RESET_ALL+'] '+'This script is meant to be used with Python 3 only.')
	sys.exit(1)

parser = argparse.ArgumentParser()
parser.add_argument('url', type=str, help = 'The URL to the video you wanna download (ex. https://twitter.com/bruhmoment/status/1247980101435822088?s=09).')
parser.add_argument('-d', '--dir',type=str, default = './videos/',dest = 'dir',help = 'The directory you wanna save the downloaded video/s to.')
parser.add_argument('-fn', '--filename',type=str, default = False,dest = 'filename',help = 'Custom filename for the downloaded video.')
parser.add_argument('-l', '--link',dest = 'link',default = 0, action = 'count', help = 'Will output a direct URL to the video.')

args = parser.parse_args()

try:
	if re.match(r'https:\/\/twitter.com\/\w{1,15}\/status\/(\d{15,25})',args.url):
		dl = vidDownload(args.url)
		if (dl.url):
			if args.link >= 1:
				print('['+Fore.GREEN+'+'+Style.RESET_ALL+'] '+'Link: '+dl.url)
			else:
				save_file(dl.url,args.dir,args.filename)
				print('['+Fore.GREEN+'+'+Style.RESET_ALL+'] '+'File successfully saved!')
		else:
			print('['+Fore.YELLOW+'+'+Style.RESET_ALL+'] '+'Theres an internal error, hang on...')
			pretty_log(dl.log)
	else:
		sys.exit('['+Fore.RED+'+'+Style.RESET_ALL+'] '+"Invalid URL format, example: https://twitter.com/bruhmoment/status/1247980101435822088 (with or without the 's?=xx')\n"+'['+Fore.RED+'+'+Style.RESET_ALL+'] '+'For more details, use -h.')

except Exception as e:
	print('['+Fore.RED+'+'+Style.RESET_ALL+'] '+'There was an error, please submit a report with the details below.')
	logging.error('Error at %s', 'division', exc_info=e)
