# ADR: Adoção do SQLite como Banco de Dados Embutido

**Data:** 07/08/2025<br />
**Status:** Accepted<br />
**Autores:** Responsável Técnico: Pedro H C Schneider (Engenheiro e Arquiteto do Projeto), Consultoria Técnica: ChatGPT (Arquiteto/Engenheiro Sênior DevSecOps)

## Contexto

O aplicativo Pomodoro será uma aplicação desktop multiplataforma (Linux, Windows e macOS), desenvolvida em Python, com foco em produtividade pessoal. A aplicação requer persistência de dados para funcionalidades críticas desde o início, incluindo:

- Sessões de Pomodoro e estatísticas históricas
- Configurações do usuário
- Dados relacionados a plugins instalados e ativos

Como o sistema será modular e deverá operar **offline**, o banco de dados precisa ser **embutido, leve, confiável e compatível com múltiplos sistemas operacionais**. Além disso, a arquitetura geral do projeto (Hexagonal + Plugins) demanda que o banco possa ser facilmente encapsulado por um repositório para preservar a separação entre domínio e infraestrutura.

## Decisão

Adotar o **SQLite** como sistema de banco de dados local.

- Embutido diretamente no Python (`sqlite3`)
- ACID, confiável, estável e maduro
- Compatível com todas as plataformas alvo (Linux, Windows, macOS)
- Permite backups simples (via cópia do arquivo `.db`)
- Suporte completo a SQL e ferramentas de administração

A camada de persistência será isolada por um **Repository Pattern**, mantendo o domínio desacoplado e garantindo possibilidade futura de substituição.

## Alternativas Consideradas

| Alternativa                | Considerações                                                       |
| -------------------------- | ------------------------------------------------------------------- |
| **Arquivos JSON/YAML/INI** | Simples de manipular, mas não escalável nem eficiente para buscas   |
| **TinyDB**                 | Banco NoSQL em JSON, fácil de usar, mas pouco robusto               |
| **DuckDB**                 | Otimizado para análise de dados em larga escala, overkill neste caso |
| **MongoDB (mongita)**      | Simula MongoDB localmente, mas exige libs externas e maior acoplamento |
| **SQLite**                 | Equilibrado, confiável, amplamente suportado, com mínima dependência |

## Justificativa

O **SQLite** foi escolhido por:

- Ter **baixo custo de entrada** (já embutido no Python)
- Ser **maduro e bem testado em aplicações reais**
- Suportar **transações ACID**, garantindo integridade dos dados
- Possibilitar **migração futura com baixo impacto**, desde que os repositórios sejam implementados corretamente
- Permitir que o app funcione **100% offline** com persistência confiável

## Consequências

### Positivas:
- Persistência local leve, embutida e confiável
- Portabilidade total entre plataformas
- Boa performance para volume de dados esperado
- Backup/restauração simples
- Facilita testes com bancos isolados por ambiente

### Negativas:
- Suporte limitado a concorrência em ambientes multi-thread
- Requer controle e versionamento de schema (migrações)
- Pode se tornar limitado caso o app cresça exponencialmente em uso ou volume de dados

## Reversibilidade

**Sim.**

Desde que a persistência seja abstraída por meio de interfaces (`SessionRepository`, `StatsRepository`, etc.), o SQLite pode ser substituído por qualquer outro mecanismo com suporte equivalente:

- Outro banco relacional (ex: PostgreSQL)
- Banco NoSQL (ex: MongoDB)
- Armazenamento baseado em arquivos

A mudança exigiria apenas a implementação de novos adapters sem afetar o domínio da aplicação.

## Referências

- [SQLite – Official Site](https://sqlite.org/index.html)
- [Python sqlite3 — Standard Library](https://docs.python.org/3/library/sqlite3.html)
- [Repository Pattern – Martin Fowler](https://martinfowler.com/eaaCatalog/repository.html)
- [SQLAlchemy SQLite Dialect](https://docs.sqlalchemy.org/en/20/dialects/sqlite.html) *(caso ORM venha a ser usado futuramente)*
