# Entrenamiento

Una sesión es una **receta de fases**: calentamiento + fases del catálogo + vuelta a la calma. Los tipos de entrenamiento no son bloques fijos sino recetas sobre un mismo catálogo de bloques, lo que permite ajustar recetas sin tocar código.

Fuente editable: [`data/recetas.xlsx`](../data/recetas.xlsx). Datos para el código: [`data/bloques.json`](../data/bloques.json) y [`data/recetas.json`](../data/recetas.json).

## Catálogo de bloques

| ID | Bloque | Posición | Rueda | RPM | Música | BPM música | Zona |
|---|---|---|---|---|---|---|---|
| CAL | Calentamiento | Sentado | 2–3 | 85–95 | 1:1 | 85–95 | Z1 |
| LLA | Llano | Sentado | 3–4 | 90–100 | 1:1 | 90–100 | Z2 |
| TEM | Tempo | Sentado | 5–6 | 90–100 | 1:1 | 90–100 | Z3 |
| SSU | Subida suave | Sentado | 5–6 | 75–85 | ½ tempo | 150–170 | Z3 |
| SUS | Subida sentado | Sentado | 6–7 | 70–80 | ½ tempo | 140–160 | Z4 |
| SUP | Subida de pie | De pie | 7–8 | 60–75 | ½ tempo | 120–150 | Z4 |
| SUR | Subida de pie (remate) | De pie | 8–9 | 60–70 | ½ tempo | 120–140 | Z5 |
| I30 | Intervalos 30/30 | Sentado / de pie | 6–7 | 100–110 | 1:1 | 100–110 | Z4 |
| I40 | Intervalos 40/20 | Sentado / de pie | 6–8 | 100–115 | 1:1 | 100–115 | Z5 |
| I20 | Intervalos 20/10 (Tabata) | Sentado / de pie | 7–9 | 105–120 | 1:1 | 105–120 | Z5 |
| SPR | Sprint | Sentado | 5–6 | 100–120 | 1:1 | 100–120 | Z5 |
| REC | Recuperación | Sentado | 2–3 | 80–90 | 1:1 | 80–90 | Z1 |
| CLM | Vuelta a la calma | Sentado | 1–2 | 70–90 | Suave | 70–90 | Z1 |

La rueda es una indicación subjetiva de 1 a 10: la bici del gimnasio no mide nada. Cada bloque lleva también una frase tipo para el coach (en `bloques.json`).

## Reglas de diseño

1. **Bloque mínimo de 3′**, lo que dura aproximadamente una canción. Por debajo no hay tema que encaje.
2. **Los intervalos cortos van dentro de un bloque.** La canción se elige por la cadencia de la parte de trabajo y el coach vocea cada cambio (40 s / 20 s…).
3. **HIIT: calidad antes que cantidad.** El bloque de series es casi fijo (máximo 3 series de ~7′: 4′ de intervalos + 3′ de recuperación). El tiempo extra de las sesiones largas va a activación y apoyo, no a más series. El HIIT de 60′ tiene 12′ de intervalos.
4. **Protocolos de intervalos de menos a más intenso**, con el Tabata al final como remate: 15′ = 20/10 + 20/10 · 30′ = 40/20 → 20/10 · 45′ y 60′ = 30/30 → 40/20 → 20/10. El Tabata son 6 rondas en 3′ u 8 en 4′.
5. **Activación previa a HIIT y Escalada en Z2–Z3** (llano → tempo), nunca Z4: llegar a las series en zona, no cansado.
6. **Escalada: la última subida es siempre el remate**, rueda 8–9, «la que pueda cada uno».
7. **Continuo con subida suave** (rueda 5–6), un escalón por debajo de la subida sentado normal: rompe la monotonía sin convertirlo en fuerza.
8. **Escalado por repetición, no por compresión.** De 60′ a 15′ se acortan calentamiento y calma (mínimo 3′) y se repite menos la unidad central; nunca se comprimen los bloques proporcionalmente.
9. **Las 16 recetas cuadran al minuto** con su duración. `recetas.xlsx` lo comprueba en la pestaña Control.

