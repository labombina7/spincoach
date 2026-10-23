# Plan y riesgos

## Fases

Cada fase termina con un criterio comprobable. La fase 0 existe para matar pronto los tres riesgos que podrían tumbar el proyecto.

| Fase | Alcance | Criterio de salida |
|---|---|---|
| 0 · Pruebas de concepto | OAuth + App Remote reproduciendo una playlist · BPM de ReccoBeats sobre la biblioteca real · voz con *ducking* sobre Spotify con la pantalla bloqueada | ≥ 80 % de la biblioteca con BPM · 60′ de voz sobre Spotify en segundo plano sin cortes |
| 1 · Datos | Importación, BPM en segundo plano, carga de `data/*.json`, mezclas sugeridas y manuales | Biblioteca importada y mezclas creadas desde la app |
| 2 · Motor y playlists | Generación por bloque, combinaciones, renovación con diff | «Renovar» crea o actualiza la playlist y cada fase cuadra a ±90 s |
| 3 · Sesión en vivo | Pantalla en sesión, reloj, saltos por recorte, guion y voz del coach | Sesión de 60′ completa con desfase < 5 s |
| 4 · Cobertura | Regla de cobertura contra 60′ y ampliación con Last.fm | Una combinación corta se amplía sola y lo muestra en la renovación |
| 5 · Pulido | Resumen post-sesión, historial, editor de bloque | — |

## Riesgos

| Riesgo | Impacto | Mitigación |
|---|---|---|
| Spotify recorta más la API (ya lo hizo en nov. 2024 y feb. 2026) | Alto | Estado local, un único cliente de Spotify, solo endpoints básicos |
| ReccoBeats no cubre la biblioteca o desaparece | Alto | Medir cobertura en fase 0 · caché permanente · alternativa Tunebat (de pago) |
| iOS corta el audio de la app en segundo plano | Alto | Fase 0 · sesión de audio activa durante toda la sesión |
| Errores de BPM (doble o mitad) | Medio | Encaje con ×2 y ÷2 · quitar el tema desde Spotify lo descarta |
| Desfase entre reloj y reproducción | Medio | Eventos del App Remote + consulta periódica · cambios de bloque en límites de tema |
| Términos de Spotify sobre superponer voz | Bajo en uso personal | Revisar si pasa a producto |
| Límite de 5 usuarios y Premium del propietario | Bajo en uso personal | Asumido |
| Condiciones de Last.fm para uso comercial | Bajo | Solo uso personal en v1 |

## Preguntas abiertas

- Plataforma: iOS nativo (recomendado) o React Native. Ver [Arquitectura](arquitectura.md).
- ¿Se permite corregir a mano el BPM de un tema?
- ¿Tipo «Recuperación» en una versión posterior?
- ¿Bloque de «saltos» (alternar sentado/de pie cada 4–8 tiempos)?
