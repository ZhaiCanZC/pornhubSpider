# pornhun爬虫
可以获取pornhub的视频信息
## getVideoList 任意页面的视频列表
传入一个url如 www.pornhub.com/video?c=111&page=1<br>
该函数会返回一个字典，格式如下：<br>
```
{
	{
    'title':'田川祐夢 c930',        #视频标题
    'preview' : 'https://xxxxxxx', #视频预览片段
    'pic' : 'https://xxxxxxx',     #视频封面
    'url' : 'https://xxxxxxx',     #视频播放地址
    'time' : 20.00                 #视频时长
    }，
    ...
}
```

## ~~getVideoUrl 视频的全部清晰度下载地址及视频ID~~
该函数已弃用<br>

## getVideoInfo 视频的基本信息及全部清晰度下载地址
传入视频播放地址，可解析出视频的基本信息及全部清晰度下载地址（ID用于获取相似推荐），<br>
返回值为 PornHubVideo 类对象，可使用 print 函数打印其内容<br>
打印内容格式如下：<br>
```
{
    "pageUrl": "https://www.pornhub.com/view_video.php?viewkey=***************",
    "viewkey": "***************",
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
## getVideoSimilar 视频的全部相关推荐
传入视频ID,获取该视频ID的全部相似推荐（共60个），返回格式与getVideoList相同<br>
