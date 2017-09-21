
#https://stackoverflow.com/questions/14817210/using-buttons-in-tkinter-to-navigate-to-different-pages-of-the-application
#http://www.tkdocs.com/tutorial/grid.html
#http://effbot.org/tkinterbook/grid.htm
#https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter

"""
ToDo:
Wlan Funktionalitaetssd - 2x
"""

from tkinter import *
import tkinter as tk
import time
import sys
import os
import json
import io
import pygame
from shutil import copyfile
#import NetworkManager

class Struktur(tk.Tk):
    akt_frame=""
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Optionen, Einstellungen, Uhr_laeuft, WLAN):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Uhr_laeuft")

        self.Update_Uhr()

        pygame.mixer.init()

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        Struktur.akt_frame = page_name

    def Update_Uhr(self):
        # abspeichern der Intro Variablen
        Intro().save()
        # Update-Funktion der Uhr
        Uhr().Update()
        # Update der Schalter in den Einstellungen
        Uhr().plus_runden()
        Uhr().minus_runden()
        Uhr().plus_runde()
        Uhr().minus_runde()
        Uhr().plus_pause()
        Uhr().minus_pause()
        # Update
        self.timer = self.after(Intro.update_frames, self.Update_Uhr)

class Intro(tk.Frame):
    # gespeichert
    try:
        with open('data.json') as data_file:
            data = json.load(data_file)
    except:
        copyfile("data.json_bak", "data.json")
        with open('data.json') as data_file:
            data = json.load(data_file)

    runden = data["runden"]
    runde = data["runde"]
    pause = data["pause"]

    tensec = data["tensec"]
    tensec_anzeige = data["tensec_anzeige"]
    volume = data["volume"]
    ton = data["ton"]
    skin = data["skin"]

    # gesetzt
    start = False
    start_pause = True
    reset = 0
    
    runden_counter = runden
    runde_counter = runde
    pause_counter = pause
    
    pause_zeit = 0
    startzeit = 0

    mouse_down_plus_runden = False
    mouse_down_plus_runde = False
    mouse_down_plus_pause = False
    mouse_down_minus_runden = False
    mouse_down_minus_runde = False
    mouse_down_minus_pause = False

    if sys.platform == 'linux':
        update_frames = 1000
    if sys.platform == 'darwin':
        update_frames = 10

    if volume == 1:
        volume_label = "50%"
    if volume == 2:
        volume_label = "75%"
    if volume == 3:
        volume_label = "100%"

    def __init__(self, *args, **kwargs):
        pass

    def save(self):
        # speichern
        data = {}
        data["runden"] = Intro.runden
        data["runde"] = Intro.runde
        data["pause"] = Intro.pause

        data["tensec"] = Intro.tensec
        data["tensec_anzeige"] = Intro.tensec_anzeige
        data["volume"] = Intro.volume
        data["ton"] = Intro.ton
        data["skin"] = Intro.skin

        # Write JSON file
        with io.open('data.json', 'w') as outfile:
            str_ = json.dumps(data, indent=4, sort_keys=True, separators=(',', ': '))
            outfile.write(str(str_))

class Skin(tk.Frame):
    def __init__(self, *args, **kwargs):
        pass

    # Optionen
    color_bg_Optionen = "black"
    color_bg_buttons_Optionen = "white"
    color_fg_Optionen = "black"
    color_font_Optionen = "black"

    # Einstellungen
    color_bg_Einstellungen = "black"
    color_bg_buttons_Einstellungen = "white"
    color_fg_Einstellungen = "white"
    color_font_Einstellungen = "black"

    # Uhr_laeuft
    color_bg_Uhr = "black"
    color_bg_buttons_Uhr = "white"
    color_fg_Uhr = "white"
    color_font_Uhr = "black"

    # globale Einstellungen
    font = "Arial"

