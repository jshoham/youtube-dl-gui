__author__ = 'jshoham'

import argparse
import sys
import Tkinter as Tk
import tkFileDialog
import ttk
import youtubedl


class YoutubeDLApp(Tk.Tk):
    def __init__(self, *args, **kwargs):
        Tk.Tk.__init__(self, *args, **kwargs)
        self.dlpath = Tk.StringVar()
        self.dlpath.set(youtubedl.default_path)

        self.title("YoutubeDL")
        self.geometry('500x250')
        self.resizable(width=False, height=False)

        container = Tk.Frame(self, background='white')
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.frames[StartPage] = StartPage(container, self)
        self.frames[OptionsPage] = OptionsPage(container, self)

        self.show_frame(StartPage)

    def show_frame(self, controller):
        frame = self.frames[controller]
        frame.tkraise()


class StartPage(Tk.Frame):
    class StdoutRedirector(object):
        def __init__(self,widget, oldstdout=None):
            self.widget = widget
            self.oldstdout = oldstdout

        def write(self,string):
            self.widget.insert(Tk.END,string)
            self.widget.see(Tk.END)
            if self.oldstdout:
                self.oldstdout.write(string)

        def flush(self):
            pass

    def __init__(self, parent, controller):
        Tk.Frame.__init__(self, parent, background='white')
        self.grid(row=0, column=0, sticky=Tk.NSEW)
        self.grid_columnconfigure(0, weight=1)

        options_button = ttk.Button(self, text='...', width=3,
                                    command=lambda: controller.show_frame(OptionsPage))
        options_button.grid(row=0, column=2, sticky=Tk.NE)
        spacer = Tk.Frame(self)
        spacer.grid(row=1, column=0, columnspan=3, pady=20)
        label = Tk.Label(self, text="URL to download:", background='white')
        label.grid(row=2, column=0, columnspan=3)
        self.url_entry = ttk.Entry(self, width=50)
        self.url_entry.grid(row=3, column=0, columnspan=3)
        go_button = ttk.Button(self, text='Go', command=lambda: self.go_button_action(controller))
        go_button.grid(row=4, column=0, columnspan=3, pady=5)

        # Audio checkbox
        s = ttk.Style()
        s.configure('TCheckbutton', background='white')
        self.audio_opt = Tk.BooleanVar()
        audio_checkbox = ttk.Checkbutton(self, text='extract audio', variable=self.audio_opt, style='TCheckbutton',
                                         command=lambda: self.audio_checkbox_action(controller))
        audio_checkbox.grid(row=5, column=0, columnspan=3)
        # default audio to ON
        self.audio_opt.set(True)
        self.audio_checkbox_action(controller)

        #console display
        console_display = Tk.Text(self, height=5)
        console_display.grid(row=6, column=0, columnspan=3)

        sys.stdout = self.StdoutRedirector(console_display, sys.stdout)

    def audio_checkbox_action(self, controller):
        if self.audio_opt.get():
            print 'Extract audio turned on (mp3)'
        else:
            print 'Extract audio turned off'


    def go_button_action(self, controller):
        options = argparse.Namespace()
        options.audio = self.audio_opt
        options.path = controller.dlpath.get()
        options.url = self.url_entry.get()
        print options.path
        if not options.url:
            print 'No url given.'
        else:
            youtubedl.run(options)
            print 'Finished.'



class OptionsPage(Tk.Frame):
    def __init__(self, parent, controller):
        Tk.Frame.__init__(self, parent, background='white')
        self.grid(row=0, column=0, sticky=Tk.NSEW)
        self.grid_columnconfigure(0, weight=1)

        home_button = ttk.Button(self, text='Home',
                                 command=lambda: controller.show_frame(StartPage))
        home_button.grid(row=0, column=2, sticky=Tk.NE)

        subframe = Tk.Frame(self, background='white')
        subframe.grid(row=1, column=0, columnspan=3, sticky=Tk.NSEW)

        # displays the download path option as shown below:
        # Save location: <dl_path> [change]
        page_label = Tk.Label(subframe, text='Options', background='white')
        page_label.grid(row=0, column=0, columnspan=4)

        dlpath_label = Tk.Label(subframe, text='Save location:', background='white')
        dlpath_label.grid(row=1, column=0, ipadx=10, sticky=Tk.E)
        dlpath_actual_label = ttk.Label(subframe, textvariable=controller.dlpath, width=40,
                                       anchor=Tk.W, relief=Tk.GROOVE, background='white')
        dlpath_actual_label.grid(row=1, column=1)
        dlpath_button = ttk.Button(subframe, text='Change...',
                                   command=lambda: self.dlpath_button_action(controller))
        dlpath_button.grid(row=1, column=2)

    def dlpath_button_action(self, controller):
        new_dlpath = tkFileDialog.askdirectory(title='Choose a save location',
                                               initialdir=controller.dlpath.get())
        if new_dlpath:
            controller.dlpath.set(new_dlpath)

app = YoutubeDLApp()
app.mainloop()