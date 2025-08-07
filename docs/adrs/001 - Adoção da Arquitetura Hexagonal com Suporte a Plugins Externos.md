# ADR: Adoção da Arquitetura Hexagonal com Suporte a Plugins Externos

**Data:** 07/08/2025<br />
**Status:** Accepted<br />
**Autores:** Responsável Técnico: Pedro H C Schneider (Engenheiro e Arquiteto do Projeto), Consultoria Técnica: ChatGPT (Arquiteto/Engenheiro Sênior DevSecOps)

## Contexto

O sistema em questão é um aplicativo desktop multiplataforma (Linux, Windows, macOS), escrito em Python. Ele será voltado à produtividade pessoal, com interface gráfica (GUI), integração com o system tray e suporte a internacionalização. Um dos diferenciais estratégicos é sua extensibilidade: funcionalidades adicionais serão desenvolvidas e distribuídas como **plugins externos**, podendo ser criadas pela comunidade ou comercializadas por meio de uma loja integrada.

Esse cenário exige uma base arquitetural que proporcione **desacoplamento claro entre domínio, interface e infraestrutura**, **modularidade real** e **capacidade de crescimento sustentável**, mantendo a manutenibilidade e testabilidade do sistema. A decisão arquitetural precisa ser tomada agora, pois o projeto encontra-se em fase inicial de estruturação.

## Decisão

Adotar a **Arquitetura Hexagonal (Ports & Adapters)** como estrutura base do projeto, permitindo:

- Domínio isolado, independente de frameworks e infraestrutura
- Adapters externos para GUI, system tray, persistência, notificações, etc.
- Plugins externos integrados por meio de portas bem definidas (interfaces)
- Injeção de dependência para acoplamento dinâmico de funcionalidades externas

Além disso, será estruturado um **mecanismo padrão de carregamento de plugins**, com contratos formais (interfaces) que permitirão o desenvolvimento e a integração de novas funcionalidades sem necessidade de recompilar o sistema principal.

## Alternativas Consideradas

- **Arquitetura monolítica tradicional com GUI acoplada ao domínio**
  Simples de implementar, mas ineficaz para modularização e crescimento com plugins. Alto acoplamento prejudicaria a manutenção e extensibilidade.

- **Clean Architecture pura (com camadas interdependentes)**
  Abordagem sólida, mas sem foco explícito na entrada/saída como portas/adapters, o que dificultaria o desacoplamento necessário para plugins externos.

- **MVP simples e acoplado, com refatorações futuras**
  Menor esforço inicial, mas criaria dívida técnica desde o início. Risco elevado de dificultar futuras implementações modulares.

- **Arquitetura orientada a serviços dentro de um único processo (micropacotes)**
  Boa separação, mas não atenderia ao requisito de extensibilidade por meio de plugins dinâmicos, tampouco oferece simplicidade na integração GUI + domínio.

## Justificativa

A **Arquitetura Hexagonal** foi escolhida por:

- Promover um **desacoplamento claro e escalável**
- Permitir **testes automatizados em isolamento**
- Ser **ideal para integração de módulos externos (plugins)**
- Garantir **evolução técnica sustentável**
- Alinhar-se ao objetivo de **monetização via extensões**

Essa abordagem favorece a consistência do core, preservando integridade mesmo com a adição de funcionalidades por terceiros.

## Consequências

### Positivas:
- Sistema altamente modular e extensível
- Facilidade em criar, testar e manter novas funcionalidades
- Capacidade de expandir o produto sem alterar o núcleo
- Suporte a comunidade de desenvolvedores e a modelos de negócio baseados em plugins

### Negativas:
- Curva de aprendizado e maior complexidade inicial
- Necessidade de contratos bem definidos e documentação robusta
- Maior exigência de disciplina arquitetural e testes em múltiplas plataformas

## Reversibilidade

**Sim, mas com custo médio/alto.**
Caso a arquitetura precise ser simplificada no futuro (ex: para reduzir escopo ou acelerar entregas), será necessário:

- Remover a estrutura de ports/adapters
- Reacoplar domínio, GUI e infraestrutura
- Eliminar carregamento dinâmico de plugins

Essa mudança implicaria refatorações amplas e perda de extensibilidade. Portanto, a reversão deve ser cuidadosamente avaliada.

## Referências

- [Alistair Cockburn – Hexagonal Architecture (original paper)](https://alistair.cockburn.us/hexagonal-architecture/)
