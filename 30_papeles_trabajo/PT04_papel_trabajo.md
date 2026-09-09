# PT04 · Papel de trabajo — Auditoría de configuración segura

**Curso:** SI-084 · Auditoría de Sistemas  
**Semana:** 04  
**Rama de trabajo:** `s04-taller`  
**Estado:** En ejecución  

> Este papel de trabajo consolida los resultados obtenidos durante el Taller 04. Cada afirmación debe poder rastrearse a un archivo de evidencia. Al cierre, las evidencias se referenciarán mediante URLs sobre la etiqueta `taller-04`.

---

## A. Auditoría del sistema anfitrión con Lynis

### A.1 Evidencia generada

- `20_evidencia/E04_config/lynis-report.dat`
- `20_evidencia/E04_config/lynis-consola.txt`
- `docs/evidencias/S04/salidas/lynis-hardening.txt`
- `docs/evidencias/S04/salidas/lynis-warning-count.txt`
- `docs/evidencias/S04/salidas/lynis-hallazgos.txt`
- `docs/evidencias/S04/salidas/lynis-top3.txt`

### A.2 Resultado

- `hardening_index`: **53/100**
- Entradas `warning[]`: **0**

La ejecución no produjo entradas de tipo `warning[]`. Para no declarar hallazgos inexistentes, se seleccionaron tres `suggestion[]` de mayor impacto de seguridad para su análisis.

### A.3 Tres sugerencias analizadas

| ID Lynis | Resultado | Control ISO/IEC 27001:2022 | Análisis de auditoría |
|---|---|---|---|
| `FIRE-4590` | Configurar un firewall/filtro de paquetes para tráfico entrante y saliente | **A.8.20 Seguridad de redes** | La ausencia de filtrado incrementa la superficie de exposición y puede permitir comunicaciones no autorizadas. |
| `ACCT-9628` | Habilitar `auditd` para recopilar información de auditoría | **A.8.15 Registro de eventos** | Sin registros de auditoría suficientes disminuye la capacidad de rastreo, investigación y atribución de eventos. |
| `FINT-4350` | Instalar una herramienta de integridad de archivos | **A.8.16 Actividades de monitorización** | El monitoreo de integridad permite detectar modificaciones no autorizadas o anómalas sobre archivos críticos. |

### A.4 Observación / limitación

La ejecución se realizó con Docker Desktop sobre Windows. Lynis evaluó el entorno Linux expuesto al contenedor y no constituye una auditoría nativa del sistema operativo Windows anfitrión. Esta limitación se conserva como parte de la trazabilidad de la prueba.

---

## B. Cumplimiento formal con OpenSCAP

### B.1 Evidencia generada

- `20_evidencia/E04_config/oscap-resultados.xml`
- `20_evidencia/E04_config/oscap-reporte.html`
- `docs/evidencias/S04/salidas/oscap-resumen.txt`
- `docs/evidencias/S04/salidas/oscap-fallos.txt`

### B.2 Perfil evaluado

`xccdf_org.ssgproject.content_profile_cis_level1_server`

### B.3 Resultado

| Métrica | Resultado |
|---|---:|
| PASS | **128** |
| FAIL | **3** |
| Total PASS + FAIL | **131** |
| Fallos High | **0** |
| Fallos Medium | **3** |
| Score mostrado por el reporte | **96.6 %** |

La guía esperaba cinco reglas fallidas de severidad alta. La ejecución real produjo únicamente tres fallos y todos fueron de severidad `medium`; no se agregaron resultados inexistentes.

### B.4 Reglas fallidas

