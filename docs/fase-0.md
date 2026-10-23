# Fase 0 · Pruebas de concepto

Objetivo: comprobar antes de construir que las tres piezas de las que depende todo funcionan en tu iPhone con tu cuenta. Si alguna falla, se cambia el plan aquí y no a mitad del desarrollo.

| # | Prueba | Criterio de éxito | Cómo |
|---|---|---|---|
| 1 | Reproducir una playlist con el App Remote SDK desde una app Swift | Reproduce, pausa, salta tema y lee la posición | App mínima en Xcode |
| 2 | Cobertura de BPM de tu biblioteca en ReccoBeats | ≥ 80 % de temas con BPM y recetas de 60′ cubiertas | [`tools/bpm_coverage.py`](../tools/bpm_coverage.py), sin Xcode |
| 3 | Voz sobre Spotify con la pantalla bloqueada | 60′ con avisos cada minuto, sin cortes y con el volumen de Spotify bajando al hablar | La misma app de la prueba 1 |

## Preparación (una vez)

### Spotify Developer Dashboard

1. Entra en [developer.spotify.com/dashboard](https://developer.spotify.com/dashboard) con tu cuenta Premium y crea una app «Spin Coach».
2. APIs: marca **Web API** e **iOS**.
3. Redirect URIs:
   - `spincoach://callback` (la app de iOS)
   - `http://127.0.0.1:8888/callback` (el script de la prueba 2; Spotify no acepta `localhost`)
4. En la configuración de iOS indica el **Bundle ID** que usarás en Xcode, p. ej. `com.labombina7.spincoach`.
5. En «User Management» añade tu propio email (modo desarrollo: máx. 5 usuarios).
6. Copia el **Client ID**. No hace falta el Client Secret: usamos PKCE.

### Proyecto en Xcode

1. Nuevo proyecto **iOS App**, interfaz **SwiftUI**, nombre `SpinCoach`, el Bundle ID del paso anterior, iOS 17 como mínimo. Guárdalo en `ios/` dentro de este repositorio.
2. Añade el SDK de Spotify para iOS (repositorio `spotify/ios-sdk` en GitHub), por Swift Package Manager si la versión lo permite o arrastrando `SpotifyiOS.xcframework`.
3. `Info.plist`:
   - URL Types → esquema `spincoach` (para volver de la autorización).
   - `LSApplicationQueriesSchemes` → `spotify` (para abrir la app de Spotify).
4. Signing & Capabilities → **Background Modes** → *Audio, AirPlay, and Picture in Picture* (prueba 3).
5. Prueba siempre en el **iPhone real** con la app de Spotify instalada: el App Remote no funciona en el simulador.

## Prueba 2: cobertura de BPM

Se puede hacer ya, desde la terminal del Mac:

```bash
export SPOTIFY_CLIENT_ID=<tu client id>
python3 tools/bpm_coverage.py
```

Abre el navegador para autorizar, importa tus canciones guardadas y tus playlists propias, consulta el BPM en ReccoBeats y muestra:

- % de temas con BPM (objetivo ≥ 80 %);
- minutos de música que encajan en cada uno de los 13 bloques;
- si con toda tu biblioteca se cubren las recetas de 60′ de cada tipo (regla de 1,5×).

API de ReccoBeats confirmada el 23-10-2026: `GET https://api.reccobeats.com/v1/audio-features?ids=<IDs de Spotify>`, sin autenticación; cada elemento de `content` trae `href` (enlace al tema en Spotify) y `tempo`. **Rechaza (403, error 1010 de Cloudflare) el User-Agent por defecto de Python**: hay que enviar uno propio, también desde la app iOS. El nº máximo de IDs por petición sigue por confirmar (el script usa 40). El script guarda una respuesta cruda en `tools/out/reccobeats_muestra.json`. Los resultados (`tools/out/`) no se suben al repositorio.

### Resultado de la primera ejecución (23-10-2026)

- 459 temas importados, **251 con BPM en ReccoBeats (55 %)**, por debajo del objetivo del 80 %.
- Los huecos están repartidos por todos los lotes (ningún lote vacío): no es un fallo de las peticiones, sino **temas que no están en el catálogo de ReccoBeats**, concentrados en música en español (Pablo López, Pereza, Love of Lesbian…).
- Aun así, con toda la biblioteca se cubren las 4 recetas de 60′.
- Siguiente paso: probar [GetSongBPM](https://getsongbpm.com/api) como segunda fuente solo para los temas sin BPM (búsqueda por título y artista). Es gratuita con clave, a cambio de enlazarles desde la app. El script ya la usa si existe `GETSONGBPM_API_KEY`.
- Estado (23-10-2026): solicitada la clave con backlink en [labombina7.github.io/spincoach](https://labombina7.github.io/spincoach/) (GitHub Pages desde `/docs`). Pendiente de que llegue por email; no bloquea la fase 0.

## Pruebas 1 y 3: qué debe hacer la app mínima

Una sola pantalla con:

1. **Conectar**: autorización con el SDK (`SPTSessionManager` / `SPTAppRemote`) y conexión a la app de Spotify.
2. **Reproducir**: lanzar una playlist propia por su URI; botones pausa, siguiente; etiqueta con tema actual y posición, actualizada por los eventos del reproductor.
3. **Coach de prueba**: un temporizador que cada 60 s dice «Minuto N» con `AVSpeechSynthesizer`, con la sesión de audio en `.playback` + `.duckOthers` solo mientras habla.
4. **Bloquear el móvil** y dejarlo 60′: deben oírse los 60 avisos, la música debe bajar en cada uno y volver a su volumen.

Anotar en este documento lo que se observe (cortes, retrasos, interrupciones con llamadas o notificaciones).

## Resultados

| Prueba | Fecha | Resultado | Notas |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |
