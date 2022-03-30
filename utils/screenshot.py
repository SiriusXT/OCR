from PIL import ImageGrab
from  tkinter import Canvas,Tk
import ctypes
import base64
from io import BytesIO
import threading
class Screenshot():
    def __init__(self):
        self.__start_x, self.__start_y = 0, 0
        self.__scale = 1
        self.__win = Tk()

        # self.__win.iconbitmap(default=os.path.expanduser('~')+r'/OCRP/icon/icon.ico')
        self.__win.title("正在截图")
        self.__win.attributes("-alpha", 0.5)  # 设置窗口半透明
        self.__win.attributes("-fullscreen", True)  # 设置全屏
        self.__win.attributes("-topmost", True)  # 设置窗口在最上层
        self.__width, self.__height = self.__win.winfo_screenwidth(), self.__win.winfo_screenheight()
        # 创建画布
        self.__canvas = Canvas(self.__win, width=self.__width, height=self.__height, bg="white")
        self.__win.bind('<Button-1>', self.xFunc1)  # 绑定鼠标左键点击事件
        self.__win.bind('<ButtonRelease-1>', self.xFunc3)  # 绑定鼠标左键点击释放事件
        self.__win.bind('<B1-Motion>', self.xFunc2)  # 绑定鼠标左键点击移动事件
        self.__win.bind('<Escape>', self.esc)  # 绑定Esc按键退出事件

        user32 = ctypes.windll.user32
        gdi32 = ctypes.windll.gdi32
        dc = user32.GetDC(None)
        widthScale = gdi32.GetDeviceCaps(dc, 8)  # 分辨率缩放后的宽度
        width = gdi32.GetDeviceCaps(dc, 118)  # 原始分辨率的宽度
        self.__scale = width / widthScale
        self.__win.mainloop()  # 窗口持久化
    def esc(self,event):
        self.__win.destroy()
    def xFunc3(self,event):
        if event.x == self.__start_x or event.y == self.__start_y:
            self.__win.destroy()
            return
        self.__win.update()
        self.__win.destroy()
        sx = min(self.__scale * self.__start_x, self.__scale * event.x)
        ex = max(self.__scale * self.__start_x, self.__scale * event.x)
        sy = min(self.__scale * self.__start_y, self.__scale * event.y)
        ey = max(self.__scale * self.__start_y, self.__scale * event.y)
        img = ImageGrab.grab((sx-1, sy-1, ex+1, ey+1))
        # self.image_bin = img
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        self.img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')

    def xFunc1(self, event):
        self.__start_x, self.__start_y = event.x, event.y
    def xFunc2(self, event):
        if event.x == self.__start_x or event.y == self.__start_y:
            return
        self.__canvas.delete("prscrn")
        self.__canvas.create_rectangle(self.__start_x, self.__start_y, event.x, event.y,
                                       fill='black', outline='red', tag="prscrn")
        # 包装画布
        self.__canvas.pack()

    def getBase64(self):
        return self.img_str

class screenshotThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        self.img_str = Screenshot().getBase64()
    def getBase64(self):
        return self.img_str