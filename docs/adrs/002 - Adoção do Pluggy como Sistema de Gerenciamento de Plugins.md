# ADR: Adoção do Pluggy como Sistema de Gerenciamento de Plugins

**Data:** 07/08/2025<br />
**Status:** Accepted<br />
**Autores:** Responsável Técnico: Pedro H C Schneider (Engenheiro e Arquiteto do Projeto), Consultoria Técnica: ChatGPT (Arquiteto/Engenheiro Sênior DevSecOps)

## Contexto

O aplicativo Pomodoro será um software desktop multiplataforma (Linux, Windows e macOS), escrito em Python, com foco em produtividade pessoal. Desde o início, o projeto será modular, permitindo a extensão das funcionalidades via **plugins externos**.

Esses plugins deverão ser **instaláveis isoladamente**, **carregados dinamicamente**, **executados com segurança** e **capazes de adicionar telas, configurações ou funcionalidades específicas** ao app principal, sem necessidade de recompilar o sistema ou alterar seu core.

Além disso, há planos de criar uma **loja de plugins**, com possibilidade de monetização e contribuições da comunidade, o que torna fundamental um sistema de plugins robusto, padronizado e fácil de manter.

## Decisão

O sistema de plugins do app será implementado utilizando o **[Pluggy](https://pluggy.readthedocs.io/)** — um framework leve de gerenciamento de plugins, baseado em **hooks e contratos explícitos**.

- O core do sistema definirá *hookspecs* (interfaces) para pontos de extensão.
- Cada plugin implementará *hookimpls*, registrando funcionalidades específicas.
- O app poderá carregar múltiplos plugins e resolver seus contratos dinamicamente.
- Metadados e controle de versão serão tratados diretamente via pluggy.

## Alternativas Consideradas

### 1. `importlib` manual com discovery em pastas
**Vantagens:** controle total sobre o carregamento
**Desvantagens:** requer implementação própria de sistema de metadados, validações e isolamento. Pouco escalável e mais suscetível a falhas.

### 2. `pluggy` (escolhida)
**Vantagens:** API enxuta, validada por grandes projetos como pytest. Alta extensibilidade, segurança por padrão e boa documentação.
**Desvantagens:** adiciona uma dependência externa e requer padrão de implementação dos hooks.

### 3. `entry_points` com `importlib.metadata` (PEP 621/610)
**Vantagens:** integração com sistema de pacotes Python (pip, poetry).
**Desvantagens:** exige empacotamento formal dos plugins e publicação de metadados. Maior complexidade para ambientes offline e multiplataforma.

### 4. Sistema próprio com JSON + scripts Python carregados dinamicamente
**Vantagens:** liberdade máxima na estruturação
**Desvantagens:** alto risco de segurança, dificuldade de manutenção, necessidade de reinventar contratos e carregamento. Baixa robustez.

## Justificativa

Pluggy foi escolhido por:

- Ser maduro, usado em projetos relevantes da comunidade Python
- Permitir definição de pontos de extensão (hooks) de forma formal e explícita
- Oferecer isolamento funcional, facilitando o teste e manutenção de cada plugin
- Evitar acoplamento direto entre plugins e o core do sistema
- Operar bem em ambientes offline, sem exigir publicação em PyPI

## Consequências

### Positivas:
- Plugins bem definidos, com pontos de extensão controlados
- Redução significativa de riscos relacionados à execução arbitrária
- Facilidade de manutenção, versionamento e testes
- Permite múltiplos plugins atuando em um mesmo hook (ex: várias telas ou ações integradas)

### Negativas:
- Introduz uma dependência externa (pluggy)
- Requer padrão fixo de implementação, documentação e testes
- Plugins mal escritos podem impactar a execução dos hooks globais, exigindo boas práticas de desenvolvimento

## Reversibilidade

**Sim, com esforço técnico considerável.**

Para reverter essa decisão, seria necessário:

- Refatorar todos os pontos de integração com `pluggy` para uma nova API ou abordagem (ex: entrada manual via `importlib`)
- Alterar todos os plugins existentes ou descontinuá-los
- Lidar com quebra de compatibilidade retroativa, o que impactaria também a loja e a comunidade de desenvolvedores

Portanto, embora reversível, o custo técnico e estratégico da reversão é significativo.

## Referências

- [Pluggy Documentation](https://pluggy.readthedocs.io/)
- [Pluggy – Source code](https://github.com/pytest-dev/pluggy)
- [PEP 621 – Storing project metadata in pyproject.toml](https://peps.python.org/pep-0621/)
- [PEP 610 – Recording the origin of installed distributions](https://peps.python.org/pep-0610/)
