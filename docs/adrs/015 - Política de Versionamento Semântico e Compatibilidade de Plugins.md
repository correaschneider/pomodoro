# ADR: Política de Versionamento Semântico e Compatibilidade de Plugins

**Data:** 07/08/2025<br />
**Status:** Accepted<br />
**Autores:** Responsável Técnico: Pedro H C Schneider (Engenheiro e Arquiteto do Projeto), Consultoria Técnica: ChatGPT (Arquiteto/Engenheiro Sênior DevSecOps)

## Contexto

O app Pomodoro adota uma arquitetura extensível baseada em **plugins externos**, com execução isolada, permissões controladas e contratos bem definidos. Para garantir estabilidade, suporte técnico e evolução sustentável da plataforma, é necessário definir uma política clara de versionamento e controle de compatibilidade entre o núcleo do sistema e seus plugins.

O projeto também prevê a criação futura de uma **loja de plugins**, o que torna ainda mais crítica a rastreabilidade e o controle sobre quais versões são suportadas em cada release.

## Decisão

A política oficial de versionamento será baseada no padrão **SemVer – Semantic Versioning**, com o formato:

```

MAJOR.MINOR.PATCH

````

Exemplo de versões válidas:

- `1.0.0` — primeira versão estável
- `1.2.3` — incrementos compatíveis com a major atual
- `2.0.0` — introdução de breaking changes

### Compatibilidade com Plugins

Todos os **plugins deverão declarar explicitamente a faixa de versões compatíveis** do app, através do campo `compatible_with`, dentro do arquivo `plugin.toml`.

Exemplo:

```toml
[plugin]
name = "focus_boost"
version = "1.2.0"
compatible_with = ">=1.0.0,<2.0.0"
````

A validação dessa faixa será feita automaticamente no momento da instalação e no carregamento dinâmico dos plugins. Plugins incompatíveis serão rejeitados com mensagem amigável ao usuário.

## Alternativas Consideradas

| Estratégia                          | Prós                                         | Contras                                               |
| ----------------------------------- | -------------------------------------------- | ----------------------------------------------------- |
| **SemVer (MAJOR.MINOR.PATCH)**      | Padrão da indústria, previsível              | Requer disciplina para aplicação correta              |
| **Versão contínua baseada em data** | Simples de gerar, útil para releases rápidos | Não expressa compatibilidade automaticamente          |
| **Versão fixa (ex: v1, v2)**        | Fácil de gerenciar em grandes ciclos         | Pouco flexível, não informa granularidade de mudanças |

A estratégia escolhida foi **SemVer**, por ser a única que permite rastrear com clareza **breaking changes** e **garantir segurança na evolução de um sistema com dependências externas**.

## Justificativa

* Permite que plugins especifiquem de forma precisa com quais versões do app são compatíveis
* Suporta validação automática e bloqueio de versões inseguras
* Facilita rollback, changelog, update automático e suporte técnico
* Evita falhas causadas por mudanças inesperadas na API
* Compatível com futuras integrações com sistemas de update, loja de plugins e scripts de build

## Consequências

### Positivas

* Proteção contra carregamento de plugins incompatíveis
* Diagnóstico de falhas facilitado por controle de versão
* Automatização da compatibilidade e simplificação da loja
* Redução de regressões e bugs silenciosos após updates

### Negativas

* Requer rigor na aplicação do versionamento SemVer
* Necessário manter changelog e documentar mudanças que afetam contratos de plugin
* Plugins podem ser rejeitados mesmo sendo funcionalmente compatíveis se a faixa `compatible_with` estiver desatualizada

## Reversibilidade

**Tecnicamente sim, mas altamente desaconselhável.**

Abandonar o SemVer exigiria a reestruturação completa do sistema de validação de plugins, e causaria:

* Quebra da loja de plugins
* Inconsistência nos contratos entre núcleo e extensões
* Perda de previsibilidade na evolução do sistema

Reverter exigiria comunicar publicamente todos os autores de plugins e revisar toda a documentação de desenvolvimento.

## Referências

* [https://semver.org/lang/pt-BR/](https://semver.org/lang/pt-BR/)
* [PEP 440 – Python Versioning Scheme](https://peps.python.org/pep-0440/)
* [Rust Cargo compatibility metadata](https://doc.rust-lang.org/cargo/reference/specifying-dependencies.html#specifying-dependencies-from-cratesio)
* Exemplos de validação semver com [`packaging.version`](https://packaging.pypa.io/en/stable/version.html) e `semver` PyPI lib

## Restrições Técnicas e Organizacionais

* O PluginManager deverá fazer parsing e validação do campo `compatible_with`
* O sistema de update do app deverá incluir a versão atual no JSON remoto
* Todos os plugins hospedados ou enviados à loja deverão seguir essa convenção
* Breaking changes no app exigem incremento da versão MAJOR
