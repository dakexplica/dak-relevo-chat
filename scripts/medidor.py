#!/usr/bin/env python3
"""Medidor de dak-relevo-chat (hook UserPromptSubmit de Claude Code).

En cada mensaje mide en silencio cuánto ha crecido el chat leyendo su transcript.
Mientras esté ligero no imprime nada (cero costo). Cuando cruza un nivel, mete una
línea en el contexto para que Claude sugiera el relevo en una pausa natural.

Lo nuevo (v2): el aviso queda PENDIENTE hasta que Claude de verdad lo ofrece. Si
Claude estaba a media tarea y se le pasó, en el siguiente mensaje se lo recuerda
(corto). Sabe que ya lo ofreció porque la oferta lleva la marca 🔄. Así nunca
"a veces sí y a veces no".

Niveles (tokens que creció el chat desde que empezó; se cambian en
~/.dakexplica/dak-relevo-chat.json con "aviso_1" y "aviso_2"):
  1 = creció >= aviso_1, o ya se compactó una vez
  2 = creció >= aviso_2, o ya se compactó 2+ veces
Solo lee archivos locales; no usa red. Ante cualquier error, se queda callado.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comun  # noqa: E402

MARCA = "🔄".encode()


def ya_ofrecido(transcript, desde_byte):
    """¿Claude escribió una oferta con la marca 🔄 después del aviso?"""
    with open(transcript, "rb") as f:
        f.seek(desde_byte)
        nuevo = f.read()
    for linea in nuevo.split(b"\n"):
        if MARCA not in linea:
            continue
        try:
            j = json.loads(linea)
        except ValueError:
            continue
        if j.get("type") == "assistant" and not j.get("isSidechain"):
            return True
    return False


def decir(texto):
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit",
                                             "additionalContext": texto}}, ensure_ascii=False))


def main():
    entrada = json.load(sys.stdin)
    ruta = entrada.get("transcript_path")
    sesion = entrada.get("session_id") or "sin-id"
    carpeta = entrada.get("cwd") or os.getcwd()
    if not ruta or not os.path.exists(ruta):
        return
    comun.recordar_carpeta(carpeta, sesion, ruta)

    cfg = comun.leer_config()
    if cfg.get("medidor") is False:  # la persona lo apagó
        return
    aviso1 = int(cfg.get("aviso_1") or comun.AVISO_1)
    aviso2 = int(cfg.get("aviso_2") or comun.AVISO_2)

    inicial, actual, comp = comun.medir(ruta)
    if not inicial or not actual:
        return
    crecimiento = max(actual - inicial, 0)
    nivel = 0
    if crecimiento >= aviso1 or comp >= 1:
        nivel = 1
    if crecimiento >= aviso2 or comp >= 2:
        nivel = 2

    est = comun.estado_sesion(sesion)
    avisado = est.get("nivel", 0)
    pidio = "relevo" in (entrada.get("prompt") or "").lower()

    # La persona misma habló del relevo: el aviso pendiente queda atendido.
    if pidio and avisado:
        est["ofrecido"] = True
        comun.guardar_estado_sesion(sesion, est)
        return

    if nivel > avisado:
        est = {"nivel": nivel, "ofrecido": False, "desde": os.path.getsize(ruta)}
        comun.guardar_estado_sesion(sesion, est)
        if comp:
            dato = (f"se ha compactado {comp} {'vez' if comp == 1 else 'veces'} "
                    f"(cada respuesta vuelve a leer {comun.miles(actual)} tokens)")
        else:
            dato = (f"creció {comun.miles(crecimiento)} tokens desde que empezó "
                    f"(cada respuesta vuelve a leer {comun.miles(actual)} tokens; uno nuevo arrancaría con {comun.miles(inicial)})")
        fuerza = ("Ya está muy pesado: dilo con claridad y explica en una línea que aquí cada mensaje "
                  "gasta varias veces más tokens que en un chat nuevo. " if nivel == 2 else "")
        decir(
            f"[medidor dak-relevo-chat] Este chat ya {dato}. {fuerza}"
            "No cortes lo que estás haciendo. Al TERMINAR esta respuesta (o la primera que cierre una "
            "tarea), ofrece el relevo con la skill dak-relevo-chat en UNA línea que empiece con 🔄 "
            "(la marca es obligatoria: así el medidor sabe que ya lo ofreciste). Si tienes una "
            "herramienta de botones o de cierre de turno con botones, úsala: «🔄 Este chat ya está pesado "
            "(cada respuesta vuelve a leer ~X tokens; uno nuevo arranca con ~Y). ¿Lo paso a un chat nuevo?» "
            "con «Sí, pásalo a un chat nuevo» / «Ahora no». Di los números: es lo que convence. Una sola vez por aviso."
        )
        return

    if avisado and not est.get("ofrecido"):
        if ya_ofrecido(ruta, est.get("desde", 0)):
            est["ofrecido"] = True
            comun.guardar_estado_sesion(sesion, est)
            return
        decir(
            "[medidor dak-relevo-chat] Sigue pendiente ofrecer el relevo (no se ha ofrecido). "
            f"Cada respuesta vuelve a leer {comun.miles(actual)} tokens. Si esta respuesta cierra algo, "
            "termina con la línea 🔄 (o los botones) ofreciéndolo; si estás a media tarea, al acabarla."
        )


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
