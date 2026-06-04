import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
from core.config import *
from core.utils import resource_path

class CropEditor(ctk.CTkToplevel):
    def __init__(self, parent, image_path, callback, lang_code):
        super().__init__(parent)
        self.lang = lang_code
        self.callback = callback
        self.title("Crop Editor")
        self.geometry("900x750")
        self.attributes("-topmost", True)
        self.configure(fg_color="#000")
        
        try:
            self.iconbitmap(resource_path("App.ico"))
        except:
            pass

        self.pil_img = Image.open(image_path)
        self.orig_w, self.orig_h = self.pil_img.size
        
        self.cv_w, self.cv_h = 800, 550
        self.scale = min(self.cv_w / self.orig_w, self.cv_h / self.orig_h)
        self.disp_w = int(self.orig_w * self.scale)
        self.disp_h = int(self.orig_h * self.scale)
        
        self.offset_x = (self.cv_w - self.disp_w) // 2
        self.offset_y = (self.cv_h - self.disp_h) // 2

        img_resized = self.pil_img.resize((self.disp_w, self.disp_h), Image.Resampling.LANCZOS)
        self.tk_img = ImageTk.PhotoImage(img_resized)

        ctk.CTkLabel(self, text=LANG[self.lang]["crop_tip"], text_color="gray").pack(pady=5)
        
        self.canvas = tk.Canvas(self, width=self.cv_w, height=self.cv_h, bg="#111", highlightthickness=0, cursor="arrow")
        self.canvas.pack(pady=10)
        self.canvas.create_image(self.offset_x, self.offset_y, anchor="nw", image=self.tk_img)

        ctk.CTkButton(self, text=LANG[self.lang]["btn_apply"], fg_color=COLOR_ACCENT, hover_color=COLOR_ACCENT_HOVER, text_color="black", command=self.finish).pack(pady=10)

        self.rect_x1 = self.offset_x
        self.rect_y1 = self.offset_y
        self.rect_x2 = self.offset_x + self.disp_w
        self.rect_y2 = self.offset_y + self.disp_h
        
        self.drag_mode = None
        self.last_mouse_x = 0
        self.last_mouse_y = 0
        self.overlay_ids = []
        self.handle_ids = []
        self.rect_outline_id = None
        
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<Motion>", self.on_hover)
        
        self.draw_selection()

    def draw_selection(self):
        for oid in self.overlay_ids:
            self.canvas.delete(oid)
        self.overlay_ids = []
        fill_color = "black"
        stipple = "gray50" 
        
        self.overlay_ids.append(self.canvas.create_rectangle(0, 0, self.cv_w, self.rect_y1, fill=fill_color, stipple=stipple, outline=""))
        self.overlay_ids.append(self.canvas.create_rectangle(0, self.rect_y2, self.cv_w, self.cv_h, fill=fill_color, stipple=stipple, outline=""))
        self.overlay_ids.append(self.canvas.create_rectangle(0, self.rect_y1, self.rect_x1, self.rect_y2, fill=fill_color, stipple=stipple, outline=""))
        self.overlay_ids.append(self.canvas.create_rectangle(self.rect_x2, self.rect_y1, self.cv_w, self.rect_y2, fill=fill_color, stipple=stipple, outline=""))

        if self.rect_outline_id:
            self.canvas.delete(self.rect_outline_id)
        self.rect_outline_id = self.canvas.create_rectangle(self.rect_x1, self.rect_y1, self.rect_x2, self.rect_y2, outline=COLOR_ACCENT, width=2)
        
        for hid in self.handle_ids:
            self.canvas.delete(hid)
        self.handle_ids = []
        h_size = 8
        coords = [(self.rect_x1, self.rect_y1), (self.rect_x2, self.rect_y1), (self.rect_x1, self.rect_y2), (self.rect_x2, self.rect_y2)]
        for cx, cy in coords:
            self.handle_ids.append(self.canvas.create_rectangle(cx-h_size, cy-h_size, cx+h_size, cy+h_size, fill=COLOR_ACCENT, outline="black"))

    def get_interaction_mode(self, x, y):
        th = 15
        if abs(x - self.rect_x1) < th and abs(y - self.rect_y1) < th: return "nw"
        if abs(x - self.rect_x2) < th and abs(y - self.rect_y1) < th: return "ne"
        if abs(x - self.rect_x1) < th and abs(y - self.rect_y2) < th: return "sw"
        if abs(x - self.rect_x2) < th and abs(y - self.rect_y2) < th: return "se"
        if self.rect_x1 < x < self.rect_x2 and self.rect_y1 < y < self.rect_y2: return "move"
        return None

    def on_press(self, event):
        self.drag_mode = self.get_interaction_mode(event.x, event.y)
        self.last_mouse_x = event.x
        self.last_mouse_y = event.y

    def on_drag(self, event):
        if not self.drag_mode: return
        dx = event.x - self.last_mouse_x
        dy = event.y - self.last_mouse_y
        min_x = self.offset_x
        max_x = self.offset_x + self.disp_w
        min_y = self.offset_y
        max_y = self.offset_y + self.disp_h
        
        if self.drag_mode == "move":
            w = self.rect_x2 - self.rect_x1
            h = self.rect_y2 - self.rect_y1
            nx1 = self.rect_x1 + dx
            ny1 = self.rect_y1 + dy
            nx2 = nx1 + w
            ny2 = ny1 + h
            if nx1 < min_x: nx1 = min_x; nx2 = min_x + w
            if nx2 > max_x: nx2 = max_x; nx1 = max_x - w
            if ny1 < min_y: ny1 = min_y; ny2 = min_y + h
            if ny2 > max_y: ny2 = max_y; ny1 = max_y - h
            self.rect_x1, self.rect_y1, self.rect_x2, self.rect_y2 = nx1, ny1, nx2, ny2
        else:
            if "w" in self.drag_mode: self.rect_x1 = min(max(self.rect_x1 + dx, min_x), self.rect_x2 - 10)
            if "e" in self.drag_mode: self.rect_x2 = max(min(self.rect_x2 + dx, max_x), self.rect_x1 + 10)
            if "n" in self.drag_mode: self.rect_y1 = min(max(self.rect_y1 + dy, min_y), self.rect_y2 - 10)
            if "s" in self.drag_mode: self.rect_y2 = max(min(self.rect_y2 + dy, max_y), self.rect_y1 + 10)

        self.last_mouse_x = event.x
        self.last_mouse_y = event.y
        self.draw_selection()

    def on_hover(self, event):
        mode = self.get_interaction_mode(event.x, event.y)
        if mode == "move": self.canvas.config(cursor="fleur")
        elif mode in ["nw", "se"]: self.canvas.config(cursor="sizing_nwse")
        elif mode in ["ne", "sw"]: self.canvas.config(cursor="sizing_nesw")
        else: self.canvas.config(cursor="arrow")

    def finish(self):
        real_x = int((self.rect_x1 - self.offset_x) / self.scale)
        real_y = int((self.rect_y1 - self.offset_y) / self.scale)
        real_w = int((self.rect_x2 - self.rect_x1) / self.scale)
        real_h = int((self.rect_y2 - self.rect_y1) / self.scale)
        self.callback((real_w, real_h, real_x, real_y))
        self.destroy()

