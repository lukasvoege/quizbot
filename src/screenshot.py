from PIL import ImageGrab
import win32gui

def screenshot():
    toplist, winlist = [], []
    def enum_cb(hwnd, results):
        winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
    win32gui.EnumWindows(enum_cb, toplist)

    windowlist = [(hwnd, title) for hwnd, title in winlist if 'memu' in title.lower()]
    print(windowlist)
    hwnd = windowlist[-1][0]

    win32gui.SetForegroundWindow(hwnd)
    bbox = win32gui.GetWindowRect(hwnd)
    img = ImageGrab.grab(bbox)
    width, height = img.size
    img.save('capture.jpg')

    print(bbox)
    print(f'width: {width} - height: {height}')

    return img