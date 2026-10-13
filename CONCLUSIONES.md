# Conclusiones y reflexión final - TP02 Robot Unitree Go2

## Resumen del trabajo

Se instaló y verificó el entorno (Python 3.14.4, MuJoCo 3.14.0, modelos oficiales de Unitree), se puso en marcha el gemelo digital del Go2 y se desarrolló un controlador de misiones modular en `mi_tp02.py`, con cuatro funciones: `comando_es_valido`, `ejecutar_comando`, `ejecutar_mision` y `generar_reporte`. Se probaron `MISION_BASICA`, `MISION_CON_ERRORES`, `MISION_CUADRADO` y una misión propia (`MISION_PROPIA`).

## Reflexión (sección 20 del orientador)

**a) ¿Cuál fue la principal dificultad de instalación?**
La instalación de Python, MuJoCo y los modelos no presentó errores: el comando `py -3 -m pip install mujoco` terminó bien, las tres DLL de Visual C++ ya estaban presentes y la verificación dio `[OK]` en los tres elementos. 

**b) ¿Qué error requirió mayor investigación?**
El error del `cd`. El mensaje no decía que la carpeta no existiera, por lo que hubo que interpretar que PowerShell separaba la ruta en varios argumentos por los espacios.

**c) ¿Qué solución resultó efectiva y por qué?**
Encerrar la ruta entre comillas dobles. Las comillas indican a PowerShell que toda la ruta es un único argumento. Después de aplicarla se pudo ejecutar la verificación y el simulador.

**d) ¿Qué intento no funcionó y qué aprendieron de él?**
El `cd` sin comillas. Aprendimos que en PowerShell las rutas con espacios deben ir entre comillas y que conviene evitar espacios en los nombres de carpetas de proyectos. También decidimos no modificar los motivos de rechazo por sintaxis, que quedaron genéricos: aprendí a distinguir entre algo que funciona y algo que se puede explicar mejor.

**e) ¿Qué diferencia encontraron entre una guía antigua y la arquitectura actual?**
Las guías anteriores usaban distancia/velocidad y ángulo/sentido, y requerían CycloneDDS y el SDK oficial de Unitree. La versión actual usa velocidad y tiempo (distancia = velocidad × tiempo; ángulo = velocidad × tiempo, con el signo indicando el sentido) y se comunica con MuJoCo por un socket local en `127.0.0.1:8765` a través de `robot.py`. Así deja de depender de componentes que fallaban en Windows y macOS, y el código del alumno no cambia.

**f) ¿Hasta qué nivel lograron avanzar?**
Nivel 10. Python reconocido (1), MuJoCo importado (2), modelos Go2 disponibles (3), verificación correcta (4), ventana abierta (5), Go2 visible (6), programa conectado (7), `MISION_BASICA` ejecutada (8), `MISION_CON_ERRORES` procesada sin abortar (9) y reporte final generado (10).

**g) Si tuvieran que continuar trabajando, ¿cuál sería el próximo paso?**
1. Permitir elegir la misión desde un menú o argumento, sin editar `main()`.
2. Devolver desde `ejecutar_comando` un resultado estructurado (estado y mensaje) en lugar de detectar el rechazo buscando texto.

## Conclusiones técnicas

- **Diseño modular:** cada función tiene una responsabilidad clara, por lo que cambiar la misión no obliga a reescribir el controlador.
- **Validación en dos capas:** la validación previa (`comando_es_valido`) descarta comandos mal formados, y el `try/except` de `ErrorDeSeguridad` captura los que superan los límites del robot (0.2 m/s, 0.5 rad/s, 10 s). En `MISION_CON_ERRORES` esto dio 4 ejecutados, 3 rechazados por seguridad y 4 omitidos por sintaxis, sin cortar la misión.
- **Alcance del simulador:** que el programa funcione en el simulador valida la lógica, pero no garantiza el mismo comportamiento en el robot físico.