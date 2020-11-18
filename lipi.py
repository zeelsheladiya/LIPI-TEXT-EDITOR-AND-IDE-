
# LIPI TEXT EDITOR AND IDE
# AUTHOR : ZEEL SHELADIYA , MIHIR SURATI , SAMIP , SOMPRAKASH PRADHAN

import wx
import sys
import os
import wx.lib.agw.flatnotebook as fnb


class Tab(wx.Panel):
    # Initialize Tab
    def __init__(self, parent):
        # Initialize wxPanel
        wx.Panel.__init__(self, parent=parent)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)

        # create text control in tab
        self.text_control = wx.TextCtrl(self, style=wx.TE_MULTILINE|wx.TE_RICH2)

        # set focus to text editor canvas
        self.text_control.SetFocus

        # set font size and family
        self.font = wx.Font(15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, True)

        self.text_control.SetFont(self.font)
        self.sizer.Add(self.text_control, -1, wx.EXPAND)

        # set text colour
        self.text_control.SetForegroundColour(wx.BLACK)

        # set background colour
        self.text_control.SetBackgroundColour(wx.WHITE)

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
    def __init__(self,parent=None):

        # initialize wxframe
        wx.Frame.__init__(self,None,wx.ID_ANY, "LIPI IDE", size=(800,600))

        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel.SetSizer(self.sizer)

        # create the notebook
        self.notebook = fnb.FlatNotebook(self.panel)
        self.notebook.SetFont(wx.Font(15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, True))

        self.notebook.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.on_tab_change)

        # call the hight-level setup function
        self.SetupEditor()

    def SetupEditor(self):
        # Setup the default tab
        self.SetupDefaultTab()

        # Setup the menu bar
        self.SetupMenuBar()

        # Setup Toolbar
        self.SetupToolBar()

        # Setup Keyboard shortcuts
        self.SetupKeyboardShortcuts()

        # Create the status bar
        self.CreateStatusBar(2)
        self.StatusBar.SetStatusWidths([-5, -1])
        self.StatusBar.SetBackgroundColour((220, 220, 220))
        self.StatusBar.SetStatusText("", 0)
        self.StatusBar.SetStatusText("", 1)

        # Open editor maximized
        self.Maximize()
        self.Layout()

    # Function to setup default tab
    def SetupDefaultTab(self):
        # Create the default tab
        self.default_tab = Tab(self.notebook)
        self.notebook.AddPage(self.default_tab, "Untitled")
        self.sizer.Add(self.notebook, 1, wx.EXPAND | wx.ALL)

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
        self.Bind(wx.EVT_MENU,self.OnCloseTab,id=self.keyboard_CLOSE_TAB)

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
        #setup toolbar here
        #self.toolbar = self.CreateToolBar()
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
        self.get_filetype(new_tab.pathname, new_tab.filetype)

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
                # Check if a new tabe needs to be created to display contents of opened file
                if (self.notebook.GetPageCount() == 1
                        and self.notebook.GetCurrentPage().text_control.GetValue() == ""):
                    self.notebook.GetCurrentPage().text_control.SetValue(filehandle.read())
                    self.notebook.GetCurrentPage().filename = filename
                    self.notebook.GetCurrentPage().directory = directory
                    self.notebook.GetCurrentPage().pathname = pathname
                    self.notebook.GetCurrentPage().filetype = filetype
                    self.get_filetype(self.notebook.GetCurrentPage().pathname, self.notebook.GetCurrentPage().filetype)

                    self.notebook.GetCurrentPage().last_save = self.notebook.GetCurrentPage().text_control.GetValue()

                    self.notebook.GetCurrentPage().saved = True
                else:
                    new_tab = Tab(self.notebook)
                    new_tab.filename = filename
                    new_tab.directory = directory
                    new_tab.pathname = pathname
                    new_tab.filetype = filetype
                    self.get_filetype(new_tab.pathname, new_tab.filetype)

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
                    self.get_filetype(pathname, filetype)
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
                self.get_filetype(pathname, filetype)
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
    def on_tab_change(self, e):
        current_page = self.notebook.GetCurrentPage()
        self.get_filetype(current_page.pathname, current_page.filetype)
        e.Skip()

    # Displaying file type in status-bar
    def get_filetype(self, pathname, filetype):

        if filetype != '':
            filetype = pathname.split('.')

            switcher = {
                'py': 'Python',
                'c': 'C',
                'cpp': 'C++',
                'txt': 'Text',
                'doc': 'Word',
                'docx': 'Word',
                'html': 'HTML',
                'css': 'CSS',
                'js': 'JavaScript',
                'php': 'PHP',
                'pdf': 'PDF'
            }

            ftype = switcher.get(filetype[1], "." + filetype[1])

            self.StatusBar.SetStatusText(ftype + " File", 1)
        else:
            self.StatusBar.SetStatusText("", 1)


if __name__ == "__main__":
    # Create a wx App
    app = wx.App(False)
    # Create the editor frame
    frame = Frame()
    # Show the frame
    frame.Show()
    # Start the mainloop
    app.MainLoop()