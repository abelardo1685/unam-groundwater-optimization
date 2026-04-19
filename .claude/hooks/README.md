# Hooks

Scripts shell que Claude Code ejecuta automáticamente en respuesta a eventos.
Se configuran en `settings.json` bajo la clave `hooks`.

## Hooks útiles para este proyecto

| Evento | Script | Propósito |
|---|---|---|
| `PostToolUse(Write)` | `format_python.sh` | Auto-formatea .py con black tras cada escritura |
| `PostToolUse(Bash)` | `log_command.sh` | Registra comandos ejecutados en sesión |
| `Stop` | `remind_git.sh` | Recuerda hacer commit al terminar sesión |

## Ejemplo de configuración en settings.json

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [{ "type": "command", "command": ".claude/hooks/format_python.sh" }]
      }
    ]
  }
}
```
