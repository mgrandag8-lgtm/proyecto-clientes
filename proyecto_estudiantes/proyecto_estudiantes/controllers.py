from models import Estudiante
from shared.json_manager import GestorJSON


class ClienteController:
    MODELO = None
    ARCHIVO = ""
    CAMPOS_BUSCABLES = ()

    _gestor = None

    @classmethod
    def _registros(cls):
        return cls._gestor.leer()

    @classmethod
    def siguiente_id(cls):
        registros = cls._registros()

        if len(registros) == 0:
            return 1

        ids = []

        for registro in registros:
            ids.append(registro["id"])

        return max(ids) + 1

    @classmethod
    def emails_registrados(cls, excepto_id=None):
        emails = set()

        for registro in cls._registros():

            if registro["id"] != excepto_id:
                emails.add(registro["email"].lower())

        return emails

    @classmethod
    def crear(cls, datos):
        try:
            email = datos["email"].lower()

            if email in cls.emails_registrados():
                return False, "El email ya está registrado"

            objeto = cls.MODELO(
                cls.siguiente_id(),
                datos["nombre"],
                datos["apellido"],
                datos["email"],
                datos["carnet"]
            )

            registros = cls._registros()

            registros.append(objeto.a_diccionario())

            cls._gestor.guardar(registros)

            return True, "Estudiante creado correctamente"

        except ValueError as error:
            return False, str(error)

    @classmethod
    def listar(cls):
        objetos = []

        for registro in cls._registros():
            objetos.append(
                cls.MODELO.desde_diccionario(registro)
            )

        return objetos

    @classmethod
    def obtener(cls, id_estudiante):
        for estudiante in cls.listar():

            if estudiante.id == id_estudiante:
                return estudiante

        return None

    @classmethod
    def buscar(cls, termino):
        termino = termino.lower()

        resultados = []

        for registro in cls._registros():

            for campo in cls.CAMPOS_BUSCABLES:

                valor = str(
                    registro.get(campo, "")
                ).lower()

                if termino in valor:
                    resultados.append(
                        cls.MODELO.desde_diccionario(registro)
                    )
                    break

        return resultados

    @classmethod
    def actualizar(cls, id_estudiante, cambios):
        estudiante = cls.obtener(id_estudiante)

        if estudiante is None:
            return False, "Estudiante no encontrado"

        try:
            if "email" in cambios:

                nuevo_email = cambios["email"].lower()

                if nuevo_email in cls.emails_registrados(id_estudiante):
                    return False, "El email ya está registrado"

            for campo, valor in cambios.items():

                if campo in cls.MODELO.CAMPOS:
                    setattr(estudiante, campo, valor)

            registros = cls._registros()

            for i in range(len(registros)):

                if registros[i]["id"] == id_estudiante:
                    registros[i] = estudiante.a_diccionario()
                    break

            cls._gestor.guardar(registros)

            return True, "Estudiante actualizado correctamente"

        except ValueError as error:
            return False, str(error)

    @classmethod
    def eliminar(cls, id_estudiante):
        registros = cls._registros()

        nuevos = []

        encontrado = False

        for registro in registros:

            if registro["id"] == id_estudiante:
                encontrado = True
            else:
                nuevos.append(registro)

        if not encontrado:
            return False, "Estudiante no encontrado"

        cls._gestor.guardar(nuevos)

        return True, "Estudiante eliminado correctamente"


class EstudianteController(ClienteController):
    MODELO = Estudiante
    ARCHIVO = "data/estudiantes.json"

    CAMPOS_BUSCABLES = (
        "nombre",
        "apellido",
        "email",
        "carnet"
    )

    _gestor = GestorJSON(ARCHIVO)

    @classmethod
    def carnets_registrados(cls, excepto_id=None):
        carnets = set()

        for registro in cls._registros():

            if registro["id"] != excepto_id:
                carnets.add(
                    registro["carnet"].upper()
                )

        return carnets

    @classmethod
    def crear(cls, datos):
        carnet = datos["carnet"].upper()

        if carnet in cls.carnets_registrados():
            return False, "El carnet ya está registrado"

        return super().crear(datos)

    @classmethod
    def actualizar(cls, id_estudiante, cambios):

        if "carnet" in cambios:

            carnet = cambios["carnet"].upper()

            if carnet in cls.carnets_registrados(id_estudiante):
                return False, "El carnet ya está registrado"

        return super().actualizar(
            id_estudiante,
            cambios
        )

    @classmethod
    def agregar_nota(
        cls,
        id_estudiante,
        materia,
        nota
    ):
        estudiante = cls.obtener(id_estudiante)

        if estudiante is None:
            return False, "Estudiante no encontrado"

        try:
            estudiante.agregar_nota(
                materia,
                nota
            )

            registros = cls._registros()

            for i in range(len(registros)):

                if registros[i]["id"] == id_estudiante:
                    registros[i] = estudiante.a_diccionario()
                    break

            cls._gestor.guardar(registros)

            return True, "Nota agregada correctamente"

        except ValueError as error:
            return False, str(error)

    @classmethod
    def materias_ofertadas(cls):
        materias = set()

        for estudiante in cls.listar():
            materias.update(estudiante.materias)

        return materias

    @classmethod
    def materias_en_comun(
        cls,
        id_a,
        id_b
    ):
        estudiante_a = cls.obtener(id_a)
        estudiante_b = cls.obtener(id_b)

        if estudiante_a is None:
            return None

        if estudiante_b is None:
            return None

        return estudiante_a.materias_en_comun(
            estudiante_b
        )