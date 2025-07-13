import customtkinter as ctk
from tkinter import messagebox
from src.controllers.questions_controller import QuestionsController
from src.models.postgres.entities.question import Question, QuestionTypes
from src.gui.view.create_question_view import CreateQuestionView


class QuestionView(ctk.CTkToplevel):
    def __init__(self, parent, user_id: int) -> None:
        super().__init__(parent)
        self.__controller = QuestionsController()
        self.user_id = user_id
        self.title("Perguntas do Usuário")
        self.geometry("640x760")
        self.resizable(False, True)
        self.grab_set()

        self.configure(fg_color=("#23272e", "#23272e"))

        self.scrollable_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=("#f5f6fa", "#23272e"),
            corner_radius=16,
            width=580,
            height=650,
        )
        self.scrollable_frame.pack(padx=20, pady=(20, 10), fill="both", expand=True)

        # Botão de adicionar nova pergunta com design melhorado
        add_button = ctk.CTkButton(
            self,
            text="✨ Nova Pergunta",
            command=self._adicionar_pergunta,
            fg_color=("#3498db", "#3498db"),
            hover_color=("#2980b9", "#2980b9"),
            font=("Segoe UI", 15, "bold"),
            height=50,
            width=250,
            corner_radius=15,
        )
        add_button.pack(pady=(0, 25))

        self.question_widgets = []
        self._carregar_perguntas()

    def _carregar_perguntas(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        questions = self.__controller.fetch_all_by_user(self.user_id)

        for question in questions:
            self._criar_card(question)

    def _criar_card(self, question: Question):
        card = ctk.CTkFrame(
            self.scrollable_frame,
            fg_color=("#ffffff", "#3a3a3a"),
            corner_radius=16,
            border_width=1,
            border_color=("#e9ecef", "#555555"),
        )
        card.pack(padx=15, pady=15, fill="x")

        # Pergunta
        question_label = ctk.CTkLabel(
            card,
            text="📝 Pergunta:",
            font=("Segoe UI", 12, "bold"),
            text_color=("#2c3e50", "#ecf0f1"),
        )
        question_label.pack(anchor="w", padx=15, pady=(15, 5))

        entry_question = ctk.CTkEntry(
            card,
            placeholder_text="Digite sua pergunta aqui...",
            width=560,
            height=40,
            font=("Segoe UI", 12),
            corner_radius=8,
        )
        entry_question.insert(0, question.question)
        entry_question.pack(padx=15, pady=(0, 10))

        # Tipo de pergunta
        type_label = ctk.CTkLabel(
            card,
            text="🎯 Tipo:",
            font=("Segoe UI", 12, "bold"),
            text_color=("#2c3e50", "#ecf0f1"),
        )
        type_label.pack(anchor="w", padx=15, pady=(0, 5))

        option_type = ctk.CTkOptionMenu(
            card,
            values=[qt.value for qt in QuestionTypes],
            width=200,
            height=38,
            font=("Segoe UI", 12),
            corner_radius=8,
            button_color=("#3498db", "#3498db"),
            button_hover_color=("#2980b9", "#2980b9"),
        )
        option_type.set(question.question_type.value)
        option_type.pack(anchor="w", padx=15, pady=(0, 10))

        # Resposta
        response_label = ctk.CTkLabel(
            card,
            text="💡 Resposta (opcional):",
            font=("Segoe UI", 12, "bold"),
            text_color=("#2c3e50", "#ecf0f1"),
        )
        response_label.pack(anchor="w", padx=15, pady=(0, 5))

        entry_response = ctk.CTkEntry(
            card,
            placeholder_text="Digite a resposta esperada (opcional)...",
            width=560,
            height=40,
            font=("Segoe UI", 12),
            corner_radius=8,
        )
        if question.response:
            entry_response.insert(0, question.response)
        entry_response.pack(padx=15, pady=(0, 15))

        # Botões lado a lado
        buttons_frame = ctk.CTkFrame(card, fg_color="transparent")
        buttons_frame.pack(padx=15, pady=(0, 15), fill="x", anchor="center")

        save_button = ctk.CTkButton(
            buttons_frame,
            text="💾 Salvar",
            fg_color=("#27ae60", "#27ae60"),
            hover_color=("#229954", "#229954"),
            font=("Segoe UI", 12, "bold"),
            width=160,
            height=40,
            corner_radius=10,
            command=lambda: self._salvar_pergunta(
                question.id,
                entry_question.get(),
                option_type.get(),
                entry_response.get(),
            ),
        )
        save_button.pack(side="left", padx=(0, 10))

        delete_button = ctk.CTkButton(
            buttons_frame,
            text="🗑️ Deletar",
            fg_color=("#e74c3c", "#e74c3c"),
            hover_color=("#c0392b", "#c0392b"),
            font=("Segoe UI", 12, "bold"),
            width=160,
            height=40,
            corner_radius=10,
            command=lambda: self._deletar_pergunta(question.id),
        )
        delete_button.pack(side="left", padx=(10, 0))

    def _salvar_pergunta(
        self, question_id: int, question_text: str, question_type: str, response: str
    ):
        try:
            self.__controller.update_question(
                question_id=question_id,
                user_id=self.user_id,
                question=question_text,
                question_type=question_type,
                response=response,
            )
            messagebox.showinfo(
                "✅ Sucesso", "Pergunta atualizada com sucesso!", parent=self
            )
        except Exception as e:
            messagebox.showerror(
                "❌ Erro", f"Erro ao salvar pergunta:\n\n{str(e)}", parent=self
            )

    def _deletar_pergunta(self, question_id: int):
        if messagebox.askyesno(
            "⚠️ Confirmação",
            "Tem certeza que deseja deletar esta pergunta?",
            parent=self,
        ):
            try:
                self.__controller.delete_question(question_id)
                self._carregar_perguntas()
                messagebox.showinfo(
                    "✅ Sucesso", "Pergunta deletada com sucesso!", parent=self
                )
            except Exception as e:
                messagebox.showerror(
                    "❌ Erro", f"Erro ao deletar pergunta:\n\n{str(e)}", parent=self
                )

    def _adicionar_pergunta(self):
        # Abre a tela de criação de pergunta
        CreateQuestionView(
            parent=self, user_id=self.user_id, callback_refresh=self._carregar_perguntas
        )
