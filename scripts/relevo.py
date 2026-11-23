#!/usr/bin/env python3
"""Herramienta de dak-relevo-chat. Uso:

  python3 relevo.py paso0              ¿Está todo? (Python, medidor, arranque automático)
  python3 relevo.py instalar           Instala los 2 avisos automáticos (con respaldo de settings.json)
  python3 relevo.py desinstalar        Los quita
  python3 relevo.py preparar [carpeta] Guarda la nota anterior en el historial y dice dónde va la nueva
  python3 relevo.py ruta [carpeta]     Solo dice dónde está la nota de este proyecto (no toca nada)
  python3 relevo.py peso [carpeta]     Cuánto pesa el chat actual y con cuánto arrancaría uno nuevo
  python3 relevo.py historial [carpeta] Notas anteriores de este proyecto

Solo biblioteca estándar; no usa red.
"""
import json
import os
import shutil
import sys
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import comun  # noqa: E402

import atexit as _atexit


def _aviso_version():
    """Al terminar, revisa en silencio si hay versión nueva de la skill (máx. 1 vez al día)."""
    try:
        import importlib.util, os as _os
        ruta = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "version.py")
        spec = importlib.util.spec_from_file_location("dak_version", ruta)
        modulo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(modulo)
        modulo.avisar()
    except Exception:
        pass


_atexit.register(_aviso_version)


SETTINGS = os.path.join(comun.CASA, ".claude", "settings.json")
HOOKS = {
    "UserPromptSubmit": os.path.join(AQUI, "medidor.py"),
    "SessionStart": os.path.join(AQUI, "al_abrir.py"),
}


def _leer_settings():
    try:
        with open(SETTINGS) as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def _instalado(settings, evento, script):
    nombre = os.path.basename(script)
    for grupo in settings.get("hooks", {}).get(evento, []):
        for h in grupo.get("hooks", []):
            cmd = h.get("command", "")
            if "dak-relevo-chat" in cmd and nombre in cmd:
                return cmd
    return None


def paso0():
    ok = sys.version_info >= (3, 7)
    print(f"{'✓' if ok else '✗'} Python {sys.version.split()[0]}" + ("" if ok else " (necesita 3.7 o más nuevo)"))
    try:
        s = _leer_settings()
    except ValueError:
        print("✗ No pude leer ~/.claude/settings.json (está mal escrito). No lo toco.")
        return 1
    faltan = 0
    nombres = {"UserPromptSubmit": "Medidor (te avisa cuando el chat ya pesa)",
               "SessionStart": "Arranque automático (el chat nuevo recoge la nota solo)"}
    for evento, script in HOOKS.items():
        cmd = _instalado(s, evento, script)
        if cmd and script in cmd:
            print(f"✓ {nombres[evento]}")
        elif cmd:
            print(f"✗ {nombres[evento]}: apunta a otra carpeta. Corre «instalar» para corregirlo.")
            faltan += 1
        else:
            print(f"✗ {nombres[evento]}: no está instalado (opcional, se instala con permiso).")
            faltan += 1
    print(f"· Notas de relevo en {comun.RELEVOS}")
    return 0 if ok and not faltan else 2


def instalar():
    try:
        s = _leer_settings()
    except ValueError:
        print("✗ ~/.claude/settings.json está mal escrito; no lo toco. Arréglalo y vuelve a intentar.")
        return 1
    if os.path.exists(SETTINGS):
        copia = SETTINGS + f".respaldo-dak-relevo-chat-{time.strftime('%Y%m%d-%H%M%S')}"
        shutil.copy2(SETTINGS, copia)
        print(f"· Respaldo de tu configuración: {copia}")
    hooks = s.setdefault("hooks", {})
    for evento, script in HOOKS.items():
        grupos = hooks.setdefault(evento, [])
        # Quita versiones viejas de este mismo aviso (por si la skill cambió de carpeta).
        for g in grupos:
            g["hooks"] = [h for h in g.get("hooks", [])
                          if not ("dak-relevo-chat" in h.get("command", "")
                                  and os.path.basename(script) in h.get("command", ""))]
        grupos[:] = [g for g in grupos if g.get("hooks")]
        grupos.append({"hooks": [{"type": "command", "command": f'python3 "{script}"', "timeout": 10}]})
    os.makedirs(os.path.dirname(SETTINGS), exist_ok=True)
    tmp = SETTINGS + ".tmp"
    with open(tmp, "w") as f:
        json.dump(s, f, ensure_ascii=False, indent=2)
    os.replace(tmp, SETTINGS)
    print("✓ Instalados el medidor y el arranque automático. Funcionan desde el próximo mensaje.")
    return 0


