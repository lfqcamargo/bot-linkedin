import customtkinter as ctk
from tkinter import messagebox
from src.composer.fetch_all_users_composer import fetch_all_users_composer
from src.composer.delete_user_composer import delete_user_composer
from src.gui.view.create_user_view import CreateUserView

# Definindo tema global e cor de destaque
ctk.set_appearance_mode("dark")  # ou "light" se preferir
ctk.set_default_color_theme("blue")

class HomeView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(corner_radius=20, fg_color=("#f5f6fa", "#23272e"))
        self.pack(fill="both", expand=True, padx=30, pady=30)

        self.label_title = ctk.CTkLabel(
            self,
            text="Bem-vindo!",
            font=("Arial", 28, "bold"),
            text_color=("#222", "#fff")
        )
        self.label_title.pack(pady=(10, 25))

        self.frame_top = ctk.CTkFrame(self, corner_radius=15, fg_color=("#e3e6f0", "#2c2f36"))
        self.frame_top.pack(fill="x", padx=10, pady=5)

        self.btn_create_user = ctk.CTkButton(
            self.frame_top,
            text="➕ Cadastrar Usuário",
            command=self.create_user,
            width=180,
            height=38,
            font=("Arial", 14, "bold"),
            fg_color="#4e73df",
            hover_color="#2e59d9",
            corner_radius=10
        )
        self.btn_create_user.pack(side="left", padx=8, pady=8)

        self.btn_run_bot = ctk.CTkButton(
            self.frame_top,
            text="🤖 Rodar Bot",
            command=self.run_bot,
            width=140,
            height=38,
            font=("Arial", 14, "bold"),
            fg_color="#1cc88a",
            hover_color="#17a673",
            corner_radius=10
        )
        self.btn_run_bot.pack(side="left", padx=8, pady=8)

        # Separador visual
        ctk.CTkLabel(self, text="", height=2, fg_color=("#d1d3e2", "#393e46")).pack(fill="x", padx=10, pady=(18, 0))

        self.label_users = ctk.CTkLabel(
            self,
            text="Usuários cadastrados:",
            font=("Arial", 18, "bold"),
            text_color=("#222", "#fff")
        )
        self.label_users.pack(pady=(18, 8))

        self.frame_lista = ctk.CTkFrame(self, corner_radius=15, fg_color=("#fff", "#23272e"))
        self.frame_lista.pack(padx=10, pady=5, fill="both", expand=True)

        self.__update_list_users()

    def __update_list_users(self):
        for widget in self.frame_lista.winfo_children():
            widget.destroy()

        users = fetch_all_users_composer().handle()

        if users:
            header = ctk.CTkLabel(
                self.frame_lista,
                text="Nome | Email | Telefone",
                font=("Arial", 13, "bold"),
                text_color=("#4e73df", "#4e73df")
            )
            header.grid(row=0, column=0, columnspan=3, sticky="w", padx=10, pady=6)

            for idx, user in enumerate(users, start=1):
                name = user.get("name", "")
                email = user.get("email", "")
                phone = user.get("phone", "")

                bg = "#f8f9fc" if idx % 2 == 0 else "#e3e6f0"
                bg_dark = "#23272e" if idx % 2 == 0 else "#2c2f36"

                info = f"{name} | {email} | {phone}"
                label = ctk.CTkLabel(
                    self.frame_lista,
                    text=info,
                    font=("Consolas", 12),
                    anchor="w",
                    fg_color=(bg, bg_dark),
                    corner_radius=8,
                    width=320
                )
                label.grid(row=idx, column=0, sticky="w", padx=10, pady=3)

                btn_edit = ctk.CTkButton(
                    self.frame_lista,
                    text="✏️ Editar",
                    width=80,
                    height=30,
                    font=("Arial", 12, "bold"),
                    fg_color="#36b9cc",
                    hover_color="#258fa3",
                    corner_radius=8,
                    command=lambda u=user: self.edit_user(u)
                )
                btn_edit.grid(row=idx, column=1, padx=4, pady=3)

                btn_del = ctk.CTkButton(
                    self.frame_lista,
                    text="🗑️ Remover",
                    width=100,
                    height=30,
                    font=("Arial", 12, "bold"),
                    fg_color="#e74a3b",
                    hover_color="#be2617",
                    corner_radius=8,
                    command=lambda u=user: self.delete_user(u)
                )
                btn_del.grid(row=idx, column=2, padx=4, pady=3)
        else:
            label = ctk.CTkLabel(
                self.frame_lista,
                text="Nenhum usuário cadastrado.",
                font=("Consolas", 13),
                text_color="#888"
            )
            label.pack(pady=18)

    def create_user(self):
        screen = CreateUserView(self)
        self.wait_window(screen)
        self.__update_list_users()

    def edit_user(self, user: dict):
        screen = CreateUserView(self, user=user)
        self.wait_window(screen)
        self.__update_list_users()

    def delete_user(self, user: dict):
        if messagebox.askyesno("Remover Usuário", f"Tem certeza que deseja remover o usuário '{user.get('name', '')}'?"):
            try:
                delete_user_composer().handle({"id": user["id"]})
                messagebox.showinfo("Removido", f"Usuário '{user.get('name', '')}' removido com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro inesperado: {e}", parent=self)

            self.__update_list_users()

    def run_bot(self):
        messagebox.showinfo("Bot", "Bot será implementado futuramente.")
