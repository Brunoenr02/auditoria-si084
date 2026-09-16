# PT05-C — Acta de prueba de restauración

| Campo | Valor |
|---|---|
| Sistema restaurado | Base de datos ERP (`si084_db`) |
| Fecha y hora de la prueba (UTC) | 2026-09-16 |
| RTO declarado por la organización | No declarado |
| Tiempo real medido | Ver `20_evidencia/E05_infra/tiempo_restauracion.txt` |
| RPO declarado / punto de restauración obtenido | Último snapshot disponible en restic |
| Verificación de integridad (hash) | Coincide |
| Excepciones observadas | Se corrigió conversión de rutas de Git Bash antes de la restauración válida |
| Conclusión sobre la eficacia operativa del control | La restauración fue ejecutada correctamente, la integridad fue verificada mediante SHA-256 y `restic check --read-data` no reportó errores. |
