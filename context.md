# 📘 Contexto Geral do Projeto – Pomodoro App

## 🧭 Visão Geral

**Pomodoro App** é um aplicativo multiplataforma (Linux, Windows, macOS) desenvolvido em **Python**, com interface gráfica moderna e amigável, baseado na técnica de produtividade Pomodoro.

O projeto é **modular** e extensível por **plugins externos**, permitindo que qualquer funcionalidade (inclusive telas) possa ser adicionada dinamicamente por desenvolvedores terceiros ou pela equipe principal.

---

## 🎯 Objetivos do Projeto

- Criar uma **ferramenta de produtividade simples e eficiente**, com foco em usabilidade.
- Fornecer uma base sólida para **extensões via plugins**, com controle de qualidade e segurança.
- Garantir que o app funcione **offline**, seja fácil de instalar e mantenha compatibilidade multiplataforma.
- Manter o código **escalável, testável e seguro**, seguindo boas práticas modernas de arquitetura e DevSecOps.

---

## 🧱 Arquitetura

- **Hexagonal Architecture (Ports & Adapters)** com inspiração em Clean Architecture.
- Plugins seguem **contrato de integração via hooks** (usando [pluggy](https://pluggy.readthedocs.io)).
- Camadas principais:
  - `core/`: domínio e casos de uso
  - `adapters/`: GUI, notificações, tray
  - `infrastructure/`: banco local, i18n, update
  - `plugin_manager/`: carregamento e verificação de plugins
  - `plugins/`: plugins locais ou em desenvolvimento

---

## 📦 Stack Técnica

- **Python 3.12+**
- **PySide6** para GUI (Qt for Python)
- **SQLite** como banco de dados local
- **pluggy** para sistema de plugins
- **PyInstaller** para empacotamento
- **GitHub Actions** para CI/CD
- **gettext** para internacionalização
- **logging** com rotação para observabilidade
- **System Tray** nativo via `QSystemTrayIcon`

---

## 🔐 DevSecOps & Segurança

- Security by Design: plugins são validados por metadata e versão
- Plugins não devem acessar diretamente rede ou disco sem permissão explícita
- Logs são rotacionados e mantidos localmente, sem coleta remota
- Atualizações são checadas via JSON remoto com verificação de integridade
- Política de versionamento segue **SemVer** com checagem automática de compatibilidade de plugins

---

## 📂 Organização do Código

```bash
pomodoro_app/
├── main.py                     # Ponto de entrada
├── core/                       # Entidades e casos de uso
├── adapters/                   # GUI, tray, notificações
├── infrastructure/            # DB, i18n, config, updates
├── plugin_manager/            # Gestão e carregamento de plugins
├── plugins/                   # Plugins locais em desenvolvimento
├── tests/                     # Testes unitários e de integração
├── resources/                 # Ícones, temas, imagens
├── docs/                      # ADRs, este contexto, futuras specs
│   └── adr/
├── pyproject.toml
└── README.md
````

---

## 📐 Boas Práticas Adotadas

* Arquitetura modular baseada em interfaces e injeção de dependência
* Código limpo, legível e coeso (seguindo Clean Code)
* Plugins devem ser autocontidos e declarar:

  * Nome, versão, descrição
  * Hooks implementados
  * Compatibilidade com versão do app
* Commits com mensagens semânticas (ex: `feat:`, `fix:`, `refactor:`)
* Testes com `pytest`, usando mocks e cobertura mínima garantida
* CI obrigatória para PRs: lint + testes + build
* ADRs documentadas para cada decisão relevante

---

## 🔄 Como contribuir

1. Leia este `context.md` e os ADRs em `docs/adr/`
2. Mantenha a separação entre domínio, interface e infraestrutura
3. Escreva testes para toda nova funcionalidade
4. Documente novos hooks, se adicionar ao sistema de plugins
5. Siga as regras de segurança e compatibilidade descritas nos ADRs

---

## 📅 Histórico e Evolução

A base do projeto foi estruturada a partir de 07/08/2025, com decisões formalizadas via ADRs.
Cada funcionalidade relevante é rastreada por uma ADR, e todas são públicas no repositório.

---

## 🙋‍♂️ Responsável Técnico

* Nome: \[Seu Nome Aqui]
* GitHub: \[github.com/seuusuario]
* Função: Autor, mantenedor e revisor técnico
* Arquitetura, planejamento e segurança: Assistido por ChatGPT (OpenAI)

---

## 📄 Última atualização

07/08/2025
