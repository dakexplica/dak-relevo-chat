---
name: dak-relevo-chat
description: >-
  Pasa el trabajo de un chat pesado a un chat NUEVO y limpio sin perder el hilo. Escribe una nota de relevo corta (solo lo que vive en este chat), guarda lo duradero en el archivo de estado del proyecto, abre el chat nuevo desde cero (nunca copiando la conversación) y ofrece archivar el viejo con botones. Trae un medidor que te avisa solo cuando el chat ya pesa (con números: cuántos tokens vuelve a leer cada respuesta y cuánto menos gasta uno nuevo) y un arranque automático: el chat nuevo recoge la nota solo, aunque lo abras a mano o uses /clear. Guarda las últimas 10 notas de cada proyecto. Incluye una mini guía interactiva de ~5 min. Úsala cuando digan /dak-relevo-chat, "relevo", "hagamos relevo", "cambiemos de chat", "pásalo a un chat nuevo", "abre otro chat y seguimos", "este chat ya está pesado/lento/muy largo", "Claude ya está lento o se le olvidan cosas", "hazme un resumen para seguir en otro chat", "¿en qué íbamos?", "¿qué hicimos la vez pasada?", "guía del relevo", aunque no nombren la skill. También cuando aparezca en el contexto un aviso "[medidor dak-relevo-chat]" o "[dak-relevo-chat]": ahí la skill dice cómo y cuándo actuar.
---

# dak-relevo-chat

Cuando un chat crece, cada mensaje vuelve a leer todo lo anterior: el trabajo se vuelve más lento, más caro (se come el plan) y menos preciso, porque Claude tiene que encontrar lo importante entre muchísimo texto. Un chat nuevo arranca ligero, pero da miedo que "se le olvide todo". Esta skill resuelve las dos cosas: el chat nuevo arranca limpio **y** sabiendo exactamente en qué iban.

La clave: casi todo lo que el chat nuevo necesita **ya existe fuera de este chat**. El `CLAUDE.md` y el archivo de estado del proyecto (`ESTADO-ACTUAL.md`, `PROGRESO.md`, `README`…) se leen en cada chat nuevo. Así que la nota de relevo solo lleva lo que **únicamente vive en este chat**. Por eso es corta, y entre más corta, más barato arranca el chat nuevo.

**Habla en español claro, sin tecnicismos**, y tutea. Las rutas de abajo usan `<skill>` = la carpeta donde está instalada esta skill (normalmente `~/.claude/skills/dak-relevo-chat`). `<carpeta>` = la carpeta de trabajo de este chat.

## Primera vez · Paso 0 y mini guía

**Paso 0 · ¿Está todo?** La primera vez (y si algo falla), corre:

```bash
python3 <skill>/scripts/relevo.py paso0
```

Revisa Python y los dos avisos automáticos, que son **opcionales** (la skill funciona sin ellos cuando la pides):
- **Medidor:** en cada mensaje mide en silencio cuánto pesa el chat y, al pasar un nivel, te pide que ofrezcas el relevo.
- **Arranque automático:** cuando se abre un chat nuevo en esa carpeta, recoge solo la nota de relevo.

Si faltan, explícalos en una frase cada uno y **pide permiso antes de instalar**: tocan la configuración de Claude Code (`~/.claude/settings.json`); se guarda un respaldo antes y se quitan con `relevo.py desinstalar`. Con su sí: `python3 <skill>/scripts/relevo.py instalar`. Funcionan desde el siguiente mensaje (el arranque automático, desde el siguiente chat). Si dice que no, sigue: la skill funciona igual cuando la pida. **En la app de Claude (claude.ai)** no hay avisos automáticos ni archivos: sáltate el Paso 0 y usa el modo "app de Claude" del paso 4.

