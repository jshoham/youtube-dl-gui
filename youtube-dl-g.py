__author__ = 'Jake'

from Tkinter import *
import ttk
import os
import youtube_dl
import traceback


class YoutubeDLApp(Tk):
    def __init__(self, *args, **kwargs):
        self.ydl_opts = {}
        #default save location
        DEFAULT_DOWNLOAD_PATH = os.path.join(os.path.expandvars('%userprofile%'), 'downloads')
        self.ydl_opts['outtmpl'] = '{}\%(title)s.%(ext)s'.format(DEFAULT_DOWNLOAD_PATH)
        self.ydl_opts['ignoreerrors'] = True

        Tk.__init__(self, *args, **kwargs)
        self.title("YoutubeDL")
        self.geometry('500x250')
        self.resizable(width=False, height=False)

        container = Frame(self, background='white')
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.frames[StartPage] = StartPage(container, self)
        self.frames[OptionsPage] = OptionsPage(container, self)

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, background='white')
        self.grid(row=0, column=0, sticky=NSEW)
        self.grid_columnconfigure(0, weight=1)

        options_button = ttk.Button(self, text='...', width=3,
                                    command=lambda: controller.show_frame(OptionsPage))
        options_button.grid(row=0, column=2, sticky=NE)
        spacer = Frame(self)
        spacer.grid(row=1, column=0, columnspan=3, pady=20)
        label = Label(self, text="URL to download:", background='white')
        label.grid(row=2, column=0, columnspan=3)
        self.url_entry = ttk.Entry(self, width=50)
        self.url_entry.grid(row=3, column=0, columnspan=3)
        button = ttk.Button(self, text='Go', command=lambda: self.go_button(controller))
        button.grid(row=4, column=0, columnspan=3, pady=5)

        # Audio checkbox
        s = ttk.Style()
        s.configure('TCheckbutton', background='white')
        self.audio_opt = BooleanVar()
        audio_checkbox = ttk.Checkbutton(self, text='extract audio', variable=self.audio_opt, style='TCheckbutton',
                                         command=lambda: self.audio_changed(controller))
        audio_checkbox.grid(row=5, column=0, columnspan=3)
        # default audio to ON
        self.audio_opt.set(True)
        self.audio_changed(controller)

        # Test checkbox
        self.test_opt = BooleanVar()
        test_checkbox = ttk.Checkbutton(self, text='test run', variable=self.test_opt, style='TCheckbutton',
                                        command=lambda: self.test_changed(controller))
        test_checkbox.grid(row=6, column=0, columnspan=3)

    def audio_changed(self, controller):
        if self.audio_opt.get():
            print 'Extract audio turned on (mp3)'
            controller.ydl_opts['format'] = 'bestaudio/best'
            controller.ydl_opts['writethumbnail'] = True
            if not 'postprocessors' in controller.ydl_opts:
                controller.ydl_opts['postprocessors'] = []
            controller.ydl_opts['postprocessors'].extend([{'key': 'FFmpegExtractAudio',
                                                      'preferredcodec': 'mp3'},
                                                     {'key': 'EmbedThumbnail'}])
            #print 'after {}'.format(controller.ydl_opts['postprocessors'])

        else:
            print 'Extract audio turned off'
            del controller.ydl_opts['format']
            del controller.ydl_opts['writethumbnail']
            #print 'before {}'.format(controller.ydl_opts['postprocessors'])
            controller.ydl_opts['postprocessors'].remove({'key': 'FFmpegExtractAudio',
                                                          'preferredcodec': 'mp3'})
            controller.ydl_opts['postprocessors'].remove({'key': 'EmbedThumbnail'})
            #print 'after {}'.format(controller.ydl_opts['postprocessors'])

    def test_changed(self, controller):
        if self.test_opt.get():
            print 'test mode turned on. (Doesnt do anything yet)'

        else:
            print 'test mode turned off'


    def go_button(self, controller):
        url = self.url_entry.get()
        try:
            print 'using options: {}'.format(controller.ydl_opts)
            with youtube_dl.YoutubeDL(controller.ydl_opts) as ydl:
                ydl.download([url])
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback)
            traceback.print_exception(exc_type, exc_value, exc_traceback)


class OptionsPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, background='white')
        self.grid(row=0, column=0, sticky=NSEW)
        self.grid_columnconfigure(0, weight=1)

        home_button = ttk.Button(self, text='Home',
                                 command=lambda: controller.show_frame(StartPage))
        home_button.grid(row=0, column=2, sticky=NE)
        page_label = Label(self, text='Options', background='white')
        page_label.grid()


app = YoutubeDLApp()
app.mainloop()