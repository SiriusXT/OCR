## 更新
1. 增加自定义文字识别，该方法以utils/server.py作为后端，调用pytools/zidingyi_ocr_text.py用于识别，**不限次数**。
2. 重写了代码增加了可扩展性。想要添加新功能的话，只需要更改conf.ini和app.py中的import部分，然后在pytools文件夹下创建对应的文件就行。参考其他功能。
3. 部分bug修复。
4. 另外：
    自己写了*本地文字识别接口bendi_ocr_text.py*,该方法使用了paddleocr,无需联网即可识别，运行正常，但是打包较为复杂且文件较大,故并未打包在exe中，感兴趣的童鞋可以参考。
## 简介

OCR工具：支持文字识别、公式识别。

官网：[OCR工具-文字识别，公式识别，语音识别 &#8211; 小天狼星没有星](https://siriussang.top/?p=81)

软件默认快捷方式：Alt+O。

软件均默认使用作者自己的接口，如果经常用可以自定义接口。

### 文字识别

1。使用百度OCR接口，本软件总共每天50000次/天免费机会。如果使用完了可以自定义api，免费申请网站为：[百度文字识别,覆盖全面,响应迅速,准确率超99%-百度AI开放平台](https://ai.baidu.com/tech/ocr/general)，自定义api每个用户都是每天50000次/天免费机会。
2。使用自定义的服务端，该服务端使用的程序在utils/server中，不限次数无限调用，用户也可以部署在自己的服务器中。
### 公式识别

使用mathpix接口，总共每月1000次。可以自定义api，申请网站为：[Mathpix Accounts](https://accounts.mathpix.com/ocr-api/)

~~### 语音识别~~

~~使用百度语音识别接口，总共2万次免费机会。申请网站为：[语音识别-百度AI开放平台](https://ai.baidu.com/tech/speech)。~~
