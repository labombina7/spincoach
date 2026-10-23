# Integración con Spotify

Spotify da la biblioteca, guarda las playlists de cada combinación y reproduce. **No** da BPM, recomendaciones ni artistas relacionados para apps nuevas: eso sale de ReccoBeats y Last.fm (ver [Motor](motor.md)).

## Autenticación

- OAuth 2.0 **Authorization Code con PKCE** (app móvil, sin secreto de cliente).
- Tokens en el llavero del dispositivo; *refresh* automático.
- La reproducción usa el **App Remote SDK** de Spotify, que controla la app de Spotify instalada y exige Premium. Desde febrero de 2026 `GET /me` ya no devuelve `product`, así que no se puede comprobar Premium por adelantado: se detecta por el error del App Remote y se muestra un aviso.

### Scopes

| Scope | Para qué |
|---|---|
| `user-library-read` | Canciones guardadas (Liked Songs) |
| `user-follow-read` | Artistas que sigues |
| `user-top-read` | Artistas y temas más escuchados (pesos del sorteo) |
| `playlist-read-private`, `playlist-read-collaborative` | Tus playlists como fuente de mezclas y leer las playlists de combinación |
| `playlist-modify-private`, `playlist-modify-public` | Crear y renovar las playlists «Spin ·» |
| `user-read-playback-state`, `user-modify-playback-state` | Estado y control de reproducción vía Web API (respaldo) |
| `app-remote-control` | Control de la app de Spotify desde el App Remote SDK |

## Endpoints que usamos

| Uso | Endpoint | Notas |
|---|---|---|
| Canciones guardadas | `GET /me/tracks` | Paginado |
| Tus playlists | `GET /me/playlists` | |
| Contenido de una playlist | `GET /playlists/{id}/items` | **Solo** playlists tuyas o colaborativas |
| Artistas seguidos | `GET /me/following?type=artist` | Paginado por cursor |
| Más escuchados | `GET /me/top/artists`, `GET /me/top/tracks` | Solo como señal de peso |
| Datos de un artista (géneros) | `GET /artists/{id}` | **Uno a uno**: el endpoint por lotes `GET /artists` se eliminó |
| Catálogo de un artista | `GET /artists/{id}/albums` → `GET /albums/{id}` | Sustituye a «top tracks», eliminado |
| Búsqueda | `GET /search` | Máximo **10** resultados por página; filtros `artist:`, `track:`, `genre:` |
| Crear playlist de combinación | `POST /me/playlists` | |
| Renovar su contenido | `PUT /playlists/{id}/items` | Reemplaza todo el contenido en una llamada (hasta 100 temas) |

## Restricciones vigentes para apps nuevas

Desde el [27 de noviembre de 2024](https://developer.spotify.com/blog/2024-11-27-changes-to-the-web-api): sin acceso a Audio Features (BPM), Audio Analysis, Recommendations, Related Artists, playlists editoriales o algorítmicas de Spotify ni *preview URLs* en respuestas múltiples.

Desde [febrero de 2026](https://developer.spotify.com/documentation/web-api/tutorials/february-2026-migration-guide), en modo desarrollo:

- Máximo 5 usuarios por app y el propietario necesita Premium activo; si caduca, la app deja de funcionar.
- Eliminados los endpoints por lotes (`GET /tracks`, `/artists`, `/albums`…): todo es uno a uno.
- Eliminado `GET /artists/{id}/top-tracks`.
- Eliminados los campos `popularity` (temas, álbumes, artistas) y `followers` de artistas.
- `GET /search` limitado a 10 resultados por página.
- Endpoints de playlists renombrados de `/tracks` a `/items`; la lectura de contenido solo funciona en playlists propias o colaborativas.

## Consecuencias de diseño

- **Las playlists de otros no sirven como fuente.** Si quieres usar una editorial o la de un amigo, cópiala primero en Spotify a una playlist tuya.
- **Importar cuesta llamadas.** Sin endpoints por lotes, géneros y catálogos de artistas se piden uno a uno: se hace en segundo plano, con caché, y respetando el `Retry-After` de las respuestas 429.
- **Sin popularidad**, el peso de un tema en el sorteo sale de tus más escuchados y de tu propio historial, no de Spotify.
- **Todo el acceso pasa por un único cliente** dentro de la app, para absorber el próximo recorte en un solo sitio.