## Tipos

| Tipo | Objetivo | Unidad central que se repite |
|---|---|---|
| Continuo | Resistencia en zona baja y estable | Ciclo llano + tempo o subida suave |
| Progresivo | Intensidad por escalones, pico al final | Escalón (llano → tempo → subida sentado → de pie → sprint) |
| HIIT | Series de trabajo y descanso | Serie: intervalos + recuperación |
| Escalada | Fuerza: cadencia baja, rueda alta | Subida: sentado → de pie, con recuperación entre subidas |

Recuperación (solo Z1–Z2) queda fuera de v1.

## Recetas

### Continuo 15′

| # | Fase | Bloque | Min | Inicio |
|---|---|---|---|---|
| 1 | Calentamiento | Calentamiento | 4 | 0′ |
| 2 | Base | Llano | 4 | 4′ |
| 3 | Ondulación | Tempo | 4 | 8′ |
| 4 | Calma | Vuelta a la calma | 3 | 12′ |

### Continuo 30′

| # | Fase | Bloque | Min | Inicio |
|---|---|---|---|---|
| 1 | Calentamiento | Calentamiento | 6 | 0′ |
| 2 | Ciclo 1 | Llano | 6 | 6′ |
| 3 | Ciclo 1 | Tempo | 4 | 12′ |
| 4 | Ciclo 2 | Llano | 5 | 16′ |
| 5 | Ciclo 2 | Subida suave | 4 | 21′ |
| 6 | Calma | Vuelta a la calma | 5 | 25′ |

### Continuo 45′

| # | Fase | Bloque | Min | Inicio |
|---|---|---|---|---|
| 1 | Calentamiento | Calentamiento | 8 | 0′ |
| 2 | Ciclo 1 | Llano | 7 | 8′ |
| 3 | Ciclo 1 | Tempo | 5 | 15′ |
| 4 | Ciclo 2 | Llano | 6 | 20′ |
| 5 | Ciclo 2 | Subida suave | 5 | 26′ |
| 6 | Ciclo 3 | Llano | 5 | 31′ |
| 7 | Ciclo 3 | Tempo | 4 | 36′ |
| 8 | Calma | Vuelta a la calma | 5 | 40′ |

### Continuo 60′

| # | Fase | Bloque | Min | Inicio |
|---|---|---|---|---|
| 1 | Calentamiento | Calentamiento | 8 | 0′ |
| 2 | Ciclo 1 | Llano | 8 | 8′ |
| 3 | Ciclo 1 | Tempo | 6 | 16′ |
| 4 | Ciclo 2 | Llano | 8 | 22′ |
| 5 | Ciclo 2 | Subida suave | 6 | 30′ |
| 6 | Ciclo 3 | Llano | 8 | 36′ |
| 7 | Ciclo 3 | Tempo | 6 | 44′ |
| 8 | Calma | Vuelta a la calma | 10 | 50′ |

> Subida suave: rueda 5-6, sin apretar

### Progresivo 15′

| # | Fase | Bloque | Min | Inicio |
|---|---|---|---|---|
| 1 | Calentamiento | Calentamiento | 4 | 0′ |
| 2 | Escalón 1 | Tempo | 4 | 4′ |
| 3 | Escalón 2 | Subida sentado | 4 | 8′ |
| 4 | Calma | Vuelta a la calma | 3 | 12′ |

> Sin escalón de llano: el calentamiento hace de base

### Progresivo 30′