**La mini guía (solo se ofrece una vez).** Al empezar, revisa si `~/.dakexplica/dak-relevo-chat.json` tiene `"guia_ofrecida": true`:
- **Si no**, es la primera vez (da igual cómo la instalaron, o si te pidieron un relevo directo). Antes de cualquier otra cosa, ofrécela **con botones y todo lo importante dentro de la pregunta** (en la app, el texto previo a un botón se resume):
  - Pregunta: "Es la primera vez que usas Relevo de chat. ¿Quieres que te enseñe rápido a usarla y sacarle el mayor provecho? Son unos 5 min."
  - **Sí, enséñame (5 min)**: "3 pasos cortos: lo dejo listo, haces tu primer relevo y ves cómo te avisa solo"
  - **No, úsala directo**: "hago lo que me pediste; la guía la abres cuando quieras con «ábreme la guía del relevo»"
  - Sin herramienta de botones: el mismo texto con "responde 1 o 2".

  Luego guarda `"guia_ofrecida": true` en ese archivo (crea la carpeta si hace falta; no borres lo que ya tenga). Con **Sí**: abre `guia/leccion-1.md` y síguela. Con **No**: haz directo lo que pidió (si te pidió un relevo, hazlo); si solo instaló, dile en una línea cómo usarla («Usando la skill dak-relevo-chat, haz el relevo»).
- **Si ya está**, no vuelvas a preguntar.
- Frases que abren la guía siempre: «ábreme la guía del relevo», «empieza la guía» (si esta skill es la que se está usando), «retoma la guía» (donde se quedó, campo `leccion`), «guía lección 2», «sal de la guía».
- **Antes de cada lección lee `guia/estilo.md`.** Cada lección es un guion para Claude (lo que dices, **ACCIÓN** y **ALTO**). Nunca sigas sin que la persona conteste.

## Aviso de versión nueva (silencioso)

**No lo corras tú aparte:** los scripts de la skill lo revisan solos al terminar (máximo una vez al día; el resto del día no tarda nada) y casi siempre no dicen nada. Si en la salida de un script ves una línea `NUEVA …`, sigue lo de abajo. Corre los scripts con `python3` normal, sin `-I` (son de la skill, no descargas).

Casi siempre no imprime nada y entonces **no digas ni una palabra del tema**: esta revisión no existe para la persona. Solo imprime si hay una versión más nueva en el repo oficial `dakexplica/dak-relevo-chat`, así: `NUEVA 1.1.0 | qué cambió`. Revisa como máximo una vez al día y, sin internet, se calla.

Si imprimió una línea `NUEVA …`: haz primero el trabajo que te pidieron y, **al final de tu respuesta, en una sola línea**, avisa («Por cierto: hay una versión nueva de Relevo de chat (1.1.0: qué cambió). ¿La actualizo?») con botones **Sí, actualízala** / **Ahora no** (si no existe la herramienta de botones: «responde 1 o 2»).
- **Sí:** dile en una frase qué vas a hacer y actualiza solo desde el repo oficial. Con Claude Code: si `<skill>` está en `~/.claude/skills/`, `npx -y skills add dakexplica/dak-relevo-chat -g -y --agent claude-code`; si está dentro de un proyecto, el mismo comando sin `-g`, desde la carpeta del proyecto. Luego confirma con `python3 <skill>/scripts/version.py --estado` que ya dice la versión nueva. **Si `<skill>` tiene una carpeta `.git`, es la copia de quien la creó: nunca actualices encima.** Si eso no se puede o la instalaron con el .zip en la app de Claude: dile que descargue el `.zip` nuevo en github.com/dakexplica/dak-relevo-chat/releases y lo suba en Configuración → Capacidades → Skills. Nunca instales ni descargues otra cosa.
- **Ahora no:** corre `python3 <skill>/scripts/version.py --omitir <versión>` y no vuelvas a mencionar esa versión (sí la siguiente).
- **Nunca interrumpas una guía ni un relevo en curso con este aviso.** En un relevo, la pregunta de archivar va primero; el aviso de versión, si hay, en el chat nuevo o en el siguiente uso.

