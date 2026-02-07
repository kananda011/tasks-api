Tasks API (To do list) FastAPI + MongoBD + Docker

API REST para gerenciamento de tarefa com operação CRUD e regras de validações definidas no desafio.

✅ Funcionalidades
-Criar tarefas:"POST/tasks"
-Listar tarefas:"GET/tasks" (com filtros opcionais por "status" e "priority")
-Buscar tarefas :"GET/tasks/{id}"
-Atualiza tarefa: "PUT/tasks/{id}"
-Deleta tarefa: "DELETE/tasks/{id}"

📌 Regras de negócio e validações
- Status permitido: "pending", "in_progress", "completed", "cancelled"
- Prioridade: "low", "medium", "high"
Validações obrigátorias
- "title" obrigatório (min 3/ max 100 caracteres)
- status deve ser válido
- "due_date" não pode ser no passado
- tarefas com status "completed" não pode ser editadas

🧰 Tecnologias

- Python + FastAPI
-MongoDB (NOsql)
- Docker + Docker compose
-Documentação Swagger (via FastAPI em "/docs")

Como executar 

-Docker
-Docket Compose

Subir a aolicação
Na raiz do projeto execute:
"docker compose up --build"

