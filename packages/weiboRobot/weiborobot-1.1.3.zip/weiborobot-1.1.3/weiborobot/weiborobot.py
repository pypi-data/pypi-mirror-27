#-*-coding:utf-8-*-


"""
weiborobot:the module providesone base class ,every user can user it to send weibo

you must have username,password,app_key,app_serret,callback_url

app_key,app_secret,callback_url is set in weibo platform,you should set up your app first

Of Course,you can inherit from the base class


Copyright C Haibo wang.2017

"""
from copy import copy
from auth import WeiboAuth





class WeiboRobot(object):

	"""
		>> from weiborobot import WeiboRobt
		>> robot = WeiboRobot('username','password','app_key','app_secret',callback_url=callback_url)
		>> text = 'wffwf'
		>> robot.communicate('/statuses/share','post',status=text)
		>> print robot.communicate('/statuses/user_timeline','get')
	"""

	def __init__(self,username,passwd,app_key,app_secret,callback_url=None,domain=u'http://hbnnforever.cn'):
		"""
		the class is one api to weiboauth
		domain:the domain is used to add http for sending weibo.because from 2017.6.26 on,sending weibo api
		is statuses/share.so you must add one domain in text.
		the default value is my website.you can add value whatever you want to add.
		"""
		#the text must have http.
		self.domain = domain
		self.weibo = WeiboAuth(username,passwd,app_key,app_secret,callback_url)
		self.robot = self._client_robot

	@property
	def _client_robot(self):
		#when the instance is created ,the instance should create code,set token for the client
		#the class use proxy design ,the robot does everyting that client does
		self.weibo.set_token()
		return self.weibo.client

	def encode_text(self,**kwargs):
		"""
		the parameters must be encoded to unicode
		:param kwargs:
		:return:
		"""
		for key in kwargs:
			if not isinstance(kwargs[key],unicode):
				kwargs[key] = unicode(kwargs[key],'utf-8')
		return kwargs

	def communicate(self,path,method,**kwargs):
		"""
		you must know about weibo api.
		:param path: path is according to weibo api.you must pass the right path
		:param method: get or post
		:param kwargs: the parameters you should pass for the request url.
		:return:
		"""
		if path.startswith('/') or path.endswith('/'):
			path = path.strip('/')
		# from 2017.6.26,sending weibo should use share.so you must add one http link addr.
		if kwargs:
			kwargs = self.encode_text(**kwargs)
			if 'share' in path:
				if 'status' in kwargs:
					kwargs['status'] = ' '.join([
					   '(',
						self.domain,
						')',
						kwargs['status']
					])
		paths = path.split('/')
		if len(paths) > 3 or len(paths) == 0 :
			raise ValueError('the path is wrong,pls check right path in weibo api.')

		robot = self.robot
		for p in paths:
			robot = getattr(robot,p)
		return getattr(robot,method)(**kwargs)


