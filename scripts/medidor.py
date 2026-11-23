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
        if MARCA not in linea and b'\\ud83d\\udd04' not in linea:
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

    inicial, actual, comp = comun.medir(ruta)
    if not inicial or not actual:
        return
    crecimiento = max(actual - inicial, 0)
    cabe = comun.ventana(comun.maximo(ruta), cfg)
    lleno = actual / cabe
    # Cuántas veces más cuesta cada mensaje aquí que en un chat nuevo DE ESTA CUENTA
    # (la base cambia mucho según los conectores y herramientas de cada quien).
    veces = actual / inicial if inicial else 0
    aprendido = cfg.get("aprendido") or {}
    paciencia = int(aprendido.get("paciencia", 0))  # sube con cada «ahora no», baja con cada «sí»
    p1 = min(float(cfg.get("aviso_1_pct") or comun.AVISO_1_PCT) + 0.08 * paciencia, 0.78)
    v1 = float(cfg.get("aviso_1_veces") or comun.AVISO_1_VECES) + 0.5 * paciencia
    p2 = float(cfg.get("aviso_2_pct") or comun.AVISO_2_PCT)
    trabajo = crecimiento >= comun.MIN_CRECIMIENTO and actual >= comun.MIN_ACTUAL
    nivel = 0
    if (trabajo and veces >= v1 and lleno >= p1) or comp >= 1:
        nivel = 1  # ya conviene: cambiar ahorra de verdad y el chat va avanzado
    if (trabajo and lleno >= p2) or comp >= 2:
        nivel = 2  # tope: está por compactarse (resumirse solo y perder detalle)

    est = comun.estado_sesion(sesion)
    avisado = est.get("nivel", 0)
    texto_persona = (entrada.get("prompt") or "").lower().strip()
    acepta = "relevo" in texto_persona or "chat nuevo" in texto_persona or texto_persona.startswith(("sí", "si,", "si ", "va", "dale", "ok"))
    rechaza = any(f in texto_persona for f in ("ahora no", "todavía no", "todavia no", "aún no", "aun no", "después", "despues", "luego", "sigamos aquí", "sigamos aqui")) or texto_persona in ("no", "no.", "nop")
    tam = os.path.getsize(ruta)
    hubo_oferta = ya_ofrecido(ruta, max(tam - 150_000, 0))

    # Aprende de la persona (una vez por oferta): «ahora no» = esperar más la próxima vez; «sí» = vas bien.
    if hubo_oferta and (acepta or rechaza) and est.get("respondido") != est.get("nivel", -1):
        paciencia = paciencia + 1 if rechaza and not acepta else max(paciencia - 1, 0)
        aprendido["paciencia"] = min(paciencia, 4)
        comun.guardar_config({"aprendido": aprendido})
        est["respondido"] = est.get("nivel", -1)
        est["ofrecido"] = True
        comun.guardar_estado_sesion(sesion, est)

    if (acepta or rechaza) and avisado:
        est["ofrecido"] = True
        comun.guardar_estado_sesion(sesion, est)
        return

    if nivel > avisado:
        # Si Claude ya lo ofreció hace poco (o la persona ya contestó), no se repite.
        ya = acepta or rechaza or hubo_oferta
        est = {"nivel": nivel, "ofrecido": ya, "desde": tam}
        comun.guardar_estado_sesion(sesion, est)
        if ya:
            return
        if comp:
            dato = (f"se ha compactado {comp} {'vez' if comp == 1 else 'veces'} "
                    f"(cada respuesta vuelve a leer {comun.miles(actual)} tokens)")
        else:
            dato = (f"está {round(lleno * 100)} % lleno ({comun.miles(actual)} de {comun.miles(cabe)}): "
                    f"cada respuesta vuelve a leer {comun.miles(actual)} tokens y uno nuevo de esta cuenta arrancaría con "
                    f"{comun.miles(inicial)}, o sea {veces:.1f} veces menos")
        fuerza = ("Ya está muy lleno y pronto se va a compactar (resumir solo y perder detalle): ofrécelo en "
                  "cuanto cierres lo que estás haciendo, explicando en una línea que aquí cada mensaje gasta "
                  "varias veces más tokens que en un chat nuevo. " if nivel == 2 else "")
        decir(
            f"[medidor dak-relevo-chat] Este chat ya {dato}. {fuerza}"
            "Con criterio: no cortes lo que estás haciendo, y si lo que sigue es parte de la MISMA tarea "
            "(y aún cabe), espera a terminarla: un relevo por fase, no varios para el mismo tema. Cuando "
            "cierres una tarea o fase (o la persona cambie de tema), ofrece el relevo con la skill dak-relevo-chat en UNA línea que empiece con 🔄 "
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
