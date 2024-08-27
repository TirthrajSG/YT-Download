from pathlib import Path
from tkinter import *
from tkinter import ttk, filedialog
from tkinter.filedialog import asksaveasfile
import webbrowser
from pytube import YouTube
from PIL  import Image, ImageTk
import requests
from io import BytesIO


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"A:\Python\YT Download\build\assets\frame0")

def humanReadable(a):
    if a < 999:
        return f'{a}'
    elif a > 999 and a < 1000000:
        return f'{a//1000}.{int(((a%1000)/100)//1)}K'
    else:
        return f'{a//1000000}.{int(((a%1000000)/100)//100)}M'
        

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def timeconvert(a):
    if a//3600==0:
        return f'{a//60} mins {a%60} secs'
    else:
        return f'{a//3600} hrs {(a%3600)//60} mins {(a%3600)%60} secs'

def setTN(img):
    img = img.resize((320,180))
    tkimg = ImageTk.PhotoImage(img)
    thumbnail.config(image=tkimg)
    thumbnail.image = tkimg

def bytes_to_megabytes(bytes_size):
    megabytes_size = bytes_size / (1024 ** 2)
    return megabytes_size

def progress_func(stream,chunk, bytes_remaining):
    current = stream.filesize - bytes_remaining
    done_percent = int(100 * current / stream.filesize)
    prglbl.config(text=f'{done_percent} %')
    prglbl.update()
    progress['value']=done_percent
    progress.update()
    if progress['value'] > 48: prglbl.config(bg='aqua')


def complete_func(stream, path):
    progress.config(value=0)
    prglbl.config(text=f'{0} %')
    prglbl.config(bg='#6a719a')

def search():
    description.delete('1.0', END)
    drop.config(values=[])


    button_1.config(cursor='exchange')
    strms = []
    try:
        global img_
        global yt
        link = url.get()
        yt = YouTube(link,on_progress_callback=progress_func, on_complete_callback=complete_func)
        th_link = yt.thumbnail_url

        response = requests.get(th_link)
        img = Image.open(BytesIO(response.content))
        img_ = img
        setTN(img)

        description.insert(END, f'''Title: {yt.title}
                           \nViews: {humanReadable(yt.views)}
                           \nDate: {yt.publish_date}
                           \nLength: {timeconvert(yt.length)}
                           \nChannel: {yt.author}
                           \nDescription:\n{yt.description}''')

        for strm in yt.streams:
            if strm.type == 'video':
                strms.append(f'{strm.mime_type} {strm.resolution} {strm.fps}fps {strm.filesize_mb} mb')
            else:
                strms.append(f'{strm.mime_type} {strm.abr} {strm.filesize_mb} mb')
        
        drop.config(values=strms)
        drop.current(0)

        log.config(state='normal')
        log.insert(END, f'Video Loaded... {yt.title}\n\n')
        log.config(state='disabled')

    except Exception as e:
        log.config(state='normal')
        log.insert(END, f'{e}\n\n')
        log.config(state='disabled')

        
    button_1.config(cursor='cross')
    

def download():
    
    button_2.config(cursor='exchange')
    try:
        index = drop.current()
        folder_selected = filedialog.askdirectory()
        if folder_selected == '': return
        yt.streams[index].download(folder_selected)
        # yt.streams.get_highest_resolution().download(folder_selected)
        log.config(state='normal')
        log.insert(END, f'Video Downloaded... {yt.title}\n\n')
        log.config(state='disabled')
    except Exception as e:

        log.config(state='normal')
        log.insert(END, f'{e}\n\n')
        log.config(state='disabled')
        
    button_1.config(cursor='cross')

def ssaveThumb():
    if len(yt.title) > 15: title = yt.title[0:14]
    else: title = yt.title
    f = asksaveasfile(initialfile = f'{title}.png',
defaultextension=".png",filetypes=[("All Files","*.*"),("PNG","*.png"),("JPG","*.jpg"),("JPEG","*.jpeg")])
    try:
        img_.save(f.name)
        log.config(state='normal')
        log.insert(END, f'{f.name} is saved successfully\n\n')
        log.config(state='disabled')
    except Exception as e:
        log.config(state='normal')
        log.insert(END, f'{e}\n\n')
        log.config(state='disabled')

def share(i):

    if i == 1:
        webbrowser.open('https://github.com/TirthrajSG')
    elif i == 2:
        webbrowser.open('https://www.youtube.com/@indianprayers6091')
    else:
        webbrowser.open('https://www.instagram.com/tirthrajsg/')




window = Tk()

window.geometry("1000x635")
window.configure(bg = "#4AB1E8")


