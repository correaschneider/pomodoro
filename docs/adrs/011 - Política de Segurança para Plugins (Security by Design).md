# ADR: Política de Segurança para Plugins (Security by Design)

**Data:** 07/08/2025<br />
**Status:** Accepted<br />
**Autores:** Responsável Técnico: Pedro H C Schneider (Engenheiro e Arquiteto do Projeto), Consultoria Técnica: ChatGPT (Arquiteto/Engenheiro Sênior DevSecOps)

## Contexto

O app Pomodoro será extensível por meio de **plugins externos**, que poderão adicionar telas, configurações, comportamentos e integrações. Os plugins serão mantidos em repositórios separados e poderão ser desenvolvidos por terceiros, inclusive com suporte futuro a uma **loja de plugins**.

Permitir execução de código externo dentro do processo principal impõe **riscos significativos** à estabilidade, integridade e segurança do sistema. Por isso, é necessário definir uma **política clara de segurança para plugins**, mesmo no MVP, seguindo o princípio de **security by design** desde o início da arquitetura modular.

## Decisão

Adotar uma **estratégia híbrida de segurança para plugins**, combinando:

1. **Validação estática antes do carregamento**
   - Estrutura obrigatória (`__init__.py`, `plugin.toml`, `main.py`, etc.)
   - Verificação de versão mínima da API
   - Tipos e contratos implementados (ex: via `pluggy.PluginValidationError`)

2. **Permissões declarativas no `plugin.toml`**
   - Campos como: `access.filesystem = false`, `access.network = false`, `requires.gui = true`, etc.
   - Atributos utilizados para **limitar acesso e avisar o usuário** antes da ativação

3. **Execução no mesmo processo**, mas:
   - **Com escopo controlado por interfaces**
   - **Sem acesso direto ao core** sem passar pelas portas definidas (Hexagonal)
   - **Sandbox parcial por abstração e isolamento por hook**

4. **Logs de erro e exceções isolados por plugin**
   - Qualquer erro causado por um plugin não afeta os demais nem o core

5. **Planejamento para suporte a assinaturas digitais**
   - Plugins distribuídos por terceiros poderão, futuramente, ser **assinados digitalmente**
   - Infraestrutura de chave pública/privada será avaliada para versão 2

## Alternativas Consideradas

| Alternativa                                    | Prós                                  | Contras                                                 |
| ---------------------------------------------- | ------------------------------------- | ------------------------------------------------------- |
| **Execução direta de código Python do plugin** | Simples, direto                       | Alta exposição a riscos de código malicioso ou instável |
| **Plugins declarando permissões em metadata**  | Controlável, permite análise estática | Exige enforcement no carregador                         |
| **Plugins executados em subprocesso isolado**  | Segurança máxima, crash isolado       | Complexo de implementar no início                       |
| **Assinatura digital de plugins**              | Garante integridade e origem          | Requer infraestrutura de chaves e distribuição          |
| **Lista de permissões e validações locais**    | Médio controle, fácil de implementar  | Pode ser burlável se mal projetado                      |

## Justificativa

A abordagem híbrida escolhida oferece o melhor equilíbrio entre:

- **Viabilidade no MVP** (baixo custo de implementação)
- **Controle sobre o que o plugin pode ou não fazer**
- **Preparação para evolução futura**, com isolamento por processo ou assinatura

Manter os plugins no **mesmo processo**, mas com **validação antecipada**, **contrato formal** e **controle por interfaces**, permite desenvolver uma base segura e auditável para extensões do sistema, sem atrasar a entrega.

## Consequências

### Positivas:
- Reduz riscos de execução arbitrária e falhas no núcleo
- Base preparada para future-proof (assinatura e subprocessos)
- Plugins podem ser avaliados antes da ativação
- Estabilidade do app mesmo com plugins problemáticos
- Interface amigável para desenvolvedores seguirem um padrão seguro

### Negativas:
- A execução no mesmo processo ainda representa risco limitado
- Requer que os contratos e interfaces sejam bem definidos e testados
- Erros de enforcement podem ser explorados por plugins mal-intencionados
- A segurança dependerá da qualidade do `PluginManager` e da validação dos metadados

## Reversibilidade

**Sim.**

Desde que os **plugins continuem implementando contratos e não acessem diretamente componentes internos**, será possível no futuro:

- Mover a execução para **subprocessos isolados**
- Introduzir **assinatura digital obrigatória**
- Adotar **controle granular de permissões em tempo de execução**

Essas mudanças exigirão ajustes no `PluginManager`, mas **não invalidarão os plugins existentes** se as interfaces forem respeitadas.

## Referências

- [OWASP – Secure Design Principles](https://owasp.org/www-project-top-ten/2017/A10_2017-Insufficient_Logging%26Monitoring)
- [Python Pluggy – Hook and Plugin System](https://pluggy.readthedocs.io/)
- [PEP 621 – pyproject.toml plugin metadata](https://peps.python.org/pep-0621/)
- [Securing Plugin Architectures (Mozilla)](https://wiki.mozilla.org/Plugins/Security)
