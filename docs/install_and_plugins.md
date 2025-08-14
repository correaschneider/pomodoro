# Instalação, Artefatos e Plugins

Este documento descreve como instalar e executar os artefatos gerados no CI/CD, e como usar o diretório de plugins em runtime.

## Artefatos de Build (CI/CD)

- O workflow em `.github/workflows/ci.yml` cria artefatos por sistema operacional e os publica como artefatos do job e em Releases quando houver tags que iniciam com `v`.
- Nome do artefato: `dist-${OS}` contendo a pasta `dist/` do PyInstaller.
- Layout típico (Linux):
  - `dist/pomodoro_app/pomodoro_app` (binário one-folder)

## Instalação e Execução (Artefatos)

- Baixe o artefato correspondente ao seu sistema operacional no Release.
- Extraia o conteúdo e execute o binário:
  - Linux: `./dist/pomodoro_app/pomodoro_app --smoke`
  - Windows/macOS: execute o binário correspondente dentro de `dist/` (nome pode variar conforme o sistema).
- Observação: no Linux, pode ser necessário `chmod +x` no binário.

## Diretório de Plugins (Runtime)

O aplicativo cria (se necessário) e utiliza um diretório de plugins em runtime. O caminho segue o padrão do sistema via `platformdirs.user_data_dir("pomodoro_app")/plugins`:

- Linux: `~/.local/share/pomodoro_app/plugins`
- macOS: `~/Library/Application Support/pomodoro_app/plugins`
- Windows: `%LOCALAPPDATA%\\pomodoro_app\\plugins`

A função `ensure_plugins_base_dir()` garante a criação do diretório quando chamada.

## Estrutura de um Plugin

Cada plugin deve residir em uma subpasta dentro de `.../plugins` com, no mínimo, o arquivo `main.py`:

```
<plugins_dir>/meu_plugin/
  ├─ main.py            # obrigatório
  └─ plugin.toml        # opcional (metadados)
```

Regras básicas:
- `main.py` é carregado e registrado pelo `PluginManager` via `pluggy`.
- Metadados são lidos de `plugin.toml` quando presente (compatibilidade, nome, permissões). Ver ADR-007/015.
- Plugins que requerem GUI podem ser ignorados quando a GUI não estiver disponível.

## Execução em Modo Smoke

Para verificar rapidamente a execução:

- Via fonte: `PYTHONPATH=$(pwd) python -m pomodoro_app --smoke`
- Via artefato (Linux): `./dist/pomodoro_app/pomodoro_app --smoke`

## Observações de Segurança

- Plugins são carregados do diretório do usuário; instale apenas plugins confiáveis.
- Logs de erros de plugins são emitidos com prefixo `plugin.*`. Consulte os arquivos de log em `~/.local/share/pomodoro_app/logs/` (Linux; varia por SO).
