# ADR: Estratégia de Verificação e Notificação de Atualizações

**Data:** 07/08/2025<br />
**Status:** Accepted<br />
**Autores:** Responsável Técnico: Pedro H C Schneider (Engenheiro e Arquiteto do Projeto), Consultoria Técnica: ChatGPT (Arquiteto/Engenheiro Sênior DevSecOps)

## Contexto

O app Pomodoro será distribuído como um aplicativo desktop standalone (empacotado via `.exe`, `.dmg` e `.AppImage`), com foco em funcionar **offline** e de forma **multiplataforma**. Para manter a base de usuários atualizada com as últimas versões — incluindo **correções de bugs**, **melhorias de segurança** e **novos recursos** — é necessário um sistema confiável de verificação de atualizações.

A atualização automática completa (como ocorre em apps com instaladores nativos ou gerenciadores de pacotes) não é viável no MVP. Ainda assim, é crucial notificar o usuário sobre novas versões disponíveis, de forma segura, discreta e que funcione em ambientes offline parcial.

## Decisão

A estratégia de atualização será implementada com **verificação periódica via JSON remoto** hospedado em um domínio controlado (ex: GitHub Pages ou API REST).

- O app consultará periodicamente (ex: ao iniciar ou 1x/dia) um arquivo JSON remoto
- O JSON conterá: número da última versão, changelog resumido, URL de download e hash opcional
- Se houver nova versão, será exibida uma notificação amigável
- Caso o app esteja offline, o mecanismo usará cache e tentará novamente depois
- A atualização em si será feita manualmente pelo usuário, baixando o novo instalador

## Alternativas Consideradas

| Alternativa                                                       | Prós                                          | Contras                                                    |
| ----------------------------------------------------------------- | --------------------------------------------- | ---------------------------------------------------------- |
| **Verificação via JSON remoto (GitHub Pages ou API)**             | Simples, fácil de versionar, offline-friendly | Não atualiza o app automaticamente, só notifica            |
| **Uso de updater embutido (ex: PyUpdater, WinSparkle)**           | Atualização automática completa               | Complexidade alta, integração frágil em ambientes diversos |
| **Distribuição via gerenciador externo (ex: Snap, Brew, Winget)** | Integração com SO                             | Fora do escopo do MVP, limita o controle de distribuição   |
| **Instalação manual com changelog no app**                        | Simples e direto                              | Exige ação ativa do usuário para verificar                 |

## Justificativa

A opção por um **JSON remoto versionado** foi motivada por:

- Ser **simples de implementar** e **manter com CI/CD**
- Permitir **notificações automatizadas**, sem obrigar o usuário a checar manualmente
- Ter **alta compatibilidade com o modelo de distribuição atual**
- Ser **reversível**, podendo ser substituído por atualizador automático no futuro
- Não depender de instalação externa ou integradores de pacotes

## Consequências

### Positivas:
- Mantém os usuários informados sobre novas versões
- Integração simples com GitHub Actions para atualização do JSON
- Funciona bem com empacotamento standalone
- Reversível e evolutivo
- Offline-friendly: pode fazer cache e revalidar periodicamente

### Negativas:
- A atualização exige ação manual do usuário
- O app depende de acesso à internet para verificar novas versões
- A origem do JSON precisa ser confiável e protegida contra spoofing
- Necessário cuidar da experiência de notificação para não ser invasiva

## Reversibilidade

**Sim.**

O módulo de verificação de atualização será encapsulado como um **serviço isolado**, podendo ser substituído posteriormente por:

- Um atualizador embutido (como o PyUpdater ou custom scripts)
- Integração com gerenciadores de pacote (Snap, Flatpak, Brew, Winget)
- Um sistema de autoatualização proprietário

Desde que as dependências estejam isoladas e bem documentadas, a troca de estratégia será viável com refatoração moderada.

## Referências

- [PyUpdater](https://www.pyupdater.org/)
- [GitHub Pages – Static File Hosting](https://pages.github.com/)
- [JSON Schema – Best practices](https://json-schema.org/)
- [WinSparkle – Auto-update framework for Windows](https://winsparkle.org/)
- [Example: Electron JSON Update Strategy](https://www.electron.build/auto-update)
