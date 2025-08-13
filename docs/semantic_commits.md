## Conventional Commits (resumo)

- Formato: `type(scope): descrição curta`
- Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`
- Scope: opcional, kebab-case (ex.: `core`, `gui`, `infra-db`)
- Subject: imperativo, sem ponto final, até 72 chars
- Body: opcional (por quê/como), linhas até 72 chars
- Footer: referências, `BREAKING CHANGE: <descrição>` quando aplicável

Exemplos:

```text
feat(task-1.2): adiciona pyproject.toml e entry point

fix(gui): corrige crash ao fechar janela secundária

feat(core)!: muda contrato do TimerService

BREAKING CHANGE: TimerService agora exige timezone explícito
```

