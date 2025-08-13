### Logging e Observabilidade

Use `setup_logging()` antes de inicializar a aplicação para criar handlers rotativos e capturar warnings.

Namespaces sugeridos:
- `pomodoro.core`
- `pomodoro.adapters.gui`, `pomodoro.adapters.system_tray`, `pomodoro.adapters.notifications`, `pomodoro.adapters.cli`
- `pomodoro.infrastructure.db`, `.i18n`, `.config`, `.update`
- `plugin.<plugin_name>`

Arquivos e roteamento:
- `app.log` recebe logs do namespace `pomodoro` (e pais via propagação)
- `events.log` recebe logs de `pomodoro.core`
- `plugin_errors.log` recebe logs de `plugin.*` (sem propagação)

Exemplo de uso:

```python
from pomodoro_app.infrastructure.logging import setup_logging, get_logger

def main():
    setup_logging()
    log = get_logger("pomodoro.core")
    log.info("App iniciado")

if __name__ == "__main__":
    main()
```

Override de nível via ambiente (dev local):
```bash
export POMODORO_LOG_LEVEL=DEBUG
```

