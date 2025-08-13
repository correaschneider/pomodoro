<context>
# Overview
Pomodoro App é um aplicativo desktop multiplataforma (Linux, Windows, macOS) focado em produtividade, com GUI moderna em PySide6, execução offline, e extensível por plugins externos via Pluggy. O produto atende usuários que desejam gerenciar ciclos de foco e pausa de forma leve, integrada ao system tray, com notificações nativas e overlay visual.

Metadata essencial:
- Produto: Pomodoro App
- Versão do PRD: 1.0.0
- Dono técnico: Responsável Técnico (ver `context.md`)
- Estado: Draft inicial consolidado a partir de ADRs 001–015 e `context.md`
- Fontes: ver ADRs em `docs/adrs/` e `context.md`

Links de referência rápida:
- Contexto do projeto: [`context.md`](../context.md)
- ADR-001 — Arquitetura Hexagonal: [`docs/adrs/001 - Adoção da Arquitetura Hexagonal com Suporte a Plugins Externos.md`](./adrs/001%20-%20Ado%C3%A7%C3%A3o%20da%20Arquitetura%20Hexagonal%20com%20Suporte%20a%20Plugins%20Externos.md)
- ADR-002 — Pluggy: [`docs/adrs/002 - Adoção do Pluggy como Sistema de Gerenciamento de Plugins.md`](./adrs/002%20-%20Ado%C3%A7%C3%A3o%20do%20Pluggy%20como%20Sistema%20de%20Gerenciamento%20de%20Plugins.md)
- ADR-003 — SQLite: [`docs/adrs/003 - Adoção do SQLite como Banco de Dados Embutido.md`](./adrs/003%20-%20Ado%C3%A7%C3%A3o%20do%20SQLite%20como%20Banco%20de%20Dados%20Embutido.md)
- ADR-004 — gettext: [`docs/adrs/004 - Adoção de gettext com Arquivos .po-.mo para Internacionalização.md`](./adrs/004%20-%20Ado%C3%A7%C3%A3o%20de%20gettext%20com%20Arquivos%20.po-.mo%20para%20Internacionaliza%C3%A7%C3%A3o.md)
- ADR-005 — PySide6: [`docs/adrs/005 - Escolha do Framework de GUI – PySide6 (Qt for Python).md`](./adrs/005%20-%20Escolha%20do%20Framework%20de%20GUI%20%E2%80%93%20PySide6%20(Qt%20for%20Python).md)
- ADR-006 — Update via JSON: [`docs/adrs/006 - Estratégia de Verificação e Notificação de Atualizações.md`](./adrs/006%20-%20Estrat%C3%A9gia%20de%20Verifica%C3%A7%C3%A3o%20e%20Notifica%C3%A7%C3%A3o%20de%20Atualiza%C3%A7%C3%B5es.md)
- ADR-007 — API de Plugin (Pluggy): [`docs/adrs/007 - API de Plugin e Contrato de Integração com Pluggy.md`](./adrs/007%20-%20API%20de%20Plugin%20e%20Contrato%20de%20Integra%C3%A7%C3%A3o%20com%20Pluggy.md)
- ADR-008 — Layout de Pastas: [`docs/adrs/008 - Layout de Pastas e Convenções do Projeto.md`](./adrs/008%20-%20Layout%20de%20Pastas%20e%20Conven%C3%A7%C3%B5es%20do%20Projeto.md)
- ADR-009 — CI/CD: [`docs/adrs/009 - Estratégia de CI-CD com GitHub Actions para Build Multiplataforma.md`](./adrs/009%20-%20Estrat%C3%A9gia%20de%20CI-CD%20com%20GitHub%20Actions%20para%20Build%20Multiplataforma.md)
- ADR-010 — Notificações/Overlay: [`docs/adrs/010 - Sistema de Notificações e Overlay Visual para Ciclos de Pomodoro.md`](./adrs/010%20-%20Sistema%20de%20Notifica%C3%A7%C3%B5es%20e%20Overlay%20Visual%20para%20Ciclos%20de%20Pomodoro.md)
- ADR-011 — Segurança de Plugins: [`docs/adrs/011 - Política de Segurança para Plugins (Security by Design).md`](./adrs/011%20-%20Pol%C3%ADtica%20de%20Seguran%C3%A7a%20para%20Plugins%20(Security%20by%20Design).md)
- ADR-012 — Logging/Observabilidade: [`docs/adrs/012 - Estratégia de Logging e Observabilidade.md`](./adrs/012%20-%20Estrat%C3%A9gia%20de%20Logging%20e%20Observabilidade.md)
- ADR-013 — Empacotamento: [`docs/adrs/013 - Estratégia de Empacotamento e Distribuição Multiplataforma.md`](./adrs/013%20-%20Estrat%C3%A9gia%20de%20Empacotamento%20e%20Distribui%C3%A7%C3%A3o%20Multiplataforma.md)
- ADR-014 — System Tray (QSystemTrayIcon): [`docs/adrs/014 - Suporte ao System Tray com QSystemTrayIcon (PySide6).md`](./adrs/014%20-%20Suporte%20ao%20System%20Tray%20com%20QSystemTrayIcon%20(PySide6).md)
- ADR-015 — SemVer/Compatibilidade: [`docs/adrs/015 - Política de Versionamento Semântico e Compatibilidade de Plugins.md`](./adrs/015%20-%20Pol%C3%ADtica%20de%20Versionamento%20Sem%C3%A2ntico%20e%20Compatibilidade%20de%20Plugins.md)

