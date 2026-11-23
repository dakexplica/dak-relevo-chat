#!/usr/bin/env python3
"""Hook SessionStart de dak-relevo-chat: el chat nuevo recoge solo la nota de relevo.

Si en esta carpeta hay una nota de relevo reciente (menos de 3 días) que ningún chat
ha recogido todavía, le avisa a Claude para que la lea y ofrezca seguir. Así funciona
aunque la persona abra el chat nuevo a mano o use /clear en la terminal.
Solo lee archivos locales; ante cualquier error se queda callado.
"""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comun  # noqa: E402

VIGENCIA = 3 * 24 * 3600


def main():
    entrada = json.load(sys.stdin)
    if entrada.get("source") not in (None, "startup", "clear"):
        return  # al reanudar o compactar no hace falta
    carpeta = entrada.get("cwd") or os.getcwd()
    nota = comun.ruta_nota(carpeta)
    if not os.path.exists(nota):
        return
    edad = time.time() - os.path.getmtime(nota)
    if edad > VIGENCIA:
        return
    marca = nota + ".recogida"
    if os.path.exists(marca) and os.path.getmtime(marca) >= os.path.getmtime(nota):
        return  # otro chat ya la recogió
    with open(marca, "w") as f:
        f.write(entrada.get("session_id") or "")
    with open(nota, encoding="utf-8") as f:
        titulo = f.readline().strip("# \n")
    horas = int(edad // 3600)
    hace = f"hace {horas} h" if horas else "hace unos minutos"
    texto = (
        f"[dak-relevo-chat] En esta carpeta hay una nota de relevo de {hace}: «{titulo}» "
        f"({nota}). Viene de un chat anterior que se puso pesado. Léela antes de responder. "
        "Si el primer mensaje de la persona tiene que ver con ese trabajo (o es un saludo, "
        "«seguimos», «¿en qué íbamos?»), arranca diciéndole en 3-5 líneas en qué iban y el "
        "siguiente paso. Si pide otra cosa, haz lo que pide y menciona la nota en una línea al final."
    )
    if comun.leer_config().get("pendiente") == "leccion-3-en-chat-nuevo":
        texto += " La persona viene de la guía de dak-relevo-chat: sigue con su guia/leccion-3.md."
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart",
                                             "additionalContext": texto}}, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
