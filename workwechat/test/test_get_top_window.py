from win32api import GetSystemMetrics
import win32gui, win32print,win32con
Screen_dict = {"wide": GetSystemMetrics(win32con.SM_CXSCREEN), "high": GetSystemMetrics(win32con.SM_CYSCREEN)}
import time
from pywinauto import Application
from airtest.aircv import imread,get_resolution,show_origin_size
import pywinauto


def get_real_resolution():
    """获取真实的分辨率"""
    hDC = win32gui.GetDC(0)
    wide = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
    high = win32print.GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)
    return {"wide": wide, "high": high}

class Test():
    def __init__(self):
        self.scale = round(get_real_resolution()['wide'] / Screen_dict['wide'], 2)

    def connect_window_before_shot(self,title):
        '''
        connect to target window before screen shot it.
        (Exactly due to solve the connect too many times lead to window breakdown.)
        '''
        app = Application().connect(title_re=title)
        hwin = app.top_window()
        hwin.set_focus()
        return hwin
    
    def send_keys(self, keys):
        """
        输入keys中的内容，如果是'\n'则意为回车发送
        """
        if keys in ('\n',):
            pywinauto.keyboard.SendKeys('\n', with_newlines=True)
            return
        # parsed_keys = self.parse_key(keys)
        parsed_keys = keys
        pywinauto.keyboard.SendKeys(parsed_keys, with_spaces=True)
        return False if parsed_keys == keys else True

    def shot_target_window(self,title,hwin,file_name=None):
        '''
        connect to the target window and shotscreen.
        '''
        try:
            if file_name is not None:
                self.file_name = title+'_'+file_name+'_'+str(round(time.time() * 1000))
            else:
                self.file_name = title + '_' + str(round(time.time() * 1000))
            file_path =r'log\\%s.png' %self.file_name
            img = hwin.capture_as_image().save(file_path)
            return file_path
        except Exception as e:
            print(f'some error occured when connect to the {title} window,detail info:{e}')
            return None

    def get_img_size(self,file_path):
        '''
        give a opposite img file path,return img size.
        '''
        img = imread(filename=file_path)
        # show_origin_size(img)
        h,w = get_resolution(img)
        return h,w

    def check_window_status(self):
        '''
        check if the target window have been openned,if exists,directly doing task.
        '''
        hwin = self.connect_window_before_shot(title='企业微信')
        file = self.shot_target_window(title='企业微信',hwin=hwin)
        h,w = self.get_img_size(file_path=file)
        print(f'\n\t —— 当前顶部窗口大小为{h}x{w},屏幕缩放大小为{self.scale},真实窗口大小为{h//self.scale}x{w//self.scale}——')
        # self.send_keys('%{F4}')

    def get_top_hwin(self):
        hwin = self.connect_window_before_shot(title='企业微信')

        print('0.',hwin.print_control_identifiers())
        print('1.',hwin)
        print('2.',hwin.window_text())
        print('3.',hwin.rectangle())
        print('4.',hwin.parent())
        print('5.',hwin.root())
        print('6.',hwin.set_focus())
        print('8.',hwin.top_level_parent())
        print('7.',hwin.texts())
        print('9.',hwin.hide_from_taskbar())   #从Windows任务栏隐藏对话框
        print('10.',hwin.is_in_taskbar())   #检查对话框是否显示在Windows任务栏中
        print('11.',hwin.show_in_taskbar())      #在Windows任务栏中显示该对话框
        print('12.',hwin.class_name())
        print('13.',hwin.friendly_class_name())
        print('14.',hwin.descendants())
        print('15.',hwin.get_properties())      #获取属性字典        
        print('16.',type(hwin.client_rects()[0]))      #获取属性字典
        print(hwin.client_rects()[0].top)
        print(hwin.client_rects()[0].bottom)
        print(hwin.client_rects()[0].left)
        print(hwin.client_rects()[0].right)

if __name__ == "__main__":
    T =Test()
    T.get_top_hwin()