from aip import AipOcr
import pyperclip
from PIL import ImageGrab
import tkinter
import ctypes
import io
import keyboard
import wx
import wx.adv
import _thread
import sys
from win10toast import ToastNotifier
import configparser
class MyTaskBarIcon(wx.adv.TaskBarIcon):
    ICON = "ocr.ico"  # 图标地址
    ID_ABOUT = wx.NewIdRef()  # 菜单选项“关于”的ID
    ID_EXIT = wx.NewIdRef()  # 菜单选项“退出”的ID
    # ID_SHOW_WEB = wx.NewId()  # 菜单选项“显示页面”的ID
    TITLE = "OCR" #鼠标移动到图标上显示的文字

    def __init__(self):
        wx.adv.TaskBarIcon.__init__(self)
        self.SetIcon(wx.Icon(self.ICON), self.TITLE)  # 设置图标和标题
        self.Bind(wx.EVT_MENU, self.onAbout, id=self.ID_ABOUT)  # 绑定“关于”选项的点击事件
        self.Bind(wx.EVT_MENU, self.onExit, id=self.ID_EXIT)  # 绑定“退出”选项的点击事件
        # self.Bind(wx.EVT_MENU, self.onShowWeb, id=self.ID_SHOW_WEB)  # 绑定“显示页面”选项的点击事件

    # “关于”选项的事件处理器
    def onAbout(self, event):
        wx.MessageBox('程序作者：Sirius \n最后更新日期：2020-12-4', "关于")

    # “退出”选项的事件处理器
    def onExit(self, event):
        wx.Exit()
        sys.exit(0)
    # “显示页面”选项的事件处理器
    def onShowWeb(self, event):
        pass

    # 创建菜单选项
    def CreatePopupMenu(self):
        menu = wx.Menu()
        for mentAttr in self.getMenuAttrs():
            menu.Append(mentAttr[1], mentAttr[0])
        return menu

    # 获取菜单的属性元组
    def getMenuAttrs(self):
        return [#('进入程序', self.ID_SHOW_WEB),
                ('关于', self.ID_ABOUT),
                ('退出', self.ID_EXIT)]


class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self)
        MyTaskBarIcon()#显示系统托盘图标


class MyApp(wx.App):
    def OnInit(self):
        MyFrame()
        return True

class CTkPrScrn:
    def __init__(self):
        self.__start_x, self.__start_y = 0, 0
        self.__scale = 1

        self.__win = tkinter.Tk()
        self.__win.attributes("-alpha", 0.4)  # 设置窗口半透明
        self.__win.attributes("-fullscreen", True)  # 设置全屏
        self.__win.attributes("-topmost", True)  # 设置窗口在最上层

        self.__width, self.__height = self.__win.winfo_screenwidth(), self.__win.winfo_screenheight()

        # 创建画布
        self.__canvas = tkinter.Canvas(self.__win, width=self.__width, height=self.__height, bg="white")

        self.__win.bind('<Button-1>', self.xFunc1)  # 绑定鼠标左键点击事件
        self.__win.bind('<ButtonRelease-1>', self.xFunc1)  # 绑定鼠标左键点击释放事件
        self.__win.bind('<B1-Motion>', self.xFunc2)  # 绑定鼠标左键点击移动事件
        # self.__win.bind('<Escape>', lambda e: self.__win.destroy())  # 绑定Esc按键退出事件

        user32 = ctypes.windll.user32
        gdi32 = ctypes.windll.gdi32
        dc = user32.GetDC(None)
        widthScale = gdi32.GetDeviceCaps(dc, 8)  # 分辨率缩放后的宽度
        # heightScale = gdi32.GetDeviceCaps(dc, 10)  # 分辨率缩放后的高度
        width = gdi32.GetDeviceCaps(dc, 118)  # 原始分辨率的宽度
        # height = gdi32.GetDeviceCaps(dc, 117)  # 原始分辨率的高度
        self.__scale = width / widthScale
        self.__win.mainloop()  # 窗口持久化
    def xFunc1(self, event):
        # print(f"鼠标左键点击了一次坐标是:x={g_scale * event.x}, y={g_scale * event.y}")
        if event.state == 8:  # 鼠标左键按下
            self.__start_x, self.__start_y = event.x, event.y
        elif event.state == 264:  # 鼠标左键释放
            if event.x == self.__start_x or event.y == self.__start_y:
                return

            self.__win.update()
            # sleep(0.5)
            self.__win.destroy()
            sx = min(self.__scale * self.__start_x,self.__scale * event.x)
            ex = max(self.__scale * self.__start_x,self.__scale * event.x)
            sy = min(self.__scale * self.__start_y,self.__scale * event.y)
            ey = max(self.__scale * self.__start_y,self.__scale * event.y)
            img = ImageGrab.grab((sx, sy,ex,ey))
            img_bytes = io.BytesIO()
            img.save(img_bytes, format="PNG")
            self.image_bin = img_bytes.getvalue()
    def xFunc2(self, event):
        # print(f"鼠标左键点击了一次坐标是:x={self.__scale * event.x}, y={self.__scale * event.y}")
        if event.x == self.__start_x or event.y == self.__start_y:
            return
        self.__canvas.delete("prscrn")
        self.__canvas.create_rectangle(self.__start_x, self.__start_y, event.x, event.y,
                                       fill='black', outline='red', tag="prscrn")
        # 包装画布
        self.__canvas.pack()


def OCR(APP_ID, API_KEY, SECRET_KEY,image_bin):
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    options = {}
    options["detect_direction"] = "true"
    options["probability"] = "true"
    return client.basicAccurate(image_bin, options)['words_result']


""" 你的 APPID AK SK """
cf = configparser.ConfigParser()
cf.read("api.conf")
APP_ID = cf.get("default", "APP_ID")
API_KEY = cf.get("default", "API_KEY")
SECRET_KEY = cf.get("default", "SECRET_KEY")

def 通知(title,msg,icon_path,duration):
    try:
        ToastNotifier().show_toast(title=title, msg=msg,
                     icon_path=icon_path,duration=duration)
    except:
        pass

def CTkPrScrn_OCR():
    toast = ToastNotifier()

    try:
        image = CTkPrScrn()
        image_bin = image.image_bin
    except Exception as e:
        # print("截图出错\n" + str(e))
        _thread.start_new_thread(通知, ("截图出错", str(e), r"ocr.ico", 3))
        # toast.show_toast(title="截图出错", msg=str(e),
        #                  icon_path=r"ocr.ico", duration=3)
    else:
        try:
            returnresult=OCR(APP_ID, API_KEY, SECRET_KEY, image_bin)
            result = ""
            for line in returnresult:
                result += line['words'] + "\n"
            pyperclip.copy(result)
            # print("识别结果已经复制到剪切板")
            _thread.start_new_thread(通知, ("识别结果已经复制到剪切板", result, r"ocr.ico", 3))
            # toast.show_toast(title="识别结果已经复制到剪切板", msg=result,
            #                  icon_path=r"ocr.ico", duration=3)
        except Exception as e:
            # print("OCR出错\n" + str(e))
            _thread.start_new_thread(通知, ("OCR出错",str(e),r"ocr.ico",15))
            # toast.show_toast(title="OCR出错", msg="str(e)",
            #                  icon_path=r"ocr.ico", duration=3)


def tuopan(a):
    app = MyApp()
    app.MainLoop()

_thread.start_new_thread( tuopan, (1 ,) )

keyboard.add_hotkey('alt+o', CTkPrScrn_OCR)
keyboard.wait()




