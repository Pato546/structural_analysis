import wx

# from wx.lib.floatcanvas import FloatCanvas
# from wx.lib.pdfviewer.viewer import pdfViewer


ICON_DIR = r'icons\light_icons\png\1x'


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
        super().__init__(*args, **kwargs, title="SASP")

        icon = wx.Icon(r'icons\computer.ico')

        self.SetIcon(icon)

        self.menubar()
        self.toolbar()
        self.statusbar()

        self.SetInitialSize((900, 600))

    def menubar(self):
        menubar = wx.MenuBar()

        # File
        file_menu = wx.Menu()

        new = file_menu.Append(wx.ID_NEW, "&New")
        new.SetBitmap(wx.Bitmap(f'{ICON_DIR}\\new.png'))

        file_menu.AppendSeparator()

        open_ = file_menu.Append(wx.ID_OPEN, "&Open")
        open_.SetBitmap(wx.Bitmap(f'{ICON_DIR}\\open.png'))

        save = file_menu.Append(wx.ID_SAVE, "&Save")
        save.SetBitmap(wx.Bitmap(f'{ICON_DIR}\\save.png'))

        save_as = file_menu.Append(wx.ID_SAVEAS, "&Save As")
        save_as.SetBitmap(wx.Bitmap(f'{ICON_DIR}\\save-as.png'))

        file_menu.AppendSeparator()

        exit_ = file_menu.Append(wx.ID_EXIT, "&Exit")
        exit_.SetBitmap(wx.Bitmap(f'{ICON_DIR}\\exit.png'))

        # View
        view_menu = wx.Menu()
        zoom_in = view_menu.Append(wx.ID_ZOOM_IN, "Zoom &In")
        zoom_in.SetBitmap(wx.Bitmap(f'{ICON_DIR}\\zoom-in.png'))

        zoom_out = view_menu.Append(wx.ID_ZOOM_OUT, "Zoom &Out")
        zoom_out.SetBitmap(wx.Bitmap(f'{ICON_DIR}\\zoom-out.png'))

        view_menu.AppendSeparator()

        define_grid = view_menu.Append(wx.ID_ANY, "&Define Grid")
        define_grid.SetBitmap(wx.Bitmap(f'{ICON_DIR}\\grid.png'))

        show_grid = view_menu.Append(wx.ID_ANY, "&Show Grid")

        show_axes = view_menu.Append(wx.ID_ANY, "&Show Axes")
        show_axes.SetBitmap(wx.Bitmap(f'{ICON_DIR}\\coordinates-2d-xy.png'))

        view_menu.AppendSeparator()

        refresh_window = view_menu.Append(wx.ID_ANY, "Refresh Window")
        refresh_window.SetBitmap(wx.Bitmap(f'{ICON_DIR}\\button-refresh.png'))

        refresh_view = view_menu.Append(wx.ID_ANY, "Refresh View")

        # Structure
        structure_menu = wx.Menu()
        node = structure_menu.Append(wx.ID_ANY, "Node")
        member = structure_menu.Append(wx.ID_ANY, "Member")
        structure_menu.AppendSeparator()
        cross_section = structure_menu.Append(wx.ID_ANY, "Cross Sections")

        # Define
        define_menu = wx.Menu()
        load = define_menu.Append(wx.ID_ANY, "Load on Joint/Member")
        define_menu.AppendSeparator()
        load_case = define_menu.Append(wx.ID_ANY, "Load Case")
        load_combination = define_menu.Append(wx.ID_ANY, "Load Combination")

        # Analyze
        analyze_menu = wx.Menu()
        run = analyze_menu.Append(wx.ID_ANY, "Run Static Analysis")
        tabulate = analyze_menu.Append(wx.ID_ANY, "Tabulate Static Analysis Results")

        # Design
        design_menu = wx.Menu()
        steel_design = design_menu.Append(wx.ID_ANY, "Steel Frame Design")
        concrete_design = design_menu.Append(wx.ID_ANY, "Concrete Frame Design")

        # Display
        draw_menu = wx.Menu()
        bending_moment = draw_menu.Append(wx.ID_ANY, "Bending Moment")
        shear_force = draw_menu.Append(wx.ID_ANY, "Shear Force")
        reaction = draw_menu.Append(wx.ID_ANY, "Reactions")
        deflection = draw_menu.Append(wx.ID_ANY, "Deflection")

        # Options
        options_menu = wx.Menu()
        mode = wx.Menu()
        student = mode.AppendRadioItem(wx.ID_ANY, "Student")
        professional = mode.AppendRadioItem(wx.ID_ANY, "Professional")
        options_menu.AppendMenu(wx.ID_ANY, "Mode", mode)
        theme = wx.Menu()
        light = theme.AppendRadioItem(wx.ID_ANY, "Light")
        dark = theme.AppendRadioItem(wx.ID_ANY, "Dark")
        options_menu.AppendMenu(wx.ID_ANY, "Themes", theme)

        # Tools
        tools_menu = wx.Menu()

        # Help
        help_menu = wx.Menu()
        quick_intro = help_menu.Append(wx.ID_ANY, "Quick Introduction")
        about = help_menu.Append(wx.ID_ANY, "About")

        list_of_menus = (
            (file_menu, "&File"),
            (view_menu, "&View"),
            (structure_menu, "&Structure"),
            (define_menu, "Define"),
            (analyze_menu, "&Analyze"),
            (design_menu, "Design"),
            (draw_menu, "Draw"),
            (options_menu, "&Options"),
            (tools_menu, "&Tools"),
            (help_menu, "&Help"),
        )

        for menu, title in list_of_menus:
            menubar.Append(menu=menu, title=title)

        self.SetMenuBar(menubar)

    def toolbar(self):
        self.CreateToolBar()

    def statusbar(self):
        self.CreateStatusBar()


if __name__ == "__main__":
    app = wx.App()
    win = MainWindow(None)
    win.Show()

    app.MainLoop()
