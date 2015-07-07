__author__ = 'Jake'

from Tkinter import *
import ttk
import youtube_dl

class YoutubeDLApp(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title("YoutubeDL")
        self.geometry('500x250')
        self.resizable(width=False, height=False)

        container = Frame(self, background='white')
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        start_frame = StartPage(container)
        self.frames[StartPage] = start_frame
        start_frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(StartPage)

        self.ydl_opts = {}

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent, background='white')

        spacer = Frame(self)
        spacer.pack(pady=20)
        label = Label(self, text="URL to download:", background='white')
        label.pack()
        self.url_entry = ttk.Entry(self, width=50)
        self.url_entry.pack()
        button = ttk.Button(self, text='Go', command=self.go_button)
        button.pack(pady=5)
        

    def go_button(self):
        url = self.url_entry.get()
        try:
            with youtube_dl.YoutubeDL(app.ydl_opts) as ydl:
                ydl.download([url])
        except:
            print 'error'







app = YoutubeDLApp()
app.mainloop()