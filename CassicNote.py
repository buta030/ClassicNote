import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinter.scrolledtext import ScrolledText

class NotepadClone:
    def __init__(self, root):
        self.root = root
        self.root.title("無題 - メモ帳")
        self.root.geometry("800x600")

        self.filename = None
        self.word_wrap = tk.BooleanVar(value=False)
        self.status_visible = tk.BooleanVar(value=False)

        self.text = ScrolledText(root, undo=True, wrap='none', font=("Consolas", 11))
        self.text.pack(fill=tk.BOTH, expand=True)
        self.text.bind("<<Modified>>", self.on_modified)

        self.create_menus()
        self.create_status_bar()
        self.update_title()

    def create_menus(self):
        menubar = tk.Menu(self.root)

        # ファイルメニュー
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="新規", command=self.new_file, accelerator="Ctrl+N")
        filemenu.add_command(label="開く...", command=self.open_file, accelerator="Ctrl+O")
        filemenu.add_command(label="上書き保存", command=self.save_file, accelerator="Ctrl+S")
        filemenu.add_command(label="名前を付けて保存...", command=self.save_file_as)
        filemenu.add_separator()
        filemenu.add_command(label="終了", command=self.root.quit)
        menubar.add_cascade(label="ファイル", menu=filemenu)

        # 編集メニュー
        editmenu = tk.Menu(menubar, tearoff=0)
        editmenu.add_command(label="元に戻す", command=self.text.edit_undo, accelerator="Ctrl+Z")
        editmenu.add_separator()
        editmenu.add_command(label="切り取り", command=lambda: self.root.focus_get().event_generate("<<Cut>>"), accelerator="Ctrl+X")
        editmenu.add_command(label="コピー", command=lambda: self.root.focus_get().event_generate("<<Copy>>"), accelerator="Ctrl+C")
        editmenu.add_command(label="貼り付け", command=lambda: self.root.focus_get().event_generate("<<Paste>>"), accelerator="Ctrl+V")
        editmenu.add_command(label="削除", command=self.delete_text)
        editmenu.add_separator()
        editmenu.add_command(label="すべて選択", command=lambda: self.text.tag_add("sel", "1.0", "end"), accelerator="Ctrl+A")
        menubar.add_cascade(label="編集", menu=editmenu)

        # 書式メニュー
        formatmenu = tk.Menu(menubar, tearoff=0)
        formatmenu.add_checkbutton(label="自動改行", variable=self.word_wrap, command=self.toggle_wrap)
        menubar.add_cascade(label="書式", menu=formatmenu)

        # 表示メニュー
        viewmenu = tk.Menu(menubar, tearoff=0)
        viewmenu.add_checkbutton(label="ステータス バー", variable=self.status_visible, command=self.toggle_status)
        menubar.add_cascade(label="表示", menu=viewmenu)

        # ヘルプメニュー
        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="バージョン情報", command=self.show_about)
        menubar.add_cascade(label="ヘルプ", menu=helpmenu)

        self.root.config(menu=menubar)

        # ショートカット
        self.root.bind('<Control-n>', lambda event: self.new_file())
        self.root.bind('<Control-o>', lambda event: self.open_file())
        self.root.bind('<Control-s>', lambda event: self.save_file())
        self.root.bind('<Control-a>', lambda event: self.text.tag_add("sel", "1.0", "end"))

    def create_status_bar(self):
        self.status = tk.Label(self.root, text="行 1、列 1", anchor='w')
        self.status.pack(side=tk.BOTTOM, fill=tk.X)
        self.text.bind('<KeyRelease>', self.update_status)
        self.update_status()
        self.status.pack_forget()  # 初期状態では非表示

    def toggle_status(self):
        if self.status_visible.get():
            self.status.pack(side=tk.BOTTOM, fill=tk.X)
        else:
            self.status.pack_forget()

    def update_status(self, event=None):
        try:
            row, col = self.text.index(tk.INSERT).split(".")
            self.status.config(text=f"行 {int(row)}、列 {int(col)+1}")
        except:
            pass

    def toggle_wrap(self):
        self.text.config(wrap='word' if self.word_wrap.get() else 'none')

    def delete_text(self):
        try:
            self.text.delete("sel.first", "sel.last")
        except:
            pass

    def new_file(self):
        self.filename = None
        self.text.delete(1.0, tk.END)
        self.update_title()

    def open_file(self):
        path = filedialog.askopenfilename(filetypes=[("テキストファイル", "*.txt"), ("すべてのファイル", "*.*")])
        if path:
            with open(path, "r", encoding="utf-8") as file:
                content = file.read()
                self.text.delete(1.0, tk.END)
                self.text.insert(tk.END, content)
                self.filename = path
                self.update_title()

    def save_file(self):
        if self.filename:
            with open(self.filename, "w", encoding="utf-8") as file:
                file.write(self.text.get(1.0, tk.END))
        else:
            self.save_file_as()

    def save_file_as(self):
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("テキストファイル", "*.txt"), ("すべてのファイル", "*.*")])
        if path:
            self.filename = path
            self.save_file()
            self.update_title()

    def update_title(self):
        name = self.filename if self.filename else "無題"
        self.root.title(f"{name} - CassicNote")

    def on_modified(self, event=None):
        self.text.edit_modified(False)
        self.update_status()

    def show_about(self):
        messagebox.showinfo("バージョン情報", "CassicNote v1.0\nPython + Tkinter")

if __name__ == "__main__":
    root = tk.Tk()
    app = NotepadClone(root)
    root.mainloop()