def desinstalar():
    s = _leer_settings()
    for evento, script in HOOKS.items():
        grupos = s.get("hooks", {}).get(evento, [])
        for g in grupos:
            g["hooks"] = [h for h in g.get("hooks", []) if "dak-relevo-chat" not in h.get("command", "")]
        if evento in s.get("hooks", {}):
            s["hooks"][evento] = [g for g in grupos if g.get("hooks")]
    with open(SETTINGS, "w") as f:
        json.dump(s, f, ensure_ascii=False, indent=2)
    print("✓ Quitados. La skill sigue funcionando cuando la pidas; solo ya no avisa sola.")
    return 0


def preparar(carpeta):
    nota = comun.ruta_nota(carpeta)
    os.makedirs(comun.RELEVOS, exist_ok=True)
    print(f"NOTA: {nota}")
    if os.path.exists(nota):
        proyecto = comun.nombre_proyecto(carpeta)
        dest_dir = os.path.join(comun.HISTORIAL, proyecto)
        os.makedirs(dest_dir, exist_ok=True)
        fecha = time.strftime("%Y-%m-%d-%H%M", time.localtime(os.path.getmtime(nota)))
        dest = os.path.join(dest_dir, f"{fecha}.md")
        shutil.copy2(nota, dest)
        viejas = sorted(os.listdir(dest_dir))
        for v in viejas[:-comun.HISTORIAL_MAX]:
            os.remove(os.path.join(dest_dir, v))
        with open(nota, encoding="utf-8") as f:
            print(f"ANTERIOR (guardada en {dest}): {f.readline().strip('# ').strip()}")
        print("Si la nota anterior trae algo de otro tema que siga vivo, intégralo en la nueva.")
    else:
        print("ANTERIOR: ninguna (es el primer relevo de este proyecto)")
    peso(carpeta)
    return 0


def peso(carpeta):
    chat = comun.chat_de_carpeta(carpeta)
    if not chat or not os.path.exists(chat.get("transcript", "")):
        print("PESO: sin medir (el medidor no está instalado o este chat aún no manda mensajes)")
        return 0
    inicial, actual, comp = comun.medir(chat["transcript"])
    if not actual:
        print("PESO: sin medir")
        return 0
    veces = round(actual / inicial, 1) if inicial else None
    print(f"PESO: cada vez que respondo (o doy un paso) vuelvo a leer todo el chat: {comun.miles(actual)} tokens"
          + (f"; se ha compactado {comp} {'vez' if comp == 1 else 'veces'}" if comp else "") + ".")
    if inicial:
        print(f"NUEVO: uno nuevo arranca con {comun.miles(inicial)} (lo de base) + la nota: "
              f"unas {veces} veces menos por paso.")
    return 0


def historial(carpeta):
    d = os.path.join(comun.HISTORIAL, comun.nombre_proyecto(carpeta))
    if not os.path.isdir(d):
        print("Sin notas anteriores.")
        return 0
    for n in sorted(os.listdir(d), reverse=True):
        with open(os.path.join(d, n), encoding="utf-8") as f:
            print(f"{os.path.join(d, n)} · {f.readline().strip('# ').strip()}")
    return 0


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 0
    cmd, carpeta = args[0], (args[1] if len(args) > 1 else os.getcwd())
    acciones = {"paso0": paso0, "instalar": instalar, "desinstalar": desinstalar,
                "preparar": lambda: preparar(carpeta), "ruta": lambda: print(comun.ruta_nota(carpeta)) or 0, "peso": lambda: peso(carpeta),
                "historial": lambda: historial(carpeta)}
    if cmd not in acciones:
        print(__doc__)
        return 1
    return acciones[cmd]()


if __name__ == "__main__":
    sys.exit(main())
