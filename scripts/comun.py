"""Piezas compartidas de dak-relevo-chat (solo biblioteca estándar de Python, sin red)."""
import json
import os
import re
import subprocess
import time
import unicodedata

CASA = os.path.expanduser("~")
RELEVOS = os.path.join(CASA, ".claude", "relevos")
HISTORIAL = os.path.join(RELEVOS, ".historial")
ESTADO = os.path.join(RELEVOS, ".medidor")
CONFIG = os.path.join(CASA, ".dakexplica", "dak-relevo-chat.json")
HISTORIAL_MAX = 10  # notas viejas que se guardan por proyecto

# Niveles por defecto: cuánto creció el chat desde que empezó (tokens).
# Cada persona los puede cambiar en su config ("aviso_1" / "aviso_2").
AVISO_1 = 150_000
AVISO_2 = 300_000


def leer_config():
    try:
        with open(CONFIG) as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def guardar_config(cambios):
    datos = leer_config()
    datos.update(cambios)
    os.makedirs(os.path.dirname(CONFIG), exist_ok=True)
    with open(CONFIG, "w") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
    return datos


def raiz_proyecto(carpeta):
    """La raíz del repo de git si hay uno; si no, la carpeta tal cual."""
    try:
        r = subprocess.run(["git", "-C", carpeta, "rev-parse", "--show-toplevel"],
                           capture_output=True, text=True, timeout=5)
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        pass
    return carpeta


def nombre_proyecto(carpeta):
    """'Mi Proyecto 🎬' -> 'mi-proyecto'; 'club-hub.nosync' -> 'club-hub'."""
    base = os.path.basename(os.path.normpath(raiz_proyecto(carpeta)))
    base = re.sub(r"\.nosync$", "", base, flags=re.I)
    base = unicodedata.normalize("NFKD", base).encode("ascii", "ignore").decode()
    base = re.sub(r"[^a-zA-Z0-9]+", "-", base).strip("-").lower()
    return base or "proyecto"


def ruta_nota(carpeta):
    return os.path.join(RELEVOS, nombre_proyecto(carpeta) + ".md")


# ---------- medir un chat ----------

def _contexto(linea):
    """Tokens que carga un mensaje de Claude del chat principal, o None."""
    if b'"usage"' not in linea or b'"assistant"' not in linea:
        return None
    try:
        j = json.loads(linea)
    except ValueError:
        return None
    if j.get("type") != "assistant" or j.get("isSidechain"):
        return None
    msg = j.get("message")
    u = msg.get("usage") if isinstance(msg, dict) else None
    if not u:
        return None
    total = sum(u.get(k) or 0 for k in
                ("input_tokens", "cache_read_input_tokens", "cache_creation_input_tokens"))
    return total or None


def medir(transcript):
    """(inicial, actual, compactaciones) de un chat a partir de su transcript."""
    with open(transcript, "rb") as f:
        datos = f.read()
    comp = datos.count(b'"subtype":"compact_boundary"')
    lineas = datos.split(b"\n")
    inicial = next((c for c in map(_contexto, lineas) if c), None)
    actual = next((c for c in map(_contexto, reversed(lineas)) if c), None)
    return inicial, actual, comp


def total_leido(transcript):
    """Todos los tokens que Claude ha vuelto a leer en este chat (suma de cada respuesta o paso)."""
    vistos = {}
    with open(transcript, "rb") as f:
        for linea in f:
            if b'"usage"' not in linea or b'"assistant"' not in linea:
                continue
            try:
                j = json.loads(linea)
            except ValueError:
                continue
            if j.get("type") != "assistant" or j.get("isSidechain"):
                continue
            msg = j.get("message") or {}
            c = _contexto(linea)
            if c:
                vistos[msg.get("id") or len(vistos)] = c
    return sum(vistos.values())


def miles(n):
    if not n:
        return "?"
    if n >= 1_000_000:
        return f"~{n / 1_000_000:.1f} millones".replace(".0 ", " ")
    return f"~{round(n / 1000)} mil"


def estado_sesion(sesion):
    try:
        with open(os.path.join(ESTADO, f"{sesion}.json")) as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def guardar_estado_sesion(sesion, datos):
    os.makedirs(ESTADO, exist_ok=True)
    with open(os.path.join(ESTADO, f"{sesion}.json"), "w") as f:
        json.dump(datos, f)


def recordar_carpeta(carpeta, sesion, transcript):
    """Qué chat habló por última vez en cada carpeta (para medirlo al hacer relevo)."""
    archivo = os.path.join(ESTADO, "carpetas.json")
    try:
        with open(archivo) as f:
            datos = json.load(f)
    except (OSError, ValueError):
        datos = {}
    datos[carpeta] = {"sesion": sesion, "transcript": transcript, "t": time.time()}
    # Que no crezca para siempre: solo las 50 carpetas más recientes.
    datos = dict(sorted(datos.items(), key=lambda kv: kv[1].get("t", 0))[-50:])
    os.makedirs(ESTADO, exist_ok=True)
    with open(archivo, "w") as f:
        json.dump(datos, f)


def chat_de_carpeta(carpeta):
    try:
        with open(os.path.join(ESTADO, "carpetas.json")) as f:
            return json.load(f).get(carpeta)
    except (OSError, ValueError):
        return None
