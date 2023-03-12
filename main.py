#! /usr/bin/python3
import os
import tkinter as Tk
from tkinter import *
from tkinter.messagebox import showerror, showinfo
from pytube import YouTube
from pytube import Playlist

telecharger = []

def add_url(*event) :
    url = entry_url.get()
    if not url == '' :
        telecharger.append(url)
        try :
            yt = YouTube(url)
            listbox.insert(END, f'{url} || {yt.title}')
        except :
            try :
                playlist = Playlist(url)
                listbox.insert(END, f'{url} || {playlist.title}')
            except :
                listbox.insert(END, f'{url} || Nom inconnu')
        
        finally :
            entry_url.delete(0,END)

def telechargement() :
    
    if value.get() == '' :
        showerror('Erreur', 'Rentrer un format de téléchargement')
        return
    
    source_to = entry_chemin.get()
    output = Toplevel()
    output.title('Sortie')
    
    output_listbox = Listbox(output, height=10, width=100)
    output_listbox.pack()
    
    
    quit_boutton = Button(output, text = 'OK', command=output.quit)
    quit_boutton.pack()
    output_listbox.insert(END, f"Téléchargement en cours")
    #mp3
    for url in telecharger :
        try :
            #Vidéo unique
            if value.get() == 'Audio' :
                #audio uniquement
                yt = YouTube(url)
                video = yt.streams.filter(only_audio=True).first()
                destination = source_to
                out_file = video.download(output_path=destination)
                base, ext = os.path.splitext(out_file)
                new_file = base + '.mp3'
                os.rename(out_file, new_file)
                output_listbox.insert(END, f"{yt.title} a bien été téléchargé :).")
                
            
            elif value.get() == 'Video' :
                #Vidéo
                audio = yt.streams.filter().first()
                out_file = audio.download()
                base, ext = os.path.splitext(out_file)
                new_file = base + '.mp4'
                os.rename(out_file, new_file)
                output_listbox.insert(END, f"{yt.title} a bien été téléchargé :).")
                
        except Exception as ex :
            try :
                playlist = Playlist(url)
                videos = playlist.video_urls

                for video in videos:
                    if value.get() == 'Audio' :
                        #audio uniquement
                        yt = YouTube(url)
                        video = yt.streams.filter(only_audio=True).first()
                        destination = source_to
                        out_file = video.download(output_path=destination)
                        base, ext = os.path.splitext(out_file)
                        new_file = base + '.mp3'
                        os.rename(out_file, new_file)
                        output_listbox.insert(END, f"{yt.title} a bien été téléchargé :).")
                        
                    
                    elif value.get() == 'Video' :
                        #Vidéo
                        audio = yt.streams.filter().first()
                        out_file = audio.download()
                        base, ext = os.path.splitext(out_file)
                        new_file = base + '.mp4'
                        os.rename(out_file, new_file)
                        output_listbox.insert(END, f"{yt.title} a bien été téléchargé :).")
            except Exception as ex :
                output_listbox.insert(END, f'Une erreur s\'est produite :(. l\'url "{url}" n\'a pas pus être téléchargé, erreur : {ex}')
    output_listbox.insert(END, f"Fin des Téléchargements")
    listbox.delete(0,END)
    
    output.mainloop()

def clique_droit(event):
    try:
        m.tk_popup(event.x_root, event.y_root)
    finally:
        m.grab_release()
        
def delete_url(*event) :
    for index in listbox.curselection():
        url = listbox.get(index)
        listbox.delete(index)
        url = url.split(' || ')[0]
        telecharger.remove(url)
        
def add_playlist(*event) :
    
    url = entry_url.get()
    
    playlist = Playlist(url)
    videos = playlist.video_urls

    for video in videos:
        yt = YouTube(video)
        url = yt.watch_url
        telecharger.append(url)
        try :
            yt = YouTube(url)
            listbox.insert(END, f'{url} || {yt.title}')
        except :
            listbox.insert(END, f'{url} || Nom inconnu')
    
    entry_url.delete(0,END)
        
def edit_chemin(*event) :
    def new_chemin_save(*event) :
        new_chemin = new_chemin_entry.get()
        open('chemin_defaults_yt.txt', 'w').write(new_chemin)
        entry_chemin.delete(0,END)
        entry_chemin.insert(0, new_chemin)
        new_chemin_entry.delete(0, END)
        showinfo('Information', 'Chemin enregistré')
    chemingui = Toplevel()
    chemingui.title('Éditer le chemin par défaut')
    label = Label(chemingui, text = 'Entrer le nouveau chemin : ').pack(side=LEFT)
    new_chemin_entry = Entry(chemingui, width = 100)
    new_chemin_entry.pack()
    new_chemin_entry.bind("<Return>", new_chemin_save)
    ok_boutton = Button(chemingui, text='OK', command=new_chemin_save)
    ok_boutton.pack(side=RIGHT)
    
    

gui = Tk()
gui.title('Téléchargeur youtube')

menubar = Menu(gui)

menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="Éditer le chemin par défaut", command=edit_chemin)
menu1.add_separator()
menu1.add_command(label="Quitter", command=gui.quit)
menubar.add_cascade(label="Fichier", menu=menu1)

menu3 = Menu(menubar, tearoff=0)
menu3.add_command(label="À propos")
menubar.add_cascade(label="Aide", menu=menu3)

gui.config(menu=menubar)


m = Menu(gui, tearoff=0)

m.add_command(label="Supprimer", command=delete_url)

listbox = Listbox(gui, height=10, width=100)
listbox.pack()
listbox.bind("<Delete>", delete_url)

Frame1 = Frame(gui, relief=FLAT)
Frame1.pack()

Frame2 = Frame(Frame1, relief=FLAT)
Frame2.pack(side=RIGHT)

entry_url = Entry(Frame1, width = 80)
entry_url.pack(side=LEFT)
entry_url.bind("<Return>", add_url)

valider_bouton = Button(Frame2, text='Ajouter l\'url', command=add_url, width = 16)
valider_bouton.pack(side=BOTTOM)


playlist_boutton = Button(Frame2, text='Ajouter une playlist', command=add_playlist)
playlist_boutton.pack(side=TOP)


delete_boutton = Button(gui, text='Supprimer l\'url sélectionnée', command=delete_url)
delete_boutton.pack(side=TOP)


value = StringVar() 
bouton1 = Radiobutton(gui, text="Audio", variable=value, value='Audio')
bouton2 = Radiobutton(gui, text="Vidéo", variable=value, value='Video')
bouton1.pack()
bouton2.pack()

try :
    entry_chemin = Entry(gui, width = 100)
    entry_chemin.pack()
    entry_chemin.insert(0, open('chemin_default_yt.txt', 'r').read().splitlines()[0])
    entry_chemin.bind("<Return>", telechargement)
except :
    pass
telechargement_bouton = Button(gui, text='Téléchargement', command=telechargement)
telechargement_bouton.pack(side=TOP)

gui.mainloop()
