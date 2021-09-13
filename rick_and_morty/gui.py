from ramAPI import ramAPI
from tkinter import ttk
import tkinter as tk
import ram_display
import UPL

class gui:
    def __init__(self, RAMAPI:ramAPI) -> None:
        self.ramAPI = RAMAPI
        self.current_selected = "character"
        self.page_no = 0
        self.current_dict = {}
        self.root = tk.Tk()
        
        self.curser_selected = ""
        
        self.layout()
        self.selected_Type(self.current_selected)
        
        self.page_count.set(f"Page: {self.page_no}/{self.current_dict['info']['pages']}")
        self.root.mainloop()
    
    ## update what is in the gen_listbox
    def update_list(self, results:list) -> None:
        self.gen_listbox.delete(0, self.gen_listbox.size())
        for i in results:
            self.gen_listbox.insert(tk.END, f"[{i['id']}] {i['name']}")
        
        self.page_count.set(f"Page: {self.page_no}/{self.current_dict['info']['pages']}")

    ## what are we dealing with (character|episode|location)
    def selected_Type(self, btn_name:str) -> None:
        self.current_selected = btn_name
        
        self.current_dict = self.ramAPI.get_all(self.current_selected)
        self.update_list(self.current_dict['results'])
    
    ## continue to next page
    def next_page(self) -> None:
        if self.current_dict['info']['next'] == None:
            print("Cannot go any further")
            return
        self.current_dict = self.ramAPI.get_all(page=self.current_dict['info']['next'])
        self.page_no += 1
        self.update_list(self.current_dict['results'])
        self.page_count.set(f"Page: {self.page_no}/{self.current_dict['info']['pages']}")
    
    ## return to previous page
    def prev_page(self) -> None:
        if self.current_dict['info']['prev'] == None:
            print('There is nothing further back')
            return
        self.current_dict = self.ramAPI.get_all(page=self.current_dict['info']['prev'])
        self.page_no -= 1
        self.update_list(self.current_dict['results'])
        self.page_count.set(f"Page: {self.page_no}/{self.current_dict['info']['pages']}")
    
    def run_query(self) -> None:
        if self.current_selected == 'character':
            name = UPL.gui.prompt("Character Name", "Character name (enter to ignore)", 'ignore')
            status = UPL.gui.confirm("Character Status", "Character status:", ["alive",'dead','unknown','ignore'])
            species = UPL.gui.prompt("Character Species", "Character species (enter to ignore)", 'ignore')
            cType = UPL.gui.prompt("Character Type", "Character type (enter to ignore)", 'ignore')
            gender = UPL.gui.confirm('Character Gender', "Character gender:", ['female', 'male', 'genderless', 'unknown', 'ignore'])
        
            self.current_dict = self.ramAPI.query(get_type=self.current_selected, name=name, status=status, species=species, type=cType, gender=gender)
        
        elif self.current_selected == 'episode':
            name = UPL.gui.prompt("Episode Name", "Location name (enter to ignore)", 'ignore')
            episode = UPL.gui.prompt("Episode Code", "Episode Code (enter to ignore)", "ignore")
            self.current_dict = self.ramAPI.query(get_type=self.current_selected, name=name, episode=episode)
        
        elif self.current_selected == 'location':
            name = UPL.gui.prompt("Location Name", "Location name (enter to ignore)", 'ignore')
            cType = UPL.gui.prompt("Location Type", "Location type (enter to ignore)", 'ignore')
            dimension = UPL.gui.prompt("Location Dimension", "Location Dimension (enter to ignore)", 'ignore')
    
            self.current_dict = self.ramAPI.query(get_type=self.current_selected ,name=name, type=cType, dimension=dimension)
        
        self.page_no = 0
        self.page_count.set(f"Page: {self.page_no}/{self.current_dict['info']['pages']}")
        self.update_list(self.current_dict['results'])
        
    ## change what is currently selected
    def listBox_select(self, event) -> None:
        widget = event.widget
        selection = widget.curselection()
        picked = widget.get(selection[0])
        self.curser_selected = picked
    
    ## displaying selected data (just to prevent accidental loading)
    def load_display(self) -> None:
        item_id = self.curser_selected.split(']')[0].replace('[', '')
        page_url = self.ramAPI.urls[self.current_selected] + item_id
        ram_display.display_selected(self.ramAPI.get_all(page=page_url), self.current_selected)
    
    ## general layout of the gui
    def layout(self) -> None:
        ## top and bottom frames
        self.top_btn_frame = tk.Frame(self.root)
        self.bottom_btn_frame = tk.Frame(self.root)
        
        self.page_count = tk.StringVar(self.top_btn_frame)
        
        ## listbox and scrollbar (in case needed)
        self.gen_listbox = tk.Listbox(self.root)
        scrollbar = tk.Scrollbar(self.root)
        scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)
        
        self.gen_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.gen_listbox.yview)
        
        ttk.Label(self.top_btn_frame, textvariable=self.page_count).grid(row=0, column=0)
        
        ## Buttons
        ttk.Button(self.top_btn_frame, text='characters', command=lambda: self.selected_Type('character')).grid(row=0, column=2)
        ttk.Button(self.top_btn_frame, text='locations', command=lambda: self.selected_Type('location')).grid(row=0, column=4)
        ttk.Button(self.top_btn_frame, text='episodes', command=lambda: self.selected_Type('episode')).grid(row=0, column=6)
        ttk.Button(self.top_btn_frame, text="query", command=self.run_query).grid(row=0, column=8)
        
        ## bottom bar
        ttk.Button(self.bottom_btn_frame, text='prev', command=self.prev_page).grid(row=2, column=2)
        ttk.Button(self.bottom_btn_frame, text='next', command=self.next_page).grid(row=2, column=4)
        ttk.Button(self.bottom_btn_frame, text='Display Selected', command=self.load_display).grid(row=2, column=0)

        ## packs
        self.top_btn_frame.pack()
        self.gen_listbox.pack(fill=tk.BOTH, expand=5) 
        self.bottom_btn_frame.pack(side=tk.BOTTOM)
        
        ## window stuff
        self.root.resizable(False, False)
        self.root.geometry('500x500')
        self.root.title("Rick And Morty Index")
        self.root.iconphoto(False, tk.PhotoImage(file="images/icon.png"))
        
        ## binds
        self.root.bind("<<ListboxSelect>>", self.listBox_select)
    
def main() -> None:
    base_url = "https://rickandmortyapi.com/api/"
    ram = ramAPI(base_url)
    GUI = gui(ram)
    
if __name__ == "__main__":
    main()
    