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
        if linea.startswith("warning[]=") or linea.startswith("suggestion[]='):
            pass
else:
    print("ADVERTENCIA: no se encontró lynis-report.dat")
