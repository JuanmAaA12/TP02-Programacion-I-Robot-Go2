# =====================================================================
#  TP02 - Programacion I
#  Controlador de misiones
#
#  ESTE ES EL ARCHIVO DONDE ESCRIBIS TU PROGRAMA.
#
#  Antes de ejecutarlo:
#    1. Abri INICIAR_SIMULADOR (elegi G1 o Go2)
#    2. Espera a que aparezca la ventana con el robot
#    3. Recien ahi ejecuta este archivo
#
#  Nombre y apellido:  Juan Manuel Veiga Lucien y Manuela Almendros
#  Comision:           584524
# =====================================================================

from robot import ErrorDeSeguridad, Robot

from misiones import MISION_BASICA, MISION_CON_ERRORES, MISION_CUADRADO, MISION_PROPIA


# =====================================================================
#  PARTE 1 - Validar un comando
# =====================================================================
def comando_es_valido(comando):
    """Decide si un comando se puede ejecutar. Devuelve True o False.

    Un comando es una tupla. El primer elemento dice que hacer:

        ("avanzar", velocidad, tiempo)    velocidad en m/s, tiempo en s
        ("girar", velocidad, tiempo)      velocidad en rad/s, tiempo en s
        ("detenerse",)
        ("saludar",)

    Cosas que conviene revisar:
      - que la tupla no este vacia
      - que el nombre del comando sea uno de los cuatro validos
      - que tenga la cantidad de datos que corresponde
        (avanzar y girar llevan dos; detenerse y saludar, ninguno)
      - que velocidad y tiempo sean numeros de verdad, no textos
      - que el tiempo no sea negativo
    """
    if not isinstance(comando, tuple) or len(comando) == 0:
        return False

    accion = comando[0]

    if accion in ("avanzar", "girar"):
        if len(comando) != 3:
            return False
        
        velocidad = comando[1]
        tiempo = comando[2]

        # Validar que velocidad y tiempo sean numéricos (int o float) y no booleanos
        if not (isinstance(velocidad, (int, float)) and not isinstance(velocidad, bool)):
            return False
        if not (isinstance(tiempo, (int, float)) and not isinstance(tiempo, bool)):
            return False

        # El tiempo no puede ser negativo
        if tiempo < 0:
            return False

    elif accion in ("detenerse", "saludar"):
        if len(comando) != 1:
            return False

    else:
        # Acción no reconocida
        return False

    return True


# =====================================================================
#  PARTE 2 - Ejecutar un comando
# =====================================================================
def ejecutar_comando(robot, comando):
    """Ejecuta UN comando en el robot. Devuelve un texto con lo que paso.

    Ordenes que podes usar:

        robot.avanzar(velocidad=..., tiempo=...)
        robot.girar(velocidad=..., tiempo=...)
        robot.detenerse()
        robot.saludar()

    Ojo: aunque el comando parezca valido, el robot puede rechazarlo
    igual (por ejemplo, si la velocidad supera el limite de la materia).
    Eso llega como un ErrorDeSeguridad y conviene atraparlo.
    """
    accion = comando[0]

    try:
        if accion == "avanzar":
            robot.avanzar(velocidad=comando[1], tiempo=comando[2])
            return f"Ejecutado correctamente: avanzar(velocidad={comando[1]}, tiempo={comando[2]})"
            
        elif accion == "girar":
            robot.girar(velocidad=comando[1], tiempo=comando[2])
            return f"Ejecutado correctamente: girar(velocidad={comando[1]}, tiempo={comando[2]})"
            
        elif accion == "detenerse":
            robot.detenerse()
            return "Ejecutado correctamente: detenerse"
            
        elif accion == "saludar":
            robot.saludar()
            return "Ejecutado correctamente: saludar"

    except ErrorDeSeguridad as e:
        return f"Rechazado por seguridad del robot: {e}"
    except Exception as e:
        return f"Error inesperado al ejecutar: {e}"


# =====================================================================
#  PARTE 3 - Recorrer la mision entera
# =====================================================================
def ejecutar_mision(robot, mision, historial):
    """Recorre la lista de comandos, uno por uno.

    Por cada comando:
      - si NO es valido, lo rechaza y sigue con el siguiente
      - si es valido, lo ejecuta
      - en los dos casos, guarda en 'historial' que fue lo que paso

    Un comando invalido NO tiene que cortar la mision.
    """
    for i, comando in enumerate(mision, start=1):
        if not comando_es_valido(comando):
            motivo = f"Formato o parámetros de comando inválidos: {comando}"
            historial.append({
                "comando": comando,
                "estado": "Rechazado (Sintaxis)",
                "detalle": motivo
            })
            print(f"  [OMITIDO #{i}] {comando} -> Motivo: {motivo}")
        else:
            resultado = ejecutar_comando(robot, comando)
            if "Rechazado" in resultado:
                historial.append({
                    "comando": comando,
                    "estado": "Rechazado (Seguridad)",
                    "detalle": resultado
                })
                print(f"  [RECHAZADO #{i}] {comando} -> {resultado}")
            else:
                historial.append({
                    "comando": comando,
                    "estado": "Ejecutado",
                    "detalle": resultado
                })
                print(f"  [OK #{i}] {comando} -> {resultado}")


# =====================================================================
#  PARTE 4 - El reporte final
# =====================================================================
def generar_reporte(historial):
    """Muestra por pantalla un resumen de la mision.

    Tiene que decir, como minimo:
      - cuantos comandos se ejecutaron bien
      - cuantos se rechazaron
      - cual fue el motivo de cada rechazo
    """
    ejecutados = sum(1 for registro in historial if registro["estado"] == "Ejecutado")
    rechazados = len(historial) - ejecutados

    print("\n" + "=" * 50)
    print("        REPORTE FINAL DE LA MISIÓN")
    print("=" * 50)
    print(f"Total de comandos procesados : {len(historial)}")
    print(f"Comandos ejecutados con éxito: {ejecutados}")
    print(f"Comandos rechazados          : {rechazados}")

    if rechazados > 0:
        print("\nDetalle de Rechazos / Omisiones:")
        for idx, registro in enumerate(historial, start=1):
            if registro["estado"] != "Ejecutado":
                print(f"  {idx}. Comando: {registro['comando']}")
                print(f"     Tipo: {registro['estado']}")
                print(f"     Motivo: {registro['detalle']}")

    print("=" * 50 + "\n")


# =====================================================================
#  PROGRAMA PRINCIPAL
# =====================================================================
def main():
    robot = Robot()
    robot.conectar()

    historial = []

    try:
        # Empeza probando con MISION_BASICA.
        # Cuando funcione, proba con MISION_CON_ERRORES: esa tiene
        # comandos invalidos a proposito.
        ejecutar_mision(robot, MISION_BASICA, historial)
        generar_reporte(historial)
    finally:
        robot.detenerse()
        robot.desconectar()


if __name__ == "__main__":
    main()
