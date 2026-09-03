# Declaración de Aplicabilidad (SoA) - Extracto Laboratorio 03
**Organización:** Laboratorio de Auditoría de Sistemas de Información (SI-084)  
**Alcance:** Segmento de contenedores Docker (`si084-lab_audit_net` / `172.20.0.0/16`)  
**Estándar de referencia:** ISO/IEC 27001:2022 - Anexo A  

---

## 1. Controles Seleccionados para Mitigación

| Control ISO 27001:2022 | Nombre del Control | Estado | Justificación de Inclusión |
|---|---|---|---|
| **A.8.8** | Gestión de vulnerabilidades técnicas | Aplicable | Mitiga la presencia de sistemas operativos obsoletos (Debian 9 EOL) y servicios web vulnerables detectados en Greenbone. |
| **A.8.9** | Gestión de la configuración | Aplicable | Evita despliegues con configuraciones predeterminadas o firmas visibles de servidores web y motores de datos. |
| **A.8.20** | Seguridad de redes | Aplicable | Asegura la segmentación y aislamiento perimetral de los puertos de bases de datos (MariaDB 3306 y PostgreSQL 5432). |
| **A.8.24** | Uso de criptografía | Aplicable | Protege el tránsito de credenciales e información sensible entre el frontend y las capas de persistencia de datos. |
| **A.8.28** | Codificación segura | Aplicable | Aborda fallas a nivel de lógica de aplicación (XSS, inyecciones, deserialización) presentes en OWASP Juice Shop y DVWA. |

---

## 2. Control Excluido del Alcance

### **A.7.4 Monitoreo de la seguridad física**
* **Estado:** Excluido.
* **Justificación técnica:**  
  El entorno auditado opera como una arquitectura lógica basada íntegramente en contenedores virtualizados sobre Docker. La infraestructura física subyacente del anfitrión y las instalaciones físicas escapan de los límites operativos y competencias directas del equipo evaluado en este taller.
