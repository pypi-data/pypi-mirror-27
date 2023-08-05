#! python3

"""this is pixiv module for comiccrawler

Ex:
	http://www.pixiv.net/member_illust.php?id=2211832

"""

import re
from html import unescape
from io import BytesIO
from zipfile import ZipFile

from node_vm2 import eval

from ..core import Episode, grabhtml
from ..error import SkipEpisodeError, PauseDownloadError, is_403
from ..url import urljoin

domain = ["www.pixiv.net"]
name = "Pixiv"
noepfolder = True
config = {
	"cookie_PHPSESSID": "請輸入Cookie中的PHPSESSID"
}

def get_title(html, url):
	try:
		user = unescape(re.search("class=\"user-name\"[^>]*>([^<]+)", html).group(1))
		id = re.search(r"pixiv.context.userId = \"(\d+)\"", html).group(1)
		title = "{} - {}".format(id, user)
	except AttributeError:
		title = "[pixiv] " + unescape(re.search("<title>([^<]+)", html).group(1))
	return title

def get_episodes(html, url):
	if "pixiv.user.loggedIn = true" not in html:
		raise PauseDownloadError("you didn't login!")
	s = []
	for m in re.finditer(r'<a href="([^"]+)"><h1 class="title" title="([^"]+)">', html):
		ep_url, title = m.groups()
		uid = re.search("id=(\d+)", ep_url).group(1)
		e = Episode("{} - {}".format(uid, unescape(title)), urljoin(url, ep_url))
		s.append(e)
	return s[::-1]
	
cache = {}

def get_images_old(html, url):
	match = re.search(r'"works_display"><a (?:class="[^"]*" )?href="([^"]+)"', html)
	
	if not match:
		return
		
	inner_url = match.group(1)
	html = grabhtml(urljoin(url, inner_url), referer=url)

	if "mode=big" in inner_url:
		# single image
		img = re.search(r'src="([^"]+)"', html).group(1)
		return [img]

	if "mode=manga" in inner_url:
		# multiple image
		imgs = []
		
		def create_grabber(url):
			def grabber():
				html = grabhtml(url)
				return re.search(r'img src="([^"]+)"', html).group(1)
			return grabber

		for match in re.finditer(r'a href="(/member_illust\.php\?mode=manga_big[^"]+)"', html):
			imgs.append(create_grabber(urljoin(url, match.group(1))))

		# New manga reader (2015/3/18)
		# http://www.pixiv.net/member_illust.php?mode=manga&illust_id=19254298
		if not imgs:
			for match in re.finditer(r'originalImages\[\d+\] = ("[^"]+")', html):
				img = eval(match.group(1))
				imgs.append(img)

		return imgs

def get_images(html, url):
	if "pixiv.user.loggedIn = true" not in html:
		raise PauseDownloadError("you didn't login!")

	# ugoku
	rs = re.search(r"pixiv\.context\.ugokuIllustFullscreenData\s+= ([^;]+)", html)
	if rs:
		json = rs.group(1)
		o = eval("(" + json + ")")
		cache["frames"] = o["frames"]
		return [o["src"]]

	# new image layout (2014/12/14)
	rs = re.search(r'class="big" data-src="([^"]+)"', html)
	if rs:
		return [rs.group(1)]

	rs = re.search(r'data-src="([^"]+)" class="original-image"', html)
	if rs:
		return [rs.group(1)]

	# old image layout
	imgs = get_images_old(html, url)
	if imgs:
		return imgs
	
	# restricted
	rs = re.search('<section class="restricted-content">', html)
	if rs:
		raise SkipEpisodeError

	# error page
	rs = re.search('class="error"', html)
	if rs:
		raise SkipEpisodeError

	# id doesn't exist
	rs = re.search("pixiv.context.illustId", html)
	if not rs:
		raise SkipEpisodeError

def errorhandler(er, crawler):
	# http://i1.pixiv.net/img21/img/raven1109/10841650_big_p0.jpg
	# Private page?
	if is_403(er):
		raise SkipEpisodeError
			
def imagehandler(ext, bin):
	"""Append index info to ugoku zip"""
	if ext == ".zip":
		# add frame info
		with BytesIO(bin) as imbin:
			zip = ZipFile(imbin, "a")
			data = "\n".join(
				["{file}\t{delay}".format_map(f) for f in cache["frames"]])
			zip.writestr("index", data.encode("utf-8"))
			zip.close()
			bin = imbin.getvalue()
	return ext, bin

def get_next_page(html, url):
	match = re.search("href=\"([^\"]+)\" rel=\"next\"", html)
	if match:
		return urljoin(url, unescape(match.group(1)))
