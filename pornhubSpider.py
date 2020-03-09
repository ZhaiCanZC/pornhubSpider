import requests 
import json
import os
import re
from bs4 import BeautifulSoup as soup

class PornHubVideo(object):
    def __init__(self, flvars):
        self.pageUrl = flvars['link_url']
        self.viewkey = re.search('viewkey=([a-zA-Z0-9]+)',self.pageUrl).group(1)
        self.title = flvars['video_title']
        self.imgUrl = flvars['image_url']
        time = int(flvars['video_duration'])
        m, s = divmod(time,60)
        h, m = divmod(m,60)
        self.duration = '%02d:%02d:%02d' % (h,m,s)
        self.definitions = []
        for defin in flvars['mediaDefinitions']:
            info = {}
            info['format'] = defin['format']
            info['quality'] = defin['quality']
            info['videoUrl'] = defin['videoUrl']
            self.definitions.append(info)
        self.definitions.remove(self.definitions[-1])
    
    def __str__(self):
        info = {}
        for k in self.__dict__.keys():
            info[k] = getattr(self,k)
        
        return json.dumps(info,ensure_ascii=False,indent=4)

link = 'https://www.pornhub.com'
#获取某分类下任意页数的视频列表
def getVideoList(types,page='1',search = False):
    #url = link + '/video?c=111&page=1'
    result = []
    url = link+types+str(page)
    rep = requests.get(url)
    videoList = soup(rep.content,'lxml')
    if search:
        videoList = videoList.find('ul',id = 'videoSearchResult').findAll('li')
    else:
        videoList = videoList.find('ul',id = 'videoCategory').findAll('li')
    for i in videoList:
        try:
            title = i.a.get('title')
            result.append({
            'title':title,
            'preview' : i.img.get('data-mediabook'),
            'pic' : i.img.get('data-src'),
            'url' : i.a.get('href'),
            'time' : i.var.text
            }) 
        except:
            continue
            
    return result
    
#旧版函数，已停用
def getVideoUrl(viewkey):
    raise Exception('This method(getVideoUrl) has been abandoned.Please use "getVideoInfo" instead.')
    
#获取视频全部清晰度,地址,视频编号
def getVideoInfo(viewkey):
    url = link + '/view_video.php?viewkey='+viewkey
    rep = requests.get(url)
    doc = soup(rep.content,'lxml')
    script = doc.find(id='player').script.contents[0]
    script = re.sub('loadScriptUniqueId[\s\S]+','',script)
    script += re.search('flashvars[^ ]+',script).group(0) + ';'
    #print(script)
    import js2py
    import ast
    json_str = str(js2py.eval_js(script))
    flashvars = ast.literal_eval(json_str)
    del flashvars['hotspots']
    
    video = PornHubVideo(flashvars)
    #print(flashvars)
    #print(flashvars['mediaDefinitions'])
    
    return video
    
    
#根据视频编号获取全部相似推荐
def getVideoSimilar(ids,page=1):
    url = '%s/video/relateds?ajax=1&id=%s&page=%s&num_per_page=10'%(link,ids,page)
    result=[]
    rep = requests.get(url)
    videoList = soup(rep.content,'lxml')
    videoList = videoList.findAll('li')
    for i in videoList:
        result.append({
            'title':i.a.get('title'),
            'preview' : i.img.get('data-mediabook'),
            'pic' : i.img.get('src'),
            'url' : i.a.get('href'),
            'time' : i.var.text
        })
    #return resultStr
    return result