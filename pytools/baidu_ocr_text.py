# import base64
import requests
from pyperclip import copy as toClip
from utils.screenshot import screenshotThread

def main(config,remind):
    if config['secret_key']=='' or config['api_key']=='':
        remind("接口为空",'请在设置中填写对应接口。')
        return
    sT=screenshotThread()
    sT.start()
    try:
        proxies = {
            "http": "",
            "https": "",
        }
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + config[
            'api_key'] + '&client_secret=' + config['secret_key']
        response = requests.get(host, proxies=proxies)
        baidu_text_token = response.json()['access_token']
        sT.join()
        img_str = sT.getBase64()

        request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
        params = {"image": img_str}
        request_url = request_url + "?access_token=" + baidu_text_token
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(request_url, data=params, headers=headers, proxies=proxies)
        result = ""

        for line in response.json()['words_result']:
            result += line['words'] + "\n"
        toClip(result)
        remind("识别结果已复制", result)
    except Exception as e:
        remind("识别出错", "请检查接口")


