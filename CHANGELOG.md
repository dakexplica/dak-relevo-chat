# Qué cambió

## 1.0.3
- Si pides un relevo y tu chat todavía está ligero, te lo dice con números y te pregunta si lo hace igual.
- La guía en un chat recién abierto: avisa «ya sé que no está pesado» y te enseña cómo funciona con un relevo de práctica.
- Si pides un relevo la primera vez y tu chat sí pesa, lo hace primero; la guía se ofrece después.
- El medidor no avisa antes de ~100 mil tokens.

## 1.0.2
- Mide tu chat desde el primer momento, aunque los avisos se acaben de instalar.
- Si tu chat todavía está ligero (por ejemplo, al hacer la guía en un chat nuevo), te lo dice tal cual y te enseña un ejemplo real de uno pesado.

## 1.0.1
- Se instala bien con `npx skills add dakexplica/dak-relevo-chat` (la 1.0.0 no la reconocía el instalador).

## 1.0.0
- Primera versión pública: pasa tu trabajo a un chat nuevo y limpio sin perder el hilo. Medidor inteligente que se adapta a tu cuenta, aprende de tus «ahora no» y te avisa con números solo cuando conviene, arranque automático que recoge la nota en el chat nuevo, historial de las últimas 10 notas, pregunta de archivar con botones, mini guía de ~5 min y aviso silencioso de versiones nuevas.

> Cada vez que subimos una versión, cambian dos cosas: el número en `version.json` y este archivo. La skill avisa de una versión nueva **solo si existe**; si no hay, no dice nada.
