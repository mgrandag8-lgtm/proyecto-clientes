import json
import os


class GestorJSON:
    def __init__(self, ruta):
        self.__ruta = ruta

        carpeta = os.path.dirname(ruta)

        if carpeta and not os.path.exists(carpeta):
            os.makedirs(carpeta)

    @property
    def ruta(self):
        return self.__ruta

    def leer(self):
        if not os.path.exists(self.__ruta):
            return []

        try:
            with open(
                self.__ruta,
                "r",
                encoding="utf-8"
            ) as archivo:

                datos = json.load(archivo)

            if isinstance(datos, list):
                return datos

            return []

        except (json.JSONDecodeError, OSError):
            return []

    def guardar(self, datos):
        try:
            with open(
                self.__ruta,
                "w",
                encoding="utf-8"
            ) as archivo:

                json.dump(
                    datos,
                    archivo,
                    ensure_ascii=False,
                    indent=2
                )

            return True

        except (TypeError, OSError):
            return False