canvas = Canvas(
    window,
    bg = "#4AB1E8",
    height = 635,
    width = 1000,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    bg='#b2e2f1',
    cursor='cross',
    activebackground='#799aa4',
    borderwidth=0,
    highlightthickness=0,
    command=lambda: search(),
    relief="sunken"
)
button_1.place(
    x=841.0,
    y=86.0,
    width=131.0,
    height=40.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    bg='#436499',
    activebackground='#21314c',
    borderwidth=0,
    cursor='cross',
    highlightthickness=0,
    command=lambda: download(),
    relief="sunken"
)
button_2.place(
    x=27.0,
    y=387.0,
    width=246.0,
    height=62.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    bg='#436499',
    activebackground='#21314c',
    borderwidth=0,
    cursor='cross',
    highlightthickness=0,
    command=lambda: ssaveThumb(),
    relief="sunken"
)
button_3.place(
    x=285.0,
    y=387.0,
    width=62.0,
    height=62.0
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    bg='#4bb1e9',
    activebackground='#32769c',
    borderwidth=0,
    cursor='cross',
    highlightthickness=0,
    command=lambda: share(1),
    relief="sunken"
)
button_4.place(
    x=644.0,
    y=513.0,
    width=96.0,
    height=96.0
)

button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    bg='#4bb1e9',
    activebackground='#32769c',
    borderwidth=0,
    cursor='cross',
    highlightthickness=0,
    command=lambda: share(2),
    relief="sunken"
)
button_5.place(
    x=760.0,
    y=513.0,
    width=96.0,
    height=96.0
)

button_image_6 = PhotoImage(
    file=relative_to_assets("button_6.png"))
button_6 = Button(
    image=button_image_6,
    bg='#4bb1e9',
    activebackground='#32769c',
    borderwidth=0,
    cursor='cross',
    highlightthickness=0,
    command=lambda: share(3),
    relief="sunken"
)
button_6.place(
    x=876.0,
    y=513.0,
    width=96.0,
    height=96.0
)

canvas.create_rectangle(
    0.0,
    0.0,
    1000.0,
    67.0,
    fill="#004F6C",
    outline="")

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    30.0,
    33.0,
    image=image_image_1
)

combostyle = ttk.Style()
combostyle.theme_create('combostyle', parent='alt',
                         settings = {'TCombobox':
                                     {'configure':
                                      {'selectbackground': '#B2E2F0',
                                       'selectforeground' : 'black',
                                       'fieldbackground': '#B2E2F0',
                                       'background': '#B2E2F0',
                                       'foreground' : 'black'
                                       }}})
combostyle.theme_use('combostyle')

progressstyle = ttk.Style()
progressstyle.theme_create('progressstyle', parent='alt', 
                           settings={
                               'TProgressbar' :{
                                   'configure':{
                                   'background': 'aqua',
                                   'troughcolor' : '#6a719a',
                                   'darkcolor' : 'blue',
                                   'lightcolor': 'pink'
                               }
                               }
                           })
progressstyle.theme_use('progressstyle')

drop = ttk.Combobox(state='readonly',
                    font=('Georgia 20', 16))
drop.place(x = 27, y = 136, height=38, width=950)

thumbnail = Label(background='#436499')
thumbnail.place(x = 27, y= 187, width=320, height=180)

progress = ttk.Progressbar(value=0, length=100)
progress.place(x = 27, y= 464, width=945, height=33)

prglbl = Label(text='0 %', bg='#6a719a', fg='yellow', font=('Georgia 20', 14))
prglbl.place(x = 480, y= 466)

url = Entry(
    bd=0,
    bg="#B2E2F0",
    fg="#000716",
    font=('Georgia 20', 16),
    highlightthickness=0
)
url.place(
    x=27.0,
    y=86.0,
    width=803.0,
    height=38.0
)

description = Text(
    bd=0,
    bg="#436499",
    fg="#ffffff",
    font=('Georgia 20', 16),
    highlightthickness=0
)
description.place(
    x=362.0,
    y=187.0,
    width=610.0,
    height=256.0
)

log = Text(
    bd=0,
    bg="#6A719A",
    fg="#ffffff",
    font=('Georgia 20', 16),
    state='disabled',
    highlightthickness=0
)
log.place(
    x=27.0,
    y=513.0,
    width=605.0,
    height=94.0
)

canvas.create_text(
    305.0,
    11.0,
    anchor="nw",
    text="YouTube Downloader",
    fill="#4AB1E8",
    font=("JejuHallasan", 40 * -1)
)

window.title('Youtube Downloader')
window.resizable(False, False)
window.mainloop()
