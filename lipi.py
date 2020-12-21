# LIPI TEXT EDITOR AND IDE
# AUTHOR : ZEEL SHELADIYA , MIHIR SURATI , SAMIP , SOMPRAKASH PRADHAN

import wx
import sys
import os
import wx.lib.agw.flatnotebook as fnb
import wx.stc as stc


class Tab(wx.Panel):
    # Initialize Tab
    def __init__(self, parent):

        self.leftMargin = 50;

        # Initialize wxPanel
        wx.Panel.__init__(self, parent=parent)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)

        # create text control in tab
        global text_control
        text_control = stc.StyledTextCtrl(self, style=wx.TE_MULTILINE | wx.TE_WORDWRAP)

        # set focus to text editor canvas
        text_control.SetFocus()

        # set font size and family and also change font vaue from self.notebook.Setfont
        self.font = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, True)

        text_control.SetViewWhiteSpace(False)
        text_control.SetMargins(5,0)
        text_control.SetMarginType(1,stc.STC_MARGIN_NUMBER)
        text_control.SetMarginWidth(1,self.leftMargin)

        # lune controll conlor fore = text color and back = background color
        text_control.StyleSetSpec(stc.STC_STYLE_LINENUMBER,'fore:#000000,back:#e8e8e8')

        text_control.StyleSetFont(1,self.font)

        text_control.Bind(wx.EVT_KEY_UP, Frame.UpdateLineCol)
        text_control.Bind(wx.EVT_LEFT_UP, Frame.UpdateLineCol)

        #text_control.SetFont(self.font)
        self.sizer.Add(text_control, -1, wx.EXPAND)

        # set text colour
        text_control.SetForegroundColour(wx.BLACK)

        # set background colour
        text_control.SetBackgroundColour(wx.WHITE)

        # Filename of tab
        self.filename = ""

        # Directory of tab
        self.directory = ""

        # is the tab file save?
        self.saved = ""

        # Content from the last save point
        self.last_save = ""

        # File type
        self.filetype = ""

        # File Path
        self.pathname = ""