| # | Fase | Bloque | Min | Inicio |
|---|---|---|---|---|
| 1 | Calentamiento | Calentamiento | 5 | 0′ |
| 2 | Escalón 1 | Llano | 5 | 5′ |
| 3 | Escalón 2 | Tempo | 5 | 10′ |
| 4 | Escalón 3 | Subida sentado | 5 | 15′ |
| 5 | Escalón 4 | Subida de pie | 4 | 20′ |
| 6 | Calma | Vuelta a la calma | 6 | 24′ |

### Progresivo 45′

| # | Fase | Bloque | Min | Inicio |
|---|---|---|---|---|
| 1 | Calentamiento | Calentamiento | 5 | 0′ |
| 2 | Escalón 1 | Llano | 7 | 5′ |
| 3 | Escalón 2 | Tempo | 8 | 12′ |
| 4 | Escalón 3 | Subida sentado | 8 | 20′ |
| 5 | Escalón 4 | Subida de pie | 6 | 28′ |
| 6 | Final | Sprint | 4 | 34′ |
| 7 | Calma | Vuelta a la calma | 7 | 38′ |

### Progresivo 60′

| # | Fase | Bloque | Min | Inicio |
|---|---|---|---|---|
| 1 | Calentamiento | Calentamiento | 8 | 0′ |
| 2 | Escalón 1 | Llano | 10 | 8′ |
| 3 | Escalón 2 | Tempo | 10 | 18′ |
| 4 | Escalón 3 | Subida sentado | 10 | 28′ |
| 5 | Escalón 4 | Subida de pie | 8 | 38′ |
| 6 | Final | Sprint | 6 | 46′ |
| 7 | Calma | Vuelta a la calma | 8 | 52′ |

### HIIT 15′

| # | Fase | Bloque | Min | Inicio |
|---|---|---|---|---|
| 1 | Calentamiento | Calentamiento | 3 | 0′ |
| 2 | Serie 1 | Intervalos 20/10 (Tabata) | 3 | 3′ |
| 3 | Serie 1 | Recuperación | 3 | 6′ |
| 4 | Serie 2 | Intervalos 20/10 (Tabata) | 3 | 9′ |
| 5 | Calma | Vuelta a la calma | 3 | 12′ |

> Tabata corto: 6 rondas de 20/10 por serie

### HIIT 30′

| # | Fase | Bloque | Min | Inicio |
|---|---|---|---|---|
| 1 | Calentamiento | Calentamiento | 6 | 0′ |
| 2 | Activación progresiva | Tempo | 4 | 6′ |
| 3 | Serie 1 | Intervalos 40/20 | 4 | 10′ |
| 4 | Serie 1 | Recuperación | 3 | 14′ |
| 5 | Serie 2 | Intervalos 20/10 (Tabata) | 4 | 17′ |
| 6 | Serie 2 | Recuperación | 3 | 21′ |
| 7 | Calma | Vuelta a la calma | 6 | 24′ |

> Intensidad creciente: 40/20 y remate en 20/10

### HIIT 45′

| # | Fase | Bloque | Min | Inicio |
|---|---|---|---|---|
| 1 | Calentamiento | Calentamiento | 8 | 0′ |
| 2 | Activación progresiva | Llano | 4 | 8′ |
| 3 | Activación progresiva | Tempo | 4 | 12′ |
| 4 | Serie 1 | Intervalos 30/30 | 4 | 16′ |
| 5 | Serie 1 | Recuperación | 3 | 20′ |
| 6 | Serie 2 | Intervalos 40/20 | 4 | 23′ |
| 7 | Serie 2 | Recuperación | 3 | 27′ |
| 8 | Serie 3 | Intervalos 20/10 (Tabata) | 4 | 30′ |
| 9 | Serie 3 | Recuperación | 3 | 34′ |
| 10 | Calma | Vuelta a la calma | 8 | 37′ |

> Escalera de protocolos: 30/30 → 40/20 → 20/10 (Tabata al final)

### HIIT 60′

