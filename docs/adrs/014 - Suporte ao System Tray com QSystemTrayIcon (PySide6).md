# ADR: Suporte ao System Tray com QSystemTrayIcon (PySide6)

**Data:** 07/08/2025<br />
**Status:** Accepted<br />
**Autores:** Responsável Técnico: Pedro H C Schneider (Engenheiro e Arquiteto do Projeto), Consultoria Técnica: ChatGPT (Arquiteto/Engenheiro Sênior DevSecOps)

## Contexto

O app Pomodoro é uma aplicação desktop multiplataforma com foco em produtividade. Um dos principais requisitos de usabilidade é permitir que o usuário **controle o timer de forma discreta**, mesmo com a janela principal fechada. Esse tipo de comportamento é comum e esperado em apps com **execução contínua e em segundo plano**, como é o caso de temporizadores, organizadores e ferramentas de foco.

A presença de um **ícone no system tray** (bandeja do sistema) oferece uma **interface leve e persistente** para controle de estado, acesso rápido ao menu e notificações visuais.

## Decisão

Adotar o componente **`QSystemTrayIcon` do framework PySide6** (Qt) como solução oficial de system tray do app Pomodoro.

O tray deverá:

- Exibir o **ícone do app** em estado normal
- Permitir **menus contextuais** com ações básicas: iniciar, pausar, interromper ciclo, abrir configurações, sair
- **Refletir o estado atual do ciclo Pomodoro** no tooltip e/ou no ícone
- Ser **desacoplado da GUI principal**, permitindo que o app continue rodando mesmo com a janela fechada
- Estar presente desde o **MVP**

## Alternativas Consideradas

| Alternativa                        | Prós                                       | Contras                                              |
| ---------------------------------- | ------------------------------------------ | ---------------------------------------------------- |
| **pystray**                        | Simples, cross-platform, leve              | Limitado em eventos e integração visual              |
| **QSystemTrayIcon (Qt / PySide6)** | Nativo, rico em eventos e interação visual | Depende do uso do Qt/PySide6 (já adotado no projeto) |
| **tkinter + solução customizada**  | Possível workaround                        | Solução frágil, não multiplataforma                  |
| **Não ter tray e usar só GUI**     | Simples                                    | Vai contra o uso esperado e a experiência do usuário |

## Justificativa

A escolha por `QSystemTrayIcon` se deve ao fato de o projeto já utilizar **PySide6 (Qt)** como framework de interface gráfica, conforme definido na **ADR-005**. Dessa forma:

- Evitamos dependências externas
- Ganhamos integração nativa e rica com os eventos do sistema
- Podemos implementar menus dinâmicos e tooltips personalizados
- Temos suporte multiplataforma sólido com possibilidade de ajustes por SO

## Consequências

### Positivas:
- Permite que o app **continue executando mesmo sem a janela principal**
- Melhora significativamente a **usabilidade** e o fluxo de trabalho
- Oferece **feedback visual contínuo** (ex: tooltip mostrando tempo restante)
- Integrações com outras partes do sistema (notificações, overlay) ficam mais coesas
- Facilita controle via clique direto no ícone (atalhos de produtividade)

### Negativas:
- **Comportamento varia por sistema operacional** (ex: tray no macOS exige configuração específica para ativação completa)
- Pode exigir manutenção de múltiplos ícones (ex: 16x16, 32x32, 64x64) para boa renderização em diferentes sistemas
- Estado da aplicação (ex: se janela foi fechada ou minimizada) precisa ser **sincronizado com o tray**

## Reversibilidade

**Sim, com custo moderado.**

Se o uso do tray se mostrar inviável ou problemático:

- Podemos encapsular sua lógica em uma classe `TrayController`, trocável por uma implementação nula (Null Object)
- O controle pode ser transferido para um menu fixo da GUI principal
- Eventualmente, poderemos migrar para outro backend (ex: `pystray`) com funcionalidades reduzidas

Desde que a interface com o resto do app seja abstraída corretamente, a reversibilidade será possível com impacto mínimo no domínio.

## Referências

- [Qt Documentation – QSystemTrayIcon](https://doc.qt.io/qt-6/qsystemtrayicon.html)
- [PySide6 – QSystemTrayIcon Reference](https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QSystemTrayIcon.html)
- [macOS and Qt – Tray Icon Notes](https://doc.qt.io/qt-6/macos-platform-notes.html)
- [Best practices for system tray interactions](https://ux.stackexchange.com/questions/2720/what-should-be-the-best-behavior-of-an-application-in-the-system-tray)
