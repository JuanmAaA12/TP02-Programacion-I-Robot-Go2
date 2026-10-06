# Registro y análisis de problemas - TP02 Robot Unitree Go2

---

## Problema N.º 1

**Qué se estaba intentando hacer:**
Entrar a la carpeta `TP02_Programacion_I` del repositorio clonado para ejecutar la verificación del entorno (`python -m sim --solo-revisar`).

**Comando ejecutado:**
`cd C:\Juanma\2do Cuatri\Programacion I\TP Robot\UadeRobotLab\05LaboratoriosTPs\TP02_Programacion_I`

**Resultado esperado:**
Que la terminal se ubicara en la carpeta del TP.

**Resultado obtenido:**
PowerShell mostró un error y el directorio de trabajo no cambió.

**Mensaje de error:**
Set-Location : A positional parameter cannot be found that accepts argument 'Cuatri\Programacion'.
At line:1 char:1
+ cd C:\Juanma\2do Cuatri\Programacion I\TP Robot\UadeRobotLab\05Labora ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidArgument: (:) [Set-Location], ParameterBindingException
    + FullyQualifiedErrorId : PositionalParameterNotFound,Microsoft.PowerShell.Commands.SetLocationCommand


**Interpretación del grupo:**
El error no habla de que la carpeta no exista, sino de un "parámetro posicional" que no se puede asignar. Eso indica que PowerShell recibió más argumentos de los que `cd` (`Set-Location`) acepta.

**Hipótesis sobre la causa:**
La ruta contiene espacios (`2do Cuatri`, `Programacion I`, `TP Robot`). Sin comillas, PowerShell toma el espacio como separador de argumentos: `cd` recibió `C:\Juanma\2do` como ruta y `Cuatri\Programacion...` como un segundo argumento inesperado.

**Solución 1 intentada y resultado:**
Encerrar la ruta completa entre comillas dobles:
`cd "C:\Juanma\2do Cuatri\Programacion I\TP Robot\UadeRobotLab\05LaboratoriosTPs\TP02_Programacion_I"`
Resultado: `cd` funcionó y se pudo continuar con `cd entorno` y `python -m sim --solo-revisar`, que dio `Todo listo`.

**Solución 2 intentada y resultado:**
No fue necesaria.

**Estado final:** Resuelto.

**Evidencia:**
- Error: `evidencias/03_errores/captura_error_cd.png`
- Solución: `evidencias/04_soluciones/captura_cd_con_comillas.png`

**Aprendizaje:**
En PowerShell, toda ruta con espacios debe ir entre comillas. Conviene evitar espacios en las carpetas de proyectos.

---
