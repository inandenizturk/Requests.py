import tkinter as tk
from tkinter import ttk, messagebox
import requests

class HackerNewsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hacker News - Top Stories")
        self.root.geometry("600x450")

        # Üst Panel / Buton
        self.top_frame = ttk.Frame(self.root, padding=10)
        self.top_frame.pack(fill=tk.X)

        self.fetch_btn = ttk.Button(self.top_frame, text="Haberleri Getir (Top 20)", command=self.fetch_top_stories)
        self.fetch_btn.pack(side=tk.LEFT)

        self.status_label = ttk.Label(self.top_frame, text="Durum: Hazır")
        self.status_label.pack(side=tk.RIGHT)

        # Liste Alanı (Treeview)
        self.tree_frame = ttk.Frame(self.root, padding=10)
        self.tree_frame.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(self.tree_frame, columns=("Score", "Title"), show="headings")
        self.tree.heading("Score", text="Puan")
        self.tree.heading("Title", text="Başlık")
        self.tree.column("Score", width=70, anchor=tk.CENTER)
        self.tree.column("Title", width=480, anchor=tk.W)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self.tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def fetch_top_stories(self):
        self.status_label.config(text="Veriler çekiliyor...")
        self.root.update_idletasks()

        # Mevcut listeyi temizle
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            # 1. En popüler haber ID'lerini çek (API key gerektirmez)
            top_ids_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
            response = requests.get(top_ids_url, timeout=5)
            response.raise_for_status()
            story_ids = response.json()[:20]  # İlk 20 tanesini al

            # 2. Her bir haberin detayını çekip tabloya ekle
            for s_id in story_ids:
                item_url = f"https://hacker-news.firebaseio.com/v0/item/{s_id}.json"
                item_res = requests.get(item_url, timeout=5)
                if item_res.status_code == 200:
                    data = item_res.json()
                    title = data.get("title", "Başlık Yok")
                    score = data.get("score", 0)
                    self.tree.insert("", tk.END, values=(score, title))

            self.status_label.config(text="Tamamlandı.")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Hata", f"Veri çekilemedi:\n{e}")
            self.status_label.config(text="Hata oluştu.")

if __name__ == "__main__":
    root = tk.Tk()
    app = HackerNewsApp(root)
    root.mainloop()