class WLAN(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.frame_bg = tk.Frame(self, width=480, height=320, bg="black")
        self.frame_fg_w = tk.Frame(self, width=480, height=320, bg="black")
        self.frame_fg_e = tk.Frame(self, width=480, height=320, bg="black")

        self.Buttons()

        """
        text.tag_config("a", foreground="blue", underline=1)
        text.tag_bind("Enter>", show_hand_cursor)
        text.tag_bind("Leave>", show_arrow_cursor)
        text.tag_bind("Button-1>", click)
        text.config(cursor="arrow")

        text.insert(INSERT, "click here!", "a")
        """

    def Buttons(self):

        self.wlan_name = Entry(self.frame_fg_e)
        self.wlan_name.config(width=100, bg="white")
        #self.wlan_name.insert(INSERT, "click here!", "text")
        #self.wlan_name.bind("Button-1>", click)

        self.canvas_back = Canvas(self.frame_fg_e, bg='white', height=75, width=176)
        self.canvas_back.bind("<Button-1>", lambda event: self.controller.show_frame("Optionen"))
        self.label_back = Label(self.frame_fg_e, font=("Arial", 15), bg="black", fg="white", text="Back")
        self.label_back.bind("<Button-1>", lambda event: self.controller.show_frame("Optionen"))

        # Grid erstellen
        self.frame_bg.grid(column=0, row=0, sticky = NW)
        self.frame_fg_w.grid(column=0, row=0, sticky = W)
        self.frame_fg_e.grid(column=0, row=0, sticky = E)
        # Grid befuellen
        self.canvas_back.grid(column=0, row=0, pady=5)#, rowspan=4)
        self.label_back.grid(column=0, row=0, pady=5)#, rowspan=4)
        self.wlan_name.grid(column=0, row=1)

class Optionen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.frame_bg = tk.Frame(self, width=480, height=320, bg=Skin.color_bg_Optionen)
        self.frame_fg_w = tk.Frame(self, width=480, height=320, bg=Skin.color_bg_Optionen)
        self.frame_fg_e = tk.Frame(self, width=480, height=320, bg=Skin.color_bg_Optionen)

        self.Update()

    def Update(self):
        if Struktur.akt_frame == ("Optionen"):
            self.Buttons()
        self.timer = self.after(Intro.update_frames, self.Update)

    def Tensec(self):
        Intro.tensec = not Intro.tensec
        if Intro.tensec == True:
            Intro.tensec_anzeige = "Ja"
        else:
            Intro.tensec_anzeige = "Nein" 

    def Volume(self):
        if Intro.volume <= 2:
            Intro.volume += 1
        else:
            Intro.volume = 1

        if sys.platform == 'linux':
            if Intro.volume == 1:
                os.system("amixer -q sset PCM 50%")
                Intro.volume_label = "50%"
            if Intro.volume == 2:
                os.system("amixer -q sset PCM 75%")
                Intro.volume_label = "75%"
            if Intro.volume == 3:
                os.system("amixer -q sset PCM 100%")
                Intro.volume_label = "100%"

        if sys.platform == 'darwin':
            if Intro.volume == 1:
                Intro.volume_label = "50%"
            if Intro.volume == 2:
                Intro.volume_label = "75%"
            if Intro.volume == 3:
                Intro.volume_label = "100%"

    def Skin(self):
        if Intro.skin <= 2:
            Intro.skin += 1
        else:
            Intro.skin = 1

    def Ton(self):
        if Intro.ton <= 9:
            Intro.ton += 1
        else:
            Intro.ton = 1
    
    def Buttons(self):
        # 10 Seconds Warning - Button
        self.canvas_tensec = Canvas(self.frame_fg_w, bg=Skin.color_bg_buttons_Optionen, height=75, width=176, highlightthickness=0)
        self.canvas_tensec.bind("<Button-1>", lambda event: self.Tensec())
        self.label_tensec = Label(self.frame_fg_w, font=("Arial", 15), bg=Skin.color_bg_buttons_Optionen, fg=Skin.color_fg_Optionen, text="10 Seconds \nWarning: %s" % Intro.tensec_anzeige)
        self.label_tensec.bind("<Button-1>", lambda event: self.Tensec())
        # Volume
        self.canvas_volume = Canvas(self.frame_fg_w, bg=Skin.color_bg_buttons_Optionen, height=75, width=176, highlightthickness=0)
        self.canvas_volume.bind("<Button-1>", lambda event: self.Volume())
        self.label_volume = Label(self.frame_fg_w, font=("Arial", 15), bg=Skin.color_bg_buttons_Optionen, fg=Skin.color_fg_Optionen, text="Volume: %s" % Intro.volume_label)
        self.label_volume.bind("<Button-1>", lambda event: self.Volume())
        # WLAN
        self.canvas_wlan = Canvas(self.frame_fg_w, bg=Skin.color_bg_buttons_Optionen, height=75, width=176, highlightthickness=0)
        self.canvas_wlan.bind("<Button-1>", lambda event: self.controller.show_frame("WLAN"))
        self.label_wlan = Label(self.frame_fg_w, font=("Arial", 15), bg=Skin.color_bg_buttons_Optionen, fg=Skin.color_fg_Optionen, text="WLAN")
        self.label_wlan.bind("<Button-1>", lambda event: self.controller.show_frame("WLAN"))

        # Skin
        self.canvas_skin = Canvas(self.frame_fg_e, bg=Skin.color_bg_buttons_Optionen, height=75, width=176, highlightthickness=0)
        self.canvas_skin.bind("<Button-1>", lambda event: self.Skin())
        self.label_skin = Label(self.frame_fg_e, font=("Arial", 15), bg=Skin.color_bg_buttons_Optionen, fg=Skin.color_fg_Optionen, text="Skin: %s/3" % Intro.skin)
        self.label_skin.bind("<Button-1>", lambda event: self.Skin())
        # Ton
        self.canvas_ton = Canvas(self.frame_fg_e, bg=Skin.color_bg_buttons_Optionen, height=75, width=176, highlightthickness=0)
        self.canvas_ton.bind("<Button-1>", lambda event: self.Ton())
        self.label_ton = Label(self.frame_fg_e, font=("Arial", 15), bg=Skin.color_bg_buttons_Optionen, fg=Skin.color_fg_Optionen, text="Ton: %s/10" % Intro.ton)
        self.label_ton.bind("<Button-1>", lambda event: self.Ton())
        # Back
        self.canvas_back = Canvas(self.frame_fg_e, bg=Skin.color_bg_buttons_Optionen, height=75, width=176, highlightthickness=0)
        self.canvas_back.bind("<Button-1>", lambda event: self.controller.show_frame("Einstellungen"))
        self.label_back = Label(self.frame_fg_e, font=("Arial", 15), bg=Skin.color_bg_buttons_Optionen, fg=Skin.color_fg_Optionen, text="Back")
        self.label_back.bind("<Button-1>", lambda event: self.controller.show_frame("Einstellungen"))

        # Grid erstellen
        self.frame_bg.grid(column=0, row=0, sticky = NW)
        self.frame_fg_w.grid(column=0, row=0, sticky = W)
        self.frame_fg_e.grid(column=0, row=0, sticky = E)
        # Grid befuellen - Hintergrunde
        self.canvas_tensec.grid(column=0, row=0, pady=5)#, rowspan=4)
        self.canvas_volume.grid(column=0, row=1, pady=5)#, rowspan=4)
        self.canvas_wlan.grid(column=0, row=2, pady=5)#, rowspan=4)
        #self.canvas_skin.grid(column=0, row=0, pady=5)#, rowspan=4)
        #self.canvas_ton.grid(column=0, row=1, pady=5)#, rowspan=4)
        self.canvas_back.grid(column=0, row=2, pady=5)#, rowspan=4)
        # Grid befuellen - Labels
        self.label_tensec.grid(column=0, row=0, pady=5)#, rowspan=4)
        self.label_volume.grid(column=0, row=1, pady=5)#, rowspan=4)
        self.label_wlan.grid(column=0, row=2, pady=5)#, rowspan=4)
        #self.label_skin.grid(column=0, row=0, pady=5)#, rowspan=4)
        #self.label_ton.grid(column=0, row=1, pady=5)#, rowspan=4)
        self.label_back.grid(column=0, row=2, pady=5)#, rowspan=4)

class Einstellungen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        #Frame erstellen
        self.frame_bg = tk.Frame(self, width=480, height=320, bg=Skin.color_bg_Einstellungen)
        self.frame_fg = tk.Frame(self, width=480, height=320, bg=Skin.color_bg_Einstellungen)
        # Darstellen der Buttons und Labels beim Initialisieren der Klasse starten
        self.Buttons()
        self.Update()
    
    def Update(self):
        if Struktur.akt_frame == ("Einstellungen"):
            self.Labels()
        self.timer = self.after(Intro.update_frames, self.Update)

    def Zur_Uhr(self):
        Intro.reset = 1
        Uhr().Reset()
        self.controller.show_frame("Uhr_laeuft")

    def Mouse_Down_plus_runden(self):
        Intro.mouse_down_plus_runden = not Intro.mouse_down_plus_runden
    def Mouse_Down_plus_runde(self):
        Intro.mouse_down_plus_runde = not Intro.mouse_down_plus_runde
    def Mouse_Down_plus_pause(self):
        Intro.mouse_down_plus_pause = not Intro.mouse_down_plus_pause
    def Mouse_Down_minus_runden(self):
        Intro.mouse_down_minus_runden = not Intro.mouse_down_minus_runden
    def Mouse_Down_minus_runde(self):
        Intro.mouse_down_minus_runde = not Intro.mouse_down_minus_runde
    def Mouse_Down_minus_pause(self):
        Intro.mouse_down_minus_pause = not Intro.mouse_down_minus_pause

        #Elemente erstellen
    def Buttons(self):
        #Hintergrund
        self.canvas_bg = Canvas(self.frame_bg, height=320, width=480, bg=Skin.color_bg_Einstellungen, highlightthickness=0)

        # Play Button
        self.canvas_play = Canvas(self.frame_fg, bg=Skin.color_bg_buttons_Einstellungen, height=227, width=100, highlightthickness=0)
        self.canvas_play.bind("<Button-1>", lambda event: self.Zur_Uhr())
        self.image_play = PhotoImage(file = 'play50.gif')
        self.play = self.canvas_play.create_image(50, 127, anchor=CENTER, image=self.image_play)
        # Optionen Button
        self.canvas_optionen = Canvas(self.frame_fg, bg=Skin.color_bg_buttons_Einstellungen, height=30, width=100, highlightthickness=0)
        self.canvas_optionen.bind("<Button-1>", lambda event: self.controller.show_frame("Optionen"))
        self.image_optionen = PhotoImage(file = 'zahnrad25.gif')
        self.optionen = self.canvas_optionen.create_image(50, 15, anchor=CENTER, image=self.image_optionen)

        # Plus Buttons
        self.image_plus = PhotoImage(file = 'plus50.gif')
            # Runden
        self.canvas_plus_runden = Canvas(self.frame_fg, bg=Skin.color_bg_buttons_Einstellungen, height=76, width=76, highlightthickness=0)
        self.canvas_plus_runden.bind("<ButtonPress-1>", lambda event: self.Mouse_Down_plus_runden())
        self.canvas_plus_runden.bind("<ButtonRelease-1>", lambda event: self.Mouse_Down_plus_runden())
        self.plus_runden = self.canvas_plus_runden.create_image(38, 38, anchor=CENTER, image=self.image_plus)
            # Runde
        self.canvas_plus_runde = Canvas(self.frame_fg, bg=Skin.color_bg_buttons_Einstellungen, height=76, width=76, highlightthickness=0)
        self.canvas_plus_runde.bind("<ButtonPress-1>", lambda event: self.Mouse_Down_plus_runde())
        self.canvas_plus_runde.bind("<ButtonRelease-1>", lambda event: self.Mouse_Down_plus_runde())
        self.plus_runde = self.canvas_plus_runde.create_image(38, 38, anchor=CENTER, image=self.image_plus)
            # Pause
        self.canvas_plus_pause = Canvas(self.frame_fg, bg=Skin.color_bg_buttons_Einstellungen, height=76, width=76, highlightthickness=0)
        self.canvas_plus_pause.bind("<ButtonPress-1>", lambda event: self.Mouse_Down_plus_pause())
        self.canvas_plus_pause.bind("<ButtonRelease-1>", lambda event: self.Mouse_Down_plus_pause())
        self.plus_pause = self.canvas_plus_pause.create_image(38, 38, anchor=CENTER, image=self.image_plus)

        # Minus Buttons
        self.image_minus = PhotoImage(file = 'minus50.gif')
            # Runden
        self.canvas_minus_runden = Canvas(self.frame_fg, bg=Skin.color_bg_buttons_Einstellungen, height=76, width=76, highlightthickness=0)
        self.canvas_minus_runden.bind("<ButtonPress-1>", lambda event: self.Mouse_Down_minus_runden())
        self.canvas_minus_runden.bind("<ButtonRelease-1>", lambda event: self.Mouse_Down_minus_runden())
        self.minus_runden = self.canvas_minus_runden.create_image(38, 38, anchor=CENTER, image=self.image_minus)
            # Runde
        self.canvas_minus_runde = Canvas(self.frame_fg, bg=Skin.color_bg_buttons_Einstellungen, height=76, width=76, highlightthickness=0)
        self.canvas_minus_runde.bind("<ButtonPress-1>", lambda event: self.Mouse_Down_minus_runde())
        self.canvas_minus_runde.bind("<ButtonRelease-1>", lambda event: self.Mouse_Down_minus_runde())
        self.minus_runde = self.canvas_minus_runde.create_image(38, 38, anchor=CENTER, image=self.image_minus)
            # Pause
        self.canvas_minus_pause = Canvas(self.frame_fg, bg=Skin.color_bg_buttons_Einstellungen, height=76, width=76, highlightthickness=0)
        self.canvas_minus_pause.bind("<ButtonPress-1>", lambda event: self.Mouse_Down_minus_pause())
        self.canvas_minus_pause.bind("<ButtonRelease-1>", lambda event: self.Mouse_Down_minus_pause())
        self.minus_pause = self.canvas_minus_pause.create_image(38, 38, anchor=CENTER, image=self.image_minus)

    def Labels(self):
        # Labels
        self.canvas_schrift_1 = Canvas(self.frame_fg, bg=Skin.color_bg_buttons_Einstellungen, height=76, width=150, highlightthickness=0)
        self.canvas_schrift_2 = Canvas(self.frame_fg, bg=Skin.color_bg_buttons_Einstellungen, height=76, width=150, highlightthickness=0)
        self.canvas_schrift_3 = Canvas(self.frame_fg, bg=Skin.color_bg_buttons_Einstellungen, height=76, width=150, highlightthickness=0)
            # Runden
        self.runden_display = Label(self.frame_fg, font=("Arial", 15), bg=Skin.color_bg_buttons_Einstellungen, fg=Skin.color_font_Einstellungen, text="Runden: %s" % (Intro.runden))
            # Runde
        self.runde_minutes = round(Intro.runde/60)
        self.runde_seconds = round(Intro.runde - self.runde_minutes*60.0)
        self.runde_readable = ('%02d:%02d' % (self.runde_minutes, self.runde_seconds))
        self.runde = Label(self.frame_fg, font=("Arial", 15), bg=Skin.color_bg_buttons_Einstellungen, fg=Skin.color_font_Einstellungen, text="Runde: %s" % (self.runde_readable))
            # Pause
        self.pause_minutes = round(Intro.pause/60)
        self.pause_seconds = round(Intro.pause - self.pause_minutes*60.0)
        self.pause_readable = ('%02d:%02d' % (self.pause_minutes, self.pause_seconds))
        self.pause = Label(self.frame_fg, font=("Arial", 15), bg=Skin.color_bg_buttons_Einstellungen, fg=Skin.color_font_Einstellungen, text="Pause: %s" % (self.pause_readable))

        # Grid erstellen
        self.frame_bg.grid(column=0, row=0, sticky=NW)
        self.frame_fg.grid(column=0, row=0, sticky=W)#, pady=10)
        # Grid befüllen
            # Hintergrund
        self.canvas_bg.grid(column=0, row=0)
            # Buttons & Labels
                # Optionen
        self.canvas_optionen.grid(column=3, row=2, padx=33, sticky=S)
                # Play
        self.canvas_play.grid(column=3, row=0, rowspan=3, padx=33, sticky=N)
                # Runden
        self.canvas_plus_runden.grid(column=0, row=0, pady=5)
        self.runden_display.grid(column=1, row=0)
        self.canvas_schrift_1.grid(column=1, row=0, pady=5)
        self.canvas_minus_runden.grid(column=2, row=0, pady=5)
                # Runde
        self.canvas_plus_runde.grid(column=0, row=1, pady=5)
        self.runde.grid(column=1, row=1)
        self.canvas_schrift_2.grid(column=1, row=1, pady=5)
        self.canvas_minus_runde.grid(column=2, row=1, pady=5)
                # Pause
        self.canvas_plus_pause.grid(column=0, row=2, pady=5)
        self.pause.grid(column=1, row=2)
        self.canvas_schrift_3.grid(column=1, row=2, pady=5)
        self.canvas_minus_pause.grid(column=2, row=2, pady=5)

class Uhr_laeuft(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent

        self.frame_bg = tk.Frame(self, width=480, height=320, bg=Skin.color_bg_Uhr)
        self.frame_fg = tk.Frame(self, width=480, height=320, bg=Skin.color_bg_Uhr)
        self.frame_fg_timer = tk.Frame(self, width=480, height=320, bg=Skin.color_bg_Uhr)

        self.Buttons()
        self.Update()

    def Update(self):
        if Struktur.akt_frame == ("Uhr_laeuft"):
            self.Labels()
        self.timer = self.after(Intro.update_frames, self.Update)

    def Pause_Button(self):
        if Intro.start == True:
            Uhr().Start()

    def Einstellungen_Button(self):
        Intro.reset = 1
        Uhr().Reset()
        self.controller.show_frame("Einstellungen")
    
    def Buttons(self):
        # Hintergrund
        self.canvas_bg = Canvas(self.frame_bg, height=320, width=480, bg=Skin.color_bg_Uhr, highlightthickness=0)
        self.canvas_bg.bind("<Button-1>", lambda event: Uhr().Start())

        # Play/Pause Button - Anzeige unter Buttons, da Aktualisierung
        self.image_play = PhotoImage(file = "play50.gif")
        self.image_pause = PhotoImage(file = "pause50.gif")
        # Reset Button
        self.canvas_reset = Canvas(self.frame_fg, bg=Skin.color_bg_buttons_Uhr, height=75, width=176, highlightthickness=0)
        self.canvas_reset.bind("<Button-1>", lambda event: Uhr().Reset())
        self.image_reset = PhotoImage(file = 'stop50.gif')
        self.reset = self.canvas_reset.create_image(88, 37, anchor=CENTER, image=self.image_reset)
        # Einstellungen Button
        self.canvas_einstellungen = Canvas(self.frame_fg, bg=Skin.color_bg_buttons_Uhr, height=75, width=176, highlightthickness=0)
        self.canvas_einstellungen.bind("<Button-1>", lambda event: self.Einstellungen_Button())
        self.image_einstellungen = PhotoImage(file = 'einstellungen70.gif')
        self.einstellungen = self.canvas_einstellungen.create_image(88, 37, anchor=CENTER, image=self.image_einstellungen)

    def Labels(self):
        # Play/Pause Button - Anzeige
        self.canvas_play = Canvas(self.frame_fg, bg=Skin.color_bg_buttons_Uhr, height=75, width=176, highlightthickness=0)
        self.canvas_play.bind("<Button-1>", lambda event: Uhr().Start())
        if Intro.start == False:
            self.play = self.canvas_play.create_image(88, 37, anchor=CENTER, image=self.image_play)
        if Intro.start == True:
            self.play = self.canvas_play.create_image(88, 37, anchor=CENTER, image=self.image_pause)

        # Runde Counter - erstellen
        self.runde_minutes = round(Intro.runde_counter/60, 0)
        self.runde_seconds = round(Intro.runde_counter - self.runde_minutes*60.0, 0)
        self.runde_readable = ('%02d:%02d' % (self.runde_minutes, self.runde_seconds))

        # Pausen Counter - erstellen
        self.pause_minutes = round(Intro.pause_counter/60, 0)
        self.pause_seconds = round(Intro.pause_counter - self.pause_minutes*60.0, 0)
        self.pause_readable = ('%02d:%02d' % (self.pause_minutes, self.pause_seconds))

        # Runde/Pause anzeigen
        self.label_ueberschrift = Label(self.frame_fg_timer, font=("Arial", 30), bg=Skin.color_bg_Uhr, fg="white", text="Runde")
        self.label_ueberschrift.bind("<Button-1>", lambda event: Uhr().Start())
        if Intro.start_pause == True:
            self.label_ueberschrift = Label(self.frame_fg_timer, font=("Arial", 30), bg=Skin.color_bg_Uhr, fg="white", text="Runde")
            self.label_runde = Label(self.frame_fg_timer, font=("Arial", 80), bg=Skin.color_bg_Uhr, fg="white", text=self.runde_readable)
            self.label_runde.bind("<Button-1>", lambda event: Uhr().Start())
        if Intro.start_pause == False:
            self.label_ueberschrift = Label(self.frame_fg_timer, font=("Arial", 30), bg=Skin.color_bg_Uhr, fg="white", text="Pause")
            self.label_runde = Label(self.frame_fg_timer, font=("Arial", 80), bg=Skin.color_bg_Uhr, fg="white", text=self.pause_readable)
            self.label_runde.bind("<Button-1>", lambda event: Uhr().Start())

        # Runden Counter
        self.label_runden = Label(self.frame_fg_timer, font=("Arial", 30), bg=Skin.color_bg_Uhr, fg="white", text = "   " + str(Intro.runden_counter) + " / " + str(Intro.runden) + "   ")
        self.label_runden.bind("<Button-1>", lambda event: Uhr().Start())

        # Anzeige Original-Zeiten
        self.runde_org_minutes = round(Intro.runde/60)
        self.runde_org_seconds = round(Intro.runde - self.runde_minutes*60.0)
        self.runde_org_readable = ('%02d:%02d' % (self.runde_org_minutes, self.runde_org_seconds))
        self.pause_org_minutes = round(Intro.pause/60)
        self.pause_org_seconds = round(Intro.pause - self.pause_org_minutes*60.0)
        self.pause_org_readable = ('%02d:%02d' % (self.pause_org_minutes, self.pause_org_seconds))
        self.label_org_zeiten = Label(self.frame_fg_timer, font=("Arial", 12), bg=Skin.color_bg_Uhr, fg="white", text=str(self.runde_org_readable) + " / " + str(self.pause_org_readable))
        self.label_org_zeiten.bind("<Button-1>", lambda event: Uhr().Start(Uhr))

        # Grid erstellen
        self.frame_bg.grid(column=0, row=0, sticky = NW)
        self.frame_fg.grid(column=0, row=0, sticky = W)
        self.frame_fg_timer.grid(column=0, row=0, padx=15, sticky = E)

        # Grid befuellen - Hintergrund
        self.canvas_bg.grid(column=0, row=0)        

        # Grid befuellen - Buttons
        self.canvas_play.grid(column=0, row=0, pady=5)#, rowspan=4)
        self.canvas_reset.grid(column=0, row=1, pady=5)#, rowspan=4)
        self.canvas_einstellungen.grid(column=0, row=2, pady=5)# rowspan=4)

        # Grid befuellen - Label
        self.label_ueberschrift.grid(column=0, row=0)
        self.label_runde.grid(column=0, row=1)
        self.label_runden.grid(column=0, row=2)
        self.label_org_zeiten.grid(column=0, row=3)

class Uhr(tk.Frame):
    def __init__(self, *args, **kwargs):
    #    tk.Frame.__init__(self, parent)
    #    self.controller = controller
        pass

    #Runden
    def plus_runden(self):
        if Intro.runden < 99 and Intro.mouse_down_plus_runden == True:
                Intro.runden += 1

    def minus_runden(self):
        if Intro.runden > 1 and Intro.mouse_down_minus_runden == True:
            Intro.runden -= 1

    #Runde
    def plus_runde(self):
        if Intro.runde < 5999 and Intro.mouse_down_plus_runde == True:
            Intro.runde += 1

    def minus_runde(self):
        if Intro.runde > 1 and Intro.mouse_down_minus_runde == True:
            Intro.runde -= 1

    #Pause
    def plus_pause(self):
        if Intro.pause < 5999 and Intro.mouse_down_plus_pause == True:
            Intro.pause += 1

    def minus_pause(self):
        if Intro.pause > 0 and Intro.mouse_down_minus_pause == True:
            Intro.pause -= 1

    #Reset
    def Reset(self):
        if Intro.start == False: # Wenn die Uhr steht, kompletter Reset - auch Runden
            Intro.runden_counter=Intro.runden
        Intro.start = False
        Intro.start_pause = True
        Intro.runde_counter=Intro.runde
        Intro.pause_counter=Intro.pause
        Intro.pause_zeit=0

    #Start & Stop
    def Start(self):
        #Flag umsetzen
        Intro.start = not Intro.start
        #Wenn Uhr gestartet, Zeit merken
        if Intro.start == True:
            pygame.mixer.music.load("Runde.mp3")
            pygame.mixer.music.play()
            Intro.startzeit = time.time() + Intro.pause_zeit
        #Wenn Uhr neu gestartet wurde, Differenz zwischen letztem und aktuellem Start anpassen
        if Intro.start == False:
            Intro.pause_zeit = Intro.startzeit - time.time()

    #Update
    def Update(self):

        # Uhr startet
        if Intro.start == True:                                      

            # Runde startet
            if Intro.start_pause == True:
                self.execution_time = time.time() - Intro.startzeit
                Intro.runde_counter = Intro.runde - self.execution_time

                # 10 Sekunden Warnung
                if Intro.tensec == True and round(Intro.runde_counter) == 10 and Intro.runde > 12:
                    if sys.platform == 'linux':
                        pygame.mixer.music.load("10sec.mp3")
                        pygame.mixer.music.play()

                # Runde zuende
                if round(Intro.runde_counter) == 0:
                    pygame.mixer.music.load("Pause.mp3")
                    pygame.mixer.music.play()
                    if Intro.runden_counter > 1:
                        # Runde stopen & Pause starten
                        Intro.start_pause = False
                        # Runde neue fuellen
                        Intro.runde_counter = Intro.runde
                        # Zeit fuer Pause setzen
                        Intro.startzeit = time.time()
                    # letzte Runde
                    if Intro.runden_counter == 1:
                        # Runden runter zählen
                        Intro.runden_counter -= 1
                        # Stopen der Uhr
                        Intro.start = False
                        # Sound
                        pygame.mixer.music.load("End.mp3")
                        pygame.mixer.music.play()

            # Pause startet
            if Intro.start_pause == False:
                self.execution_time_pause = time.time() - Intro.startzeit
                Intro.pause_counter = Intro.pause - self.execution_time_pause

                # Pause zuende
                if round(Intro.pause_counter) == 0:
                    pygame.mixer.music.load("Runde.mp3")
                    pygame.mixer.music.play()
                    # Pause neu fuellen
                    Intro.pause_counter = Intro.pause
                    # Runde starten & Pause stoppen
                    Intro.start_pause = True
                    # Zeit fuer Start setzen
                    Intro.startzeit = time.time()
                    # Runden runter zählen
                    Intro.runden_counter -= 1
                        
if __name__ == "__main__":
    root = Struktur()

    root.wm_geometry("480x320")
    root.overrideredirect(True)
    #root.wm_attributes("-fullscreen", True)
    root.wm_attributes("-topmost", True)
    #time.sleep(0.5)

    root.mainloop()