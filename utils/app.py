import sys
sys.dont_write_bytecode = True
import wx
import wx.adv
import threading
import webbrowser
import subprocess
import pytools
import configparser
from pytools import baidu_ocr_text,zidingyi_ocr_text,mathpix_latex,mathpix_word
baidu_ocr_text,zidingyi_ocr_text,baidu_ocr_text,mathpix_latex,mathpix_word
class MyTaskBarIcon(wx.adv.TaskBarIcon):
    def __init__(self, configs):
        wx.adv.TaskBarIcon.__init__(self)
        self.configs = configs

        self.isOCRing = 0  # 1表示正在识别中，0表示没有任务进行中
        self.TITLE = "OCRP，点击开始识别，快捷键：" + self.configs["default"]["hot_key"]  # 鼠标移动到图标上显示的文字
        self.ICON = self.configs["default"]["root"] + "icons/" + \
                    self.configs[self.configs["default"]["selected"]]["icon"]
        self.SetIcon(wx.Icon(self.ICON), self.TITLE)

        self.ID_EXIT = wx.NewIdRef()  # 菜单选项“退出”的ID
        self.ID_URL = wx.NewIdRef()  # 菜单选项“显示页面”的ID
        self.ID_SET = wx.NewIdRef()  #
        self.ids={}
        for i in range(1,len(self.configs)):
            self.ids[list(self.configs.keys())[i]]=wx.NewIdRef()
        # self.id = [wx.NewIdRef() for _ in range(len(self.configs)-1)]  # 几个选项就生成几个id

        # for i in range(len(self.configs)-1):
        for value in self.ids.values():
            self.Bind(wx.EVT_MENU, self.ocr_choice_method, id=value)
        self.Bind(wx.EVT_MENU, self.onExit, id=self.ID_EXIT)  # 绑定“退出”选项的点击事件
        self.Bind(wx.EVT_MENU, self.openUrl, id=self.ID_URL)  # 绑定“显示页面”选项的点击事件
        self.Bind(wx.EVT_MENU, self.openSet, id=self.ID_SET)  # 绑定“显示页面”选项的点击事件
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.startOCR)

    def openSet(self, event):
        threading.Thread(target=subprocess.Popen,
                         args=('notepad ' + self.configs["default"]["root"] + r'conf.ini',)).start()

    def ocr_choice_method(self, event):
        self.configs["default"]["selected"] = dict([val, key] for key, val in self.ids.items())[event.GetId()]
        cf = configparser.ConfigParser()
        cf.read(self.configs["default"]["root"] + r"conf.ini", encoding="utf-8")
        cf.set("default", "selected", str(self.configs['default']['selected']))
        with open(self.configs['default']["root"] + r"conf.ini", 'w', encoding="utf-8") as file:
            cf.write(file)
        self.ICON = self.configs['default']["root"] + "icons/" + self.configs[self.configs["default"]["selected"]]["icon"]
        self.SetIcon(wx.Icon(self.ICON), self.TITLE)

    def openUrl(self, event):
        webbrowser.open('https://github.com/SiriusXT/OCR/releases/', new=0, autoraise=True)

    def onExit(self, event):
        wx.Exit()

    def startOCR(self, event=1):  ## 执行操作
        if self.isOCRing == 0:
            self.isOCRing = 1  ##设置这个值的目的是禁止并行
            try:
                fun = getattr(pytools, self.configs['default']['selected'])
                fun.main(self.configs[self.configs['default']['selected']],self.remind)
            except Exception as e:
                # print(e)
                self.remind("执行错误", str(e))
            self.isOCRing = 0
        else:
            pass

    def remind(self, title, text, msec=3000, flags=1):  ### 通知提醒
        self.ShowBalloon(title, text, msec=msec, flags=flags)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        for key in self.ids.keys():
            if self.configs['default']['selected'] == key:
                menu.Append( self.ids[key], self.configs[key]["name"],kind=wx.ITEM_RADIO)
            else:
                menu.Append( self.ids[key], self.configs[key]["name"],kind=wx.ITEM_NORMAL)
        menu.AppendSeparator()
        menu.Append( self.ID_URL, '更新',kind=wx.ITEM_NORMAL)
        menu.Append( self.ID_SET,'配置', kind=wx.ITEM_NORMAL)
        menu.Append( self.ID_EXIT,'退出',kind= wx.ITEM_NORMAL)
        return menu


