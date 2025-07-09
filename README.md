# Projeto Bot e Cadastro de Usuário

## Como rodar o projeto

1. Crie e ative o ambiente virtual:
   - Windows:
     ```
     python -m venv venv
     .\venv\Scripts\activate
     ```
   - Linux/Mac:
     ```
     python3 -m venv venv
     source venv/bin/activate
     ```

2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

3. Execute a aplicação:
   ```
   python main.py
   ```

## Estrutura do Projeto

- `main.py`: Inicialização da aplicação
- `screens/`: Telas da interface
- `usecase/`: Lógica de negócio
- `infra/`: Persistência e repositórios 