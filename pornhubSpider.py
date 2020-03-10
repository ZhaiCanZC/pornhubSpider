import requests
import json
import re
import js2py
import ast
from bs4 import BeautifulSoup as soup


class PornhubVideo(object):
    __link = 'https://www.pornhub.com'
    
    def __init__(self, viewkey, ifGetInfo=False):
        self.__pageUrl = ''
        self.__viewkey = viewkey
        self.__videoID = ''
        self.__title = ''
        self.__imgUrl = ''
        self.__duration = ''
        self.__definitions = []
        if(ifGetInfo):
            self.GetInfo()
    
    # 原始网页链接
    @property
    def pageUrl(self):
        return self.__pageUrl
    
    # viewkey
    @property
    def viewkey(self):
        return self.__viewkey
    
    # 视频ID
    @property
    def videoID(self):
        return self.__videoID
    
    # 视频标题
    @property
    def title(self):
        return self.__title
    
    # 封面图片链接
    @property
    def imgUrl(self):
        return self.__imgUrl
    
    # 视频时长
    @property
    def duration(self):
        return self.__duration
    
    # 所有格式及解析度
    @property
    def definitions(self):
        return self.__definitions
    
    def __str__(self):
        info = {}
        for k in self.__dict__.keys():
            key = re.search('__(.+)', k).group(1)
            info[key] = getattr(self, k)
        return json.dumps(info, ensure_ascii=False, indent=4)
    
    # 获取视频信息
    def GetInfo(self):
        url = self.__link + '/view_video.php?viewkey='+self.__viewkey
        rep = requests.get(url)
        doc = soup(rep.content, 'lxml')
        script = doc.find(id='player').script.contents[0]
        script = re.sub('loadScriptUniqueId[\s\S]+', '', script)
        search = re.search('flashvars_([0-9]+)', script)
        script += search.group(0) + ';'
        self.__videoID = search.group(1)
        json_str = str(js2py.eval_js(script))
        flashvars = ast.literal_eval(json_str)
        self.__pageUrl = flashvars['link_url']
        self.__title = flashvars['video_title']
        self.__imgUrl = flashvars['image_url']
        time = int(flashvars['video_duration'])
        m, s = divmod(time, 60)
        h, m = divmod(m, 60)
        self.__duration = '%02d:%02d:%02d' % (h, m, s)
        for defin in flashvars['mediaDefinitions']:
            info = {}
            info['format'] = defin['format']
            info['quality'] = defin['quality']
            info['videoUrl'] = defin['videoUrl']
            self.definitions.append(info)
        self.__definitions.remove(self.definitions[-1])
    
    # 获取相关视频
    def GetRelated(self, page=1, ifGetInfo=False):
        result = []
        if self.__videoID == '':
            return result
        url = '%s/video/relateds?ajax=1&id=%s&page=%s&num_per_page=10' % (self.__link, self.__videoID, page)
        rep = requests.get(url)
        videoList = soup(rep.content, 'lxml')
        videoList = videoList.findAll('li')
        for video in videoList:
            viewkey = video.get('_vkey')
            result.append(PornhubVideo(viewkey, ifGetInfo))
        return result
        
        
# 获取某分类下任意页数的视频列表
def getVideoList(types, page='1', search=False, ifGetInfo=False):
    # url = link + '/video?c=111&page=1'
    link = 'https://www.pornhub.com'
    result = []
    url = link+types+str(page)
    rep = requests.get(url)
    videoList = soup(rep.content, 'lxml')
    if search:
        videoList = videoList.find('ul', id='videoSearchResult').findAll('li')
    else:
        videoList = videoList.find('ul', id='videoCategory').findAll('li')
    for i in videoList:
        try:
            for video in videoList:
                viewkey = video.get('_vkey')
                result.append(PornhubVideo(viewkey, ifGetInfo))
        except:
            continue
    return result
