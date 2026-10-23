# Spin Coach · contexto para Claude Code

App iOS de uso personal para sesiones de spinning: música del Spotify del usuario ajustada por BPM a cada bloque del entrenamiento + coach de voz. Toda la especificación está en `docs/` (empieza por `README.md` y `docs/fase-0.md`).

## Estado

Fase 0 (pruebas de concepto). Prueba 2 (cobertura de BPM) hecha con `tools/bpm_coverage.py`. **Pendientes: pruebas 1 y 3** (ver `docs/fase-0.md`):
1. App mínima que reproduce una playlist con el App Remote SDK de Spotify.
3. Voz (AVSpeechSynthesizer) cada 60 s sobre la música con *ducking*, 60′ con la pantalla bloqueada.

## Stack y decisiones

- iOS nativo, **Swift + SwiftUI**, iOS 17+. El código va en `ios/`.
- Spotify: OAuth PKCE (sin client secret), redirect `spincoach://callback`, App Remote SDK oficial (`spotify/ios-sdk`). El App Remote **no funciona en el simulador**: probar en iPhone real con la app de Spotify instalada y cuenta Premium.
- Client ID de Spotify: lo aporta el usuario; **no subirlo al repo** (usar un `.xcconfig` ignorado por git o similar).
- BPM: ReccoBeats `GET https://api.reccobeats.com/v1/audio-features?ids=<spotify ids>`; exige un User-Agent propio (bloquea el de Python/por defecto con 403 Cloudflare 1010).
- Restricciones de Spotify vigentes (feb. 2026): ver `docs/spotify.md` (sin endpoints por lotes, sin top-tracks, búsqueda máx. 10, playlists `/items`).
- Catálogo de entrenamiento: `data/bloques.json` y `data/recetas.json` (fuente editable: `data/recetas.xlsx`).

## Cómo trabajar en este repo

- Documentación y mensajes en **español**.
- Cada decisión relevante se añade arriba en `docs/decisiones.md` (número, fecha, decisión, motivo).
- Los resultados de pruebas de la fase 0 se anotan en la tabla «Resultados» de `docs/fase-0.md`.
- El usuario es PM con formación de ingeniero informático: explica las decisiones técnicas a nivel de arquitectura y dile exactamente qué tiene que hacer él en Xcode o en el iPhone cuando haga falta.
- Compila con `xcodebuild` para comprobar errores antes de pedirle que pruebe en el dispositivo.
