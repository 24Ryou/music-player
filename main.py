from tkinter import *
import pygame
from tkinter import filedialog
import random

class musicplayer:

  def __init__(self , root):
    # --------------------------------- frontend --------------------------------- #
    # basic
    self.light = "white"
    self.dark = "black"
    self.select_color = "lightblue"
    self.root = root
    # menu 
    self.menubar = Menu(self.root)
    self.root.config(menu=self.menubar)
    self.my_menu = Menu(self.menubar , tearoff=False)
    self.my_menu.add_command(label="Add Files" , command=self.AddSongs)
    self.my_menu.add_command(label="Delete Files" , command=self.DeleteSongs)
    self.menubar.add_cascade(label="File" , menu=self.my_menu)
    # listbox 
    self.song_list = Listbox(self.root , selectmode=EXTENDED, bg=self.dark, fg=self.light , width="100" , height="10" , font=("arial" , 14) , activestyle="none" , selectbackground=self.select_color , selectforeground=self.dark)
    self.song_list.pack()
    self.song_list.bind("<Double-Button-1>", self.tune_changed)
    # import images 
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
    # button 
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

    # variables 
    self.playlist = {}
    self.idx = 0
    self.progress = 0
    self.musicLength = 0
    self.pause = False 
    self.repeat = False
    self.autoplay = True
    self.shuffle = False
    self.FuncLock = True
  
  def Update(self):
    """
    If the progress is less than the music length, add 1 to the progress and call the function again.
    If autoplay is true, play the next song. If shuffle is true, play a random song. If repeat is
    true, play the current song again
    """
    if self.progress < self.musicLength:
      self.progress += 1
      self.updater = self.root.after(1000, self.Update)
    elif self.autoplay:
      self.Next()
      self.Play()
    elif self.shuffle:
      self.idx = (random.randint(0 , len(self.playlist)) % len(self.playlist))
      self.Play()
    elif self.repeat:
      self.Play()

  def Play(self) :
    """
    It plays the song
    """
    self.FuncLock = False
    self.progress = 0
    self.play_btn.grid_forget()
    self.pause_btn.grid(row=0 , column=1 , padx=24 , pady=10)
    if self.pause :
      pygame.mixer.music.unpause() 
    elif self.shuffle:
      self.idx = (random.randint(0 , len(self.playlist)) % len(self.playlist))
      pygame.mixer.music.load(self.playlist[self.song_list.get(self.idx)])
      self.UpdateListBox()
      pygame.mixer.music.play()
      self.Update()
    else :
      self.pause = False
      self.musicLength = pygame.mixer.Sound(self.playlist[self.song_list.get(self.idx)]).get_length()
      pygame.mixer.music.load(self.playlist[self.song_list.get(self.idx)])
      self.UpdateListBox()
      pygame.mixer.music.play()
      self.Update()

  def Stop(self) : 
    """
    If the function lock is not active, stop the music, hide the pause button, show the play button,
    and reset the index to 0
    :return: the value of the variable self.idx. == means not changing the variable 
    """
    if self.FuncLock == True : return
    pygame.mixer.music.stop()
    self.pause_btn.grid_forget()
    self.play_btn.grid(row=0 , column=1 , padx=24 , pady=10)
    self.idx = 0

  def Pause(self) :
    """
    It removes the pause button from the grid and adds the play button to the grid. It also pauses the
    music
    """
    self.pause_btn.grid_forget()
    self.play_btn.grid(row=0 , column=1 , padx=24 , pady=10)
    pygame.mixer.music.pause()
    self.pause = True
  
  def Next(self) :
    """
    It's a function that plays the next song in the playlist.
    """
    before_idx = (self.idx) % len(self.playlist)
    self.idx = (self.idx + 1) % len(self.playlist)
    self.song_list.selection_clear(before_idx)
    self.Play()
    self.root.after_cancel(self.updater)

  def Back(self) :
    """
    It's a function that plays the previous song in the playlist.
    """
    before_idx = (self.idx) % len(self.playlist)
    self.idx = (self.idx - 1) % len(self.playlist)
    self.song_list.selection_clear(before_idx)
    self.Play()
    self.root.after_cancel(self.updater)

  def Silent(self) :
    """
    It makes the volume button disappear and the silent button appear.
    """
    self.volume_btn.grid_forget()
    self.silent_btn.grid(row=0 , column=5 , padx=24 , pady=10)
    pygame.mixer.music.set_volume(0)

  def Volume(self) :
    """
    It makes the silent button disappear and the volume button appear.
    """
    self.silent_btn.grid_forget()
    self.volume_btn.grid(row=0 , column=5 , padx=24 , pady=10)
    pygame.mixer.music.set_volume(1)
    

  def Shuffle(self) :
    """
    It's a function that changes the appearance of the shuffle button when it's clicked
    :return: Nothing is being returned.
    """
    if self.FuncLock == True : return
    self.repeat_btn.grid_forget()
    self.repeat_one_btn.grid_forget()
    self.shuffle_btn.grid(row=0 , column=4 , padx=24 , pady=10)
    self.shuffle = True
    self.autoplay = False
    self.repeat = False

  def Repeat(self) :
    """
    If the function is locked, return. If it's not locked, forget the repeat_one_btn and shuffle_btn,
    then grid the repeat_btn, set shuffle to False, autoplay to True, and repeat to False
    :return: Nothing is being returned.
    """
    if self.FuncLock == True : return
    self.repeat_one_btn.grid_forget()
    self.shuffle_btn.grid_forget()
    self.repeat_btn.grid(row=0 , column=4 , padx=24 , pady=10)
    self.shuffle = False
    self.autoplay = True
    self.repeat = False

  def RepeatOne(self) :
    """
    If the function is locked, return. If the function is locked, return. Forget the shuffle button.
    Forget the repeat button. Place the repeat one button in the grid. Set shuffle to false. Set
    autoplay to false. Set repeat to true.
    :return: Nothing is being returned.
    """
    if self.FuncLock == True : return
    if self.FuncLock == True : return
    self.shuffle_btn.grid_forget()
    self.repeat_btn.grid_forget()
    self.repeat_one_btn.grid(row=0 , column=4 , padx=24 , pady=10)
    self.shuffle = False
    self.autoplay = False
    self.repeat = True

  def AddSongs(self) :
    """
    It takes the file path of the song and splits it into a list of strings, then it takes the last
    string in the list and inserts it into the listbox.
    """
    temp_song=filedialog.askopenfilenames(initialdir="Music/",title="Choose a song", filetypes=(("Audio Files", ".wav .ogg .mp3 .flac"), ("All Files", "*.*")))
    for s in temp_song:
      self.song_list.insert(END,s.split("/")[-1])
      self.playlist[self.song_list.get(END)] = s

  def DeleteSongs(self) :
    """
    It deletes the selected songs from the playlist
    """
    curr_song=self.song_list.curselection()
    list = [self.song_list.get(x) for x in curr_song]
    for song in curr_song:
      self.song_list.delete(song)
    self.song_list.delete(curr_song[0])
    self.UpdatePlaylist(list)

  def UpdatePlaylist(self , list):
    """
    It takes a list of integers as an argument, and deletes the items in the playlist at the indices
    specified by the integers in the list
    
    :param list: The list of indexes to remove from the playlist
    """
    for x in list:
      del self.playlist[x]

  def UpdateListBox(self):
    """
    It selects the item in the listbox that corresponds to the index of the song that is currently
    playing
    """
    self.song_list.selection_set(f'{self.idx}')
    self.song_list.see(f'{self.idx}')

  def tune_changed(self , event):
    """
    The function is called when the user selects a tune from the listbox. The function then plays the
    tune
    
    :param event: The event that triggered this function
    """
    self.idx = event.widget.curselection()[0]
    self.Play()

if __name__ == '__main__':
  
  pygame.init()
  pygame.mixer.init()

  root = Tk()
  root.title("Music Player App")
  root.geometry("600x300")
  root.config(bg="white")

  x = musicplayer(root)
  root.mainloop()