## Cuando te piden el relevo

Si estás a media tarea, termina el paso que estás haciendo o déjalo en un punto de corte limpio (nada de archivos a medio editar). Luego todo de corrido, sin preguntar en cada paso: **la única pregunta es la de archivar, al final y con botones**.

### 1. Prepara

```bash
python3 <skill>/scripts/relevo.py preparar "<carpeta>"
```

Te dice: `NOTA:` dónde va la nota (una por proyecto, en `~/.claude/relevos/<proyecto>.md`, fuera del proyecto a propósito: no se cuela en git), `ANTERIOR:` si ya había una (la copia sola al historial, las últimas 10 por proyecto) `PESO:` cuántos tokens vuelve a leer cada respuesta y `NUEVO:` con cuántos arranca uno nuevo. Guarda esos números para el cierre.

### 2. Escribe la nota

Si ya existía una nota, **léela primero con Read** (la herramienta de escribir falla si no la leíste) y, si trae algo de otro tema del mismo proyecto que siga vivo, intégralo. Luego escríbela con esta plantilla:

```markdown
# Relevo — <proyecto> — <tema en pocas palabras>
<fecha AAAA-MM-DD HH:MM> · carpeta: <ruta completa> · modelo: <modelo del chat>

## En qué estamos
<2-4 líneas: el objetivo de este trabajo y en qué punto exacto quedó>

## Qué se hizo en este chat
- <cambios concretos, con rutas de archivo>

## Decisiones (y por qué)
- <decisión> — <razón>. Incluye lo que la persona pidió o rechazó explícitamente.

## Lo que NO funcionó (no repetir)
- <qué se intentó y por qué falló>

## Siguiente paso exacto
<lo primero que debe hacer el chat nuevo, tan concreto que se pueda arrancar sin preguntar>

## Pendiente de la persona
- <lo que espera una respuesta o acción suya; "nada" si no hay>
```

Reglas de la nota, y por qué:
- **Nada que ya esté en el CLAUDE.md o el archivo de estado.** El chat nuevo los lee solo; repetirlo es pagar dos veces.
- **Rutas exactas y nombres reales** (archivos, funciones, URLs, comandos). El chat nuevo no vio nada; "el archivo que arreglamos" no le sirve.
- **Lo que falló importa tanto como lo que funcionó.** Sin eso, el chat nuevo repite los mismos intentos.
- **Cero secretos.** Nunca copies contraseñas, tokens, llaves ni valores de `.env`; nombra dónde están si hace falta.
- **Corta:** 30-80 líneas. Si una sección no aplica, quítala.

### 3. Guarda lo duradero en el estado del proyecto

Si el proyecto tiene archivo de estado (`ESTADO-ACTUAL.md`, `PROGRESO.md`, `COMO FUNCIONA.md`…) y en este chat pasó algo que importa más allá de mañana (algo quedó terminado, cambió cómo funciona algo, una decisión de fondo), actualízalo en el mismo tono que ya usa. Si no existe, no lo crees. La nota es para el siguiente chat; el estado es la memoria de largo plazo.

### 4. Abre el chat nuevo, desde cero

Según dónde estés:

**a) App de escritorio de Claude (existe la herramienta para iniciar sesiones, `mcp__ccd_session__start_session`; si está diferida, cárgala con ToolSearch junto con `mcp__ccd_session_mgmt__get_session`, `mcp__ccd_session_mgmt__detach_session` y `mcp__ccd_session_mgmt__archive_session`, en UNA sola búsqueda):**
1. Averigua el id de este chat: `get_session` con `"self"`.
2. `start_session` con: `initiation` `"user_asked"` · **`context` `"fresh"`, siempre** (nunca `"fork"`: copia toda la conversación, que es justo el peso del que huimos) · `use_worktree` `false` (misma carpeta) · `title` `<Proyecto> — <tema>` · `model` solo si la persona pidió otro. Brief:
   > Vienes de un relevo: este trabajo empezó en otro chat que se puso pesado (id `<id de este chat>`). Lee primero la nota de relevo `<ruta de la nota>`, luego el CLAUDE.md y el archivo de estado del proyecto. Después di en 3-5 líneas en qué van y cuál es el siguiente paso, y pregunta si arrancas. Si el chat anterior sigue abierto (revísalo con `get_session`), termina ese primer mensaje con una línea: «El chat anterior sigue abierto; si quieres lo archivo desde aquí, dime «archívalo»». Con eso, archívalo con `archive_session`.