| # | Fase | Bloque | Min | Inicio |
|---|---|---|---|---|
| 1 | Calentamiento | Calentamiento | 10 | 0′ |
| 2 | Activación progresiva | Llano | 4 | 10′ |
| 3 | Activación progresiva | Tempo | 4 | 14′ |
| 4 | Serie 1 | Intervalos 30/30 | 4 | 18′ |
| 5 | Serie 1 | Recuperación | 3 | 22′ |
| 6 | Serie 2 | Intervalos 40/20 | 4 | 25′ |
| 7 | Serie 2 | Recuperación | 3 | 29′ |
| 8 | Serie 3 | Intervalos 20/10 (Tabata) | 4 | 32′ |
| 9 | Serie 3 | Recuperación | 3 | 36′ |
| 10 | Apoyo | Tempo | 6 | 39′ |
| 11 | Apoyo | Subida sentado | 6 | 45′ |
| 12 | Calma | Vuelta a la calma | 9 | 51′ |

> Apoyo tras las series: mantener Z3-Z4 sin buscar el máximo

### Escalada 15′

| # | Fase | Bloque | Min | Inicio |
|---|---|---|---|---|
| 1 | Calentamiento | Calentamiento | 4 | 0′ |
| 2 | Subida 1 | Subida sentado | 4 | 4′ |
| 3 | Subida 1 | Subida de pie (remate) | 4 | 8′ |
| 4 | Calma | Vuelta a la calma | 3 | 12′ |

### Escalada 30′

| # | Fase | Bloque | Min | Inicio |
|---|---|---|---|---|
| 1 | Calentamiento | Calentamiento | 6 | 0′ |
| 2 | Subida 1 | Subida sentado | 4 | 6′ |
| 3 | Subida 1 | Subida de pie | 4 | 10′ |
| 4 | Entre subidas | Recuperación | 3 | 14′ |
| 5 | Subida 2 | Subida sentado | 4 | 17′ |
| 6 | Subida 2 | Subida de pie (remate) | 4 | 21′ |
| 7 | Calma | Vuelta a la calma | 5 | 25′ |

### Escalada 45′

| # | Fase | Bloque | Min | Inicio |
|---|---|---|---|---|
| 1 | Calentamiento | Calentamiento | 6 | 0′ |
| 2 | Activación | Llano | 4 | 6′ |
| 3 | Subida 1 | Subida sentado | 4 | 10′ |
| 4 | Subida 1 | Subida de pie | 4 | 14′ |
| 5 | Entre subidas | Recuperación | 3 | 18′ |
| 6 | Subida 2 | Subida sentado | 4 | 21′ |
| 7 | Subida 2 | Subida de pie | 4 | 25′ |
| 8 | Entre subidas | Recuperación | 3 | 29′ |
| 9 | Subida 3 | Subida sentado | 4 | 32′ |
| 10 | Subida 3 | Subida de pie (remate) | 4 | 36′ |
| 11 | Calma | Vuelta a la calma | 5 | 40′ |

### Escalada 60′

| # | Fase | Bloque | Min | Inicio |
|---|---|---|---|---|
| 1 | Calentamiento | Calentamiento | 8 | 0′ |
| 2 | Activación | Llano | 5 | 8′ |
| 3 | Subida 1 | Subida sentado | 4 | 13′ |
| 4 | Subida 1 | Subida de pie | 4 | 17′ |
| 5 | Entre subidas | Recuperación | 3 | 21′ |
| 6 | Subida 2 | Subida sentado | 4 | 24′ |
| 7 | Subida 2 | Subida de pie | 4 | 28′ |
| 8 | Entre subidas | Recuperación | 3 | 32′ |
| 9 | Subida 3 | Subida sentado | 4 | 35′ |
| 10 | Subida 3 | Subida de pie (remate) | 4 | 39′ |
| 11 | Apoyo | Tempo | 8 | 43′ |
| 12 | Calma | Vuelta a la calma | 9 | 51′ |

> Remate: rueda 8-9, la que pueda cada uno
