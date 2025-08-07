# ADR: Estratégia de Logging e Observabilidade

**Data:** 07/08/2025<br />
**Status:** Accepted<br />
**Autores:** Responsável Técnico: Pedro H C Schneider (Engenheiro e Arquiteto do Projeto), Consultoria Técnica: ChatGPT (Arquiteto/Engenheiro Sênior DevSecOps)

## Contexto

O app Pomodoro será uma aplicação desktop multiplataforma, escrita em Python, com interface gráfica, suporte a plugins externos, notificações, system tray, internacionalização e empacotamento standalone.

Dado seu **modelo modular e extensível**, o sistema precisa ser capaz de:

- Registrar **eventos de execução e uso**
- Detectar e **logar falhas**, inclusive em plugins externos
- Operar **offline**
- **Ajudar no suporte ao usuário** (ex: permitir exportar logs)
- Servir como base para futura análise de **usabilidade e comportamento**

A observabilidade também é uma **camada de segurança e rastreabilidade**, especialmente para plugins que rodam em sandbox parcial.

## Decisão

Utilizar a biblioteca padrão do Python, `logging`, com uma estratégia definida para garantir visibilidade e rastreabilidade em tempo de execução:

1. **Logger centralizado**, com nomeação por módulo:
   - `pomodoro.core`, `pomodoro.adapters.gui`, `pomodoro.infrastructure.db`, `pomodoro.plugins.plugin_x`, etc.

2. **Rotação automática de arquivos** com `RotatingFileHandler`:
   - Arquivos como `app.log`, `events.log`, `plugin_errors.log`
   - Limite de tamanho configurado, com retenção de X arquivos

3. **Separação de handlers por contexto**:
   - Um handler para cada tipo de log (geral, eventos, erros de plugin)
   - Possibilidade de direcionar logs críticos para `stdout`, tray ou GUI

4. **Uso padronizado dos níveis de log**:
   - `DEBUG`: eventos internos para desenvolvimento
   - `INFO`: uso esperado e transições normais (ex: "Ciclo iniciado")
   - `WARNING`: comportamentos incomuns, mas não fatais
   - `ERROR`: falhas durante execução de ciclos ou plugins
   - `CRITICAL`: falhas que comprometem a integridade do sistema

5. **Plugins têm logger isolado por nome**, prefixado com `plugin.<nome>` e logam em `plugin_errors.log`

6. **Integração futura com Sentry ou outro sistema externo** será possível sem refatoração, via handlers adicionais

## Alternativas Consideradas

| Alternativa                              | Prós                                                | Contras                                              |
| ---------------------------------------- | --------------------------------------------------- | ---------------------------------------------------- |
| **Logging com a lib padrão (`logging`)** | Integrada, configurável, suporta múltiplos handlers | Requer configuração manual para rotacionar arquivos  |
| **Uso de log externo (ex: Sentry)**      | Excelente para erros e relatórios                   | Requer internet, fere privacidade offline            |
| **Sistema de eventos por arquivo JSON**  | Fácil de parsear/analisar                           | Menos flexível que o `logging` para níveis e formato |
| **Logs via print e console**             | Simples, útil em CLI                                | Inútil em apps GUI e impossível de manter            |

## Justificativa

A escolha por `logging` padrão se baseia em:

- Ser **robusta, estável e embutida** no Python
- Permitir rotação, múltiplos arquivos e direcionamento
- Não depender de internet (offline-friendly)
- Facilmente extensível para integrações futuras (ex: Sentry, Loki, arquivos JSON)
- Compatível com a arquitetura modular do app

## Consequências

### Positivas:
- Suporte a **diagnóstico completo do sistema**, com histórico local
- Logs podem ser usados para suporte ao usuário e relatórios de bugs
- Ajuda a rastrear falhas em plugins e partes críticas do sistema
- Estrutura de log padronizada facilita automação e análise
- Preparação para futura observabilidade externa ou envio voluntário de logs

### Negativas:
- Requer configuração de limpeza/rotação para evitar acúmulo
- A eficácia depende do uso correto pelos desenvolvedores e plugins
- Plugins precisam seguir convenção de logging para manter rastreabilidade
- Nenhum alerta em tempo real (a não ser que seja implementado em overlay ou tray)

## Reversibilidade

**Sim.**

A estrutura do `logging` permite:

- Substituir os handlers por saída para JSON, banco local ou API
- Integrar com serviços externos (Sentry, Loki, Grafana) sem alterar o código principal
- Redirecionar logs para outro sistema via `logging.Handler` customizado

## Referências

- [Python Logging — official documentation](https://docs.python.org/3/library/logging.html)
- [RotatingFileHandler](https://docs.python.org/3/library/logging.handlers.html#rotatingfilehandler)
- [Sentry for Python](https://docs.sentry.io/platforms/python/)
- [OWASP Logging Best Practices](https://owasp.org/www-project-cheat-sheets/cheatsheets/Logging_Cheat_Sheet.html)
