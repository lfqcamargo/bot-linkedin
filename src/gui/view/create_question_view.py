import customtkinter as ctk
from tkinter import messagebox
from src.controllers.questions_controller import QuestionsController
from src.models.postgres.entities.question import QuestionTypes


class CreateQuestionView(ctk.CTkToplevel):
    def __init__(self, parent, user_id: int, callback_refresh=None) -> None:
        super().__init__(parent)
        self.__controller = QuestionsController()
        self.user_id = user_id
        self.callback_refresh = callback_refresh

        self.title("✨ Criar Nova Pergunta")
        self.geometry("600x500")
        self.resizable(False, False)
        self.grab_set()
        self.configure(fg_color=("#1a1a1a", "#1a1a1a"))

        # Frame principal com gradiente visual
        main_frame = ctk.CTkFrame(
            self,
            fg_color=("#ffffff", "#2d2d2d"),
            corner_radius=20,
            border_width=2,
            border_color=("#e0e0e0", "#404040"),
        )
        main_frame.pack(padx=25, pady=25, fill="both", expand=True)

        # Header com ícone e título
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=25, pady=(25, 20))

        # Ícone e título
        title_label = ctk.CTkLabel(
            header_frame,
            text="✨ Criar Nova Pergunta",
            font=("Segoe UI", 22, "bold"),
            text_color=("#2c3e50", "#ecf0f1"),
        )
        title_label.pack()

        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Preencha os campos abaixo para criar sua pergunta",
            font=("Segoe UI", 12),
            text_color=("#7f8c8d", "#bdc3c7"),
        )
        subtitle_label.pack(pady=(5, 0))

        # Separador visual
        separator = ctk.CTkFrame(
            main_frame, height=2, fg_color=("#3498db", "#3498db"), corner_radius=1
        )
        separator.pack(fill="x", padx=25, pady=(0, 25))

        # Container para os campos
        fields_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        fields_frame.pack(fill="both", expand=True, padx=25, pady=(0, 25))

        # Campo Pergunta
        question_container = ctk.CTkFrame(
            fields_frame,
            fg_color=("#f8f9fa", "#3a3a3a"),
            corner_radius=12,
            border_width=1,
            border_color=("#e9ecef", "#555555"),
        )
        question_container.pack(fill="x", pady=(0, 20))

        question_label = ctk.CTkLabel(
            question_container,
            text="📝 Pergunta",
            font=("Segoe UI", 14, "bold"),
            text_color=("#2c3e50", "#ecf0f1"),
        )
        question_label.pack(anchor="w", padx=20, pady=(15, 8))

        self.question_entry = ctk.CTkEntry(
            question_container,
            placeholder_text="Digite sua pergunta aqui...",
            width=500,
            height=45,
            font=("Segoe UI", 13),
            corner_radius=10,
        )
        self.question_entry.pack(padx=20, pady=(0, 15))

        # Campo Tipo de Pergunta
        type_container = ctk.CTkFrame(
            fields_frame,
            fg_color=("#f8f9fa", "#3a3a3a"),
            corner_radius=12,
            border_width=1,
            border_color=("#e9ecef", "#555555"),
        )
        type_container.pack(fill="x", pady=(0, 20))

        type_label = ctk.CTkLabel(
            type_container,
            text="🎯 Tipo de Pergunta",
            font=("Segoe UI", 14, "bold"),
            text_color=("#2c3e50", "#ecf0f1"),
        )
        type_label.pack(anchor="w", padx=20, pady=(15, 8))

        self.type_option = ctk.CTkOptionMenu(
            type_container,
            values=[qt.value for qt in QuestionTypes],
            width=500,
            height=45,
            font=("Segoe UI", 13),
            corner_radius=10,
            button_color=("#3498db", "#3498db"),
            button_hover_color=("#2980b9", "#2980b9"),
        )
        self.type_option.set(QuestionTypes.TEXT.value)
        self.type_option.pack(padx=20, pady=(0, 15))

        # Campo Resposta (opcional)
        response_container = ctk.CTkFrame(
            fields_frame,
            fg_color=("#f8f9fa", "#3a3a3a"),
            corner_radius=12,
            border_width=1,
            border_color=("#e9ecef", "#555555"),
        )
        response_container.pack(fill="x", pady=(0, 25))

        response_label = ctk.CTkLabel(
            response_container,
            text="💡 Resposta (opcional)",
            font=("Segoe UI", 14, "bold"),
            text_color=("#2c3e50", "#ecf0f1"),
        )
        response_label.pack(anchor="w", padx=20, pady=(15, 8))

        self.response_entry = ctk.CTkEntry(
            response_container,
            placeholder_text="Digite a resposta esperada (opcional)...",
            width=500,
            height=45,
            font=("Segoe UI", 13),
            corner_radius=10,
        )
        self.response_entry.pack(padx=20, pady=(0, 15))

        # Botões com design melhorado
        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=25, pady=(0, 25))

        # Botão Cancelar
        cancel_button = ctk.CTkButton(
            buttons_frame,
            text="❌ Cancelar",
            fg_color=("#e74c3c", "#e74c3c"),
            hover_color=("#c0392b", "#c0392b"),
            font=("Segoe UI", 14, "bold"),
            width=180,
            height=50,
            corner_radius=12,
            command=self._cancelar,
        )
        cancel_button.pack(side="left", padx=(0, 15))

        # Botão Salvar
        save_button = ctk.CTkButton(
            buttons_frame,
            text="💾 Salvar Pergunta",
            fg_color=("#27ae60", "#27ae60"),
            hover_color=("#229954", "#229954"),
            font=("Segoe UI", 14, "bold"),
            width=180,
            height=50,
            corner_radius=12,
            command=self._salvar,
        )
        save_button.pack(side="right", padx=(15, 0))

        # Centralizar os botões
        buttons_frame.pack_configure(anchor="center")

        # Focar no primeiro campo
        self.question_entry.focus()

    def _salvar(self):
        question_text = self.question_entry.get().strip()
        question_type = self.type_option.get()
        response_text = self.response_entry.get().strip()

        # Validação
        if not question_text:
            messagebox.showerror(
                "❌ Erro",
                "A pergunta é obrigatória!\n\nPor favor, preencha o campo 'Pergunta' antes de salvar.",
                parent=self,
            )
            self.question_entry.focus()
            return

        try:
            self.__controller.create_question(
                user_id=self.user_id,
                question=question_text,
                question_type=question_type,
                response=response_text if response_text else None,
            )

            messagebox.showinfo(
                "✅ Sucesso",
                "Pergunta criada com sucesso!\n\nA nova pergunta foi adicionada à sua lista.",
                parent=self,
            )

            # Chama o callback para atualizar a lista de perguntas
            if self.callback_refresh:
                self.callback_refresh()

            self.destroy()

        except Exception as e:
            messagebox.showerror(
                "❌ Erro", f"Erro ao criar pergunta:\n\n{str(e)}", parent=self
            )

    def _cancelar(self):
        # Confirmação antes de cancelar se há dados preenchidos
        question_text = self.question_entry.get().strip()
        response_text = self.response_entry.get().strip()

        if question_text or response_text:
            if not messagebox.askyesno(
                "⚠️ Confirmar Cancelamento",
                "Você tem dados não salvos.\n\nTem certeza que deseja cancelar?",
                parent=self,
            ):
                return

        self.destroy()
