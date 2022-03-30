import keyboard
import wx
import wx.adv
import configparser
from utils.app import MyTaskBarIcon

import sys
sys.dont_write_bytecode = True
def Init():
    root = "./"
    cf = configparser.ConfigParser()
    try:
        cf.read(root + r'conf.ini', encoding="utf-8")
        cf.get("default", "hot_key")
        cf.get("default", "selected")
    except:
        f2 = open(root + r'conf.ini', 'w+', encoding="utf-8")
        f2.write('''[default]
hot_key = Alt+o
selected = zidingyi_ocr_text

[baidu_ocr_text]
api_key = 
secret_key = 
name = 百度文字识别
icon = text.ico

[zidingyi_ocr_text]
name = 自定义文字识别
icon = text.ico

;[bendi_ocr_text]
;name = 本地文字识别
;icon = text.ico

[mathpix_word]
app_id = 
app_key = 
name = 公式识别为word
icon = word.ico

[mathpix_latex]
app_id = 
app_key = 
name = 公式识别为latex
icon = latex.ico
''')
        f2.close()

    cf.read(root + r'conf.ini', encoding="utf-8")
    config={}
    config["default"]={}
    config["default"]["root"]=root
    config["default"]["hot_key"]=cf.get("default", "hot_key")
    config["default"]["selected"]= cf.get("default", "selected")
    for sec in cf.sections():
        if sec != "default":
            config[sec]={}
            for opt in cf.options(sec):
                config[sec][opt]=cf.get(sec, opt)
    # if config["baidu_ocr_text"]['api_key'] == '':
    #     config["baidu_ocr_text"]['api_key']=' '
    #     config["baidu_ocr_text"]['secret_key']=' '
    # if config["mathpix_latex"]['app_id']=='' :
    #     config["mathpix_latex"]['app_id'] =' '
    #     config["mathpix_latex"]['app_key'] = ' '
    # if config["mathpix_word"]['app_id']=='' :
    #     config["mathpix_word"]['app_id'] =' '
    #     config["mathpix_word"]['app_key'] = ' '
    return config


class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self)
class MyApp(wx.App):
    def OnInit(self):
        MyFrame()
        return True


if __name__ == '__main__':
    configs = Init()
    app = MyApp()
    MyTaskBar = MyTaskBarIcon(configs)  # 显示系统托盘图标
    try:
        keyboard.add_hotkey(configs["default"]["hot_key"], MyTaskBar.startOCR, args=tuple())
    except:
        keyboard.add_hotkey('Alt+o', MyTaskBar.startOCR, args=tuple())
        MyTaskBar.remind("快捷键设置错误", "默认为:Alt+o", 2000)
    app.MainLoop()
    keyboard.remove_hotkey('Alt+o')
