# Sesión en vivo

Durante la sesión la app de Spotify reproduce la música y Spin Coach lleva el reloj, salta los temas recortados y habla por encima bajando el volumen de la música.

## Reproducción

- Se inicia la playlist de la combinación desde el primer tema con el **App Remote SDK** (contexto de playlist: la pantalla de bloqueo y el coche muestran «Spin · …»).
- La app conoce el plan exacto (`PistaSesion`): orden, inicio y fin de cada tema.
- **Recortes**: cuando un tema llega a su `fin_reproduccion_s`, la app baja el volumen en 3 s y salta al siguiente.
- **Cambios de bloque**: coinciden con cambios de tema por diseño, así la música refuerza la indicación.

## Sincronización

- El reloj de la sesión es el de la app; la posición de Spotify se usa para corregirlo.
- Se escucha el estado del reproductor del App Remote (eventos de cambio de tema, pausa y posición) y, de respaldo, se consulta cada 5–10 s.
- **Pausa** en Spotify o en la app → se pausa el reloj y el guion del coach.
- **Salto de tema** manual → se recalcula en qué fase está la sesión. «Saltar bloque» en la app salta al primer tema de la siguiente fase.
- Objetivo: desfase < 5 s en una sesión de 60′.

## Voz del coach

### Guion

Se genera antes de empezar, como lista de eventos `(t, texto, prioridad)` a partir de la receta:

| Evento | Cuándo | Ejemplo |
|---|---|---|
| Aviso de cambio | 10 s antes de cada fase | «En 10 segundos, de pie» |
| Cuenta atrás | 3-2-1 antes del cambio | «Tres, dos, uno… ¡arriba!» |
| Indicación de bloque | Al empezar la fase | Frase tipo del bloque (`frase_coach`) + rueda objetivo |
| Intervalos | Cada cambio trabajo/descanso dentro de I30/I40/I20 | «¡Ya!» · «Suelta» |
| Ánimo | Cada 2 o 4′ (configurable) o nunca | «Mantén el ritmo con el bombo» |
| Última subida | Al entrar en el remate | «Última subida, rueda 8 o 9, la que puedas» |

Las frases variables (ánimos, indicaciones) pueden generarse con un LLM para que no suenen siempre igual. Estilos: energética, tranquila, técnica.

### Síntesis

- **Frases del guion**: TTS de calidad (OpenAI o ElevenLabs) generado antes de empezar y cacheado.
- **Frases de intervalo** («¡ya!», «suelta», cuenta atrás): clips cortos pregrabados y reutilizados, porque necesitan precisión al segundo.
- **Respaldo**: voz del sistema si no hay red o falla el servicio.

### Mezcla de audio (*ducking*)

- iOS: sesión de audio con `.duckOthers` mientras habla el coach; al terminar, se desactiva para devolver el volumen a Spotify.
- La app necesita el modo de audio en segundo plano para seguir hablando con la pantalla bloqueada. **Es el principal riesgo técnico**: se valida en la fase 0.

## Pantalla en sesión

Bloque actual y cuenta atrás en grande, cadencia y rueda objetivo, última frase del coach, próximo cambio, tema actual con su BPM y relación de pedalada, y tres controles: silenciar voz, pausa y saltar bloque.

## Términos de Spotify

Superponer voz propia a la música de Spotify es aceptable para uso personal. Si el proyecto se convirtiera en producto, los términos de desarrollador de Spotify son restrictivos con mezclar su contenido con el propio y habría que revisarlos.
