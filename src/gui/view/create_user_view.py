import customtkinter as ctk
from tkinter import messagebox, filedialog
from typing import Optional
from src.composer.create_user_composer import create_user_composer
from src.composer.update_user_composer import update_user_composer
from src.controllers.errors.validate_exception import ValidationException

class CreateUserView(ctk.CTkToplevel):
    def __init__(self, parent, user: Optional[dict] = None):
        super().__init__(parent)
        self.title("Cadastro de Usuário" if user is None else "Editar Usuário")
        self.geometry("440x620")
        self.resizable(False, False)
        self.grab_set()
        self.user = user

        self.configure(bg="#23272e")  # fundo escuro

        self.frame = ctk.CTkFrame(self, corner_radius=18, fg_color=("#f5f6fa", "#23272e"))
        self.frame.pack(padx=30, pady=30, fill="both", expand=True)

        self.label_title = ctk.CTkLabel(
            self.frame,
            text="Cadastro de Usuário" if user is None else "Editar Usuário",
            font=("Arial", 22, "bold"),
            text_color=("#222", "#fff")
        )
        self.label_title.pack(pady=(18, 12))

        self.entry_name = ctk.CTkEntry(self.frame, placeholder_text="Nome", width=320, height=36, font=("Arial", 13))
        self.entry_name.pack(pady=10)

        self.entry_email = ctk.CTkEntry(self.frame, placeholder_text="Email", width=320, height=36, font=("Arial", 13))
        self.entry_email.pack(pady=10)

        self.entry_password = ctk.CTkEntry(self.frame, placeholder_text="Senha", show="*", width=320, height=36, font=("Arial", 13))
        self.entry_password.pack(pady=10)

        self.entry_confirm = ctk.CTkEntry(self.frame, placeholder_text="Confirmar Senha", show="*", width=320, height=36, font=("Arial", 13))
        self.entry_confirm.pack(pady=10)

        self.entry_birthday = ctk.CTkEntry(self.frame, placeholder_text="Data de Nascimento (DD/MM/AAAA)", width=320, height=36, font=("Arial", 13))
        self.entry_birthday.pack(pady=10)
        self.entry_birthday.bind('<KeyRelease>', self._formatar_data)

        self.curriculum_label = ctk.CTkLabel(self.frame, text="Nenhum currículo selecionado", font=("Arial", 11), text_color="#888")
        self.curriculum_label.pack(pady=(10, 0))
        self.btn_curriculum = ctk.CTkButton(
            self.frame,
            text="📄 Selecionar Currículo (PDF)",
            command=self.select_curriculum,
            width=220,
            height=34,
            font=("Arial", 12, "bold"),
            fg_color="#36b9cc",
            hover_color="#258fa3",
            corner_radius=10
        )
        self.btn_curriculum.pack(pady=6)
        self.curriculum_path = None
        self.curriculum_bytes: Optional[bytes] = None

        self.entry_phone = ctk.CTkEntry(self.frame, placeholder_text="Telefone (apenas números)", width=320, height=36, font=("Arial", 13))
        self.entry_phone.pack(pady=10)

        self.btn_register = ctk.CTkButton(
            self.frame,
            text=("✅ Cadastrar" if user is None else "💾 Salvar"),
            command=self.__save,
            width=220,
            height=40,
            font=("Arial", 15, "bold"),
            fg_color="#4e73df",
            hover_color="#2e59d9",
            corner_radius=12
        )
        self.btn_register.pack(pady=(24, 12))

        if user is not None:
            self.preencher_campos(user)

    def preencher_campos(self, user: dict):
        self.entry_name.insert(0, user.get("name", ""))
        self.entry_email.insert(0, user.get("email", ""))
        self.entry_password.insert(0, user.get("password", ""))
        self.entry_confirm.insert(0, user.get("password", ""))
        # Converter data do formato ISO para pt-BR
        data_iso = user.get("birthday_date", "")
        if data_iso:
            try:
                ano, mes, dia = data_iso.split("-")
                data_br = f"{dia}/{mes}/{ano}"
            except Exception:
                data_br = data_iso
            self.entry_birthday.insert(0, data_br)
        self.curriculum_label.configure(text="Currículo já cadastrado", text_color="#36b9cc")
        self.curriculum_bytes = user.get("curriculum", None)
        self.entry_phone.insert(0, user.get("phone", ""))

    def select_curriculum(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            self.curriculum_path = file_path
            self.curriculum_label.configure(text=f"Currículo: {file_path.split('/')[-1]}", text_color="#36b9cc")
            with open(file_path, "rb") as f:
                self.curriculum_bytes = f.read()
            messagebox.showinfo("Arquivo selecionado", f"Currículo selecionado: {file_path}", parent=self)

    def _formatar_data(self, event=None):
        valor = self.entry_birthday.get().replace("/", "")
        novo = ""
        for i, c in enumerate(valor):
            if i == 2 or i == 4:
                novo += "/"
            novo += c
            if i >= 7:
                break
        self.entry_birthday.delete(0, 'end')
        self.entry_birthday.insert(0, novo)

    def __save(self):
        try:
            # Converter data para ISO (YYYY-MM-DD)
            data_br = self.entry_birthday.get().strip()
            data_iso = ""
            if data_br:
                partes = data_br.split("/")
                if len(partes) == 3:
                    data_iso = f"{partes[2]}-{partes[1]}-{partes[0]}"
                else:
                    data_iso = data_br  # fallback
            props = {
                "name": self.entry_name.get().strip(),
                "email": self.entry_email.get().strip(),
                "password": self.entry_password.get(),
                "birthday_date": data_iso,
                "phone": self.entry_phone.get().strip(),
                "curriculum": self.curriculum_bytes or b"",
            }
            if self.user is None:
                controller = create_user_composer()
                controller.handle(props)
                messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!", parent=self)
            else:
                props["id"] = self.user["id"]
                controller = update_user_composer()
                controller.handle(props)
                messagebox.showinfo("Sucesso", "Usuário atualizado com sucesso!", parent=self)
            self.destroy()
        except ValidationException as e:
            messagebox.showerror("Erro de Validação", str(e), parent=self)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado: {e}", parent=self)