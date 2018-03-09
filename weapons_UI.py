#!/usr/bin/python3

import tkinter as tk
import tkinter.ttk
import weapons

class WeaponsManagerUI(tk.Frame):

    def __init__(self, save_data, on_close=None):

        self._save_data = bytearray(save_data)
        self._items_manager = weapons.WeaponsRecordManager(self._save_data)
        self.updated_items = {}

        root = tk.Toplevel()
        root.geometry('640x480')
        root.title("NieR;Automata Weapons Editor")

        super().__init__(root)
        self.pack(side="top", fill="both", expand=True)
        self.create_widgets()

        if callable(on_close):
            self.bind("<Destroy>", lambda _: on_close(self._save_data))

			
    def create_widgets(self):
        right_frame = tk.Frame(self, background="#eeeeee", width=20)

        tk.Button(right_frame, text="Save", width=8, height=3, state="disabled", command=self.on_save_clicked).grid(row=1, column=0)
        tk.Button(right_frame, text="Close", width=8, height=3, command=self.on_close_clicked).grid(row=2, column=0)
        canvas = tk.Canvas(self, borderwidth=0, background="#ccffff", width=30)
        frame = tk.Frame(canvas, background="#ffffff")
        vsb = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        right_frame.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window((4, 4), window=frame, anchor="nw", tags="self.frame")
        frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        self.populate(frame)

    def populate(self, parent):
        available_weapons = weapons.WeaponsRecord.AVAILABLE_WEAPONS
        
        tk.Label(parent, text="Found", width=6, borderwidth="1", relief="solid").grid(row=0, column=1)
        tk.Label(parent, text="Level", width=6, borderwidth="1", relief="solid").grid(row=0, column=3)
        tk.Label(parent, text="New", width=4, borderwidth="1", relief="solid").grid(row=0, column=4)
        tk.Label(parent, text="Story", width=5, borderwidth="1", relief="solid").grid(row=0, column=5)
        tk.Label(parent, text="Kills", width=6, borderwidth="1", relief="solid").grid(row=0, column=6)
        
        # available_sizes = [i for i in range(31)]
        for rowe in range(self._items_manager.SAVE_DATA_WEAPONS_COUNT):
            row=rowe+1
            item_name = tk.StringVar()
            weapon_level = tk.StringVar(name="%u" % row)
            weapon_kills = tk.StringVar()
            weapon_new = tk.StringVar()
            weapon_story = tk.StringVar()
            weapon_found = tk.StringVar()
            
            
            
            # For some reason, checkbuttons need both variable and textvariable, or it doesn't work. Dunno why.
            
            
            
            found_chb = tk.Checkbutton(parent, text="", variable=weapon_found, state="disabled", textvariable=weapon_found, name='found_chb@%u' % row)
            weapon_cb = tk.ttk.Combobox(parent, width=45, values=available_weapons, state="disabled", textvariable=item_name, name='combobox@%u' % row)
            level_sb = tk.Spinbox(parent, width=5, from_=1, to=4, textvariable=weapon_level, state="disabled", name='spinbox@%u' % row)
            new_chb = tk.Checkbutton(parent, text="", variable=weapon_new, textvariable=weapon_new, state="disabled", name='new_chb@%u' % row)
            story_chb = tk.Checkbutton(parent, text="", variable=weapon_story, textvariable=weapon_story, state="disabled", name='story_chb@%u' % row)
            kills_sb = tk.Spinbox(parent, width=6, from_=0, to=65535, textvariable=weapon_kills, state="disabled", name='spinbox2@%u' % row)
            id_tb = tk.Label(parent)
            
            found_chb.grid(row=row, column=1)
            weapon_cb.grid(row=row, column=2)
            level_sb.grid(row=row, column=3)
            new_chb.grid(row=row, column=4)
            story_chb.grid(row=row, column=5)
            kills_sb.grid(row=row, column=6)
            id_tb.grid(row=row, column=7)
			
            current = self._items_manager.get_item_at(rowe)
            if current != weapons.WeaponsRecord.EMPTY_RECORD:
                weapon_level.set(current.weapon_level)
                weapon_kills.set(current.weapon_kills)
                weapon_new.set(current.weapon_new)
                weapon_story.set(current.weapon_story)
                weapon_found.set("1")
                id_tb["text"] = '0x%04X' % current.weapon_id
                if -1 == current.name.find("Invalid"):
                    index = available_weapons.index(current.name)
                    weapon_cb.current(available_weapons.index(current.name))
                #weapon_cb.config(state=tk.DISABLED)
            else:
                #weapon_cb.config(values=self.available_weapons)
                weapon_cb.current(0)
                weapon_level.set(0)
                weapon_new.set(0)
                weapon_story.set(0)
                weapon_found.set("0")
                id_tb["text"] = '0x%04X' % 0
                level_sb.config(state=tk.DISABLED)
                new_chb.config(state=tk.DISABLED)
                story_chb.config(state=tk.DISABLED)
                kills_sb.config(state=tk.DISABLED)
            data = (row, item_name, weapon_level, weapon_kills)
            weapon_cb.bind("<<ComboboxSelected>>", lambda e, args=data: self.on_weapon_cb_selected(e, args))
            weapon_level.trace('w', self.on_level_sb_changed)
            weapon_kills.trace('w', self.on_kills_sb_changed)

    def on_weapon_cb_selected(self, event, args):
        asd = 0
        # print("index:{0} name:{1} count:{2}".format(args[0], args[1].get(), args[2].get()))
        # row = args[0]
        # count_sb = self.nametowidget('!canvas.!frame.spinbox@%u' % row)
        # if args[1].get() != "(Empty)":
            # record = weapons.WeaponsRecord.from_name(args[1].get())
            # if 1 == record.uq:
                # count_sb.config(to=1)
            # else:
                # count_sb.config(to=99)
            # args[2].set("0")
            # count_sb.config(state=tk.NORMAL)
        # else:
            # record = weapons.WeaponsRecord.EMPTY_RECORD
            # args[2].set("0")
            # count_sb.config(to=99)
            # count_sb.config(state=tk.DISABLED)
        # self.updated_items[row] = record

    def on_level_sb_changed(self, *args):
        asd = 0
        # if 'w' == args[2]:
            # row = args[0]
            # count_sb = self.nametowidget('!canvas.!frame.spinbox@'+row)
            # weapon_cb = self.nametowidget('!canvas.!frame.combobox@'+row)
            # count = count_sb.get()
            # record = weapons.WeaponsRecord.from_name(weapon_cb.get())
            # record.item_count = int(count)
            # self.updated_items[row] = record
    
    def on_kills_sb_changed(self, *args):
        asd = 0
        # if 'w' == args[2]:
            # row = args[0]
            # count_sb = self.nametowidget('!canvas.!frame.spinbox@'+row)
            # weapon_cb = self.nametowidget('!canvas.!frame.combobox@'+row)
            # count = count_sb.get()
            # record = weapons.WeaponsRecord.from_name(weapon_cb.get())
            # record.item_count = int(count)
            # self.updated_items[row] = record
			


    def on_save_clicked(self):
        for index, record in self.updated_items.items():
            self._items_manager.set_item_at(int(index), record)
            self._save_data[weapons.WeaponsRecordManager.SAVE_DATA_ITEMS_OFFSET:
                            weapons.WeaponsRecordManager.SAVE_DATA_ITEMS_OFFSET_END] = self._items_manager.blocks
        self.master.destroy()

    def on_close_clicked(self):
        self.master.destroy()


if __name__ == "__main__":

    root = tk.Tk()

    def open_ui():
        with open("./SlotData_0.dat", "rb") as f:
            data = f.read()
        ItemsManagerUI(data, lambda out: print(len(out)))

    tk.Button(root, text="Open", command=open_ui).pack(fill="both")

    root.mainloop()
