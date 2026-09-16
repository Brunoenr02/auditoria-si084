# H-005 — Servicio expuesto no registrado en el inventario

## Condición

Durante el reconocimiento de la red autorizada `audit_net`, Nmap identificó el servicio `si084_simplerisk` accesible mediante los puertos TCP 80 y 443.

El inventario de línea base `20_evidencia/E01_baseline/puertos.tsv` no contiene este servicio.

También se identificó `si084_srdb` exponiendo MariaDB en TCP/3306, igualmente ausente de dicha línea base.

## Criterio

ISO/IEC 27001:2022, control A.5.9 — Inventory of information and other associated assets.

## Evidencia

- `20_evidencia/E05_infra/nmap_hosts.txt`
- `20_evidencia/E05_infra/nmap_servicios.nmap`
- `20_evidencia/E05_infra/nmap_servicios.xml`
- `20_evidencia/E01_baseline/puertos.tsv`

## Riesgo

Un servicio no registrado puede quedar fuera de los procesos de asignación de responsable, actualización, monitoreo, evaluación de vulnerabilidades y retiro controlado.

## Recomendación

Actualizar el inventario de activos y servicios, asignar un responsable a cada servicio detectado y establecer un mecanismo periódico de conciliación entre el inventario declarado y la superficie de red observada.
