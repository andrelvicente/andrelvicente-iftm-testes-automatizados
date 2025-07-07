# 🧪 Testes Automatizados com FastAPI

Repositório desenvolvido como parte da disciplina de **Testes Automatizados**, utilizando FastAPI com SQLAlchemy, Pytest, e simulações da camada de serviço (`ClientService`) com `unittest.mock`.

---

## ✅ Funcionalidades

Este projeto contém:

- API REST para gerenciamento de clientes
- Endpoints para:
  - Listar todos os clientes
  - Buscar cliente por ID
  - Buscar cliente por CPF
  - Buscar clientes por renda
  - Criar, atualizar e deletar cliente
- Testes unitários e de integração com `pytest`
- Simulação de dependência da camada de serviço usando `patch`
- Banco de dados em memória (`SQLite`) para testes isolados

---

## 📁 Estrutura

```

.
├── app/
│   ├── main.py
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── repositories/
│   └── routes/
├── tests/
│   ├── services/
│   │   ├── test\_client\_service.py
│   │   └── web/
│   │       └── test\_client\_routes.py
├── requirements.txt
└── README.md

````

---

## 🚀 Como executar

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
````

### 2. Crie e ative o ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute os testes

```bash
DATABASE_URL=sqlite:///:memory: PYTHONPATH=. pytest
```

---

## 🧪 Testes

Os testes cobrem os seguintes casos:

* Buscar todos os clientes
* Buscar por ID (existente e inexistente)
* Buscar por CPF (existente e inexistente)
* Buscar por renda
* Criar cliente
* Atualizar cliente (existente e inexistente)
* Deletar cliente (existente e inexistente)

---

## 🛠 Tecnologias

* [FastAPI](https://fastapi.tiangolo.com/)
* [SQLAlchemy](https://www.sqlalchemy.org/)
* [Pydantic v2](https://docs.pydantic.dev/)
* [Pytest](https://docs.pytest.org/)
* [HTTPX](https://www.python-httpx.org/)
* [Unittest.mock](https://docs.python.org/3/library/unittest.mock.html)

---

## 👨‍🏫 Observações para o professor

* Os testes estão organizados por funcionalidade
* A camada de serviço foi mockada nos testes web
* O projeto está preparado para rodar localmente com banco em memória (isolado)
* Todos os testes foram executados com sucesso (`pytest`)

---

## 📄 Licença

Este projeto é apenas para fins acadêmicos.
