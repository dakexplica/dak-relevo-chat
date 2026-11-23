# Lección 2 · Tu primer relevo (~2 min)

> Guion para Claude. Antes lee `guia/estilo.md` y retoma `nombre`, `donde` y `objetivo` de `~/.dakexplica/dak-relevo-chat.json`. **ACCIÓN** = lo haces tú. **BOTONES** = `AskUserQuestion`. **ALTO** = esperas.

## 1 · Abre (UN mensaje que cierra el turno)

Cuando diga «sigue»:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  RELEVO DE CHAT
  ▰▰▱  Lección 2 de 3 · Tu primer relevo
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

[Si en la lección 1 salió LIGERO, empieza con el anuncio, en una línea:] **"Ya sé que este chat apenas empieza y no está pesado; igual lo hacemos para que lo veas funcionando. Cuando un chat sí pese, es exactamente igual."**

"Ahora lo más importante, [nombre]. El truco no es copiar la conversación (eso sería llevarte todo el peso). Es dejar una **nota de relevo** corta, solo con lo que vive en este chat: en qué vamos, qué decidimos, qué no funcionó y el siguiente paso. Lo demás (tu proyecto, sus archivos) el chat nuevo ya lo puede leer."

"Pídemelo tú, una sola vez, para que veas lo fácil que es. Copia y pega esto:"

```
Usando la skill dak-relevo-chat, haz el relevo
```

"Así se lo pides siempre, aunque no estés en la guía. (También entiendo «relevo» a secas o «este chat ya está pesado».)"

**ALTO.** (Es el único momento de la guía donde se escribe.)

## 2 · El relevo de verdad

**Antes de empezar, guarda** en el json: `leccion: 2`, `pendiente: "leccion-3-en-chat-nuevo"`. Así el chat nuevo sabe que sigue la lección 3.

**ACCIÓN:** haz el relevo completo como dice `SKILL.md` (pasos 1 a 6), con este chat como el trabajo:
- Si el chat está ligero (lo normal en la guía), dilo en media línea: "Aunque este chat está ligero, practicamos con él: así ves cómo pasa todo al chat nuevo." La nota cuenta esta guía: "Guía de dak-relevo-chat con [nombre]. Usa Claude en [donde]; lo que le preocupa: [objetivo]. Hechas la lección 1 y 2. Siguiente paso exacto: seguir con `guia/leccion-3.md` de la skill dak-relevo-chat." Si la persona estaba trabajando en algo suyo en este chat, inclúyelo también: es su relevo real.
- Antes de escribir la nota, avisa en una línea: "Escribo la nota de relevo y abro el chat nuevo. Unos segundos."
- Después, muéstrale la nota en un bloque corto (las secciones con 1 línea cada una), para que vea qué se lleva el chat nuevo.

Según `donde`:
- **App de escritorio:** abre el chat nuevo (paso 4a). En el brief agrega: "Estás en la guía de dak-relevo-chat: sigue con `guia/leccion-3.md` (empieza por el paso 1 de esa lección)."
- **Terminal:** "Escribe `/clear` aquí mismo. El chat se vacía, pero el nuevo recoge la nota solo y seguimos con el paso 3. (Si no instalaste el arranque automático, después del /clear pega: `Lee <ruta de la nota> y seguimos con la guía.`)"
- **claude.ai:** la nota completa en un bloque para copiar, con la última línea "Sigue con la lección 3 de la guía de dak-relevo-chat." y: "Abre un chat nuevo, pega esto y escribe «seguimos»."

## 3 · Cierre (en la app de escritorio, con la pregunta de archivar)

**App de escritorio:** el mensaje de cierre, corto, **antes** de los botones de archivar no sirve (se resume): mete todo dentro de la pregunta de archivar (paso 5 de `SKILL.md`):
"Listo, [nombre]: el chat nuevo «[título]» ya arrancó con la nota y ahí sigue el paso 3. Aquí cada respuesta vuelve a leer [peso actual] tokens; el nuevo arranca con [peso inicial]. ¿Archivo este?" · **Sí, archívalo** · **Déjalo abierto**. Con la respuesta, haz lo que dice el paso 5 (el cierre de 2-3 líneas va antes de archivar).

**Terminal y claude.ai:** cierra con:
> **Lo que lograste**
> - Hiciste tu primer relevo: la nota lleva lo que importa, nada del peso.
> - El chat nuevo va a arrancar con [peso inicial] en vez de [peso actual].
>
> **Lo que sigue:** el paso 3 ya es en el chat nuevo. Ahí vas a ver que sé en qué íbamos sin que me lo repitas.

**ALTO** (fin del turno).