# Core Features
Principais capacidades do produto e seu porquê, com visão de funcionamento em alto nível.

1) Arquitetura Hexagonal + Extensibilidade por Plugins
- O que faz: desacopla domínio de GUI/infra, permitindo plugins externos adicionarem telas, ações e configurações.
- Por que importa: escalabilidade, testabilidade e ecossistema de extensões.
- Como funciona: ports (interfaces) no core, adapters para GUI/DB/Tray/Notificações; plugins implementam hooks `pluggy`.
Referências: ADR-001, ADR-002, ADR-007, ADR-011, ADR-015, ADR-008.

2) GUI em PySide6
- O que faz: interface moderna e nativa com componentes Qt.
- Por que importa: usabilidade, performance, multiplataforma.
- Como funciona: janela principal, componentes reativos, integração com i18n e tray.
Referências: ADR-005, ADR-014, ADR-004.

3) System Tray (QSystemTrayIcon)
- O que faz: acessos rápidos para iniciar/pausar/retomar/parar ciclos, abrir configurações e sair.
- Por que importa: controle discreto em segundo plano.
- Como funciona: ícone no tray, menu contextual, tooltip com estado atual.
Referências: ADR-014.

4) Notificações e Overlay Visual
- O que faz: avisa início/fim de foco/pausa mesmo com app minimizado.
- Por que importa: reforça o fluxo de produtividade e evita perdas de timing.
- Como funciona: nativas do SO (plyer/notify2/win10toast) + overlay Qt; fallback pelo tray e logs.
Referências: ADR-010, ADR-014.

5) Internacionalização (gettext)
- O que faz: suporta múltiplos idiomas (pluralização, contexto, fallback).
- Por que importa: acessibilidade e comunidade global.
- Como funciona: marcação `_()`/`gettext()`, arquivos `.po/.mo` por idioma/domínio; plugins podem registrar seus dicionários.
Referências: ADR-004.

6) Persistência Local (SQLite)
- O que faz: armazena sessões, estatísticas, configurações e metadados de plugins.
- Por que importa: histórico e estado offline confiável.
- Como funciona: repositórios isolam o domínio (`Repository Pattern`).
Referências: ADR-003.

7) Logging e Observabilidade
- O que faz: registra eventos, erros e atividade de plugins com rotação de arquivos.
- Por que importa: suporte, diagnóstico e segurança.
- Como funciona: `logging` com handlers por contexto, `RotatingFileHandler`, separação por arquivos.
Referências: ADR-012.

8) Verificação de Atualizações via JSON
- O que faz: notifica novas versões disponíveis.
- Por que importa: mantém usuários atualizados com correções e melhorias.
- Como funciona: leitura periódica de JSON remoto (versão, changelog, url, hash), com cache e experiência não intrusiva.
Referências: ADR-006.

9) Empacotamento Multiplataforma (PyInstaller)
- O que faz: entrega binários standalone por SO.
- Por que importa: facilidade de instalação para usuários finais.
- Como funciona: inclusão de assets `.mo`, ícones/temas, hooks; executável busca plugins em pasta do usuário.
Referências: ADR-013.

10) CI/CD (GitHub Actions)
- O que faz: automatiza lint, testes, auditoria, build e release.
- Por que importa: qualidade contínua e releases consistentes.
- Como funciona: matrix por SO; artefatos publicados por tag de versão SemVer.
Referências: ADR-009, ADR-015.

# User Experience
Personas principais e fluxos-chave.

Personas:
- Usuário de produtividade: quer iniciar/pausar/retomar rapidamente, com mínima distração.
- Usuário avançado: customiza timers, notificações, idioma; utiliza plugins.
- Desenvolvedor de plugins: estende o app com telas e ações, respeitando contratos e permissões.

