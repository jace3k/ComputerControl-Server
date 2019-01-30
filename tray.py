import os
import sys
import wx
from wx.adv import TaskBarIcon

TRAY_ICON = 'icon.png'
TRAY_TOOLTIP = "Zdalne sterowanie"

APP = None


class Icon(TaskBarIcon):
    def __init__(self, pin):
        super(TaskBarIcon, self).__init__()
        self.set_icon(TRAY_ICON)
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.clicked)
        self.pin = pin

        self.ShowBalloon(
            'Uruchomiono serwer',
            'Użyj pinu {} aby połączyć się z komputerem.'.format(self.pin))
        print('Init ICON')

    def set_icon(self, path):
        icon = wx.Icon(wx.Bitmap(resource_path(path)))
        self.SetIcon(icon, TRAY_TOOLTIP)

    def clicked(self, event):
        print('clicked')

    def exit(self, event):
        wx.CallAfter(self.Destroy)
        os._exit(1)

    def CreatePopupMenu(self):
        print('Create Menu')
        menu = wx.Menu()
        item = wx.MenuItem(menu, -1, 'Wyłącz')
        menu.Bind(wx.EVT_MENU, self.exit, id=item.GetId())
        item_pin = wx.MenuItem(menu, -1, 'PIN: {}'.format(self.pin))
        menu.Append(item_pin)
        menu.AppendSeparator()
        menu.Append(item)
        return menu


def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def create_icon(pin):
    global APP
    print("Setup tray")
    APP = wx.App()
    return Icon(pin)


def main_loop():
    print('Main loop')
    APP.MainLoop()
