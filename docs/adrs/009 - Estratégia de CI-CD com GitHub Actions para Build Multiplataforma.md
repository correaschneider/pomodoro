# ADR: Estratégia de CI/CD com GitHub Actions para Build Multiplataforma

**Data:** 07/08/2025<br />
**Status:** Accepted<br />
**Autores:** Responsável Técnico: Pedro H C Schneider (Engenheiro e Arquiteto do Projeto), Consultoria Técnica: ChatGPT (Arquiteto/Engenheiro Sênior DevSecOps)

## Contexto

O app Pomodoro será um aplicativo desktop escrito em Python, com interface gráfica (PySide6), suporte a plugins, internacionalização, system tray e empacotamento standalone para **Windows, Linux e macOS**. O projeto será hospedado no GitHub.

A adoção de um fluxo de **integração contínua (CI)** e **entrega contínua (CD)** desde o início é essencial para:

- Validar a qualidade do código (lint, testes, segurança)
- Empacotar builds multiplataforma automaticamente
- Gerar artefatos prontos para distribuição (AppImage, .exe, .dmg)
- Apoiar o controle de versão, changelog e releases automatizados
- Preparar o projeto para suporte a uma loja de plugins futura

## Decisão

Adotar o **GitHub Actions** como plataforma oficial de CI/CD, com definição de workflows YAML que rodem em diferentes runners:

- **Linux (ubuntu-latest)**
- **Windows (windows-latest)**
- **macOS (macos-latest)**

Cada workflow incluirá etapas para:

1. **Linting e formatação** com `black` e `ruff`
2. **Execução de testes** com `pytest`
3. **Análise de segurança** com `pip-audit`
4. **Empacotamento** com `PyInstaller` (customizado por SO)
5. **Geração de changelog** automático (ex: `github-changelog-generator` ou script customizado)
6. **Publicação de artefatos e releases** por tag (versão semântica)

## Alternativas Consideradas

| Ferramenta/Fluxo                  | Prós                                                 | Contras                                     |
| --------------------------------- | ---------------------------------------------------- | ------------------------------------------- |
| **GitHub Actions**                | Nativo, gratuito para OSS, suporte a Linux/macOS/Win | Requer configuração e múltiplas jobs por SO |
| **GitLab CI/CD**                  | Poderoso, self-hosting possível                      | Menos popular em projetos open-source       |
| **CircleCI / TravisCI / Azure**   | Suporte corporativo e integração com PyPI            | Planos gratuitos limitados                  |
| **CI Local (Makefile + scripts)** | Útil para devs, mas não cobre builds automáticos     | Sem validação automática de PRs             |

## Justificativa

**GitHub Actions** foi escolhido por:

- Ser nativo do GitHub, onde o código-fonte será mantido
- Oferecer **suporte gratuito generoso para repositórios públicos**
- Permitir **execução paralela em múltiplas plataformas**
- Facilitar automação de **PRs, releases, changelog e auditorias**
- Ter **ecossistema maduro de ações reutilizáveis**, reduzindo boilerplate

## Consequências

### Positivas:
- Fluxo automatizado e auditável de releases
- Builds multiplataforma gerados com consistência
- PRs validados automaticamente (lint, testes, segurança)
- Time-to-release reduzido drasticamente
- Suporte futuro a builds de plugins de terceiros com a mesma estrutura

### Negativas:
- Build para macOS pode ter **filas demoradas** (limite de minutos gratuito)
- PyInstaller requer ajustes específicos por SO
- Workflow pode crescer em complexidade conforme o projeto escalar

## Reversibilidade

**Sim.**

Toda a estrutura será definida em arquivos `.github/workflows/*.yml`, isolados do core do app. Isso permite:

- Migrar para outra plataforma (GitLab CI/CD, Travis, etc.)
- Adotar self-hosted runners em caso de limitação do GitHub
- Reaproveitar os mesmos scripts de lint, teste e build

## Referências

- [GitHub Actions Documentation](https://docs.github.com/actions)
- [PyInstaller – Building on Multiple Platforms](https://pyinstaller.org/en/stable/usage.html#cross-compiling)
- [pip-audit – Auditing Python environments for known vulnerabilities](https://pypi.org/project/pip-audit/)
- [Semantic Versioning](https://semver.org/)
- [Release Drafter GitHub Action](https://github.com/release-drafter/release-drafter)
