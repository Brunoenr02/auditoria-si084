import pandas as pd
import json
import re
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
EVID = ROOT / "20_evidencia" / "E04_config"
SALIDA = ROOT / "40_hallazgos" / "PT04_matriz_control.csv"

filas = []

# =========================================================
# 1. LYNIS
# =========================================================
lynis = EVID / "lynis-report.dat"

if lynis.exists():
    for linea in lynis.read_text(encoding="utf-8", errors="ignore").splitlines():
        if linea.startswith("warning[]=") or linea.startswith("suggestion[]="):
            tipo = "warning" if linea.startswith("warning") else "suggestion"
            filas.append({
                "herramienta": "Lynis",
                "severidad": "Alta" if tipo == "warning" else "Media",
                "hallazgo": linea.split("=", 1)[1].strip()[:500],
            })
else:
    print("ADVERTENCIA: no se encontró lynis-report.dat")

# =========================================================
# 2. OPENSCAP
# =========================================================
oscap = EVID / "oscap-resultados.xml"

if oscap.exists():
    def local(tag):
        return tag.rsplit("}", 1)[-1]

    root = ET.parse(oscap).getroot()
    reglas = {}

    for elem in root.iter():
        if local(elem.tag) == "Rule":
            rid = elem.attrib.get("id")
            if not rid:
                continue

            titulo = ""
            for hijo in elem:
                if local(hijo.tag) == "title":
                    titulo = " ".join("".join(hijo.itertext()).split())
                    break

            reglas[rid] = {
                "severity": elem.attrib.get("severity", "unknown"),
                "title": titulo,
            }

    for rr in root.iter():
        if local(rr.tag) != "rule-result":
            continue

        resultado = ""
        for hijo in rr:
            if local(hijo.tag) == "result":
                resultado = (hijo.text or "").strip()
                break

        if resultado == "fail":
            rid = rr.attrib.get("idref", "")
            info = reglas.get(rid, {})
            sev = info.get("severity", "unknown").lower()
            mapa_sev = {
                "high": "Alta",
                "medium": "Media",
                "low": "Baja",
            }

            filas.append({
                "herramienta": "OpenSCAP",
                "severidad": mapa_sev.get(sev, sev.capitalize()),
                "hallazgo": (
                    f"{rid} - {info.get('title', 'Regla XCCDF fallida')}"
                )[:500],
            })
else:
    print("ADVERTENCIA: no se encontró oscap-resultados.xml")

# =========================================================
# 3. DOCKER BENCH
# =========================================================
docker_bench = EVID / "docker-bench-clean.log"
if not docker_bench.exists():
    docker_bench = EVID / "docker-bench.log"

if docker_bench.exists():
    for linea in docker_bench.read_text(encoding="utf-8", errors="ignore").splitlines():
        if re.match(r"^\[WARN\]\s+\d+\.\d+", linea):
            filas.append({
                "herramienta": "Docker Bench",
                "severidad": "Alta",
                "hallazgo": linea.replace("[WARN]", "").strip()[:500],
            })
else:
    print("ADVERTENCIA: no se encontró docker-bench.log")

# =========================================================
# 4. TRIVY - VULNERABILIDADES DE IMÁGENES
# =========================================================
for archivo in sorted(EVID.glob("trivy_*.json")):
    if archivo.name == "sbom_juiceshop.json":
        continue

    try:
        datos = json.loads(archivo.read_text(encoding="utf-8", errors="ignore"))
    except Exception as exc:
        print(f"ADVERTENCIA: no se pudo leer {archivo.name}: {exc}")
        continue

    for resultado in datos.get("Results", []):
        for vuln in resultado.get("Vulnerabilities", []) or []:
            filas.append({
                "herramienta": "Trivy",
                "severidad": vuln.get("Severity", "unknown").capitalize(),
                "hallazgo": (
                    f"{vuln.get('VulnerabilityID', '')} "
                    f"en {vuln.get('PkgName', '')} "
                    f"{vuln.get('InstalledVersion', '')}"
                ).strip()[:500],
            })

# =========================================================
# CREAR MATRIZ
# =========================================================
m = pd.DataFrame(filas)

if m.empty:
    raise SystemExit("ERROR: no se obtuvo ningún hallazgo de las herramientas.")

# =========================================================
# MAPEO ISO/IEC 27001:2022 + COBIT 2019
# =========================================================
MAPEO = [
    (r"root|privileg|capab|pam_wheel", "A.8.2 Privileged access rights", "DSS05.04"),
    (r"password|credential|secret|auth|pwquality", "A.5.17 Authentication information", "DSS05.04"),
    (r"CVE-|vulnerab|outdated|version", "A.8.8 Management of technical vulnerabilities", "DSS05.07"),
    (r"log|audit|journal", "A.8.15 Logging", "DSS01.03"),
    (r"tls|ssl|cipher|encrypt|certificate", "A.8.24 Use of cryptography", "DSS05.03"),
    (r"firewall|port|network|expose|traffic", "A.8.20 Networks security", "DSS05.02"),
    (r"config|default|hardening|apparmor|selinux|seccomp|read only|read-only", "A.8.9 Configuration management", "BAI10.02"),
    (r"backup|restore", "A.8.13 Information backup", "DSS04.07"),
    (r"memory|cpu|pid|resource", "A.8.6 Capacity management", "DSS01.03"),
    (r"healthcheck|health check|monitor|integrity", "A.8.16 Monitoring activities", "DSS05.07"),
]


def clasifica(texto):
    for patron, iso, cobit in MAPEO:
        if re.search(patron, str(texto), re.I):
            return pd.Series([iso, cobit])
    return pd.Series(["Sin clasificar", "Sin clasificar"])


m[["control_iso27001", "objetivo_cobit"]] = m["hallazgo"].apply(clasifica)

m = m[[
    "herramienta",
    "severidad",
    "hallazgo",
    "control_iso27001",
    "objetivo_cobit",
]]

SALIDA.parent.mkdir(parents=True, exist_ok=True)
m.to_csv(SALIDA, index=False, encoding="utf-8-sig")

# =========================================================
# RESUMEN
# =========================================================
print("===== MATRIZ DE CONTROL PT04 =====")

print("\nHallazgos por herramienta y severidad:")
print(m.groupby(["herramienta", "severidad"]).size().to_string())

print("\nHallazgos por herramienta:")
print(m["herramienta"].value_counts().to_string())

print("\nHallazgos por control ISO:")
print(m["control_iso27001"].value_counts().to_string())

sin = (m["control_iso27001"] == "Sin clasificar").sum()
total = len(m)
porcentaje = sin / total if total else 0

print("\nTotal de hallazgos:", total)
print("Sin clasificar:", sin)
print(f"Porcentaje sin clasificar: {porcentaje:.2%}")
print(
    "RESULTADO:",
    "CUMPLE < 20 %" if porcentaje < 0.20 else "REQUIERE CLASIFICACION MANUAL",
)

print(f"\nArchivo generado:\n{SALIDA}")