Fluxos principais:
- Controle de ciclo: iniciar → focar → notificação → pausa → repetir; acessível por GUI e tray.
- Notificações: nativas/overlay com botões de ação quando aplicável.
- Configurações: idioma, som, comportamento de overlay/tray.
- Plugins: instalação e ativação (fase futura), respeitando compatibilidade SemVer.

Considerações de UX:
- Operação suave via tray com estados claros (ADR-014).
- Notificações não intrusivas com fallback (ADR-010).
- i18n completa com fallback (ADR-004).
- Offline-first; sem bloqueios por rede.
</context>

<PRD>
# Technical Architecture
Componentes, dados, APIs e infraestrutura.

Componentes (visão Hexagonal):
- Core (domínio/casos de uso): regras de timer, ciclo Pomodoro e estados.
- Adapters: GUI (PySide6), Tray (QSystemTrayIcon), Notificações/Overlay.
- Infrastructure: DB (SQLite), i18n (gettext), update checker, logging.
- PluginManager + Plugins: definição de hookspecs e execução de hookimpls.

Data models (alto nível):
- Session: id, tipo (foco/pausa), duração, timestamps, estado.
- Stats: sessões por período, total focado, interrupções.
- Settings: idioma, sons, preferências de overlay/tray.
- PluginMetadata: nome, versão, `compatible_with`, permissões, dependências.

APIs e integrações:
- Hooks públicos (exemplos): `on_app_start`, `on_timer_tick`, `on_cycle_end`, `provide_settings_ui`.
- Update JSON: `version`, `changelog`, `url`, `hash` (ver Appendix).
- Logging: loggers por namespace (`pomodoro.core`, `pomodoro.adapters.gui`, `plugin.<nome>`).

Infraestrutura e distribuição:
- Empacotamento com PyInstaller, incluindo `.mo`, ícones/temas e launcher único.
- Artefatos por SO: `.exe` (Windows), `.AppImage`/`.tar.gz` (Linux), `.dmg` (macOS).
- CI/CD com matrizes por SO; lint (`black`, `ruff`), testes (`pytest`), segurança (`pip-audit`).

Segurança (plugins):
- Validação estática (estrutura, versão mínima da API, contratos).
- Permissões declarativas em `plugin.toml` (filesystem/network/gui).
- Execução no mesmo processo com interfaces controladas e log isolado.
Referências: ADR-011, ADR-015.

# Development Roadmap
Fases e escopo (sem datas):

- Fase 0 — Fundações: layout (ADR-008), logging básico (ADR-012).
- Fase 1 — MVP Timer + GUI + Tray: PySide6 (ADR-005), tray (ADR-014), estados básicos do ciclo.
- Fase 2 — Notificações/Overlay: ADR-010.
- Fase 3 — Persistência e i18n: ADR-003, ADR-004.
- Fase 4 — Plugin API mínima: ADR-002/007, validações (ADR-011), SemVer (ADR-015).
- Fase 5 — Update Checker: ADR-006.
- Fase 6 — Packaging/Distribuição: ADR-013.
- Fase 7 — CI/CD completo: ADR-009.
- Futuro — Loja de plugins, assinatura digital, subprocessos para isolamento avançado (evolução da ADR-011).

# Logical Dependency Chain
Ordem lógica para reduzir risco e maximizar entregas utilizáveis:

1. Layout e logging → 2. Core do timer → 3. GUI → 4. Tray → 5. Notificações/Overlay → 6. Persistência/i18n → 7. PluginManager (mínimo) → 8. Update → 9. Packaging → 10. CI/CD completo.

# Risks and Mitigations
Principais riscos e mitigação:
- Multiplataforma (tray, notificações, PyInstaller): encapsular adapters por SO; testes manuais por plataforma; fallbacks (ADR-010, ADR-013, ADR-014).
- Segurança de plugins: validações pré-load, permissões declarativas, logs isolados; futura assinatura digital (ADR-011).
- Compatibilidade SemVer: bloqueio de plugins incompatíveis e changelog disciplinado (ADR-015).
- Tamanho do binário e antivírus: documentação e assinatura de executáveis quando aplicável (ADR-013).
- UX intrusiva de notificações: configurações de intensidade e silenciamento; overlay opcional (ADR-010).
- Particularidades do macOS (tray/assinatura): ajustes específicos e testes direcionados (ADR-014, ADR-013).

# Appendix
Conteúdo granular canônico para consulta rápida. Manter atualizado junto às ADRs.