| # | Identificador XCCDF completo | Severidad | Título | Referencias declaradas por la guía SCAP | Mapeo ISO propuesto por el auditor |
|---|---|---|---|---|---|
| 1 | `xccdf_org.ssgproject.content_rule_package_pam_pwquality_installed` | Medium | Install pam_pwquality Package | CIS Ubuntu 5.3.1.3; STIG SRG-OS-000480-GPOS-00225 | **A.8.5 Autenticación segura** |
| 2 | `xccdf_org.ssgproject.content_rule_use_pam_wheel_group_for_su` | Medium | Enforce Usage of pam_wheel with Group Parameter for su Authentication | CIS Ubuntu 5.2.7; PCI DSS 2.2.6 / 2.2 | **A.8.2 Derechos de acceso privilegiado** |
| 3 | `xccdf_org.ssgproject.content_rule_permissions_local_var_log` | Medium | Verify permissions of log files | NIST SP 800-53 SI-11(a), SI-11(b), SI-11.1(iii); NIST CSF PR.AC-4, PR.DS-5; CIS Ubuntu 6.2.2.1 | **A.8.15 Registro de eventos** |

> Los controles ISO de esta tabla son un mapeo de auditoría propuesto a partir del contenido de cada regla. Las referencias CIS/NIST/STIG/PCI son las obtenidas del resultado OpenSCAP.

---

## C. CIS Docker Benchmark con Docker Bench for Security

### C.1 Evidencia generada

- `20_evidencia/E04_config/docker-bench.log`
- `20_evidencia/E04_config/docker-bench-clean.log`
- `20_evidencia/E04_config/docker-bench-warn.txt`
- `docs/evidencias/S04/salidas/docker-bench-warn-count.txt`
- `docs/evidencias/S04/salidas/docker-bench-reglas-warn.txt`
- `docs/evidencias/S04/salidas/docker-bench-seccion-4.txt`
- `docs/evidencias/S04/salidas/docker-bench-seccion-5.txt`

### C.2 Resultado general

- Líneas con `[WARN]` en la salida limpia: **174**.
- El número 174 representa líneas de advertencia, no 174 controles CIS distintos, porque varias reglas generan una línea adicional por cada contenedor afectado.

### C.3 Sección 4 — Imágenes

| Regla | Resultado | Interpretación | Control ISO/IEC 27001:2022 |
|---|---|---|---|
| `4.1` | WARN | Se detectaron múltiples contenedores ejecutándose como `root`. Esto eleva el impacto de una explotación dentro del contenedor. | **A.8.28 Codificación segura / A.8.9 Gestión de la configuración**, según el contexto del control aplicado |
| `4.5` | WARN | Docker Content Trust no está habilitado. Disminuye la garantía sobre procedencia e integridad de imágenes. | **A.8.31 Separación de entornos / gestión segura de componentes**, según criterio de implementación |
| `4.6` | WARN | Varias imágenes no incorporan `HEALTHCHECK`. Reduce la capacidad de detectar automáticamente estados degradados. | **A.8.16 Actividades de monitorización** |

### C.4 Sección 5 — Runtime

| Regla | Resultado | Riesgo / lectura de auditoría | Control ISO/IEC 27001:2022 |
|---|---|---|---|
| `5.2` | WARN | Contenedores sin perfil AppArmor | **A.8.9 Gestión de la configuración** |
| `5.3` | WARN | Contenedores sin opciones SELinux | **A.8.9 Gestión de la configuración** |
| `5.4` | WARN | Capacidad adicional `CAP_NET_ADMIN` en un contenedor | **A.8.2 Derechos de acceso privilegiado** |
| `5.8` | WARN | Uso de puerto privilegiado 443 | **A.8.20 Seguridad de redes** |
| `5.9` | WARN | Puertos publicados que requieren validación de necesidad | **A.8.20 Seguridad de redes** |
| `5.11` | WARN | Contenedores sin límite de memoria | **A.8.6 Gestión de la capacidad** |
| `5.12` | WARN | Contenedores sin restricción de CPU | **A.8.6 Gestión de la capacidad** |
| `5.13` | WARN | Filesystem raíz de contenedores montado R/W | **A.8.9 Gestión de la configuración** |
| `5.22` | WARN | Perfil seccomp por defecto deshabilitado en un componente | **A.8.9 Gestión de la configuración** |
| `5.26` | WARN | Contenedores sin restricción para adquirir privilegios adicionales | **A.8.2 Derechos de acceso privilegiado** |
| `5.27` | WARN | Ausencia de healthcheck en varios contenedores | **A.8.16 Actividades de monitorización** |
| `5.29` | WARN | Contenedores sin límite de PIDs | **A.8.6 Gestión de la capacidad** |
| `5.32` | PASS | El socket Docker no se encontró montado dentro de contenedores | **A.8.9 Gestión de la configuración** |

