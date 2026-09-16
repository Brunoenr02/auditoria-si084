# PT05-B — Contraste de inventario declarado vs. superficie real

| Servicio hallado por Nmap | Puerto | Versión | ¿Figura en inventario declarado? | ¿Tiene dueño identificado? | ¿Está en alcance SGSI? | Observación |
|---|---:|---|---|---|---|---|
| si084_dvwa / HTTP | 80 | Apache 2.4.25 (Debian) | Sí | Sí | Sí | Coincide con inventario |
| si084_srdb / MySQL | 3306 | MariaDB 11.8.9 | No | No consta | No consta | Servicio hallado no registrado en E01 |
| si084_juiceshop | 3000 | Servicio web detectado en puerto 3000 | Sí | Sí | Sí | Coincide con inventario |
| si084_wpdb / MySQL | 3306 | MariaDB 11.8.9 | Sí | Sí | Sí | Coincide con inventario |
| si084_db / PostgreSQL | 5432 | PostgreSQL 9.6.0 o posterior | Sí | Sí | Sí | Coincide con inventario |
| si084_portal / HTTP | 80 | Apache 2.4.68 (Debian) | Sí | Sí | Sí | Coincide con inventario |
| si084_simplerisk / HTTP-HTTPS | 80,443 | Apache httpd | No | No consta | No consta | Servicio hallado no registrado en E01 |

## Resultado

El contraste evidencia que la superficie real expuesta contiene servicios que no figuraban en el inventario declarado usado como línea base. En particular, `si084_simplerisk` expone HTTP/HTTPS y `si084_srdb` expone MariaDB/3306 sin aparecer en `E01_baseline/puertos.tsv`.

Criterio: ISO/IEC 27001:2022 A.5.9 — Inventory of information and other associated assets.
