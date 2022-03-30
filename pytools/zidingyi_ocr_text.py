# -*- coding: utf-8 -*-
# author:laidefa

# 载入包
import requests
import json
from utils.screenshot import screenshotThread
import hmac
import math
import base64
import struct
import hashlib
import time
from pyperclip import copy as toClip

def ssocr(config,remind):
    sT = screenshotThread()
    sT.start()
    sT.join()
    img_str = sT.getBase64()

    def longcode(secret_key):
        # secret key 的长度必须是 8 的倍数。所以如果 secret key 不符合要求，需要在后面补上相应个数的 "="
        secret_key_len = len(secret_key)
        secret_key_pad_len = math.ceil(secret_key_len / 8) * 8 - secret_key_len
        secret_key = secret_key + "=" * secret_key_pad_len
        key = base64.b32decode(secret_key)
        res = ""
        for i in (-30, 0, 30):
            duration_input = int(time.time() + i) // 30
            msg = struct.pack(">Q", duration_input)
            google_code = hmac.new(key, msg, hashlib.sha1).digest()
            o = google_code[19] & 15
            google_code = str((struct.unpack(">I", google_code[o:o + 4])[0] & 0x7fffffff) % 1000000)

            # 生成的验证码未必是 6 位，注意要在前面补 0
            if len(google_code) == 5:  # Only if length of the code is 5, a zero will be added at the beginning of the code.
                google_code = '0' + google_code
            res += google_code + " "
        return res

    params = {
        "code": longcode('请填写和server.py一样的密钥'),
        "img_str": img_str,
    }
    proxies = {
        "http": "",
        "https": "",
    }

    url = '请填写对应的服务网址'

    html = requests.post(url, json.dumps(params), proxies=proxies)

    res='\n'.join( html.json().values())
    return res


def main(config,remind):
    try:
        res=ssocr(config,remind)
        toClip(res)
        remind("识别结果已复制", res)
    except:
        remind("识别出错", "请检查服务器连接状态。")

