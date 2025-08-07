# ADR: Sistema de Notificações e Overlay Visual para Ciclos de Pomodoro

**Data:** 07/08/2025<br />
**Status:** Accepted<br />
**Autores:** Responsável Técnico: Pedro H C Schneider (Engenheiro e Arquiteto do Projeto), Consultoria Técnica: ChatGPT (Arquiteto/Engenheiro Sênior DevSecOps)

## Contexto

O app Pomodoro é uma ferramenta de produtividade baseada na técnica de gerenciamento de tempo Pomodoro. Notificações visuais e sonoras são parte **essencial** da experiência do usuário, pois o app deve ser capaz de alertar sobre **início e término de ciclos** de foco e pausa mesmo quando a janela principal estiver minimizada, oculta ou apenas em segundo plano.

O sistema precisa funcionar de forma:

- **Multiplataforma** (Windows, Linux, macOS)
- **Independente da GUI principal**
- **Discreta, mas informativa**
- **Extensível**, permitindo uso por plugins

## Decisão

Adotar um sistema híbrido de notificações, composto por três camadas:

1. **Notificações nativas do sistema operacional**
   - Usando bibliotecas como `plyer`, `notify2`, `win10toast`, dependendo do SO
   - Para mensagens rápidas e integração com centro de notificações do SO

2. **Overlay visual leve via PySide6**
   - Exibe cronômetro ou alertas em sobreposição à área de trabalho
   - Pode incluir botões de ação (ex: "Iniciar", "Adiar", "Parar")
   - Visual customizado e responsivo, sem janela padrão do app

3. **Fallbacks estruturados**
   - Se ambos os anteriores falharem: log local, ícone de tray com badge ou tooltip
   - Permite registro de falha e análise futura

Além disso, o sistema será implementado como **serviço desacoplado da GUI**, acessível via **interfaces públicas** para o core e para plugins.

## Alternativas Consideradas

| Alternativa                                                     | Prós                                                   | Contras                                                        |
| --------------------------------------------------------------- | ------------------------------------------------------ | -------------------------------------------------------------- |
| **Notificações nativas (via `plyer`, `notify2`, `win10toast`)** | Simples, já seguem os padrões do SO                    | Requer bibliotecas específicas por SO                          |
| **Overlay personalizado via Qt (PySide6)**                      | Total controle visual, possível incluir timer e botões | Mais trabalho, requer manter janela ativa ou semi-transparente |
| **Notificações sonoras apenas**                                 | Extremamente simples                                   | Acessibilidade limitada, não informativas isoladamente         |
| **Sistema de eventos com fallback (GUI + tray + log)**          | Flexível, desacoplado da GUI                           | Mais complexo de orquestrar                                    |

## Justificativa

A combinação entre notificações nativas + overlay + fallback fornece:

- **Maior cobertura de casos de uso**
- **Experiência mais rica e acessível**
- **Facilidade de integração com plugins e configurações personalizadas**
- Possibilidade de tornar o sistema **opt-in ou configurável** para usuários avançados

É uma abordagem **equilibrada entre robustez, personalização e simplicidade**, mantendo o app leve e responsivo.

## Consequências

### Positivas:
- O app poderá notificar o usuário **mesmo minimizado ou sem janela visível**
- O sistema é **extensível e configurável**, permitindo plugins registrarem notificações
- Maior controle da experiência do usuário
- Compatível com modo offline, multiplataforma e system tray

### Negativas:
- Integração com bibliotecas de notificação pode variar entre sistemas operacionais
- Overlay exige atenção à performance e renderização em segundo plano
- Requer tratamento de falhas para evitar múltiplos alertas simultâneos ou redundantes

## Reversibilidade

**Sim.**

A estrutura será modular e desacoplada:

- O overlay pode ser desabilitado sem impactar o restante do app
- O backend de notificações nativas pode ser trocado por outro sistema (ex: integração com lib OS-specific)
- O uso de notificações pode ser movido para plugins ou configurado via opções do usuário

Essa abordagem garante **manutenção e evolução seguras** no futuro.

## Referências

- [Plyer – Platform-independent API to access features commonly found on various platforms](https://plyer.readthedocs.io/en/latest/)
- [notify2 – Python interface to Linux notifications](https://pypi.org/project/notify2/)
- [win10toast – Python library to create toast notifications on Windows 10](https://pypi.org/project/win10toast/)
- [Qt QML Overlays and Transparency](https://doc.qt.io/qt-6/qml-qtquick-window-window.html#opacity-prop)
- [Best Practices for Cross-Platform Desktop Notifications](https://developer.mozilla.org/en-US/docs/Web/API/notification)
