# Spin Coach

App móvil de uso personal para sesiones de spinning: genera la música desde tu Spotify ajustada por BPM a cada bloque del entrenamiento y añade un coach de voz que te dice cuándo levantarte, sentarte o apretar rueda.

> Estado: **diseño y especificación**. Todavía no hay código.

## Cómo funciona en una frase

Eliges una **combinación** (tipo de entrenamiento + mezcla musical, p. ej. «HIIT + Rock») y una duración; la app renueva la playlist de esa combinación en tu Spotify con temas cuyo BPM encaja en cada bloque y te guía con voz mientras suena.

## Documentación

| Documento | Contenido |
|---|---|
| [Producto](docs/producto.md) | Alcance, decisiones cerradas, conceptos y flujo de pantallas |
| [Entrenamiento](docs/entrenamiento.md) | Catálogo de bloques, tipos, recetas y reglas de diseño |
| [Arquitectura](docs/arquitectura.md) | Componentes y servicios externos |
| [Modelo de datos](docs/modelo-datos.md) | Entidades y relaciones |
| [Integración con Spotify](docs/spotify.md) | OAuth, scopes, endpoints y restricciones vigentes |
| [Motor](docs/motor.md) | Importación y BPM, generación, renovación, cobertura y Last.fm |
| [Sesión en vivo](docs/sesion-en-vivo.md) | Reproducción, sincronización y voz del coach |
| [Plan y riesgos](docs/plan.md) | Fases de implementación y riesgos |
| [Decisiones](docs/decisiones.md) | Registro de decisiones con su motivo |

## Datos

- [`data/bloques.json`](data/bloques.json) — catálogo de 13 bloques (posición, rueda, RPM, BPM de la música, frase del coach).
- [`data/recetas.json`](data/recetas.json) — las 16 recetas (4 tipos × 15/30/45/60′) como lista de fases.
- [`data/recetas.xlsx`](data/recetas.xlsx) — la misma información en hoja de cálculo editable, con control de que cada receta cuadra al minuto.

`recetas.xlsx` es la fuente para revisar y editar; los JSON son lo que consume el código. Si cambias la hoja, regenera los JSON.

## Diseño UX

Prototipo de 7 pantallas (inicio, diseñar sesión, música y coach, en sesión, conectar Spotify, mezcla musical, renovar combinación) en un lienzo de Claude Design, privado del autor.