class Frame(wx.Frame):
    # initialize Frame
    def __init__(self, parent=None):

        # initialize wxframe
        wx.Frame.__init__(self, None, wx.ID_ANY, "LIPI IDE", size=(800, 600))

        #self.Bind(wx.EVT_SIZE,self.SetFileExplorerSize)
        #self.Bind(wx.EVT_SIZE,self.SetFileExplorerSize)

        self.panel = wx.Panel(self)
        # self.panel.SetPosition((200,0))
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.panel.SetSizer(self.sizer, False)

        # create the notebook
        self.notebook = fnb.FlatNotebook(self.panel)
        self.notebook.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, True))

        self.notebook.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnTabChange)
        # call the hight-level setup function
        self.SetupEditor()

    def SetupEditor(self):

        # Setup the default tab
        self.SetupDefaultTab()

        # setup the file explorer
        self.SetFileExplorer()

        # Setup the menu bar
        self.SetupMenuBar()

        # Setup Toolbar
        self.SetupToolBar()

        # Setup Keyboard shortcuts
        self.SetupKeyboardShortcuts()

        # Create the status bar
        self.SetStatusBar()
        #StatusBarLineColumn()


        # Open editor maximized
        self.Maximize()
        self.Layout()

    def SetStatusBar(self):
        global StatusBar
        StatusBar = self.CreateStatusBar(2)
        StatusBar.SetStatusWidths([-5, -1])
        StatusBar.SetBackgroundColour((220, 220, 220))
        StatusBar.SetStatusText("", 0)
        StatusBar.SetStatusText("", 1)

    # status bar line and column
    def UpdateLineCol(self,e=wx.EVT_KEY_UP):
        current = text_control
        line = current.GetCurrentLine() + 1
        col = current.GetColumn(current.GetCurrentPos())
        stat = "  Line %s, column %s " % (line, col)
        #print(line)
        Frame.SetTextInStatusbar(self,stat)

    #set text to status bar at 0 poition
    def SetTextInStatusbar(self,str):
        StatusBar.SetStatusText(str, 0)

    # file explorer control
    def SetFileExplorer(self):
        self.file_explorer_x, self.file_explorer_y = wx.Frame.GetSize(self)
        self.file_explorer = wx.GenericDirCtrl(self.panel, -1, size=(200, self.file_explorer_y-100),
                                               style=wx.DIRCTRL_3D_INTERNAL | wx.DIRCTRL_MULTIPLE | wx.DIRCTRL_EDIT_LABELS | wx.EXPAND)
        self.file_explorer.Bind(wx.EVT_DIRCTRL_FILEACTIVATED, self.OnFileSelectedFromExp)

    # file explorer control for size change
    def SetFileExplorerSize(self, e):
        self.file_explorer_x, self.file_explorer_y = wx.Frame.GetSize(self)
        self.file_explorer.SetSize((200,self.file_explorer_y-100))
        self.file_explorer.Bind(wx.EVT_DIRCTRL_FILEACTIVATED, self.OnFileSelectedFromExp)

    # Function to setup default tab
    def SetupDefaultTab(self):
        # Create the default tab
        self.default_tab = Tab(self.notebook)
        self.notebook.AddPage(self.default_tab, "Untitled")
        self.sizer.Add(self.notebook, 1, wx.EXPAND | wx.LEFT, 200)
        # self.panel.SetSizer(self.sizer)

    # function to setup menubar
    def SetupMenuBar(self):
        # Create the menubar
        self.menubar = wx.MenuBar()
        self.menu_FILE = wx.Menu()

        self.menu_NEW = self.menu_FILE.Append(wx.ID_ANY, '&New\tCtrl+N', "Create a New Tab")
        self.menu_OPEN = self.menu_FILE.Append(wx.ID_OPEN, '&Open\tCtrl+O', "Open a File")
        self.menu_FILE.AppendSeparator()
        self.menu_SAVE = self.menu_FILE.Append(wx.ID_SAVE, '&Save\tCtrl+S', "Save a File")
        self.menu_SAVE_AS = self.menu_FILE.Append(wx.ID_SAVEAS, 'Save As...', "Save File As")
        self.menu_FILE.AppendSeparator()
        self.menu_EXIT = self.menu_FILE.Append(wx.ID_EXIT, '&Quit\tCtrl+Q', "Close the Editor")

        self.menubar.Append(self.menu_FILE, "&File")
        self.SetMenuBar(self.menubar)

        self.Bind(wx.EVT_MENU, self.OnNewTab, self.menu_NEW)
        self.Bind(wx.EVT_MENU, self.OnOpen, self.menu_OPEN)
        self.Bind(wx.EVT_MENU, self.OnSave, self.menu_SAVE)
        self.Bind(wx.EVT_MENU, self.OnSaveAs, self.menu_SAVE_AS)
        self.Bind(wx.EVT_MENU, self.OnExit, self.menu_EXIT)

    # Function to setup keyboard shortcuts
    def SetupKeyboardShortcuts(self):
        # Setup Keyboard shortcuts
        self.keyboard_CLOSE_TAB = wx.NewId()
        self.Bind(wx.EVT_MENU, self.OnCloseTab, id=self.keyboard_CLOSE_TAB)

        self.accelerator_table = wx.AcceleratorTable([(wx.ACCEL_CTRL,
                                                       ord('N'),
                                                       self.menu_NEW.GetId()),
                                                      (wx.ACCEL_CTRL,
                                                       ord('O'),
                                                       self.menu_OPEN.GetId()),
                                                      (wx.ACCEL_CTRL,
                                                       ord('S'),
                                                       self.menu_SAVE.GetId()),
                                                      (wx.ACCEL_CTRL,
                                                       ord('W'),
                                                       self.keyboard_CLOSE_TAB)])

        self.SetAcceleratorTable(self.accelerator_table)

    # Function to setup toolbar
    def SetupToolBar(self):
        # setup toolbar here
        # self.toolbar = self.CreateToolBar()
        pass

    # Suppress all standard output
    def SuppressOutput(self):
        devnull = open(os.devnull, 'w')
        sys.stdout = devnull

    # Function to handle new tab
    def OnNewTab(self, e):
        new_tab = Tab(self.notebook)
        new_tab.SetFocus()
        self.notebook.AddPage(new_tab, "Untitled", select=True)
        new_tab.filetype = ''
        new_tab.pathname = ''
        self.get_filetype(new_tab.filetype)

    def OnOpen(self, e):
        # Create a File Dialog asking for the file to open
        try:
            dialog = wx.FileDialog(self,
                                   "Choose a File",
                                   self.notebook.GetCurrentPage().directory,
                                   "",
                                   "*",
                                   wx.FD_OPEN)
            if dialog.ShowModal() == wx.ID_OK:
                # Get the filename & directory
                filename = dialog.GetFilename()
                directory = dialog.GetDirectory()
                pathname = wx.FileDialog.GetPath(dialog)
                filetype = os.path.splitext(pathname)

                # Open the right file
                filehandle = open(os.path.join(directory, filename), 'r')
                # Check if a new tab needs to be created to display contents of opened file
                if (self.notebook.GetPageCount() == 1
                        and self.notebook.GetCurrentPage().text_control.GetValue() == ""):
                    self.notebook.GetCurrentPage().text_control.SetValue(filehandle.read())
                    self.notebook.GetCurrentPage().filename = filename
                    self.notebook.GetCurrentPage().directory = directory
                    self.notebook.GetCurrentPage().pathname = pathname
                    self.notebook.GetCurrentPage().filetype = filetype
                    self.get_filetype(self.notebook.GetCurrentPage().filetype)

                    self.notebook.GetCurrentPage().last_save = self.notebook.GetCurrentPage().text_control.GetValue()

                    self.notebook.GetCurrentPage().saved = True
                else:
                    new_tab = Tab(self.notebook)
                    new_tab.filename = filename
                    new_tab.directory = directory
                    new_tab.pathname = pathname
                    new_tab.filetype = filetype
                    self.get_filetype(new_tab.filetype)

                    self.notebook.AddPage(new_tab, "Untitled", select=True)
                    wx.CallAfter(new_tab.SetFocus)
                    # Populate the tab with file contents
                    new_tab.text_control.SetValue(filehandle.read())
                    new_tab.last_save = new_tab.text_control.GetValue()
                    new_tab.saved = True
                # Set the tab name to be filename
                self.notebook.SetPageText(self.notebook.GetSelection(), filename)
                filehandle.close()
            dialog.Destroy()
        except:
            dlg = wx.MessageDialog(self, "Could not Open The File ", "Error", wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()

    def OnSave(self, e):

        try:
            # Grab the content to be saved
            save_as_file_contents = self.notebook.GetCurrentPage().text_control.GetValue()
            filehandle = open(os.path.join(self.notebook.GetCurrentPage().directory,
                                           self.notebook.GetCurrentPage().filename), 'w')
            filehandle.write(save_as_file_contents)
            filehandle.close()
            self.notebook.GetCurrentPage().last_save = save_as_file_contents
            self.notebook.GetCurrentPage().saved = True
        except:
            # Check if save is required
            if (self.notebook.GetCurrentPage().text_control.GetValue()
                    != self.notebook.GetCurrentPage().last_save):
                self.notebook.GetCurrentPage().saved = False

            # Check if Save should bring up FileDialog
            if (self.notebook.GetCurrentPage().saved == False
                    and self.notebook.GetCurrentPage().last_save == ""):
                dialog = wx.FileDialog(self,
                                       "Choose a file",
                                       self.notebook.GetCurrentPage().directory,
                                       "",
                                       "*",
                                       wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
                if dialog.ShowModal() == wx.ID_OK:
                    # Grab the content to be saved
                    save_as_file_contents = self.notebook.GetCurrentPage().text_control.GetValue()

                    # Open, Write & Close File
                    save_as_name = dialog.GetFilename()
                    save_as_directory = dialog.GetDirectory()
                    pathname = wx.FileDialog.GetPath(dialog)
                    filetype = os.path.splitext(pathname)
                    filehandle = open(os.path.join(save_as_directory, save_as_name), 'w')
                    filehandle.write(save_as_file_contents)
                    filehandle.close()
                    self.notebook.SetPageText(self.notebook.GetSelection(), save_as_name)
                    self.notebook.GetCurrentPage().filename = save_as_name
                    self.notebook.GetCurrentPage().directory = save_as_directory
                    self.notebook.GetCurrentPage().last_save = save_as_file_contents
                    self.notebook.GetCurrentPage().saved = True
                    self.notebook.GetCurrentPage().pathname = pathname
                    self.notebook.GetCurrentPage().filetype = filetype
                    self.get_filetype(filetype)
                dialog.Destroy()

    def OnSaveAs(self, e):
        try:
            dialog = wx.FileDialog(self,
                                   "Choose a file",
                                   self.notebook.GetCurrentPage().directory,
                                   "",
                                   "*.*",
                                   wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
            if dialog.ShowModal() == wx.ID_OK:
                # Grab the content to be saved
                save_as_file_contents = self.notebook.GetCurrentPage().text_control.GetValue()

                # Open, Write & Close File
                save_as_name = dialog.GetFilename()
                save_as_directory = dialog.GetDirectory()
                pathname = wx.FileDialog.GetPath(dialog)
                filetype = os.path.splitext(pathname)
                filehandle = open(os.path.join(save_as_directory, save_as_name), 'w')
                filehandle.write(save_as_file_contents)
                filehandle.close()
                self.notebook.SetPageText(self.notebook.GetSelection(), save_as_name)
                self.notebook.GetCurrentPage().filename = save_as_name
                self.notebook.GetCurrentPage().directory = save_as_directory
                self.notebook.GetCurrentPage().last_save = save_as_file_contents
                self.notebook.GetCurrentPage().saved = True
                self.notebook.GetCurrentPage().pathname = pathname
                self.notebook.GetCurrentPage().filetype = filetype
                self.get_filetype(filetype)
            dialog.Destroy()
        except:
            pass

    def OnCloseTab(self, e):
        # Check if there is only 1 tab open
        if self.notebook.GetPageCount() == 1:
            self.notebook.SetPageText(self.notebook.GetSelection(), "Untitled")
            self.notebook.GetCurrentPage().filename = ""
            self.notebook.GetCurrentPage().directory = ""
            self.notebook.GetCurrentPage().last_save = ""
            self.notebook.GetCurrentPage().saved = False
            if self.notebook.GetCurrentPage().text_control != None:
                self.notebook.GetCurrentPage().text_control.SetValue("")
            # wx.CallAfter(self.notebook.GetCurrentPage().SetFocus)
        else:
            self.notebook.DeletePage(self.notebook.GetSelection())

    # Quit Application
    def OnExit(self, e):
        self.Close(True)

    # On tab change -> getting filetype
    def OnTabChange(self, e):
        current_page = self.notebook.GetCurrentPage()
        self.get_filetype(current_page.filetype)
        e.Skip()

    # Displaying file type in status-bar
    def get_filetype(self, filetype):

        if filetype != '':
            switcher = {
                '.py': 'Python',
                '.c': 'C',
                '.cpp': 'C++',
                '.txt': 'Text',
                '.cs': 'C#',
                '.html': 'HTML',
                '.css': 'CSS',
                '.js': 'JavaScript',
                '.php': 'PHP',
                '.h': 'Header'
            }

            ftype = switcher.get(filetype[1], filetype[1])

            StatusBar.SetStatusText(ftype + " File", 1)
        else:
            StatusBar.SetStatusText("", 1)

    # Opening file while double-clicked or entered in file explorer
    def OnFileSelectedFromExp(self, e):
        try:
            pathname = self.file_explorer.GetPath()
            filetype = os.path.splitext(pathname)
            directory = os.path.dirname(pathname)
            filename = os.path.basename(pathname)

            filehandle = open(pathname, 'r')

            if (self.notebook.GetPageCount() == 1
                    and self.notebook.GetCurrentPage().text_control.GetValue() == ""):
                self.notebook.GetCurrentPage().text_control.SetValue(filehandle.read())
                self.notebook.GetCurrentPage().filename = filename
                self.notebook.GetCurrentPage().directory = directory
                self.notebook.GetCurrentPage().pathname = pathname
                self.notebook.GetCurrentPage().filetype = filetype
                self.get_filetype(self.notebook.GetCurrentPage().filetype)

                self.notebook.GetCurrentPage().last_save = self.notebook.GetCurrentPage().text_control.GetValue()

                self.notebook.GetCurrentPage().saved = True
            else:
                new_tab = Tab(self.notebook)
                new_tab.filename = filename
                new_tab.directory = directory
                new_tab.pathname = pathname
                new_tab.filetype = filetype
                self.get_filetype(new_tab.filetype)
                self.notebook.AddPage(new_tab, "Untitled", select=True)
                wx.CallAfter(new_tab.SetFocus)
                # Populate the tab with file contents
                new_tab.text_control.SetValue(filehandle.read())
                new_tab.last_save = new_tab.text_control.GetValue()
                new_tab.saved = True
            # Set the tab name to be filename
            self.notebook.SetPageText(self.notebook.GetSelection(), filename)

            filehandle.close()
        except:
            pass

if __name__ == "__main__":
    # Create a wx App
    app = wx.App(False)
    # Create the editor frame
    frame = Frame()
    # Show the frame
    frame.Show()
    # Start the mainloop
    app.MainLoop()