from PIL import ImageTk, Image
from io import BytesIO
import tkinter as tk
import requests

## displaying selected character/episode/location
def display_selected(selected_dict:dict, lookup_type:str) -> None:
    win = tk.Toplevel()
    ## display avatar image
    if 'image' in selected_dict.keys():
        img_url = selected_dict['image']
        img_data = requests.get(img_url).content
        img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))
        tk.Label(win, image=img).pack()
    
    ## display name
    tk.Label(win, text=f'Name: {selected_dict["name"]}', font=("Arial", 14)).pack()
    
    ## is an episode
    if lookup_type == 'episode':
        tk.Label(win, text=f"Air Date: {selected_dict['air_date']}\nEpisode: {selected_dict['episode']}", font=("Arial", 14)).pack()
    
    ## is a character 
    elif lookup_type == 'character':
        ## dispalay stats
        tk.Label(win, text=f'Status: {selected_dict["status"]}\nSpecies: {selected_dict["species"]}\nGender: {selected_dict["gender"]}\nType: {selected_dict["type"] if selected_dict["type"] != "" else "Character"}\nOrigin: {selected_dict["origin"]["name"]}\nLocation: {selected_dict["location"]["name"]}', font=("Arial", 14)).pack()
    
    ## is a planet
    else:
        tk.Label(win, text=f"Dimension: {selected_dict['dimension']}\nType: {selected_dict['type']}", font=("Arial", 14)).pack()

    ## window conf
    win.title(selected_dict['name'])
    
    ## icon
    icon_img = tk.PhotoImage(file='images/icon.png')
    win.iconphoto(False, icon_img)
    win.mainloop()
