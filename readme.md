# pornhun爬虫
可以获取pornhub的视频信息
## getVideoList 任意页面的视频列表
传入一个url如 www.pornhub.com/video?c=111&page=1 <br>
该函数会返回一个PornhubVideo类列表，格式如下：<br>

## PornhubVideo类(Class)
用于获取并保存视频信息<br>

### 函数(methdos)

| 函数 | 解释 |
| ---- | ---- |
| PornhubVideo(url_or_viewkey, ifGetInfo=False) | 构造函数<br>-*url_or_viewkey: str* - 视频页面链接或viewkey<br>-*ifGetInfo: bool* - 是否获取信息,默认为 *False*<br>&emsp;&emsp;-*True*: 生成对象时获取视频信息。<br>&emsp;&emsp;-*False*: 生成对象时不获取视频信息，之后若需获取，可用 GetInfo() 函数。<br> |
| GetInfo() | 获取视频信息 |
| GetRelated(page=1, ifGetInfo=False) | 利用视频ID,获取该视频ID的全部相似推荐（共10个），返回格式与getVideoList相同<br>*page*: 选择要获取第几页，默认为1。<br>*ifGetInfo: bool* - 是否获取信息,默认为 *False*<br>&emsp;&emsp;-*True*: 生成对象时获取视频信息。<br>&emsp;&emsp;-*False*: 生成对象时不获取视频信息，之后若需获取，可用 GetInfo() 函数。<br> |
| RandomPorn() | 获取随机视频 | 

### 属性(properties)
| 属性 | 解释 |
| ---- | ----|
| pageUrl: str | 原始网页链接地址 |
| viewkey: str | 视频viewkey |
| videoID: str | 视频ID,用于获取相关视频 |
| title: str | 视频标题 |
| imgUrl: str | 视频封面图片链接地址 |
| duration: str | 视频时长，格式为 hh:mm:ss |
| definitions: dict | 视频所有格式、分辨率及链接 |
| isPremium: bool | 是否为会员视频 |

