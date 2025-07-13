from tkinter import messagebox, filedialog
from typing import Optional
import customtkinter as ctk
from src.controllers.errors.validate_exception import ValidationException
from src.controllers.users_controller import UsersController
from src.models.postgres.entities.user import User


class UserView(ctk.CTkToplevel):
    def __init__(self, parent, user: Optional[User] = None) -> None:
        super().__init__(parent)
        self.__users_controller = UsersController()
        self.title("Cadastro de Usuário" if user is None else "Editar Usuário")
        self.geometry("480x700")
        self.resizable(False, False)
        self.grab_set()
        self.user = user

        self.configure(corner_radius=20, fg_color=("#23272e", "#23272e"))

        self.frame = ctk.CTkFrame(
            self, corner_radius=16, fg_color=("#f5f6fa", "#23272e")
        )
        self.frame.pack(padx=24, pady=24, fill="both", expand=True)

        # Title
        ctk.CTkLabel(
            self.frame,
            text="Cadastro de Usuário" if user is None else "Editar Usuário",
            font=("Arial", 22, "bold"),
            text_color=("#222", "#fff"),
        ).pack(pady=(20, 10))

        self.entry_name = self._input("Nome")
        self.entry_email = self._input("Email")
        self.entry_password = self._input("Senha", show="*")
        self.entry_confirm = self._input("Confirmar Senha", show="*")

        self.entry_birthday = self._input("Data de Nascimento (DD/MM/AAAA)")
        self.entry_birthday.bind("<KeyRelease>", self._formatar_data)

        self.entry_phone = self._input("Telefone (apenas números)")

        # Currículo
        self.curriculum_label = ctk.CTkLabel(
            self.frame,
            text="Nenhum currículo selecionado",
            font=("Arial", 11),
            text_color="#888",
        )
        self.curriculum_label.pack(pady=(12, 4))

        ctk.CTkButton(
            self.frame,
            text="Selecionar Currículo (PDF)",
            command=self.select_curriculum,
            width=220,
            height=36,
            font=("Arial", 12, "bold"),
            fg_color="#36b9cc",
            hover_color="#258fa3",
            corner_radius=10,
        ).pack(pady=(0, 12))

        self.curriculum_path = None
        self.curriculum_bytes: Optional[bytes] = None

        # Submit Button
        ctk.CTkButton(
            self.frame,
            text="✅ Cadastrar" if user is None else "💾 Salvar",
            command=self.__save,
            width=220,
            height=44,
            font=("Arial", 15, "bold"),
            fg_color="#4e73df",
            hover_color="#2e59d9",
            corner_radius=12,
        ).pack(pady=(24, 12))

        if user is not None:
            self.preencher_campos(user)

    def _input(self, placeholder: str, show: Optional[str] = None):
        entry = ctk.CTkEntry(
            self.frame,
            placeholder_text=placeholder,
            show=show,
            width=320,
            height=40,
            font=("Arial", 13),
        )
        entry.pack(pady=8)
        return entry

    def preencher_campos(self, user: User):
        self.entry_name.insert(0, user.name)
        self.entry_email.insert(0, user.email)

        data_iso = user.birthday_date
        if data_iso:
            try:
                ano, mes, dia = data_iso.split("-")
                data_br = f"{dia}/{mes}/{ano}"
            except Exception:
                data_br = data_iso
            self.entry_birthday.insert(0, data_br)

        self.entry_phone.insert(0, user.phone)
        self.curriculum_label.configure(
            text="Currículo já cadastrado", text_color="#36b9cc"
        )
        self.curriculum_bytes = user.curriculum

    def select_curriculum(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            self.curriculum_path = file_path
            self.curriculum_label.configure(
                text=f"Currículo: {file_path.split('/')[-1]}", text_color="#36b9cc"
            )
            with open(file_path, "rb") as f:
                self.curriculum_bytes = f.read()
            messagebox.showinfo(
                "Arquivo selecionado",
                f"Currículo selecionado: {file_path}",
                parent=self,
            )

    def _formatar_data(self, event=None) -> None:
        valor = self.entry_birthday.get().replace("/", "")
        novo = ""
        for i, c in enumerate(valor):
            if i == 2 or i == 4:
                novo += "/"
            novo += c
            if i >= 7:
                break
        self.entry_birthday.delete(0, "end")
        self.entry_birthday.insert(0, novo)

    def __save(self) -> None:
        try:
            data_br = self.entry_birthday.get().strip()
            data_iso = ""
            if data_br:
                partes = data_br.split("/")
                if len(partes) == 3:
                    data_iso = f"{partes[2]}-{partes[1]}-{partes[0]}"
                else:
                    data_iso = data_br

            props = {
                "name": self.entry_name.get().strip(),
                "email": self.entry_email.get().strip().lower(),
                "password": self.entry_password.get(),
                "birthday_date": data_iso,
                "phone": self.entry_phone.get().strip(),
                "curriculum": self.curriculum_bytes or b"",
            }

            if self.user is None:
                self.__users_controller.create_user(props)
                messagebox.showinfo(
                    "Sucesso", "Usuário cadastrado com sucesso!", parent=self
                )
            else:
                props["id"] = self.user.id
                self.__users_controller.update_user(props)
                messagebox.showinfo(
                    "Sucesso", "Usuário atualizado com sucesso!", parent=self
                )

            self.destroy()

        except ValidationException as e:
            messagebox.showerror("Erro de Validação", str(e), parent=self)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado: {e}", parent=self)
