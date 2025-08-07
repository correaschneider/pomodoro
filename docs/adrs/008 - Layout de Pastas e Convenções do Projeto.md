# ADR: Layout de Pastas e Convenções do Projeto

**Data:** 07/08/2025<br />
**Status:** Accepted<br />
**Autores:** Responsável Técnico: Pedro H C Schneider (Engenheiro e Arquiteto do Projeto), Consultoria Técnica: ChatGPT (Arquiteto/Engenheiro Sênior DevSecOps)

## Contexto

O app Pomodoro está em sua fase inicial de desenvolvimento. Ele será uma aplicação desktop com foco em produtividade, escrita em Python, com interface gráfica (GUI), suporte a system tray, plugins dinâmicos, internacionalização e empacotamento multiplataforma.

Como o sistema será **modular por design** e contará com múltiplas camadas (domínio, GUI, persistência, atualizações, plugins, etc.), é essencial que a organização dos arquivos e diretórios reflita essa arquitetura, garantindo:

- **Clareza estrutural**
- **Desacoplamento entre as camadas**
- **Facilidade de testes, manutenção e evolução**
- **Integração suave com empacotadores como PyInstaller**

## Decisão

Adotar um layout de projeto baseado na **Arquitetura Hexagonal (Ports & Adapters)**, com separação explícita entre:

- **Core (domínio puro e casos de uso)**
- **Adapters (interface com mundo externo: GUI, tray, notificações, etc.)**
- **Infrastructure (implementações técnicas como banco, i18n, config)**
- **Plugins (extensões carregadas dinamicamente)**
- **Sistema de plugin manager isolado**
- **Testes organizados por escopo**
- **Assets e recursos separados**
- **Documentação e ADRs versionadas com o projeto**

Este layout facilitará a modularização, a escrita de testes, o empacotamento multiplataforma e o onboarding de novos contribuidores.

## Alternativas Consideradas

| Layout                                             | Prós                                            | Contras                                 |
| -------------------------------------------------- | ----------------------------------------------- | --------------------------------------- |
| **Flat (tudo no mesmo nível)**                     | Simples de navegar no início                    | Escala mal, difícil de modularizar      |
| **MVC tradicional (gui/models/services)**          | Familiar a muitos devs                          | Acopla camadas, quebra responsabilidade |
| **Arquitetura Hexagonal (Ports & Adapters)**       | Separa domínios, facilita testes, desacoplado   | Maior curva de entrada                  |
| **Monorepo com subpacotes (plugins como pacotes)** | Alta escalabilidade, isola plugins, facilita CI | Complexo demais para o MVP inicial      |

## Justificativa

A estrutura baseada em **Hexagonal Architecture** foi escolhida por:

- Alinhar-se à decisão já registrada na **ADR-001**
- Fornecer **fronteiras claras entre domínio, GUI e infraestrutura**
- Permitir que plugins, GUI, CLI ou mecanismos de persistência evoluam **independentemente**
- Reduzir o acoplamento e facilitar a testabilidade
- Oferecer um caminho claro para crescimento progressivo do sistema

## Consequências

### Positivas:
- Organização clara e escalável
- Facilita testes e documentação por módulo
- Torna fácil isolar e carregar plugins externos
- Mantém o domínio protegido de dependências externas
- Favorece boas práticas e contribuições externas consistentes

### Negativas:
- Curva de aprendizado inicial maior para quem não conhece Hexagonal
- Exige disciplina para manter os boundaries entre camadas
- Plugins precisam seguir convenções bem definidas para integração fluida

## Reversibilidade

**Sim, com esforço moderado.**

Como os namespaces e imports estarão organizados com base em pacotes e interfaces, seria possível reorganizar os diretórios futuramente com apoio de ferramentas como `rope`, `pyright` ou IDEs como PyCharm. A reestruturação exigiria revisão de imports e paths no build, mas não afeta o núcleo funcional do sistema se a separação estiver bem definida.

## Referências

- [Alistair Cockburn – Ports and Adapters (Hexagonal Architecture)](https://alistair.cockburn.us/hexagonal-architecture/)
- [Clean Architecture em Python – Real Python](https://realpython.com/architecture-patterns-python/)
- [PyInstaller – Custom Folder Layout](https://pyinstaller.org/en/stable/usage.html#making-a-one-folder-app)

## Layout Proposto

```bash
pomodoro_app/
├── main.py                   # ponto de entrada
├── core/                     # entidades e casos de uso (sem dependências)
│   ├── entities/
│   ├── usecases/
│   └── interfaces/           # ports (ex: SessionRepository, NotificationPort)
├── adapters/                 # implementação dos ports (adapters)
│   ├── gui/                  # GUI principal (PySide6)
│   ├── system_tray/
│   ├── notifications/
│   └── cli/                  # (opcional para debug/headless)
├── infrastructure/           # serviços técnicos e utilitários
│   ├── db/                   # SQLite, SQLAlchemy ou abstrações
│   ├── i18n/                 # arquivos .po/.mo, loaders
│   ├── config/               # leitura/escrita de configurações
│   └── update/               # verificação e notificação de novas versões
├── plugins/                  # plugins locais (em desenvolvimento/teste)
│   └── plugin_nome/
├── plugin_manager/           # pluggy integration, validation, lifecycle
├── tests/
│   ├── unit/
│   └── integration/
├── resources/                # ícones, temas, imagens
├── pyproject.toml
├── README.md
└── docs/
    └── adr/                  # Arquivos de decisão arquitetural
```