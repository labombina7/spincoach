# Producto

Spin Coach genera sesiones de spinning de 15, 30, 45 o 60 minutos con música de tu Spotify cuyo BPM encaja con la cadencia de cada bloque, y un coach de voz que guía la sesión.

## Alcance y decisiones cerradas

- **Uso personal.** App de Spotify en modo desarrollo: máximo 5 usuarios y el propietario necesita Premium.
- **16 recetas**: 4 tipos (Continuo, Progresivo, HIIT, Escalada) × 4 duraciones (15, 30, 45 y 60′). Ver [Entrenamiento](entrenamiento.md).
- **Una sesión es una receta de fases** sobre un catálogo de 13 bloques. Bloque mínimo de 3′ (≈ una canción). Los intervalos cortos van dentro de un bloque y los vocea el coach.
- **Una playlist de Spotify por combinación** tipo + mezcla («Spin · HIIT + Rock»). Se renueva al empezar desde la app, salvo que se marque «mantener esta versión».
- **Spotify como herramienta de curación**: lo que añades a esas playlists desde Spotify entra en la mezcla; lo que quitas queda descartado.
- **Cobertura contra la receta de 60′** de cada tipo. Last.fm solo entra si una combinación no la cubre.

**Fuera de alcance en v1**: sensores de cadencia o potencia, varios usuarios, catálogo musical propio.

## Conceptos

| Concepto | Qué es | Ejemplo |
|---|---|---|
| Bloque | Pieza mínima: posición, rueda, cadencia y BPM de la música | Subida de pie: de pie, rueda 7–8, 60–75 RPM, música 120–150 BPM a medio tempo |
| Receta | Lista ordenada de fases (bloque + minutos) para un tipo y una duración | HIIT 45′ |
| Mezcla | Conjunto de temas con nombre, definido por artistas, géneros y playlists propias | «Latino» |
| Combinación | Tipo de entrenamiento + mezcla; tiene su playlist en Spotify | «Progresivo + Latino» |
| Sesión | Una ejecución concreta: combinación + duración + temas asignados | Progresivo + Latino, 45′, 23 oct |

## Relación BPM ↔ cadencia

En ciclo indoor la música marca la pedalada:

- **1:1** — una pedalada por golpe (llano, tempo, sprint, intervalos). BPM = RPM.
- **½ tempo** — una pedalada cada dos golpes (subidas). BPM = 2 × RPM.

Al buscar temas se acepta también el doble o la mitad del tempo detectado, porque los detectores de BPM confunden a menudo ese factor.

## Flujo principal

1. **Conectar Spotify** (una vez): permisos, importación de la biblioteca y cálculo de BPM en segundo plano.
2. **Mezclas**: la app propone mezclas a partir de los géneros de tu biblioteca («Latino, 84 temas»); también se crean desde una playlist propia o a mano con artistas y géneros.
3. **Inicio**: tus combinaciones con la última usada destacada y el botón «Renovar y empezar».
4. **Renovar combinación**: muestra lo que cambió desde Spotify (+ añadidas, − quitadas), los temas por bloque, regenerar o fijar temas, y «mantener esta versión».
5. **En sesión**: bloque actual y cuenta atrás, cadencia y rueda objetivo, última frase del coach, siguiente cambio, tema con su BPM, y controles de silenciar voz, pausa y saltar bloque.

## Diseño visual

- Modo oscuro por defecto (salas de ciclo con poca luz).
- Código de color fijo por zona en todas las pantallas: azul recuperación, verde agua llano, lima tempo, naranja subida, rojo sprint.
- La pantalla en sesión se diseña para leerse a un metro, en el manillar y sudando: tipografía grande y 3 controles.