## A1. Ambiente e versões
- Linguagem: Python >= 3.12 (ver `context.md`).
- GUI: PySide6 (Qt for Python).
- Plugins: Pluggy.
- DB: SQLite (módulo padrão `sqlite3`).
- i18n: gettext (`.po/.mo`).
- Empacotamento: PyInstaller.
- CI/CD: GitHub Actions (Linux/Windows/macOS).

## A2. Convenções do projeto (ADR-008, ADR-012)
Diretórios principais:
```
pomodoro_app/
  core/                # domínio e casos de uso
  adapters/            # gui/, system_tray/, notifications/, cli/
  infrastructure/      # db/, i18n/, config/, update/
  plugin_manager/
  plugins/
  tests/               # unit/, integration/
  resources/
  docs/                # adrs/
```
Commits semânticos: `feat:`, `fix:`, `refactor:`, `chore:`, `docs:`, `test:`
Logs (arquivos): `app.log`, `events.log`, `plugin_errors.log`
Nomeação de loggers: `pomodoro.core`, `pomodoro.adapters.gui`, `pomodoro.infrastructure.db`, `plugin.<nome>`

## A3. Contratos de Plugin (ADR-002, ADR-007, ADR-011, ADR-015)
Hooks públicos (exemplos e propósito):
- `on_app_start`: inicialização do plugin
- `on_timer_tick`: chamado em cada tick do timer
- `on_cycle_end`: final de ciclo de foco/pausa
- `provide_settings_ui`: fornece UI de configurações do plugin

`plugin.toml` (campos essenciais):
```toml
[plugin]
name = "focus_boost"
version = "1.2.0"
compatible_with = ">=1.0.0,<2.0.0"  # SemVer do app

[access]
filesystem = false
network = false
requires_gui = true
```

Permissões (matriz básica):
- filesystem: true/false (acesso a arquivos locais)
- network: true/false (acesso à rede)
- requires_gui: true/false (exige contexto de GUI)

Regras de compatibilidade (SemVer):
- Plugins devem declarar faixa `compatible_with` e serão validados no load (ADR-015).

## A4. Persistência (ADR-003)
Entidades lógicas e campos essenciais:
- Session: id, tipo, duração, started_at, ended_at, estado
- Stats: períodos agregados, total focado, interrupções
- Settings: pares chave-valor (idioma, overlay, sons)

## A5. Notificações e Overlay (ADR-010)
Backends por SO (exemplos):
- Linux: `notify2`, ou fallback via tray/overlay
- Windows: `win10toast`, ou fallback via tray/overlay
- macOS: API nativa via wrapper, ou overlay Qt
Ordem de tentativa: Nativo → Overlay Qt → Tray/Log

## A6. Update (ADR-006)
Campos esperados no JSON remoto:
- `version` (string SemVer), `changelog` (string), `url` (uri), `hash` (opcional)

Exemplo mínimo:
```json
{
  "version": "1.0.3",
  "changelog": "Fixes and improvements",
  "url": "https://example.com/downloads/pomodoro-1.0.3.exe",
  "hash": "sha256:..."
}
```

## A7. Empacotamento (ADR-013)
Artefatos por SO:
- Windows: `.exe`
- Linux: `.AppImage` ou `.tar.gz`
- macOS: `.dmg`
Inclusões obrigatórias: `.mo`, ícones, temas, launcher, hooks de inclusão do PyInstaller.
Busca de plugins: pasta do usuário (ex.: `~/.pomodoro/plugins/`).

## A8. CI/CD (ADR-009)
Etapas por job:
- Lint: `black`, `ruff`
- Testes: `pytest`
- Segurança: `pip-audit`
- Build: PyInstaller por SO
- Release: artefatos + changelog por tag SemVer

## A9. Mapa de funcionalidades → ADRs
- Arquitetura/Hexagonal: ADR-001, ADR-008
- Plugins/Pluggy: ADR-002, ADR-007, ADR-011, ADR-015
- GUI: ADR-005
- Tray: ADR-014
- Notificações/Overlay: ADR-010
- i18n: ADR-004
- DB: ADR-003
- Logging: ADR-012
- Update: ADR-006
- Packaging: ADR-013
- CI/CD: ADR-009

## A10. Critérios de aceite por fase (resumo)
- MVP: ciclo completo via GUI/Tray; notificação simples; persistência básica; i18n pt-BR/en-US; logs rotacionados; build 1 SO.
- Plugins (beta): hooks documentados; validação e bloqueio por compat; plugin de exemplo.
- Release: builds Win/Linux/macOS; update checker ativo; changelog publicado.

</PRD>
