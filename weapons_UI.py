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

        tk.Button(right_frame, text="Save", width=8, height=3, command=self.on_save_clicked).grid(row=1, column=0)
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
        available_items = weapons.ItemsRecord.AVAILABLE_ITEMS
        # available_sizes = [i for i in range(31)]
        for row in range(self._items_manager.SAVE_DATA_ITEMS_COUNT):
            item_name = tk.StringVar()
            item_level = tk.StringVar(name="%u" % row)
            item_kills = tk.StringVar()
            tk.Label(parent, text=str(row), width=3, borderwidth="1", relief="solid").grid(row=row, column=0)
            item_cb = tk.ttk.Combobox(parent, width=50, values=available_items, state="readonly", textvariable=item_name, name='combobox@%u' % row)
            item_cb.grid(row=row, column=1)
            level_sb = tk.Spinbox(parent, width=6, from_=1, to=4, textvariable=item_level, name='spinbox@%u' % row)
            level_sb.grid(row=row, column=2)
            kills_sb = tk.Spinbox(parent, width=6, from_=0, to=9999, textvariable=item_kills, name='spinbox2@%u' % row)
            kills_sb.grid(row=row, column=3)
            id_tb = tk.Label(parent)
            id_tb.grid(row=row, column=4)
			
            current = self._items_manager.get_item_at(row)
            if current != weapons.ItemsRecord.EMPTY_RECORD:
                item_level.set(current.item_level)
                item_kills.set(current.item_kills)
                id_tb["text"] = '0x%04X' % current.item_id
                if -1 == current.name.find("Invalid"):
                    index = available_items.index(current.name)
                    item_cb.current(available_items.index(current.name))
                #item_cb.config(state=tk.DISABLED)
            else:
                #item_cb.config(values=self.available_items)
                item_cb.current(0)
                item_level.set(0)
                id_tb["text"] = '0x%s' % 0
                level_sb.config(to=4)
                level_sb_sb.config(state=tk.DISABLED)
            data = (row, item_name, item_level, item_kills)
            item_cb.bind("<<ComboboxSelected>>", lambda e, args=data: self.on_item_cb_selected(e, args))
            item_level.trace('w', self.on_count_sb_changed)
            #item_kills.trace('w', self.on_kills_sb_changed)

    def on_item_cb_selected(self, event, args):
        # print("index:{0} name:{1} count:{2}".format(args[0], args[1].get(), args[2].get()))
        row = args[0]
        count_sb = self.nametowidget('!canvas.!frame.spinbox@%u' % row)
        if args[1].get() != "(Empty)":
            record = weapons.ItemsRecord.from_name(args[1].get())
            if 1 == record.uq:
                count_sb.config(to=1)
            else:
                count_sb.config(to=99)
            args[2].set("0")
            count_sb.config(state=tk.NORMAL)
        else:
            record = weapons.ItemsRecord.EMPTY_RECORD
            args[2].set("0")
            count_sb.config(to=99)
            count_sb.config(state=tk.DISABLED)
        self.updated_items[row] = record

    def on_count_sb_changed(self, *args):
        if 'w' == args[2]:
            row = args[0]
            count_sb = self.nametowidget('!canvas.!frame.spinbox@'+row)
            item_cb = self.nametowidget('!canvas.!frame.combobox@'+row)
            count = count_sb.get()
            record = weapons.ItemsRecord.from_name(item_cb.get())
            record.item_count = int(count)
            self.updated_items[row] = record
			


    def on_save_clicked(self):
        for index, record in self.updated_weapons.items():
            self._items_manager.set_item_at(int(index), record)
            self._save_data[weapons.ItemsRecordManager.SAVE_DATA_ITEMS_OFFSET:
                            weapons.ItemsRecordManager.SAVE_DATA_ITEMS_OFFSET_END] = self._items_manager.blocks
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
