# Relevo de chat · dak-relevo-chat

¿Tus chats largos con Claude te gastan tokens, se ponen lentos o se le olvidan cosas? Es porque **cada vez que Claude responde vuelve a leer todo el chat**: entre más largo, más tokens gasta cada mensaje. Esta skill pasa tu trabajo a un **chat nuevo y limpio** sin perder el hilo: deja una nota de relevo corta (solo lo que importa), abre el chat nuevo y ese chat arranca sabiendo exactamente en qué ibas.

- **Medidor:** te avisa solo cuando el chat ya pesa, con números ("cada respuesta vuelve a leer ~300 mil tokens; uno nuevo arranca con ~60 mil. ¿Lo paso a un chat nuevo?"), y nunca a media tarea.
- **Arranque automático:** el chat nuevo recoge la nota solo, aunque lo abras a mano o uses `/clear`.
- **Historial:** guarda las últimas 10 notas de cada proyecto. Pregunta «¿qué hicimos la vez pasada?».
- En la app de escritorio abre el chat nuevo y te pregunta con botones si archiva el viejo.

Incluye una **mini guía interactiva** de unos 5 minutos (3 pasos): mides tu chat, haces tu primer relevo y ves que el chat nuevo sabe todo.

Hecha por [@dakexplica](https://www.tiktok.com/@dakexplica) · Gratis.

## Lo que necesitas
- **Claude Code** (app de escritorio o terminal). También sirve en la app de Claude (claude.ai), sin los avisos automáticos: ahí te deja la nota lista para pegar.
- **Python 3.7 o más nuevo** (viene en Mac).
- Nada más. La skill revisa si tienes todo y **te pide permiso** antes de instalar los avisos automáticos.

## Instálala

**Con Claude Code**, pega esto:

```
Instala la skill dakexplica/dak-relevo-chat con `npx skills add dakexplica/dak-relevo-chat`, revisa con su Paso 0 si me falta algo (pídeme permiso antes de instalar) y cuando esté lista, pregúntame si quiero la guía.
```

O el comando directo:

```bash
npx skills add dakexplica/dak-relevo-chat
```

**En la app de Claude:** descarga el `.zip` de la última versión (Releases, a la derecha) y súbelo en **Configuración → Capacidades → Skills → Subir skill**.

## Actualizaciones
Esta skill **no se actualiza sola**, pero te avisa. Cuando empiezas a usarla, mira (en silencio, máximo una vez al día) si hay una versión nueva en este repositorio. **Si no la hay, no dice nada.** Si la hay, al final de lo que le pediste te avisa en una línea y te pregunta si la actualiza; si dices «ahora no», no vuelve a mencionar esa versión. Nunca descarga nada sin tu permiso. Lo que cambia en cada versión está en [CHANGELOG.md](CHANGELOG.md).

También puedes actualizarla tú cuando quieras: dile a Claude «actualiza la skill dak-relevo-chat» o vuelve a correr `npx skills add dakexplica/dak-relevo-chat`, o descarga el `.zip` más reciente en **Releases**.

## Úsala

```
Usando la skill dak-relevo-chat, haz el relevo
```

También entiende «relevo», «cambiemos de chat» o «este chat ya está pesado».

## Qué es gratis y qué cuesta
La skill es gratis. Corre en tu compu y no usa internet. Al contrario: te **ahorra** plan, porque cada mensaje en un chat nuevo cuesta mucho menos que en uno largo.

## ¿Algo falla?
- **No me avisa solo:** dile a Claude «corre el Paso 0 del relevo» y acepta instalar los avisos.
- **Me avisa muy pronto o muy tarde:** cambia `aviso_1` y `aviso_2` en `~/.dakexplica/dak-relevo-chat.json` (tokens; por defecto 150000 y 300000), o pon `"medidor": false` para apagarlo.
- **Quitar los avisos:** `python3 ~/.claude/skills/dak-relevo-chat/scripts/relevo.py desinstalar`.
- **Quiero la guía otra vez:** «ábreme la guía del relevo».

## Licencia
MIT.
