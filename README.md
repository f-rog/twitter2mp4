# twitter2mp4
twitter2mp4 its a tool to download videos from Twitter. Needless of ffmpeg.

Here's what twitter2mp4 looks in action.
```
$ python twitter2mp4.py https://twitter.com/ImReeeK/status/1247980101435822088?s=09 -fn funny_video
[+] File successfully saved as funny_video.mp4 !

$ python twitter2mp4.py https://twitter.com/ImReeeK/status/1247980101435822088?s=09 -l
[+] Link: https://video.twimg.com/ext_tw_video/1247979567739879424/pu/vid/720x986/MgihvBG9E_2E-Y4I.mp4?tag=10

```

## Setup
1) Clone the repository

```
$ git clone https://github.com/hohohoesmad/twitter2mp4.git
```

2) Install the dependencies

```
$ cd twitter2mp4
$ pip install -r requirements.txt
```

3) Run twitter2mp4 (see [Usage](#usage) below for more detail)

```
$ python twitter2mp4.py
```

## Usage
```
$ python twitter2mp4.py -h
usage:  [-h] [-d DIR] [-fn FILENAME] [-l] url

positional arguments:
  url                   The URL to the video you wanna download (ex. https://t
                        witter.com/bruhmoment/status/1247980101435822088?s=09)
                        .

optional arguments:
  -h, --help            show this help message and exit
  -d DIR, --dir DIR     The directory you wanna save the downloaded video/s
                        to.
  -fn FILENAME, --filename FILENAME
                        Custom filename for the downloaded video.
  -l, --link            Will output a direct URL to the video.

```
Example:
```
$ python twitter2mp4.py https://twitter.com/ImReeeK/status/1247980101435822088?s=09 -fn funny_video
```

## Compatibility

Tested on Python 3.7 on Linux and Windows. Feel free to [open an issue] if you have bug reports or questions. If you want to collaborate, you're welcome.

[open an issue]: https://github.com/hohohoesmad/twitter2mp4/issues/new
