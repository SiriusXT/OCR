# import base64
import requests
import json
# from io import  BytesIO
from utils import screenshot
from pyperclip import copy as toClip
def main(config,remind):
    try:
        ocr_word(config,remind)
    except:
        remind("识别错误","请检查接口是否正确。")
def ocr_word(config,remind):
    img_str=screenshot.Screenshot().getBase64()
    image_uri = "data:image/jpg;base64," +img_str
    proxies = {
        "http": "",
        "https": "",
    }
    r = requests.post("https://api.mathpix.com/v3/latex",
                      data=json.dumps({'src': image_uri, 'formats': [
                          # "text",
                          #                                            "latex_simplified",
                                                                     "latex_styled",
                                                                     "mathml",
                                                                     # "asciimath",
                                                                     # "latex_list"
                                                                     ]}),

                      headers={"app_id": config["app_id"], "app_key": config["app_key"],
                               "Content-type": "application/json"},proxies=proxies)
    mathml = json.loads(r.text)['mathml']
    mathml='''<math xmlns="http://www.w3.org/1998/Math/MathML">'''+mathml[6:]
    def doSpace(mathml,starti):
        def getFF(mathml, i):
            mathml = mathml[:i]
            for i in range(i - 1, 0, -1):
                if mathml[i] == '<':
                    mathml = mathml[:i]
                    break
            for i in range(i - 1, 0, -1):
                if mathml[i] == '>':
                    y = i
                if mathml[i] == '<':
                    x = i + 1
                    break
            return x, y
        for i in range(len(mathml)):
            if mathml[i] == '∑' and i==starti:
                indexX, indexY = getFF(mathml, i)
                father = mathml[indexX:indexY]
                break
        zilei = 0
        for i in range(indexY + 1, len(mathml)):
            if mathml[i - len(father):i] == father and mathml[i - len(father) - 1:i - len(father)] == '<':
                zilei += 1
            if mathml[i - len(father):i] == father and mathml[i - len(father) - 1:i - len(father)] == '/':
                if zilei != 0:
                    zilei -= 1
                else:
                    mathml = list(mathml)
                    mathml.insert(i + 1, '<mrow><mo> </mo></mrow>')
                    mathml = ''.join(mathml)
                    break
        return  mathml
    for starti in range(len(mathml)):
        if mathml[starti]=='∑':
            mathml=doSpace(mathml,starti)
    mathml=mathml.replace('∣', '|', 10)
    # return {'mathml':mathml,
    #         'latex_styled':json.loads(r.text)['latex_styled'],
    #         'latex_confidence':json.loads(r.text)['latex_confidence']}
    toClip(mathml)
    remind("识别结果已复制", '置信度：{:.2f} '.format(json.loads(r.text)['latex_confidence']))
