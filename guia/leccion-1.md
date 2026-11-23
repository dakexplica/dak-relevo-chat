# Lección 1 · Déjalo listo y mide tu chat (~1-2 min)

> Guion para Claude. Antes lee `guia/estilo.md`. Entre comillas va la idea de lo que dices (con tus palabras). **ACCIÓN** = lo haces tú. **BOTONES** = pregunta con `AskUserQuestion` (opciones para hacer clic; si no existe la herramienta, una lista numerada corta). **ALTO** = esperas. Nunca sigas sin respuesta. Progreso en `~/.dakexplica/dak-relevo-chat.json`.

## 1 · Bienvenida (tu PRIMER mensaje, antes de cualquier botón o comando)

**Regla dura:** lo primero que ve la persona es esta bienvenida, como mensaje propio, y **con ella TERMINAS tu turno**. Nada de narrar lo que haces ni hablar de la persona en tercera persona. El Paso 0 corre después y en silencio.

**ACCIÓN:** escribe este mensaje (con tus palabras, sin quitar ninguna parte):

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  RELEVO DE CHAT
  ▰▱▱  Lección 1 de 3 · Déjalo listo y mide tu chat
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

> **¡Hola, [nombre]! Bienvenido a la guía 👋**
> En unos 5 minutos vas a ver cuánto pesa tu chat, hacer tu primer relevo y comprobar que el chat nuevo sabe exactamente en qué íbamos.
>
> *"La hice porque mis chats se ponían lentos a media obra y me daba miedo abrir otro y perderlo todo. Ahora cambio de chat en segundos y el nuevo sigue donde íbamos." — @dakexplica*
>
> Son 3 pasos cortos. Te enseño lo que pasa por dentro; cuando la uses normal, hace todo esto **sola**.

- **Cómo termina:** si no sabes su nombre, el saludo es "¡Hola! Bienvenido a la guía 👋" y cierra con **"Antes de empezar, ¿cómo te llamo?"**. Si ya lo sabes, cierra con **"Cuando estés listo, escríbeme «vamos»."** **ALTO** (fin del turno). Guarda `nombre`.

**En tu siguiente turno**, después de reaccionar en una línea ("¡Mucho gusto, [nombre]!"), los **BOTONES** (dos preguntas en la misma ventana; lo importante dentro de la pregunta):
1. "¿Dónde usas Claude casi siempre?" (si ya lo sabes por tus herramientas, no lo preguntes: dilo tú en una línea)
   - **La app de escritorio (Claude Code)**: "abro el chat nuevo yo solo"
   - **La terminal**: "escribes /clear y el chat nuevo sigue solo"
   - **claude.ai o la app del celular**: "te dejo la nota lista para pegar"
2. "¿Qué te pasa más cuando un chat se hace largo?" (no escribas para qué preguntas)
   - **Se pone lento**
   - **Se le olvidan cosas o se equivoca más**
   - **Se me acaba el plan muy rápido**
   - **Todo lo anterior**

**ALTO.** Reacciona en una línea a lo que eligió ("Lo del plan es lo que más se nota: cada mensaje vuelve a leer todo el chat"). Guarda `donde` y `objetivo`.

## 2 · Paso 0 y los dos avisos (solo en Claude Code: app de escritorio o terminal)

**ACCIÓN:** `python3 <skill>/scripts/relevo.py paso0`. Si los dos avisos ya están ✓: una línea ("Ya tienes todo listo: el medidor y el arranque automático").

Si falta alguno, **BOTONES** con todo dentro de la pregunta:
"¿Te instalo los dos avisos automáticos? El **medidor** mira en silencio cuánto pesa tu chat y te avisa cuando conviene cambiar; el **arranque automático** hace que el chat nuevo recoja la nota solo. Tocan tu configuración de Claude Code: guardo un respaldo antes y se quitan con una frase."
- **Sí, instálalos (recomendado)**
- **No, solo cuando lo pida**: "la skill funciona igual, solo no te avisa"

Con sí: `python3 <skill>/scripts/relevo.py instalar` y dile dónde quedó el respaldo. **ALTO** solo si hubo que preguntar.

En claude.ai: sáltate este paso y di en una línea: "Aquí no hay avisos automáticos; el relevo te lo hago cuando me lo pidas y te dejo la nota para pegar."

## 3 · Mide tu chat (el momento "ajá")

**Antes, avisa:** "Ahora mido cuánto pesa este chat."

**ACCIÓN:** `python3 <skill>/scripts/relevo.py peso "<carpeta>"`. (Si sale "sin medir" porque el medidor se acaba de instalar, explica que mide desde el siguiente mensaje y usa el número en la lección 2.) En claude.ai no hay número: explica la idea con palabras.

## 4 · Lo que encontré (MENSAJE obligatorio que CIERRA el turno, sin botones)

> **Listo, [nombre]. Esto pesa tu chat ahora mismo.**
>
> **Resultado**
> - Cada mensaje que me mandas, vuelvo a leer **[peso actual]** tokens antes de contestar.
> - Un chat nuevo arrancaría con **[peso inicial]**.
> - Lo que te preocupaba ([objetivo]): [cómo se conecta con ese número, en una frase: "por eso se te acaba el plan: cada mensaje paga todo lo anterior"].
>
> Y entre más crece, más le cuesta encontrar lo importante: por eso se le olvidan cosas.
>
> **Lo que lograste**
> - Lo dejaste listo[ con los avisos automáticos].
> - Viste por qué un chat largo se vuelve lento y caro.
>
> **Lo que sigue:** en el paso 2 haces tu primer relevo: me pides cambiar de chat y el nuevo arranca sabiendo en qué íbamos, sin copiar nada.

> **¿Seguimos?** Escríbeme **«sigue»**. Si prefieres dejarlo aquí, cuando quieras me dices «retoma la guía».

**ALTO** (fin del turno).

**ACCIÓN:** guarda en `~/.dakexplica/dak-relevo-chat.json`: `nombre`, `donde`, `objetivo`, `leccion: 1` (sin borrar lo que ya tenga).
