# ADR: Escolha do Framework de GUI – PySide6 (Qt for Python)

**Data:** 07/08/2025<br />
**Status:** Accepted<br />
**Autores:** Responsável Técnico: Pedro H C Schneider (Engenheiro e Arquiteto do Projeto), Consultoria Técnica: ChatGPT (Arquiteto/Engenheiro Sênior DevSecOps)

## Contexto

O aplicativo Pomodoro será uma aplicação desktop com foco em produtividade, desenvolvido em Python, multiplataforma (Linux, Windows e macOS), com interface gráfica interativa e suporte a system tray, notificações, internacionalização e extensões via plugins.

A construção da interface gráfica (GUI) será uma das primeiras entregas do MVP, e a decisão sobre o framework a ser utilizado afeta profundamente:

- A estrutura visual do projeto
- Os eventos de usuário e a arquitetura de componentes
- A integração com system tray e notificações
- A estratégia de internacionalização (i18n)
- A extensibilidade visual via plugins

## Decisão

O framework gráfico escolhido é o **PySide6** (Qt for Python), uma API moderna e poderosa baseada no framework Qt 6 com licença LGPL.

- Permite criação de GUIs nativas e modernas
- Possui ampla gama de componentes prontos e bem documentados
- Suporta system tray, notificações, temas, animações e gráficos
- Compatível com sistemas de internacionalização como QtLinguist e gettext
- Multiplataforma com excelente desempenho

## Alternativas Consideradas

| Framework          | Prós                                                            | Contras                                                            |
| ------------------ | --------------------------------------------------------------- | ------------------------------------------------------------------ |
| **Tkinter**        | Embutido no Python, fácil de usar                               | Interface desatualizada, baixa flexibilidade estética              |
| **PyQt / PySide6** | GUI moderna, rica, madura, suporte nativo a i18n                | PyQt possui licença GPL; PySide6 (escolhida) tem licença LGPL      |
| **Toga (BeeWare)** | 100% Python, multiplataforma, moderno em proposta               | Projeto ainda imaturo, estabilidade e documentação limitadas       |
| **Kivy**           | Visual moderno, bom para interfaces com toque                   | Interface não nativa, não combina com UX de apps desktop           |
| **Dear PyGui**     | Alta performance, ideal para visualizações técnicas             | Pouco adequado para interface clássica de produtividade             |

## Justificativa

**PySide6** foi escolhido por:

- Ser o **equilíbrio ideal entre robustez, performance e estética**
- Ter **licença mais permissiva (LGPL)**, evitando restrições do PyQt (GPL)
- Oferecer **amplo suporte nativo a internacionalização**, system tray e recursos visuais modernos
- Ser **altamente extensível**, o que permitirá plugins com componentes visuais customizados
- Ter **documentação extensa e comunidade ativa**, acelerando o desenvolvimento

## Consequências

### Positivas:
- Interface moderna e nativa em todas as plataformas
- Acesso a recursos avançados como gráficos, temas e overlays
- Sistema de internacionalização completo e estável
- Componentes visuais prontos para GUI responsiva
- Excelente suporte à integração com plugins visuais

### Negativas:
- Dependência do framework Qt, aumentando o tamanho final da aplicação
- Requer curva de aprendizado mais elevada em relação a alternativas como Tkinter
- Necessita empacotamento cuidadoso com ferramentas como PyInstaller para garantir compatibilidade entre sistemas

## Reversibilidade

**Tecnicamente possível, mas com alto custo.**

Trocar o framework gráfico exigiria reescrever todas as interfaces visuais, incluindo:

- Componentes principais da interface
- Integrações com tray, eventos e animações
- Plugins com GUI própria

Portanto, essa decisão deve ser considerada **estável e estratégica para o médio e longo prazo**.

## Referências

- [PySide6 Documentation (Qt for Python)](https://doc.qt.io/qtforpython/)
- [Comparison: PySide6 vs PyQt](https://wiki.qt.io/PySide_vs_PyQt)
- [Qt Internationalization with QtLinguist](https://doc.qt.io/qt-6/linguist-translators.html)
- [PyInstaller – Packaging PySide6 Apps](https://pyinstaller.org/en/stable/usage.html#support-for-pyside6)