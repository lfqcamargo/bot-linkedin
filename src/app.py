import customtkinter as ctk
from src.gui.view.home_view import HomeView

def run_app():
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.geometry("800x600")
    app.title("Minha Aplicação")

    home = HomeView(master=app)
    home.pack(fill="both", expand=True)

    app.mainloop()
