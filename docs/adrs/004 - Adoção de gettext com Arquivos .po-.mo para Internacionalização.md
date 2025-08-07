# ADR: Adoção de gettext com Arquivos .po/.mo para Internacionalização

**Data:** 07/08/2025<br />
**Status:** Accepted<br />
**Autores:** Responsável Técnico: Pedro H C Schneider (Engenheiro e Arquiteto do Projeto), Consultoria Técnica: ChatGPT (Arquiteto/Engenheiro Sênior DevSecOps)

## Contexto

O app Pomodoro será um aplicativo desktop multiplataforma (Linux, Windows, macOS), com interface gráfica e suporte nativo a plugins. Um dos requisitos principais do sistema é a **internacionalização desde o início do projeto**, permitindo suporte a múltiplos idiomas de forma organizada, extensível e compatível com ambientes offline.

A estratégia escolhida precisa:

- Ser compatível com aplicações desktop em Python
- Suportar pluralização, fallback automático e contexto
- Permitir contribuição externa na tradução (ex: comunidade, equipe de tradução)
- Suportar plugins que tragam seus próprios arquivos de tradução
- Ser compatível com ferramentas de empacotamento (como PyInstaller)

## Decisão

A estratégia de internacionalização será implementada com **`gettext`**, utilizando arquivos `.po` (editáveis) e `.mo` (compilados).

- O código-fonte usará `_()` ou `gettext()` para marcar strings traduzíveis
- Os arquivos `.po` serão organizados por idioma e domínio (ex: `locales/pt_BR/LC_MESSAGES/app.po`)
- A compilação para `.mo` ocorrerá no processo de build
- O sistema terá fallback automático para o idioma padrão
- Plugins poderão fornecer seus próprios arquivos `.mo` e registrá-los dinamicamente

## Alternativas Consideradas

| Alternativa                                         | Prós                                                                         | Contras                                                  |
| --------------------------------------------------- | ---------------------------------------------------------------------------- | -------------------------------------------------------- |
| **gettext (.po/.mo)**                               | Padrão internacional, suportado nativamente no Python, usado em apps desktop | Requer ferramentas específicas para editar arquivos      |
| **Arquivos JSON por idioma**                        | Fácil de editar manualmente e entender                                       | Sem suporte nativo para pluralização e contexto          |
| **Sistema customizado (ex: dicionário global)**     | Flexível                                                                     | Baixa escalabilidade e difícil manutenção                |
| **Bibliotecas externas (ex: Babel, polib, PyI18n)** | Algumas têm integração com web/PyQt                                          | Mais dependências, possíveis limitações para desktop GUI |

## Justificativa

O `gettext` foi escolhido por:

- Ser **compatível com o Python nativamente** via módulo `gettext`
- Oferecer **suporte robusto a pluralização, contexto e fallback**
- Ser **padrão em aplicações desktop internacionais**
- Facilitar a **edição colaborativa** com ferramentas como Poedit, Weblate ou Transifex
- Permitir que **plugins tenham seu próprio dicionário**, mantendo a modularidade

## Consequências

### Positivas:
- Traduções organizadas, padronizadas e extensíveis
- Manutenção simplificada com uso de ferramentas de mercado
- Fallback automático para idioma padrão caso a tradução esteja ausente
- Plugins com sistema de tradução independente e registrável

### Negativas:
- Necessário compilar `.po` para `.mo` no build (etapa extra)
- Exige familiaridade com ferramentas de tradução para contribuições manuais
- Leve sobrecarga no empacotamento com múltiplos arquivos `.mo`

## Reversibilidade

**Sim, com esforço moderado.**

Caso seja necessário mudar de estratégia (ex: para arquivos JSON ou bibliotecas customizadas), seria necessário:

- Substituir chamadas a `gettext()` por uma nova API de internacionalização
- Reestruturar os arquivos de tradução
- Adaptar os plugins que usam o padrão atual

Como os textos estarão externalizados e organizados por domínio e idioma, a migração pode ser automatizada em boa parte.

## Referências

- [Python `gettext` Module](https://docs.python.org/3/library/gettext.html)
- [GNU gettext utilities](https://www.gnu.org/software/gettext/)
- [Poedit – Editor de Traduções .po](https://poedit.net/)
- [Weblate – Plataforma de Tradução Colaborativa](https://weblate.org/)
- [PyInstaller – FAQ: Localizing Applications](https://pyinstaller.org/en/stable/usage.html#localizing-your-application)
