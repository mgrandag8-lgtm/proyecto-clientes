class Estudiante:
    CAMPOS = ("nombre", "apellido", "email", "carnet")
    OBLIGATORIOS = ("nombre", "apellido", "email", "carnet")

    NOTA_MINIMA = 0
    NOTA_MAXIMA = 20

    def __init__(
        self,
        id,
        nombre,
        apellido,
        email,
        carnet,
        notas=None,
        materias=None
    ):
        self.__id = id
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.carnet = carnet

        self.__notas = dict(notas) if notas else {}
        self.__materias = set(materias) if materias else set()

    @property
    def id(self):
        return self.__id

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        valor = valor.strip()

        if valor == "":
            raise ValueError("El nombre no puede estar vacío")

        self.__nombre = valor.title()

    @property
    def apellido(self):
        return self.__apellido

    @apellido.setter
    def apellido(self, valor):
        valor = valor.strip()

        if valor == "":
            raise ValueError("El apellido no puede estar vacío")

        self.__apellido = valor.title()

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, valor):
        valor = valor.strip().lower()

        if "@" not in valor:
            raise ValueError("Email inválido")

        self.__email = valor

    @property
    def carnet(self):
        return self.__carnet

    @carnet.setter
    def carnet(self, valor):
        valor = valor.strip().upper()

        if valor == "":
            raise ValueError("El carnet no puede estar vacío")

        self.__carnet = valor

    @property
    def materias(self):
        return self.__materias.copy()

    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    @staticmethod
    def nota_valida(nota):
        return (
            isinstance(nota, (int, float))
            and Estudiante.NOTA_MINIMA <= nota <= Estudiante.NOTA_MAXIMA
        )

    def inscribir_materia(self, materia):
        materia = materia.strip().title()

        if materia == "":
            raise ValueError("La materia no puede estar vacía")

        self.__materias.add(materia)

        return materia

    def agregar_nota(self, materia, nota):
        if not self.nota_valida(nota):
            raise ValueError("La nota debe estar entre 0 y 20")

        materia = self.inscribir_materia(materia)

        if materia not in self.__notas:
            self.__notas[materia] = []

        self.__notas[materia].append(nota)

    def notas_de(self, materia):
        return self.__notas.get(materia.title(), []).copy()

    @property
    def promedio(self):
        todas_las_notas = []

        for notas_materia in self.__notas.values():
            todas_las_notas.extend(notas_materia)

        if len(todas_las_notas) == 0:
            return 0

        return round(
            sum(todas_las_notas) / len(todas_las_notas),
            2
        )

    @property
    def estado(self):
        if self.promedio >= 14:
            return "Aprobado"

        return "Reprobado"

    def materias_en_comun(self, otro):
        return self.__materias & otro.materias

    def a_diccionario(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "carnet": self.carnet,
            "notas": self.__notas,
            "materias": sorted(self.__materias)
        }

    @classmethod
    def desde_diccionario(cls, datos):
        return cls(
            datos["id"],
            datos["nombre"],
            datos["apellido"],
            datos["email"],
            datos["carnet"],
            datos.get("notas", {}),
            datos.get("materias", [])
        )

    def __str__(self):
        return (
            f"ID: {self.id} | "
            f"{self.nombre_completo} | "
            f"{self.email} | "
            f"{self.carnet}"
        )