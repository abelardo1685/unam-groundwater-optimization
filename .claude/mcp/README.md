# MCP — Model Context Protocol

Carpeta reservada para servidores MCP que extiendan las capacidades de Claude en este proyecto.

## Servidores candidatos a integrar

| Servidor | Caso de uso en el curso |
|---|---|
| `mcp-filesystem` | Acceso estructurado a `literature/` y `docs/` |
| `mcp-jupyter` | Ejecutar y leer notebooks desde Claude |
| `mcp-python` | REPL Python persistente para debugging de prácticas |
| `mcp-google-drive` | Sincronizar slides y material con Drive para compartir con estudiantes |

## Configuración

Cuando instales un servidor MCP, agrégalo a `.claude/settings.json` bajo la clave `mcpServers`.

```json
{
  "mcpServers": {
    "nombre-servidor": {
      "command": "npx",
      "args": ["-y", "@nombre/mcp-servidor"],
      "env": {}
    }
  }
}
```

## Próximos pasos sugeridos
1. Instalar `mcp-filesystem` para que los agentes naveguen `literature/` directamente.
2. Explorar `mcp-jupyter` para conectar notebooks con el flujo de agentes.