3. **En cuanto arranque, sepáralo:** `detach_session` con su id. Así no te despierta con avisos que entierran la pregunta de archivar, y si archivas este chat el nuevo no se archiva con él.

Si la app se niega a abrirlo (pasa cuando el turno lo empezó un aviso automático y no un mensaje de la persona), no preguntes por archivar: deja el relevo listo y, en el siguiente mensaje de la persona, abre el chat y sigue con el paso 5.

**b) Terminal (Claude Code sin esa herramienta):** dile que escriba `/clear` aquí mismo o que abra `claude` en la misma carpeta. Con el arranque automático instalado, el chat nuevo recoge la nota solo; sin él, que pegue una línea: `Lee <ruta de la nota> y seguimos.`

**c) App de Claude (claude.ai, sin archivos entre chats):** la nota no puede guardarse en disco. Escríbela completa en un bloque de código para copiar y di: "Abre un chat nuevo (dentro del mismo Proyecto, si usas Proyectos), pega esto y escribe «seguimos»."

### 5. Archivar el chat viejo (solo en la app de escritorio)

**Siempre con botones, nunca como frase suelta al final** (una frase suelta se pierde entre los avisos de la app). Pregunta con todo el contexto dentro de la pregunta:

> "Ya abrí el chat nuevo «<título>» con la nota. ¿Archivo este? Si se queda abierto, cada vez que lo abras y le escribas vuelve a leer <peso> tokens."
> **Sí, archívalo** · **Déjalo abierto**

Sin herramienta de botones: la misma pregunta como **última línea de tu mensaje**, con "responde 1 o 2".

- **Sí:** primero escribe el cierre (paso 6, porque al archivar este chat ya no puedes escribir), luego `archive_session` con `"self"`. Si la app te pide repetir la llamada con el campo `session` que ella misma te da, repítela una vez exactamente así.
- **Déjalo abierto:** el cierre y listo.

### 6. Cierra corto

3-4 líneas: el link al chat nuevo (o qué hacer en la terminal), dónde quedó la nota, si se actualizó el archivo de estado, y el número del paso 1: *"Aquí cada respuesta volvía a leer ~435 mil tokens; el nuevo arranca con ~150 mil: casi 3 veces menos."* Nada más: cada palabra extra en este chat cuesta.

## Cuando aparece el aviso del medidor (automático)

El medidor (`scripts/medidor.py`) mete en el contexto una línea que empieza con `[medidor dak-relevo-chat]`. La persona no la ve; es para ti. Tú decides **cuándo** decirlo, pero **siempre lo dices**:

