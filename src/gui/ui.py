import wx


# from wx.lib.floatcanvas import FloatCanvas
# from wx.lib.pdfviewer.viewer import pdfViewer


class ModelCanvas(wx.Panel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PDFViewer(wx.Panel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class TabControl(wx.Notebook):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class MainWindow(wx.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, title='SASP')

        self.toolbar()
        self.statusbar()

    def menubar(self):
        pass

    def toolbar(self):
        self.CreateToolBar()

    def statusbar(self):
        self.CreateStatusBar()


if __name__ == '__main__':
    app = wx.App()
    win = MainWindow(None)
    win.Show()

    app.MainLoop()
