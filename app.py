from tkinter import *
import pygame
from tkinter import filedialog
import random

class musicplayer:

  def __init__(self , root):
    self.END = pygame.USEREVENT + 1 # song's end
    self.light = "white"
    self.dark = "black"
    self.select_color = "lightblue"
    self.root = root
    self.menubar = Menu(self.root)
    self.root.config(menu=self.menubar)
    self.my_menu = Menu(self.menubar , tearoff=False)
    self.my_menu.add_command(label="Add Files" , command=self.AddSongs)
    self.my_menu.add_command(label="Delete Files" , command=self.DeleteSongs)
    self.menubar.add_cascade(label="File" , menu=self.my_menu)

    self.song_list = Listbox(self.root , selectmode=EXTENDED, bg=self.dark, fg=self.light , width="100" , height="10" , font=("arial" , 14) , activestyle="none" , selectbackground=self.select_color , selectforeground=self.dark)
    self.song_list.pack()
    self.song_list.bind("<Double-Button-1>", self.tune_changed)

    self.play_btn_image        = PhotoImage(file="img/play.png")
    self.stop_btn_image        = PhotoImage(file="img/stop.png")
    self.next_btn_image        = PhotoImage(file="img/next.png")
    self.back_btn_image        = PhotoImage(file="img/back.png")
    self.pause_btn_image       = PhotoImage(file="img/pause.png")
    self.silent_btn_image      = PhotoImage(file="img/silent.png")
    self.volume_btn_image      = PhotoImage(file="img/volume.png")
    self.repeat_btn_image      = PhotoImage(file="img/repeat.png")
    self.shuffle_btn_image     = PhotoImage(file="img/shuffle.png")
    self.repeat_one_btn_image  = PhotoImage(file="img/repeat-once.png")

    self.btn_frame = Frame(self.root)
    self.btn_frame.pack()

    self.play_btn        = Button(self.btn_frame , image=self.play_btn_image , borderwidth=0 , command=self.Play)
    self.stop_btn        = Button(self.btn_frame , image=self.stop_btn_image , borderwidth=0 , command=self.Stop)
    self.next_btn        = Button(self.btn_frame , image=self.next_btn_image , borderwidth=0 , command=self.Next)
    self.back_btn        = Button(self.btn_frame , image=self.back_btn_image , borderwidth=0 , command=self.Back)
    self.pause_btn       = Button(self.btn_frame , image=self.pause_btn_image , borderwidth=0 , command=self.Pause)
    self.silent_btn      = Button(self.btn_frame , image=self.silent_btn_image , borderwidth=0 , command=self.Volume)
    self.volume_btn      = Button(self.btn_frame , image=self.volume_btn_image , borderwidth=0 , command=self.Silent)
    self.repeat_btn      = Button(self.btn_frame , image=self.repeat_btn_image , borderwidth=0 , command=self.RepeatOne)
    self.shuffle_btn     = Button(self.btn_frame , image=self.shuffle_btn_image , borderwidth=0 , command=self.Repeat)
    self.repeat_one_btn  = Button(self.btn_frame , image=self.repeat_one_btn_image , borderwidth=0 , command=self.Shuffle)

    self.back_btn.grid       (row=0 , column=0 , padx=24 , pady=10)
    self.play_btn.grid       (row=0 , column=1 , padx=24 , pady=10)
    self.stop_btn.grid       (row=0 , column=2 , padx=24 , pady=10)
    self.next_btn.grid       (row=0 , column=3 , padx=24 , pady=10)
    self.pause_btn.grid      (row=0 , column=1 , padx=24 , pady=10)
    self.silent_btn.grid     (row=0 , column=5 , padx=24 , pady=10)
    self.volume_btn.grid     (row=0 , column=5 , padx=24 , pady=10)
    self.repeat_btn.grid     (row=0 , column=4 , padx=24 , pady=10)
    self.shuffle_btn.grid    (row=0 , column=4 , padx=24 , pady=10)
    self.repeat_one_btn.grid (row=0 , column=4 , padx=24 , pady=10)
    self.pause_btn.grid_forget()
    self.shuffle_btn.grid_forget()
    self.repeat_one_btn.grid_forget()
    self.playlist = {}
    self.idx = 0
    self.progress = 0
    self.musicLength = 0
    self.pause = False 
    self.repeat = False
    self.autoplay = True
    self.shuffle = False
    self.FuncLock = True
    
if __name__ == '__main__':
  
  pygame.init()
  pygame.mixer.init()

  # light = "#D3DFE1"
  # dark = "#2A2C2D"

  # # play_btn.grid_forget()
  root = Tk()
  root.title("Music Player App")
  root.geometry("600x300")
  root.config(bg="white")

  x = musicplayer(root)
  root.mainloop()