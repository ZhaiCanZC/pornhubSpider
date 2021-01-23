import json
import os
import re
import threading

import js2py
import requests
from bs4 import BeautifulSoup as soup


class PornhubVideo(object):
    __link = 'https://www.pornhub.com'

    def __init__(self, url_or_viewkey, ifGetInfo=False):

        if 'http' in url_or_viewkey:
            self.__pageUrl = url_or_viewkey
            self.__viewkey = ''
        else:
            self.__pageUrl = ''
            self.__viewkey = url_or_viewkey
        self.__videoID = ''
        self.__isPremium = False
        self.__success = False
        self.__title = ''
        self.__imgUrl = ''
        self.__duration = ''
        self.__definitions = {}
        if (ifGetInfo):
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

    @property
    def isPremium(self):
        return self.__isPremium

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

    @staticmethod
    def RandomPorn():
        randomUrl = 'https://www.pornhub.com/video/random'
        while True:
            porn = PornhubVideo(randomUrl, True)
            if porn.__success:
                break
            else:
                del porn
        return porn


    # 获取视频信息
    def GetInfo(self):
        print('开始加载')
        if self.__pageUrl != '':
            url = self.__pageUrl
        else:
            url = self.__link + '/view_video.php?viewkey=' + self.__viewkey
        rep = requests.get(url)
        doc = soup(rep.content, 'lxml')

        try:
            wrapper = doc.find('div', {'class': re.compile(r'video-wrapper(.+)?')})
            title = wrapper.find('h1', {'class': 'title'})
        except:
            self.__success = False
            print('加载失败')
            return
        if (icon := title.find('i')) is not None:
            self.__isPremium = True
            self.__success = False
            print('加载失败')
            return
        else:
            self.__isPremium = False
        try:
            script = doc.find(id='player').script.contents[0]
            script = re.sub(r'playerObjList[\s\S]+', '', script)
            flashvars_search = re.search(r'flashvars_([0-9]+)', script)
            flashvars_name = flashvars_search.group(0)
            qualityitems_name = re.search(r'qualityItems_([0-9]+)', script).group(0)
        except:
            self.__success = False
            print('加载失败')
            return
        script += f'[{flashvars_name},{qualityitems_name}];'
        script_result = js2py.eval_js(script).to_list()
        flashvars = script_result[0]
        qualityitems = script_result[1]
        self.__pageUrl = flashvars['link_url']
        self.__viewkey = re.search(r'\?viewkey=(.+)', self.__pageUrl).group(1)
        self.__title = flashvars['video_title']
        self.__imgUrl = flashvars['image_url']
        time = int(flashvars['video_duration'])
        m, s = divmod(time, 60)
        h, m = divmod(m, 60)
        self.__duration = '%02d:%02d:%02d' % (h, m, s)
        for defin in flashvars['mediaDefinitions']:
            videoUrl = defin['videoUrl']
            quality = defin['quality']
            vformat = defin['format']
            if videoUrl == '' or not isinstance(quality, str):
                continue
            if vformat not in self.__definitions:
                self.__definitions[vformat] = {}
            self.__definitions[vformat][quality] = videoUrl
        for item in qualityitems:
            if 'mp4' not in self.__definitions:
                self.__definitions['mp4'] = {}
            self.__definitions['mp4'][item['text'].strip('p')] = item['url']
        self.__success = True
        if os.path.exists('scripts.py'):
            os.remove('scripts.py')
        print('加载成功')

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
    url = link + types + str(page)
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


# 根据网页链接获取viewkey
def url2viewkey(url):
    viewkey = re.search(r'\?viewkey=(.+)$').group(1)
    return viewkey
