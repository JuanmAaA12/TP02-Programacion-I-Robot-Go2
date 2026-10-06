# Bitácora de Desarrollo - TP02 Robot Unitree Go2

## Etapa 1: Caracterización del Entorno

| Elemento | Información obtenida |
|---|---|
| Sistema operativo | Windows |
| Versión del sistema operativo | Windows 11 Home, versión 10.0.26200 (Build 26200) |
| Arquitectura | x64 (PC de 64 bits) |
| Python instalado | Sí |
| Versión de Python | 3.14.4 |
| pip disponible | Sí, versión 26.0.1 (en `C:\Users\denlu\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\pip`) |
| Git disponible | Sí, versión 2.55.0.windows.4 |
| MuJoCo previamente instalado | No (se instaló durante este TP) |
| IDE utilizado | Visual Studio Code |

**Verificación de Visual C++ Redistributable (Windows):** se ejecutó `Test-Path` sobre `vcruntime140.dll`, `vcruntime140_1.dll` y `msvcp140.dll` en `C:\Windows\System32\`. Las tres devolvieron `True`, por lo que no fue necesario instalar el Redistributable y `import mujoco` carga sin errores de DLL.

**Comandos ejecutados:**
`systeminfo | findstr /B /C:"OS Name" /C:"OS Version" /C:"System Type"`, `py -3 --version`, `python --version`, `pip --version`, `git --version`, `py -3 -c "import mujoco; print(mujoco.__version__)"` (salida: `3.14.0`).

**Evidencia:** `evidencias/01_entorno/captura_entorno.png`

---

## Análisis previo de la documentación (sección 3 del orientador)

Fuentes leídas: `INSTALACION.md` y `LEEME_ESTUDIANTE.md` de `05LaboratoriosTPs/TP02_Programacion_I`.

**a) ¿Qué herramientas necesita el TP?**
- Python 3.10 o superior (ejecuta todo).
- MuJoCo, instalado con `pip` (dibuja la ventana 3D donde se ve el robot).
- Los modelos del Go2 y del G1 ya vienen incluidos en el paquete, no se descargan.
- La carpeta del laboratorio (`05LaboratoriosTPs/`), obtenida con Git.

**b) ¿Qué versión de Python se requiere?**
Python 3.10 o superior. En este equipo se usa Python 3.14.4, que cumple el requisito.

**c) ¿Qué componentes ya estaban instalados en la computadora?**
Python 3.14.4, pip 26.0.1 y Git 2.55.0 ya estaban disponibles; el IDE es Visual Studio Code. MuJoCo no estaba instalado y se agregó durante el TP. Los modelos del robot vienen con la carpeta del laboratorio.

**d) ¿Qué componentes del repositorio oficial de Unitree no son necesarios?**
- El repo oficial completo (299 MB) y los otros ocho robots: el laboratorio incluye solo G1 y Go2, recortados.

**e) Diferencias entre el TP en PDF y la versión actual del repositorio**
- Los movimientos se expresan con **velocidad y tiempo**: `robot.avanzar(velocidad, tiempo)` (m/s, s) y `robot.girar(velocidad, tiempo)` (rad/s, s). Antes se usaba distancia/velocidad y ángulo/sentido.
- Distancia = velocidad × tiempo; ángulo = velocidad × tiempo.
- En `girar()` el sentido lo da el signo: positivo = izquierda, negativo = derecha.
- Ya no se instalan CycloneDDS ni el SDK de Unitree; la guía actual pide solo Python y MuJoCo.
- El robot lanza `ErrorDeSeguridad` si se superan los límites (0.20 m/s, 0.50 rad/s, 10 s por orden) en vez de recortar en silencio.
- El simulador funciona en modo consola si no se puede abrir la ventana 3D.

---

## Etapa 4: Verificación del entorno

**Comando ejecutado** (desde `TP02_Programacion_I/entorno`):
`python -m sim --solo-revisar`

**Salida obtenida (04/10/2026):**

    [OK]    Python 3.14.4
    [OK]    MuJoCo v3.14.0
    [OK]    Modelos oficiales de Unitree ...\TP02_Programacion_I\entorno\sim\unitree_mujoco

    Todo listo.

**Resultado:** las tres verificaciones dieron `[OK]`, sin elementos faltantes. Niveles 1 a 4 alcanzados (Python reconocido, MuJoCo importado, modelos Go2 disponibles, verificación correcta).

**Incidente previo:** al intentar entrar a la carpeta del TP con `cd` fallamos por los espacios de la ruta. Ver Problema N.º 1 en `PROBLEMAS.md`.

**Evidencia:** `evidencias/02_instalacion/captura_verificacion_entorno.png`

---

## Etapa 5: Puesta en marcha del gemelo digital

**Comando ejecutado** (desde `TP02_Programacion_I`): `.\INICIAR_SIMULADOR.bat`

**Selección del robot:** `2` (Go2, robot perro, cuadrúpedo).

**Verificación automática del lanzador:**

    [OK]    Python 3.14.4
    [OK]    MuJoCo v3.14.0
    [OK]    Modelos oficiales de Unitree ...\TP02_Programacion_I\entorno\sim\unitree_mujoco
    Todo listo.

**Estado del simulador:**
- Robot: Unitree Go2 (cuadrúpedo)
- Escena: `go2/scene_uade.xml`
- Materia: `tp02-programacion-i`
- Límites: 0.2 m/s | 0.5 rad/s | 10.0 s por orden
- Transporte: local, `[LOCAL] Escuchando en 127.0.0.1:8765`

**Resultado:** simulador iniciado sin errores. Se abrió la ventana "MuJoCo : go2 - escena limpia UADE" y el robot Unitree Go2 quedó visible sobre el piso de la escena.

**Evidencia:** `evidencias/05_gemelo_digital/`

---

## Arquitectura del laboratorio

    mi_tp02.py
     |
     | robot.avanzar(...) / robot.girar(...) / robot.detenerse()
     v
    robot.py (puente: no se modifica)
     |
     | socket local 127.0.0.1:8765
     v
    Gemelo digital: MuJoCo + modelo Unitree Go2

- **`mi_tp02.py`** contiene mi controlador: valida cada comando, lo ejecuta y arma el reporte. No sabe nada de física ni de MuJoCo; solo llama a métodos del objeto `Robot`.
- **`robot.py`** es el puente. Traduce cada llamada (por ejemplo `avanzar(velocidad, tiempo)`) en un mensaje que envía por un socket local. Además aplica los límites de seguridad (0.2 m/s, 0.5 rad/s, 10 s) y lanza `ErrorDeSeguridad` si se superan. No se modifica.
- **Simulador (MuJoCo + Go2):** escucha en `127.0.0.1:8765`, recibe los mensajes y mueve el modelo del robot en la ventana 3D.

---

## Etapa 6: Primer programa contra el gemelo digital

**Comando ejecutado** 
`python mi_desarrollo/mi_tp02.py`

**Salida obtenida:**

    [OK] Conectado a Unitree Go2 (perro).
      Limites: 0.2 m/s, 0.5 rad/s, 10.0 s por orden.
      [OK #1] ('avanzar', 0.2, 2.0) -> Ejecutado correctamente
      [OK #2] ('girar', -0.5, 3.14) -> Ejecutado correctamente
      [OK #3] ('avanzar', 0.2, 2.0) -> Ejecutado correctamente
      [OK #4] ('detenerse',) -> Ejecutado correctamente
    Total de comandos procesados : 4
    Comandos ejecutados con éxito: 4
    Comandos rechazados          : 0
    [OK] Desconectado.

**Movimiento observado:** el Go2 avanzó, giró a la derecha y volvió a avanzar, quedando desplazado y rotado respecto de su posición inicial en la ventana de MuJoCo.

**Resultado:** conexión correcta, `MISION_BASICA` ejecutada sin rechazos y reporte generado.

**Evidencia:** `evidencias/06_misiones/01_mision_basica.png`

---

## Etapa 7: MISION_CON_ERRORES

**Misión:** `MISION_CON_ERRORES` (11 comandos), con el simulador abierto.

**Resultado:**
- 4 ejecutados: #1, #2, #10, #11.
- 3 rechazados por seguridad del robot (`ErrorDeSeguridad`): #3 (0.9 m/s), #4 (50 s), #5 (3.0 rad/s).
- 4 omitidos por validación previa: #6 (comando `volar`), #7 (velocidad no numérica), #8 (falta el tiempo), #9 (tiempo negativo).

**Verificación:** el programa detectó, rechazó, registró y continuó con el resto de la misión. El reporte final se generó. Nivel 9 alcanzado.

**Evidencia:** `evidencias/06_misiones/02_mision_con_errores.png`

---

## Etapa 8: MISION_CUADRADO

**Misión:** `MISION_CUADRADO` (9 comandos): 4 veces `avanzar(0.2 m/s, 2.0 s)` y `girar(-0.5 rad/s, 3.14 s)`, más `detenerse`.

**Cálculo:** cada lado recorre 0.2 × 2.0 = 0.4 m; cada giro es 0.5 × 3.14 ≈ 1.57 rad (90° a la derecha). Cuatro giros suman 360°.

**Resultado:** 9 ejecutados, 0 rechazados. Reporte final generado.

**Observación:** el Go2 terminó en la zona de partida, con la orientación original (de frente a la cámara), consistente con un recorrido cuadrado cerrado.

**Evidencia:** `evidencias/06_misiones/03_mision_cuadrado.png`

---

## Etapa 9: MISION_PROPIA

**Misión:** `MISION_PROPIA` (10 comandos), diseñada por nosotros. Es un zigzag con desvío lateral que incluye 3 comandos inválidos a propósito:

| # | Comando | Tipo | Efecto esperado |
|---|---|---|---|
| 1 | `avanzar(0.15, 2.0)` | válido | avanza 0.30 m |
| 2 | `girar(-0.4, 1.57)` | válido | gira ≈ 36° a la derecha |
| 3 | `("bailar",)` | **inválido** | rechazado por sintaxis: comando inexistente |
| 4 | `avanzar(0.20, 3.0)` | válido | avanza 0.60 m |
| 5 | `girar(0.4, 1.57)` | válido | gira ≈ 36° a la izquierda (recupera el rumbo) |
| 6 | `avanzar(0.5, 2.0)` | **inválido** | rechazado por seguridad: supera 0.20 m/s |
| 7 | `avanzar(0.15, 2.0)` | válido | avanza 0.30 m |
| 8 | `("avanzar", 0.15)` | **inválido** | rechazado por sintaxis: falta el tiempo |
| 9 | `saludar` | válido | saluda |
| 10 | `detenerse` | válido | frena |

**Diseño:** el robot se aparta del rumbo original hacia la derecha, avanza el tramo más largo, se endereza y termina avanzando y saludando. Los comandos válidos respetan los límites (≤ 0.2 m/s, ≤ 0.5 rad/s, ≤ 10 s). Los inválidos cubren los dos tipos de rechazo: validación previa y `ErrorDeSeguridad`.

**Resultado (COMPLETAR con lo que muestre la captura):** 7 ejecutados, 3 rechazados. Reporte final generado.

**Observación:** en la ventana, el Go2 quedó desplazado respecto de su posición inicial. No se midió la distancia exacta.

**Evidencia:** `evidencias/06_misiones/04_mision_propia.png`

