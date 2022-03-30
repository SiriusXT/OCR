import os
os.environ['HUB_HOME'] = "./modules"
import cv2
import numpy as np
from pyperclip import copy as toClip
import base64
from utils.screenshot import screenshotThread

import paddlehub as hub

def main(config,remind):
    sT=screenshotThread()
    sT.start()
    global ocr
    try:
        ocr
    except:
        ocr = hub.Module(name="chinese_ocr_db_crnn_mobile")

    sT.join()
    img_str=sT.getBase64()
    image_bytes = base64.b64decode(img_str)
    image_np = np.frombuffer(image_bytes, dtype=np.uint8)
    image_np2 = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
    # up = np.full((5, image_np.shape[1], 3), 0)
    # left = np.full((image_np.shape[0] + 10, 5, 3), 0)
    # image_np1 = np.concatenate((left, np.concatenate((up, image_np, up), axis=0), left), axis=1)
    img = cv2.cvtColor(image_np2, cv2.COLOR_RGB2BGR)
    results = ocr.recognize_text(
        images=[img],  # 图片数据，ndarray.shape 为 [H, W, C]，BGR格式；
        use_gpu=False,  # 是否使用 GPU；若使用GPU，请先设置CUDA_VISIBLE_DEVICES环境变量
        visualization=False,  # 是否将识别结果保存为图片文件；
        output_dir=r'out.png',  # 图片的保存路径，默认设为 ocr_result；
        box_thresh=0.2,  # 检测文本框置信度的阈值；
        text_thresh=0.2
    )

    res = str()
    result=results[0]["data"]
    for i in range(len(result)):
        if i==0:
            res += result[i]["text"]
        elif abs(result[i]["text_box_position"][0][1]-result[i-1]["text_box_position"][0][1])<5:
            res = res +" "+result[i]["text"]
        else:
            res =res+"\n"+result[i]["text"]
    toClip(res)
    if res:
        remind("识别结果已复制", res)
    else:
        remind("识别错误", "未识别到内容。")
