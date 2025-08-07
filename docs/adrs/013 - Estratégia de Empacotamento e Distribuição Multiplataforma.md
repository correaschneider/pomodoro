# ADR: Estratégia de Empacotamento e Distribuição Multiplataforma

**Data:** 07/08/2025<br />
**Status:** Accepted<br />
**Autores:** Responsável Técnico: Pedro H C Schneider (Engenheiro e Arquiteto do Projeto), Consultoria Técnica: ChatGPT (Arquiteto/Engenheiro Sênior DevSecOps)

## Contexto

O app Pomodoro será um aplicativo desktop escrito em Python com GUI (PySide6), plugins externos, notificações, overlay visual, suporte a system tray, internacionalização, e execução 100% offline. Desde o início, o projeto tem como objetivo ser **multiplataforma** (Windows, Linux, macOS).

É essencial que a distribuição seja:

- **Simples para o usuário final**
- **Segura e íntegra**
- **Offline-ready**
- **Compatível com o pipeline de CI/CD**
- **Independente de ambientes como pip, venv, conda**

O método de empacotamento impacta diretamente a forma como o sistema lida com paths, configurações, arquivos de tradução, plugins e atualizações futuras.

## Decisão

Adotar o **PyInstaller** como empacotador oficial para o MVP, gerando artefatos finais específicos por sistema operacional:

- `.exe` para **Windows**
- `.AppImage` ou `.tar.gz` para **Linux**
- `.dmg` para **macOS**

Com as seguintes diretrizes:

- Incluir **todos os assets necessários** (ex: arquivos `.mo`, ícones, temas)
- Incluir um **launcher unificado** (`main.py`) como ponto de entrada
- Utilizar **hooks personalizados** para garantir inclusão de dependências não detectadas automaticamente
- Definir **ícone, nome do app, splash screen e metadata** em cada build
- Plugins permanecerão **fora do binário**, mas o executável saberá buscar na pasta `~/.pomodoro/plugins/` ou equivalente por SO

## Alternativas Consideradas

| Alternativa                                            | Prós                                                  | Contras                                                |
| ------------------------------------------------------ | ----------------------------------------------------- | ------------------------------------------------------ |
| **PyInstaller**                                        | Empacotamento único, multiplataforma, fácil de usar   | Gera binários grandes, pode precisar de ajustes por SO |
| **cx_Freeze**                                          | Similar ao PyInstaller, também robusto                | Menos documentado e ativo                              |
| **Nuitka**                                             | Compila Python para binário real (mais seguro/rápido) | Mais complexo e difícil de depurar                     |
| **Conda + zip/manual**                                 | Bom para ambientes controlados                        | Muito técnico para usuários finais                     |
| **Repositórios de pacotes do SO (ex: Snap, MSI, DMG)** | Integra com o SO, updates automáticos                 | Complexo de gerenciar para cada plataforma             |

## Justificativa

O **PyInstaller** foi escolhido por:

- Ser **maduro**, amplamente utilizado na comunidade Python
- Suportar empacotamento completo de **apps gráficos multiplataforma**
- Ser **fácil de integrar com CI/CD (GitHub Actions)** para gerar releases automatizados
- Permitir **controle sobre inclusão de arquivos estáticos**, configs e traduções
- Gerar um executável standalone, facilitando o uso por **usuários leigos**

## Consequências

### Positivas:
- Empacotamento multiplataforma padronizado
- Usuário final baixa e executa sem necessidade de Python instalado
- Compatível com CI/CD, GitHub Releases e sistema de verificação de atualização
- Suporte a customizações visuais (ícones, splash, metadata)
- Facilita empacotamento inicial do MVP sem overhead extra

### Negativas:
- Tamanho final dos binários pode variar entre **30MB a 70MB**
- Antivírus no Windows podem gerar **falsos positivos**
- Ajustes por SO podem ser necessários para path de arquivos ou permissões
- Atualização automática precisa ser gerenciada externamente (ex: via sistema de update por JSON)

## Reversibilidade

**Sim.**

O uso do PyInstaller não acopla a aplicação a ele de forma irreversível. Será possível migrar futuramente para:

- **Nuitka**, para builds otimizados e mais seguros
- **cx_Freeze**, para distribuição mais modular
- **Empacotamento nativo** com Snap, MSI, Brew, etc.
- **Containers AppImage com sandboxing e assinatura digital**

Desde que os assets estejam organizados e os paths sejam relativos e configuráveis, a transição pode ser feita com impacto moderado.

## Referências

- [PyInstaller Official Documentation](https://pyinstaller.org/)
- [Best practices with PyInstaller and PySide6](https://github.com/pyinstaller/pyinstaller/issues?q=pyside6)
- [Creating cross-platform desktop apps in Python](https://realpython.com/pyinstaller-python/)
- [GitHub Actions: Building PyInstaller binaries](https://github.com/marketplace/actions/build-using-pyinstaller)
- [AppImage — Linux universal packaging](https://appimage.org/)
- [Signing Windows executables](https://learn.microsoft.com/en-us/windows/win32/seccrypto/code-signing)
