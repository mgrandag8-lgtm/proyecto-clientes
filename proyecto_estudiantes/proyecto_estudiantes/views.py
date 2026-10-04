from controllers import EstudianteController
from shared.herramientas import limpiar_pantalla, pausa


class MenuEstudiantes:
    def __init__(self):
        self.activo = True

    def mostrar_menu(self):
        limpiar_pantalla()

        print("=" * 45)
        print("          MENÚ DE ESTUDIANTES")
        print("=" * 45)

        print("1. Crear estudiante")
        print("2. Ver estudiantes")
        print("3. Buscar estudiante")
        print("4. Ver estudiante por ID")
        print("5. Actualizar estudiante")
        print("6. Eliminar estudiante")
        print("7. Agregar nota")
        print("8. Ver promedio")
        print("9. Materias en común")
        print("10. Materias ofertadas")
        print("0. Salir")

    def crear(self):
        limpiar_pantalla()

        print("CREAR ESTUDIANTE\n")

        nombre = input("Nombre: ")
        apellido = input("Apellido: ")
        email = input("Email: ")
        carnet = input("Carnet: ")

        datos = {
            "nombre": nombre,
            "apellido": apellido,
            "email": email,
            "carnet": carnet
        }

        exito, mensaje = EstudianteController.crear(datos)

        print("\n", mensaje)

        pausa()

    def listar(self):
        limpiar_pantalla()

        print("LISTA DE ESTUDIANTES\n")

        estudiantes = EstudianteController.listar()

        if len(estudiantes) == 0:
            print("No hay estudiantes registrados")

        else:
            for estudiante in estudiantes:
                print(estudiante)

        pausa()

    def buscar(self):
        limpiar_pantalla()

        termino = input(
            "Ingrese nombre, apellido, email o carnet: "
        )

        resultados = EstudianteController.buscar(
            termino
        )

        print()

        if len(resultados) == 0:
            print("No se encontraron resultados")

        else:
            for estudiante in resultados:
                print(estudiante)

        pausa()

    def ver_por_id(self):
        limpiar_pantalla()

        try:
            id_estudiante = int(
                input("ID del estudiante: ")
            )

            estudiante = EstudianteController.obtener(
                id_estudiante
            )

            if estudiante is None:
                print("Estudiante no encontrado")

            else:
                print()
                print(estudiante)
                print(
                    "Promedio:",
                    estudiante.promedio
                )
                print(
                    "Estado:",
                    estudiante.estado
                )

        except ValueError:
            print("Ingrese un ID válido")

        pausa()

    def actualizar(self):
        limpiar_pantalla()

        try:
            id_estudiante = int(
                input("ID del estudiante: ")
            )

        except ValueError:
            print("ID inválido")
            pausa()
            return

        estudiante = EstudianteController.obtener(
            id_estudiante
        )

        if estudiante is None:
            print("Estudiante no encontrado")
            pausa()
            return

        print(
            "\nDeje vacío lo que no desea cambiar\n"
        )

        nombre = input(
            f"Nombre [{estudiante.nombre}]: "
        )

        apellido = input(
            f"Apellido [{estudiante.apellido}]: "
        )

        email = input(
            f"Email [{estudiante.email}]: "
        )

        carnet = input(
            f"Carnet [{estudiante.carnet}]: "
        )

        cambios = {}

        if nombre != "":
            cambios["nombre"] = nombre

        if apellido != "":
            cambios["apellido"] = apellido

        if email != "":
            cambios["email"] = email

        if carnet != "":
            cambios["carnet"] = carnet

        exito, mensaje = EstudianteController.actualizar(
            id_estudiante,
            cambios
        )

        print("\n", mensaje)

        pausa()

    def eliminar(self):
        limpiar_pantalla()

        try:
            id_estudiante = int(
                input("ID del estudiante: ")
            )

        except ValueError:
            print("ID inválido")
            pausa()
            return

        respuesta = input(
            "¿Seguro que desea eliminarlo? (si/no): "
        ).lower()

        if respuesta not in ("si", "sí", "s"):
            print("Operación cancelada")
            pausa()
            return

        exito, mensaje = EstudianteController.eliminar(
            id_estudiante
        )

        print(mensaje)

        pausa()

    def agregar_nota(self):
        limpiar_pantalla()

        try:
            id_estudiante = int(
                input("ID del estudiante: ")
            )

            materia = input(
                "Materia: "
            )

            nota = float(
                input("Nota de 0 a 20: ")
            )

        except ValueError:
            print(
                "Ingrese valores numéricos válidos"
            )
            pausa()
            return

        exito, mensaje = EstudianteController.agregar_nota(
            id_estudiante,
            materia,
            nota
        )

        print("\n", mensaje)

        pausa()

    def ver_promedio(self):
        limpiar_pantalla()

        try:
            id_estudiante = int(
                input("ID del estudiante: ")
            )

        except ValueError:
            print("ID inválido")
            pausa()
            return

        estudiante = EstudianteController.obtener(
            id_estudiante
        )

        if estudiante is None:
            print("Estudiante no encontrado")

        else:
            print()
            print(
                "Estudiante:",
                estudiante.nombre_completo
            )

            print(
                "Promedio:",
                estudiante.promedio
            )

            print(
                "Estado:",
                estudiante.estado
            )

        pausa()

    def materias_comun(self):
        limpiar_pantalla()

        try:
            id_a = int(
                input("ID del primer estudiante: ")
            )

            id_b = int(
                input("ID del segundo estudiante: ")
            )

        except ValueError:
            print("Ingrese IDs válidos")
            pausa()
            return

        materias = (
            EstudianteController.materias_en_comun(
                id_a,
                id_b
            )
        )

        if materias is None:
            print("Uno de los estudiantes no existe")

        elif len(materias) == 0:
            print(
                "Los estudiantes no tienen materias en común"
            )

        else:
            print("\nMaterias en común:")

            for materia in materias:
                print("-", materia)

        pausa()

    def materias_ofertadas(self):
        limpiar_pantalla()

        materias = (
            EstudianteController.materias_ofertadas()
        )

        print("MATERIAS OFERTADAS\n")

        if len(materias) == 0:
            print("No hay materias registradas")

        else:
            for materia in sorted(materias):
                print("-", materia)

        pausa()

    def ejecutar(self):
        while self.activo:
            self.mostrar_menu()

            opcion = input(
                "\nSeleccione una opción: "
            )

            if opcion == "1":
                self.crear()

            elif opcion == "2":
                self.listar()

            elif opcion == "3":
                self.buscar()

            elif opcion == "4":
                self.ver_por_id()

            elif opcion == "5":
                self.actualizar()

            elif opcion == "6":
                self.eliminar()

            elif opcion == "7":
                self.agregar_nota()

            elif opcion == "8":
                self.ver_promedio()

            elif opcion == "9":
                self.materias_comun()

            elif opcion == "10":
                self.materias_ofertadas()

            elif opcion == "0":
                self.activo = False
                print("Programa finalizado")

            else:
                print("Opción inválida")
                pausa()