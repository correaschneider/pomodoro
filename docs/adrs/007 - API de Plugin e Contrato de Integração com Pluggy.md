# ADR: API de Plugin e Contrato de Integração com Pluggy

**Data:** 07/08/2025<br />
**Status:** Accepted<br />
**Autores:** Responsável Técnico: Pedro H C Schneider (Engenheiro e Arquiteto do Projeto), Consultoria Técnica: ChatGPT (Arquiteto/Engenheiro Sênior DevSecOps)

## Contexto

O app Pomodoro será modular desde sua concepção, com funcionalidades extensíveis por meio de **plugins externos**. Esses plugins poderão:

- Adicionar **telas** (ex: estatísticas personalizadas, modos alternativos)
- Estender ou modificar **configurações**
- Executar **ações programadas** (ex: enviar webhooks, tocar sons)
- Integrar com **outros plugins** ou **serviços locais**

A flexibilidade do sistema de plugins é um diferencial estratégico, permitindo futuras monetizações (loja de plugins), contribuições da comunidade e rápida evolução do ecossistema.

Para garantir interoperabilidade, segurança e manutenibilidade, é necessário definir **um contrato formal e padronizado para os plugins** — incluindo como são identificados, carregados, registrados e validados.

## Decisão

Será adotada uma **API de Plugin baseada no framework `pluggy`**, com **hooks explícitos definidos pelo app Pomodoro**. Cada plugin deverá implementar um ou mais desses hooks, registrando funcionalidades específicas.

Características principais da decisão:

- O core define os **hookspecs** (contratos)
- Plugins implementam os **hookimpls**
- Um **PluginManager** central será responsável pelo discovery, validação, compatibilidade e execução dos plugins
- Plugins poderão declarar **dependências de outros plugins** e **versão mínima da API**

## Alternativas Consideradas

| Alternativa                                          | Prós                              | Contras                                                           |
| ---------------------------------------------------- | --------------------------------- | ----------------------------------------------------------------- |
| **Interface com Pluggy e hooks explícitos**          | Extensível, documentável, modular | Requer definição cuidadosa de nomes e assinaturas dos hooks       |
| **Sistema de entrada via entry_points (PEP 621)**    | Compatível com PyPI, poetry       | Menos controle sobre escopo e integração dinâmica                 |
| **Carregamento manual com `importlib` + convenções** | Simples de começar                | Propenso a erros, difícil de escalar                              |
| **Plugins como microservices via IPC/local socket**  | Altamente isolado                 | Overkill para o escopo, difícil de manter sincronização de estado |

## Justificativa

A escolha por `pluggy` se justifica por:

- **Desacoplamento completo** entre core e plugins
- **Capacidade de múltiplos plugins** atuarem sobre o mesmo ponto (ex: várias ações ao finalizar um Pomodoro)
- **Facilidade de documentação**, versionamento e testes dos hooks
- Modelo **já validado** em projetos como `pytest`, `tox` e `devpi`
- Permitir que os plugins sejam desenvolvidos, mantidos e versionados de forma **independente**

## Consequências

### Positivas:
- API de plugins clara e padronizada
- Permite testes automatizados com mocks e simulações de plugins
- Plugins podem declarar dependências e interoperar entre si
- Base sólida para construção de uma **loja de plugins**
- Contrato desacoplado do core permite evolução paralela

### Negativas:
- Exige estrutura e padronização nos repositórios de plugins
- Necessária curva de aprendizado para desenvolvedores externos
- Versões de hook mal gerenciadas podem causar falhas em tempo de execução (ex: assinatura quebrada)

## Reversibilidade

**Sim, com esforço controlado.**

A principal exigência para reversibilidade é **encapsular o uso de `pluggy` em um `PluginManager` próprio**. Dessa forma, a lógica de carregamento, execução e verificação dos plugins permanece sob controle, permitindo trocar o backend de integração (ex: para entry_points, registrador próprio ou microserviços) sem afetar o domínio ou a interface dos plugins.

## Referências

- [Pluggy Documentation](https://pluggy.readthedocs.io/)
- [PEP 621 – pyproject.toml metadata](https://peps.python.org/pep-0621/)
- [Pytest Plugin System](https://docs.pytest.org/en/stable/writing_plugins.html)
- [API Design Best Practices](https://martinfowler.com/articles/richardsonMaturityModel.html)