### C.5 Observación sobre la numeración

La versión ejecutada de Docker Bench utiliza la regla **5.32** para comprobar que el socket Docker no se monte dentro de contenedores, y dicha regla resultó `PASS`. En esta versión, la regla `5.31` corresponde a namespaces de usuario y también resultó `PASS`. Se conservan los identificadores reales del log en lugar de sustituirlos por la numeración de ejemplo de la guía.

---

## D. Trivy — Vulnerabilidades, IaC, secretos y SBOM

### D.1 Evidencia generada

- `20_evidencia/E04_config/trivy_bkimminich_juice-shop_latest.json`
- `20_evidencia/E04_config/trivy_mariadb_11.json`
- `20_evidencia/E04_config/trivy_postgres_16.json`
- `20_evidencia/E04_config/trivy_wordpress_latest.json`
- `20_evidencia/E04_config/trivy_resumen.txt`
- `20_evidencia/E04_config/trivy_iac.txt`
- `20_evidencia/E04_config/trivy_secretos.txt`
- `20_evidencia/E04_config/sbom_juiceshop.json`
- `docs/evidencias/S04/salidas/trivy-conteo-vulnerabilidades.txt`
- `docs/evidencias/S04/salidas/trivy-secretos-resumen.txt`
- `docs/evidencias/S04/salidas/trivy-iac-resumen.txt`

### D.2 Vulnerabilidades de imágenes

| Imagen | HIGH | CRITICAL | Total |
|---|---:|---:|---:|
| `bkimminich/juice-shop:latest` | 45 | 8 | 53 |
| `mariadb:11` | 21 | 1 | 22 |
| `postgres:16` | 98 | 14 | 112 |
| `wordpress:latest` | 210 | 21 | 231 |
| **Total** | **374** | **44** | **418** |

Se identificaron **418 vulnerabilidades HIGH/CRITICAL** en las cuatro imágenes evaluadas. WordPress concentró el mayor volumen de hallazgos, seguido de PostgreSQL.

### D.3 Infraestructura como código (IaC)

Se ejecutó `trivy config --severity HIGH,CRITICAL` sobre `entorno/`. El reporte devolvió `Not scanned`, por lo que no se interpreta como cero malas configuraciones y se registra como limitación de la ejecución.

### D.4 Secretos

- **Secretos detectados: 0**
- **Archivos afectados: 0**

### D.5 SBOM CycloneDX

Se generó `20_evidencia/E04_config/sbom_juiceshop.json` en formato **CycloneDX** para `bkimminich/juice-shop:latest`. Se relaciona con **ISO/IEC 27001:2022 A.8.8 — Gestión de vulnerabilidades técnicas**.

---

## E. Matriz de control consolidada

### E.1 Evidencia generada

- `30_papeles_trabajo/PT04_matriz_control.py`
- `40_hallazgos/PT04_matriz_control.csv`
- `docs/evidencias/S04/salidas/PT04_matriz_resumen.txt`

### E.2 Resultado de consolidación

La matriz consolidó resultados de **Lynis, OpenSCAP, Docker Bench y Trivy**.

| Herramienta | Severidad | Hallazgos |
|---|---|---:|
| Docker Bench | Alta | 27 |
| Lynis | Media | 28 |
| OpenSCAP | Media | 3 |
| Trivy | Critical | 44 |
| Trivy | High | 374 |
| **Total** |  | **476** |

