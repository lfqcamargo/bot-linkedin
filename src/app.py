import customtkinter as ctk
from src.gui.view.home_view import HomeView


def run_app() -> None:
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("Bot Canditar-se a Empregos")

    app.after(0, lambda: app.state("zoomed"))
    home = HomeView(master=app)
    home.pack(fill="both", expand=True)

    app.mainloop()
