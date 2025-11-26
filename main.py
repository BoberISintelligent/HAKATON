import tkinter as tk
from tkinter import messagebox
from gspread_file import upload_to_google_sheets

class CampApp:
    def __init__(self, root):
        self.root = root
        root.title("Laagrite otsing")
        root.geometry("400x200")
        root.resizable(False, False)

        self.label = tk.Label(root, text="Vajuta nuppu, et alustada otsingut ja üleslaadimist Google Sheets'i")
        self.label.pack(pady=20)

        self.search_btn = tk.Button(root, text="Alusta otsingut", command=self.run_search)
        self.search_btn.pack(pady=10)

        self.url_label = tk.Label(root, text="", fg="blue", cursor="hand2")
        self.url_label.pack(pady=10)
        self.url_label.bind("<Button-1>", lambda e: self.open_link())

        self.sheet_url = ""

    def run_search(self):
        self.label.config(text="Otsing ja tabelisse üleslaadimine käib...")
        self.root.update()

        # Käivitame otsingu ainult nupule vajutamisel
        from searchengine import searcheng
        camps = searcheng()

        # Laeme andmed Google Sheetsi
        from gspread_file import upload_to_google_sheets
        sheet_url = upload_to_google_sheets(camps)

        self.sheet_url = sheet_url
        self.url_label.config(text="Tabel on valmis! Vajuta siia, et avada")
        self.label.config(text="Otsing on lõpetatud")

    def open_link(self):
        if self.sheet_url:
            import webbrowser
            webbrowser.open(self.sheet_url)

if __name__ == "__main__":
    root = tk.Tk()
    app = CampApp(root)
    root.mainloop()
    