### E.3 Clasificación ISO/IEC 27001:2022

| Control / clasificación | Cantidad |
|---|---:|
| A.8.8 Management of technical vulnerabilities | 415 |
| Sin clasificar | 24 |
| A.8.15 Logging | 9 |
| A.8.2 Privileged access rights | 8 |
| A.5.17 Authentication information | 6 |
| A.8.9 Configuration management | 4 |
| A.8.20 Networks security | 4 |
| A.8.6 Capacity management | 3 |
| A.8.16 Monitoring activities | 2 |
| A.8.13 Information backup | 1 |

### E.4 Cumplimiento del criterio

- Total de hallazgos: **476**
- Sin clasificar: **24**
- Porcentaje sin clasificar: **5.04 %**
- Criterio requerido: **< 20 %**
- Resultado: **CUMPLE**

Aunque el umbral ya se cumple, en el Paso F se revisarán los 24 elementos sin clasificar y una muestra de las asignaciones automáticas para comprobar que los mapeos sean razonables y no solo cuantitativamente suficientes.

---

## F. Diseño frente a eficacia operativa

### F.1 Validaciones efectuadas

1. **Porcentaje sin clasificar:** 24 de 476 hallazgos, equivalente a **5.04 %**. Cumple el criterio de menos del 20 %.
2. **OpenSCAP:** se obtuvieron 3 reglas fallidas de severidad Medium y 0 High. Las tres reglas fallidas conservan su identificador XCCDF completo.
3. **Diseño vs. eficacia operativa:** se analizó el control con mayor concentración de hallazgos.

### F.2 Control seleccionado

**ISO/IEC 27001:2022 A.8.8 — Gestión de vulnerabilidades técnicas**

La matriz consolidada concentra **415 hallazgos** en este control. Trivy identificó **418 vulnerabilidades HIGH/CRITICAL** en las cuatro imágenes analizadas.

### F.3 Clasificación

**Deficiencia de eficacia operativa.**

El control no está ausente: existen actividades de identificación de vulnerabilidades y A.8.8 ya forma parte del alcance de auditoría. Sin embargo, el volumen de vulnerabilidades HIGH y CRITICAL demuestra que la identificación no está acompañada por una ejecución suficientemente eficaz del seguimiento y remediación.

Se recomienda fortalecer la ejecución mediante responsables, plazos de remediación, priorización por criticidad, actualización de imágenes y reescaneo posterior.

### F.4 Evidencia

- `docs/evidencias/S04/salidas/PT04_validacion.txt`
- `40_hallazgos/PT04_matriz_control.csv`


---

## G. Problemas y mejoras

1. La ejecución se realiza sobre Docker Desktop en Windows; algunas pruebas de host Linux deben interpretarse considerando la VM Linux de Docker Desktop.
2. Lynis produjo cero `warning[]`; se analizaron tres sugerencias relevantes sin alterar la evidencia real.
3. OpenSCAP produjo tres fallos `medium` y cero `high`, aunque la guía esperaba cinco fallos de severidad alta.
4. La versión actual de Docker Bench presenta una numeración diferente a la mencionada en la guía para la verificación del socket Docker.
5. Trivy IaC devolvió `Not scanned` para `entorno/`; se conserva esta salida como limitación en lugar de declararla como ausencia de malas configuraciones.

---

## H. Pregunta de transferencia

**Pendiente al cierre:** ¿qué riesgo correría una organización real si este proceso de auditoría se hiciera mal?

---

## I. URLs de evidencia al cierre

| Resultado | URL |
|---|---|
| Lynis | Pendiente después de versionar la evidencia |
| OpenSCAP | Pendiente después de versionar la evidencia |
| Docker Bench | Pendiente después de versionar la evidencia |
| Trivy | Pendiente después de versionar la evidencia |
| Matriz consolidada | Pendiente después de versionar la evidencia |
| Pull Request `s04-taller` → `develop` | Pendiente |
| Etiqueta `taller-04` | Pendiente |
