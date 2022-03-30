import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
# import numpy
import cv2
import numpy as np
# from pyperclip import copy as toClip
import base64
# from utils.screenshot import screenshotThread
from paddleocr import PaddleOCR
import hmac
import math
# import base64
import struct
import hashlib
import time
def shortcode(secret_key):
    # secret key 的长度必须是 8 的倍数。所以如果 secret key 不符合要求，需要在后面补上相应个数的 "="
    secret_key_len = len(secret_key)
    secret_key_pad_len = math.ceil(secret_key_len / 8) * 8 - secret_key_len
    secret_key = secret_key + "=" * secret_key_pad_len
    key = base64.b32decode(secret_key)
    duration_input = int(time.time()) // 30

    msg = struct.pack(">Q", duration_input)
    google_code = hmac.new(key, msg, hashlib.sha1).digest()
    o = google_code[19] & 15
    google_code = str((struct.unpack(">I", google_code[o:o+4])[0] & 0x7fffffff) % 1000000)

    # 生成的验证码未必是 6 位，注意要在前面补 0
    if len(google_code) == 5:  # Only if length of the code is 5, a zero will be added at the beginning of the code.
        google_code = '0' + google_code
    return google_code


global ocr
try:
    ocr
except:
    ocr = PaddleOCR(use_angle_cls=True, det_model_dir="./modules/det", rec_model_dir="./modules/rec",
                    cls_model_dir="./modules/cls")  # need to run only once to download and load model into memory

# 创建数据模型
class Item(BaseModel):
    code: str
    img_str: str

app = FastAPI()


@app.get("/")
async  def root():
    return 'Hello World!'


@app.post("/pre")
async def fcao_predict(item: Item):
    item_dict = item.dict()
    img_str=item_dict['img_str']
    longcode=item_dict['code']
    if shortcode('请填写自定义密钥用于生成验证码') not in longcode:return{"status":"error"}
    image_bytes = base64.b64decode(img_str)
    image_np = np.frombuffer(image_bytes, dtype=np.uint8)
    image_np2 = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
    # up = np.full((5, image_np.shape[1], 3), 0)
    # left = np.full((image_np.shape[0] + 10, 5, 3), 0)
    # image_np1 = np.concatenate((left, np.concatenate((up, image_np, up), axis=0), left), axis=1)
    img = cv2.cvtColor(image_np2, cv2.COLOR_RGB2BGR)
    results = ocr.ocr(img, cls=True)
    res = ''
    for x in results:
        res += x[1][0] + "\n"
    res = res[:-1]
    return {"res":res}

if __name__ == '__main__':
    uvicorn.run(app=app,
                host="0.0.0.0",
                port=8086,
                workers=1)