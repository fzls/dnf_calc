#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------
# File   : ui_components
# Date   : 2020/5/19 0019
# Author : Chen Ji
# Email  : fzls.zju@gmail.com
# -------------------------------
import tkinter.font
import tkinter.messagebox
import tkinter.ttk
from tkinter import *


# copy from https://gist.github.com/bakineugene/76c8f9bcec5b390e45df
# http://tkinter.unpythonic.net/wiki/VerticalScrolledFrame
class VerticalScrolledFrame(Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling
    """

    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        canvas = Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())

        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())

        canvas.bind('<Configure>', _configure_canvas)


# Combopicker code from @SilverHalo https://stackoverflow.com/questions/34549752/how-do-i-enable-multiple-selection-of-values-from-a-combobox
class Picker(tkinter.ttk.Frame):
    def __init__(self, master=None, activebackground='#b1dcfb', dict_intvar_item={}, values=[], entry_wid=None, activeforeground='black', selectbackground='#003eff', selectforeground='white', command=None, borderwidth=1, relief="solid"):
        self._selected_item = None

        self._values = values

        self._entry_wid = entry_wid

        self._sel_bg = selectbackground
        self._sel_fg = selectforeground

        self._act_bg = activebackground
        self._act_fg = activeforeground

        self._command = command
        tkinter.ttk.Frame.__init__(self, master, borderwidth=borderwidth, relief=relief)

        self.bind("<FocusIn>", lambda event: self.event_generate('<<PickerFocusIn>>'))
        self.bind("<FocusOut>", lambda event: self.event_generate('<<PickerFocusOut>>'))

        self._font = tkinter.font.Font()

        self.frame = VerticalScrolledFrame(self)
        self.frame.pack()

        self.dict_checkbutton = {}
        self.dict_checkbutton_var = {}
        self.dict_intvar_item = dict_intvar_item

        for index, item in enumerate(self._values):
            self.dict_intvar_item[item] = tkinter.IntVar()
            self.dict_checkbutton[item] = tkinter.ttk.Checkbutton(self.frame.interior, text=item, variable=self.dict_intvar_item[item], command=lambda ITEM=item: self._command(ITEM))
            self.dict_checkbutton[item].grid(row=index, column=0, sticky=tkinter.NSEW)
            self.dict_intvar_item[item].set(0)


class Combopicker(tkinter.ttk.Entry, Picker):
    def __init__(self, master, values=[], entryvar=None, entrywidth=None, entrystyle=None, onselect=None, activebackground='#b1dcfb', activeforeground='black', selectbackground='#003eff', selectforeground='white', borderwidth=1,
                 relief="solid"):

        if entryvar is not None:
            self.entry_var = entryvar
        else:
            self.entry_var = tkinter.StringVar()

        self.dict_intvar_item = {}

        entry_config = {}
        if entrywidth is not None:
            entry_config["width"] = entrywidth

        if entrystyle is not None:
            entry_config["style"] = entrystyle

        tkinter.ttk.Entry.__init__(self, master, textvariable=self.entry_var, **entry_config, state="readonly")

        self._is_menuoptions_visible = False

        self.picker_frame = Picker(self.winfo_toplevel(), dict_intvar_item=self.dict_intvar_item, values=values, entry_wid=self.entry_var, activebackground=activebackground, activeforeground=activeforeground,
                                   selectbackground=selectbackground, selectforeground=selectforeground,
                                   command=self._on_selected_check)

        self.bind_all("<1>", self._on_click, "+")

        self.bind("<Escape>", lambda event: self.hide_picker())

    @property
    def current_value(self):
        try:
            value = self.entry_var.get()
            return value
        except ValueError:
            return None

    def get_selected_entrys(self):
        return self.entry_var.get().split(",")

    @current_value.setter
    def current_value(self, INDEX):
        self.entry_var.set(self.values.index(INDEX))

    def set(self, checked_values):
        # 清空所有选项
        for item, intvar in self.dict_intvar_item.items():
            intvar.set(0)
        # 清空内容栏
        self.entry_var.set("")

        if checked_values is None:
            return

        # 添加选项与内容
        temp_value = ""
        for item in checked_values:
            try:
                self.dict_intvar_item[item].set(1)
                if len(temp_value) != 0:
                    temp_value += ","
                temp_value += str(item)
            except:
                pass

        self.entry_var.set(temp_value)

    def _on_selected_check(self, SELECTED):

        value = []
        if self.entry_var.get() != "" and self.entry_var.get() != None:
            temp_value = self.entry_var.get()
            value = temp_value.split(",")

        if str(SELECTED) in value:
            value.remove(str(SELECTED))

        else:
            value.append(str(SELECTED))

        value.sort()

        temp_value = ""
        for index, item in enumerate(value):
            if item != "":
                if index != 0:
                    temp_value += ","
                temp_value += str(item)

        self.entry_var.set(temp_value)

    def _on_click(self, event):
        str_widget = str(event.widget)

        if str_widget == str(self):
            if not self._is_menuoptions_visible:
                self.show_picker()
        else:
            if not str_widget.startswith(str(self.picker_frame)) and self._is_menuoptions_visible:
                self.hide_picker()

    def show_picker(self):
        if not self._is_menuoptions_visible:
            self.picker_frame.place(in_=self, relx=0, rely=1, relwidth=1)
            self.picker_frame.lift()

        self._is_menuoptions_visible = True

    def hide_picker(self):
        if self._is_menuoptions_visible:
            self.picker_frame.place_forget()

        self._is_menuoptions_visible = False
