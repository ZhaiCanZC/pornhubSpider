# pornhun爬虫
可以获取pornhub的视频信息
## getVideoList 任意页面的视频列表
传入一个url如 www.pornhub.com/video?c=111&page=1<br>
该函数会返回一个PornhubVideo类列表，格式如下：<br>

```
[
    <pornhubSpider.PornhubVideo object at **************>,
    <pornhubSpider.PornhubVideo object at **************>,
    <pornhubSpider.PornhubVideo object at **************>,
    ...
]
```

## PornhubVideo类
用于获取并保存视频信息<br>

### PornhubVideo(viewkey, ifGetInfo=False)
构造函数<br>
-viewkey(string): 视频viewkey<br>
-ifGetInfo(bool): 是否获取信息,默认为 False<br>
&emsp;&emsp;-True: 生成对象时获取视频信息。<br>
&emsp;&emsp;-False: 生成对象时不获取视频信息，之后若需获取，可用 GetInfo() 函数。<br>

### PornhubVideo.pageUrl
string类，原始网页链接地址<br>

### PornhubVideo.viewkey
string类，视频viewkey<br>

### PornhubVideo.videoID
string类，视频ID,用于获取相关视频<br>

### PornhubVideo.title
string类，视频标题<br>

### PornhubVideo.imgUrl
string类，原视频封面图片链接地址<br>

### PornhubVideo.duration
string类，视频时长，格式为 00:00:00<br>

### PornhubVideo.definitions
列表，视频所有格式、分辨率及链接<br>
格式如下：<br>

```
[
	{
		"format": "mp4",	#格式
		"quality": "720",	#分辨率
		"videoUrl": ""		#链接
	},
	{
		"format": "hls",
		"quality": "720",
		"videoUrl": ""
	},
	...
]
```

### PornhubVideo.GetInfo()
获取视频信息<br>

### PornhubVideo.GetRelated(page=1, ifGetInfo=False)
利用视频ID,获取该视频ID的全部相似推荐（共10个），返回格式与getVideoList相同<br>
-page: 选择要获取第几页，默认为1。<br>
-ifGetInfo(bool): 是否获取信息,默认为 False<br>
&emsp;&emsp;-True: 生成对象时获取视频信息。<br>
&emsp;&emsp;-False: 生成对象时不获取视频信息，之后若需获取，可用 GetInfo() 函数。<br>

### 信息内容打印
对象直接使用 print() 函数进行打印，也可用 str() 函数转换为字符串<br>
打印及字符串内容格式如下：<br>

```
{
	"pageUrl": "https://www.pornhub.com/view_video.php?viewkey=***************",
	"viewkey": "***************",
	"videoID": "*********",
	"title": "********",
	"imgUrl": "",
	"duration": "00:00:00",
	"definitions": [
		{
			"format": "mp4",
			"quality": "720",
			"videoUrl": ""
		},
		{
			"format": "hls",
			"quality": "720",
			"videoUrl": ""
		},
		...
	]
}
```
