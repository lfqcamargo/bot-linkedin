from tkinter import messagebox
import customtkinter as ctk
from src.controllers.users_controller import UsersController
from src.controllers.run_linkedin_bot_controller import RunLinkedinBotController
from src.gui.view.user_view import UserView
from src.gui.view.question_view import QuestionView


class HomeView(ctk.CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master)

        self.__users_controller = UsersController()
        self.__bot_controller = RunLinkedinBotController()

        self.configure(corner_radius=20, fg_color=("#23272e", "#23272e"))
        self.pack(fill="both", expand=True, padx=0, pady=0)

        self.__create_header()
        self.__card_list_users()
        self.__create_footer()

    def delete_user(self, user: dict) -> None:
        if messagebox.askyesno(
            "Remover Usuário",
            f"Tem certeza que deseja remover o usuário '{user.name}'?",
        ):
            try:
                self.__users_controller.delete({"id": user.id})
                messagebox.showinfo(
                    "Removido",
                    f"Usuário '{user.name}' removido com sucesso!",
                )
            except Exception as e:
                messagebox.showerror("Erro", f"Erro inesperado: {e}", parent=self)
            self.__update_list_users()

    def questions(self, user: dict) -> None:
        pass

    def run_bot(self):
        users = self.__users_controller.fetch_all_users()
        if not users:
            messagebox.showinfo("Aviso", "Nenhum usuário cadastrado.")
            return

        modal = ctk.CTkToplevel(self)
        modal.title("Selecionar Usuário para Rodar o Bot")
        modal.geometry("400x300")
        modal.transient(self)
        modal.grab_set()

        label = ctk.CTkLabel(
            modal, text="Selecione um usuário:", font=("Arial", 16, "bold")
        )
        label.pack(pady=10)

        # Acessa propriedades com ponto agora
        user_names = [f"{u.name} ({u.email})" for u in users]
        user_map = {f"{u.name} ({u.email})": u for u in users}

        selected_user = ctk.StringVar(value=user_names[0])
        option_menu = ctk.CTkOptionMenu(
            modal, values=user_names, variable=selected_user, width=300
        )
        option_menu.pack(pady=15)

        def confirmar():
            user_selected = user_map[selected_user.get()]
            try:
                self.__bot_controller.handle({"id": user_selected.id})
                messagebox.showinfo(
                    "Bot Rodando",
                    f"O bot foi iniciado para o usuário {user_selected.name}!",
                )
            except Exception as e:
                messagebox.showerror("Erro", f"Ocorreu um erro ao rodar o bot:\n{e}")
            modal.destroy()

        btn_confirmar = ctk.CTkButton(
            modal,
            text="✅ Rodar Bot",
            command=confirmar,
            fg_color="#1cc88a",
            hover_color="#17a673",
        )
        btn_confirmar.pack(pady=15)

    def __create_header(self) -> None:
        self.header = ctk.CTkFrame(self, fg_color="#23272e", corner_radius=0)
        self.header.pack(fill="x", pady=(0, 0))
        ctk.CTkLabel(
            self.header,
            text="🤖 Bot de Empregos",
            font=("Arial", 32, "bold"),
            text_color="#4e73df",
        ).pack(side="left", padx=(40, 18), pady=(18, 10))
        ctk.CTkLabel(
            self.header,
            text="Bem-vindo ao painel de gestão!",
            font=("Arial", 18),
            text_color="#fff",
        ).pack(side="left", pady=(18, 10))

        self.frame_top = ctk.CTkFrame(
            self, corner_radius=15, fg_color=("#2c2f36", "#2c2f36")
        )
        self.frame_top.pack(fill="x", padx=40, pady=(10, 18))
        self.btn_create_user = ctk.CTkButton(
            self.frame_top,
            text="➕ Cadastrar Usuário",
            command=self.__create_user,
            width=200,
            height=44,
            font=("Arial", 15, "bold"),
            fg_color="#4e73df",
            hover_color="#2e59d9",
            corner_radius=12,
        )
        self.btn_create_user.pack(side="left", padx=12, pady=12)
        self.btn_run_bot = ctk.CTkButton(
            self.frame_top,
            text="🤖 Rodar Bot",
            command=self.run_bot,
            width=160,
            height=44,
            font=("Arial", 15, "bold"),
            fg_color="#1cc88a",
            hover_color="#17a673",
            corner_radius=12,
        )
        self.btn_run_bot.pack(side="left", padx=12, pady=12)

    def __card_list_users(self) -> None:
        self.card_list = ctk.CTkFrame(
            self, corner_radius=18, fg_color=("#fff", "#23272e")
        )
        self.card_list.pack(padx=40, pady=(24, 10), fill="both", expand=True)

        self.label_users = ctk.CTkLabel(
            self.card_list,
            text="Usuários Cadastrados",
            font=("Arial", 24, "bold"),
            text_color=("#222", "#fff"),
        )
        self.label_users.pack(pady=(18, 8))

        self.users_list_frame = ctk.CTkFrame(
            self.card_list, corner_radius=15, fg_color=("#f5f6fa", "#23272e")
        )
        self.users_list_frame.pack(padx=10, pady=5, fill="both", expand=True)

        self.__update_list_users()

    def __update_list_users(self) -> None:
        # Limpa a lista atual
        for widget in self.users_list_frame.winfo_children():
            widget.destroy()

        # Configura colunas do container principal
        self.users_list_frame.grid_columnconfigure(0, weight=2)
        self.users_list_frame.grid_columnconfigure(1, weight=3)
        self.users_list_frame.grid_columnconfigure(2, weight=2)
        self.users_list_frame.grid_columnconfigure(3, weight=1)

        # Cabeçalho
        ctk.CTkLabel(
            self.users_list_frame,
            text="Nome",
            font=("Arial", 14, "bold"),
            text_color="#4e73df",
            anchor="w",
        ).grid(row=0, column=0, padx=10, pady=6, sticky="w")

        ctk.CTkLabel(
            self.users_list_frame,
            text="Email",
            font=("Arial", 14, "bold"),
            text_color="#4e73df",
            anchor="w",
        ).grid(row=0, column=1, padx=10, pady=6, sticky="w")

        ctk.CTkLabel(
            self.users_list_frame,
            text="Telefone",
            font=("Arial", 14, "bold"),
            text_color="#4e73df",
            anchor="w",
        ).grid(row=0, column=2, padx=10, pady=6, sticky="w")

        # Cabeçalho "Ações" dentro de um frame, só texto, centralizado
        actions_header_frame = ctk.CTkFrame(
            self.users_list_frame, fg_color="transparent"
        )
        actions_header_frame.grid(
            row=0, column=3, padx=10, pady=6, sticky="e"
        )  # fixa à direita

        ctk.CTkLabel(
            actions_header_frame,
            text="Ações",
            font=("Arial", 14, "bold"),
            text_color="#4e73df",
            anchor="e",  # alinhamento do texto à direita
        ).pack(fill="x")

        # Lista de usuários
        users = self.__users_controller.fetch_all_users()

        for i, user in enumerate(users, start=1):
            # Nome
            ctk.CTkLabel(
                self.users_list_frame,
                text=user.name or "—",
                font=("Arial", 13),
                text_color=("#23272e", "#fff"),
                anchor="w",
            ).grid(row=i, column=0, padx=10, pady=4, sticky="w")

            # Email
            ctk.CTkLabel(
                self.users_list_frame,
                text=user.email or "—",
                font=("Arial", 13),
                text_color=("#23272e", "#fff"),
                anchor="w",
            ).grid(row=i, column=1, padx=10, pady=4, sticky="w")

            # Telefone
            ctk.CTkLabel(
                self.users_list_frame,
                text=user.phone or "—",
                font=("Arial", 13),
                text_color=("#23272e", "#fff"),
                anchor="w",
            ).grid(row=i, column=2, padx=10, pady=4, sticky="w")

            # Ações (botões)
            actions_frame = ctk.CTkFrame(self.users_list_frame, fg_color="transparent")
            actions_frame.grid(row=i, column=3, padx=10, pady=4, sticky="e")

            button_style = dict(
                width=42,
                height=38,
                font=("Arial", 15, "bold"),
                corner_radius=14,
                border_width=0,
            )

            ctk.CTkButton(
                actions_frame,
                text="✏️",
                fg_color="#4a90e2",
                hover_color="#357ABD",
                **button_style,
                command=lambda u=user: self.edit_user(u),
            ).pack(side="left", padx=8)

            ctk.CTkButton(
                actions_frame,
                text="❓",
                fg_color="#f5a623",
                hover_color="#c4871d",
                **button_style,
                command=lambda u=user: self.__open_questions(u),
            ).pack(side="left", padx=8)

            ctk.CTkButton(
                actions_frame,
                text="🗑️",
                fg_color="#e94e3d",
                hover_color="#b33021",
                **button_style,
                command=lambda u=user: self.delete_user(u),
            ).pack(side="left", padx=8)

    def __create_footer(self) -> None:
        self.footer = ctk.CTkFrame(self, fg_color="transparent")
        self.footer.pack(fill="x", side="bottom", pady=(0, 8))
        ctk.CTkLabel(
            self.footer,
            text="Desenvolvido por Lucas Fernando Quinato de Camargo • v1.0",
            font=("Arial", 11, "italic"),
            text_color="#888",
        ).pack(side="right", padx=18)

    def __create_user(self) -> None:
        screen = UserView(self)
        self.wait_window(screen)
        self.__update_list_users()

    def __open_questions(self, user) -> None:
        screen = QuestionView(self, user_id=user.id)
        self.wait_window(screen)
        self.__update_list_users()

    def edit_user(self, user: dict) -> None:
        screen = UserView(self, user=user)
        self.wait_window(screen)
        self.__update_list_users()
