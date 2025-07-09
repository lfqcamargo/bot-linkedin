class UpdateUserController:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def handle(self, props: dict) -> None:
        user_id = props.get("id")
        if user_id is None:
            raise ValueError("ID do usuário é obrigatório para edição.")
        self.user_repository.update(type('User', (), props)()) 