- **Decide como una persona, no con un número fijo.** Avisa cuando se juntan dos cosas: el chat ya va avanzado (≈45 % de su espacio, como la barra "Contexto" de la app) **y** cambiar ahorra de verdad en ESA cuenta: cada mensaje cuesta 3 veces o más que en un chat nuevo de esa misma persona (alguien con muchos conectores arranca pesado y le conviene más tarde; alguien ligero, antes). **Aprende de la persona:** cada «ahora no» hace que la siguiente vez espere más; cada «sí» lo regresa. Y un tope de seguridad: al 80 % (o si ya se compactó) avisa siempre, porque está por resumirse solo y perder detalle. Un chat que apenas empezó a trabajar no avisa.
- **No lo ofrezcas por tu cuenta** si el medidor está instalado: él decide cuándo; tú, el momento exacto.
- **Un relevo por fase, no varios para el mismo tema.** Si lo que sigue es parte de la misma tarea y aún cabe, espera a terminarla. El mejor momento: acabas de cerrar algo, o la persona cambia de tema o de fase.
- **Nunca a media tarea.** Termina lo que estás haciendo.
- **Al cerrar algo**, al final de esa respuesta, ofrécelo en UNA línea que **empiece con 🔄** (la marca es obligatoria: así el medidor sabe que ya lo ofreciste y deja de recordártelo). Si tienes botones o un cierre de turno con botones, úsalos: con los números dentro: *"🔄 Este chat ya está pesado: cada respuesta vuelve a leer ~300 mil tokens; uno nuevo arranca con ~60 mil. ¿Lo paso a un chat nuevo?"* · **Sí, pásalo a un chat nuevo** · **Ahora no**. Que quede claro a qué dice que sí: a pasar el trabajo a un chat nuevo sin perder nada.
- **Si se te pasó**, el medidor te lo recuerda en el siguiente mensaje ("Sigue pendiente…"): ofrécelo en cuanto cierres algo.
- **Una vez por aviso.** Si dice que no, no insistas: el medidor solo vuelve a avisar si el chat sube al siguiente nivel; ese segundo aviso dilo más claro.
- Con el sí, sigue los pasos de arriba.

Todo se ajusta solo. Si alguien quiere tocarlo, en `~/.dakexplica/dak-relevo-chat.json`: `"aviso_1_pct"` (0.45), `"aviso_1_veces"` (3), `"aviso_2_pct"` (0.8), `"ventana"` (cuánto cabe; si no se pone, lo deduce: 200 mil o 1 millón), `"aprendido": {"paciencia": 0-4}` (lo que aprendió) o `"medidor": false` para apagarlo.

## Cuando aparece el aviso de arranque (automático)

Si al abrir un chat ves `[dak-relevo-chat] En esta carpeta hay una nota de relevo…`, lee la nota antes de responder. Si el primer mensaje tiene que ver con ese trabajo (o es un saludo, «seguimos», «¿en qué íbamos?»), arranca con las 3-5 líneas de en qué iban y el siguiente paso. Si pide otra cosa, hazla y menciona la nota en una línea al final. Si `~/.dakexplica/dak-relevo-chat.json` tiene `"pendiente": "leccion-3-en-chat-nuevo"`, la persona viene de la guía: sigue con `guia/leccion-3.md`.

## "¿En qué íbamos?" y el historial

- «¿En qué íbamos?» / «seguimos»: `python3 <skill>/scripts/relevo.py ruta "<carpeta>"` te dice dónde está la nota (sin tocar nada); léela y resume en 3-5 líneas.
- «¿Qué hicimos la vez pasada / la semana pasada?»: `python3 <skill>/scripts/relevo.py historial "<carpeta>"` lista las últimas 10 notas; lee las que hagan falta.

## Archivos de la skill

| Archivo | Para qué |
|---|---|
| `scripts/relevo.py` | Paso 0, instalar/quitar los avisos, preparar la nota, medir el peso, historial |
| `scripts/medidor.py` | Aviso automático cuando el chat ya pesa (insiste hasta que se ofrece con 🔄) |
| `scripts/al_abrir.py` | Arranque automático: el chat nuevo recoge la nota solo |
| `scripts/comun.py` | Piezas compartidas (nombre del proyecto, medir un chat, configuración) |
| `scripts/version.py` | Aviso silencioso de versión nueva (solo habla si hay una; `--omitir X` = «ahora no») |
| `version.json` · `CHANGELOG.md` | La versión instalada y qué cambió en cada una |
| `guia/` | La mini guía: `estilo.md` + 3 lecciones |
