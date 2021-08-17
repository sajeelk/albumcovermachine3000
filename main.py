import urllib.request, spotipy, time, tkinter as tk
from config import *
from datetime import datetime
from suntime import Sun
from geocoder import ip
from PIL import Image, ImageTk
from spotipy.oauth2 import SpotifyOAuth
from sys import argv

def switch_color():
	global dark
	dark = not dark
	if dark:
		window.configure(bg='black')
		atext.config(bg='black', fg='white')
	else:
		window.configure(bg='white')
		atext.config(bg='white', fg='black')


def update_album():
	if use_sp:
		try:
			np = sp.currently_playing()
			album = sp.album(np['item']['album']['uri'])
		except:
			time.sleep(1)
			return update_album()
	else:
		album = sp.album(argv[1])

	return album

def update_window(album):
	nalbum = update_album()
	if album != nalbum:
		for widget in window.winfo_children():
		    widget.destroy()
		album = nalbum

		window.bind('<Button-1>', lambda a: switch_color())
		imgarr = album['images'][0]
		urllib.request.urlretrieve(imgarr['url'], "/Users/sajeelk/Documents/cover/cover.png")
		im = Image.open("/Users/sajeelk/Documents/cover/cover.png")
		render = ImageTk.PhotoImage(im)
		img = tk.Label(image=render, highlightthickness=0, borderwidth=0)
		img.image = render
		img.place(x=((sw / 2) - (imgarr['width'] / 2)), y=((sc / 2) - (imgarr['height'] / 2)))



		name = album['name']
		if "(" in name and \
			any(x in name[name.find("(")+1:name.find(")")] for x in ["Original", "Deluxe", "Expanded", "Remastered", "Anniversary", "Edition"]):
			name = name.split("(")[0]
		if "[" in name and \
			any(x in name[name.find("[")+1:name.find("]")] for x in ["Original", "Deluxe", "Expanded", "Remastered", "Anniversary", "Edition"]):
			name = name.split("[")[0]
		print(name)

		npline = (', '.join([artist['name'] for artist in album['artists']]) if len(album['artists']) < 4 else "Various Artists" ) + " - " + name

		global atext
		atext = tk.Label(text=npline)
		atext.place(x=(sw / 2), y=((sc / 2) - (imgarr['width'] / 2) - 50), anchor="center")
		atext.config(font=('Courier', 30))
		if dark:
			atext.config(bg='black', fg='white')
	if use_sp:
		window.after(1000, update_window, album)

scope = "user-read-playback-state"
sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope,
	client_id=CLIENT_ID,
	client_secret=CLIENT_SECRET,
	redirect_uri='https://google.com/'))


window = tk.Tk()
window.attributes('-fullscreen', True)

a = ip('me').latlng
s = Sun(a[0], a[1])
global sr, ss
sr = s.get_local_sunrise_time()
ss = s.get_local_sunset_time()
if sr < datetime.now(sr.tzinfo) < ss:
	dark = False
else:
	dark = True

window.configure(bg=('black' if dark else 'white'), cursor='none')
window.focus_force()
sw = window.winfo_screenwidth()
sc = window.winfo_screenheight()

global use_sp
use_sp = False if len(argv) == 2 else True

window.after(0, update_window, "")
window.mainloop()
