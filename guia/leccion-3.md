# Lección 3 · El chat nuevo ya sabe todo, y te avisa solo (~1-2 min)

> Guion para Claude. **Esta lección se da en el CHAT NUEVO.** Antes lee `guia/estilo.md`, la nota de relevo y `~/.dakexplica/dak-relevo-chat.json` (`nombre`, `donde`, `objetivo`). **ALTO** = esperas.

## 1 · El momento "ya sabe" (tu PRIMER mensaje en el chat nuevo; cierra el turno)

Cuando arranques (por el brief, por el aviso de arranque automático o porque pegaron la nota):

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  RELEVO DE CHAT
  ▰▰▰  Lección 3 de 3 · El chat nuevo ya sabe todo
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

> **Ya estamos en el chat nuevo, [nombre]. 👋**
> Fíjate en lo que sé sin que me lo repitas:
> - Te llamas [nombre] y usas Claude en [donde].
> - Lo que te preocupa de los chats largos: [objetivo].
> - Íbamos en la guía: hiciste la lección 1 y tu primer relevo.
> - [Si en el chat anterior había trabajo suyo: en qué iba y su siguiente paso, en 1 línea.]
>
> Y este chat arrancó ligero: [peso inicial] en vez de [peso del chat viejo] (si lo tienes; si no, quita la línea).

Si el chat anterior sigue abierto (app de escritorio): una línea "El chat anterior sigue abierto; si quieres lo archivo desde aquí, dime «archívalo»."

> **Última cosa y terminamos.** Escríbeme **«sigue»**.

**ACCIÓN:** guarda `leccion: 3`, quita `pendiente`. **ALTO** (fin del turno).

## 2 · Que te avise solo + cierre (UN mensaje, cierra el turno y la guía)

Con el «sigue»:

> **Para que nunca tengas que acordarte:**
> - El **medidor** mide en silencio cada mensaje. Cuando el chat ya pesa, al terminar lo que estemos haciendo (nunca a media tarea) te escribo una línea así:
>
>   🔄 *Este chat ya está pesado: cada respuesta vuelve a leer ~300 mil tokens; uno nuevo arranca con ~60 mil. ¿Lo paso a un chat nuevo?*
>
>   Dices que sí y hago todo lo que viste. Si dices que no, no insisto.
> - Cada nota se guarda: las últimas 10 de cada proyecto. Pregúntame «¿qué hicimos la vez pasada?» y te lo cuento.

(Si no instaló los avisos o está en claude.ai: cambia la primera viñeta por "Cuando sientas que el chat se pone lento, solo dime «relevo»". Si quiere instalarlos ahora, hazlo.)

> **Lo que lograste**
> - Viste cuánto pesa un chat largo y por qué se vuelve lento.
> - Hiciste tu primer relevo y comprobaste que el chat nuevo sabe en qué iban.
> - [Con avisos: Te va a avisar solo cuando convenga.]
>
> **De aquí en adelante ya no necesitas la guía.** Todo esto la herramienta lo hace **sola, sin que le digas cada paso**. Cuando un chat se ponga pesado, solo pega esto:

```
Usando la skill dak-relevo-chat, haz el relevo
```

> Esta herramienta es de **@dakexplica**: sígueme para la siguiente. Las demás están gratis en el link de mi perfil. 🙌

**Una sola frase para copiar.** Nada de listas de comandos ni tips al final.

**ACCIÓN:** guarda `terminada: true`. **ALTO** (fin de la guía).
