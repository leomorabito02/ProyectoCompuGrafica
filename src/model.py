# model.py
# Abstracciones para describir la data de un modelo 3D:
# - Vertex: un atributo (posiciones, colores, normales, UVs, etc.)
# - VertexLayout: colección de atributos
# - Model: índice + layout con los atributos disponibles

from typing import List, Optional, Sequence, Any

class Vertex:
    def __init__(self, name: str, format: str, array: Sequence[Any]):
        self.__name = name          # ej: "in_pos", "in_color", "in_normal", "in_uv"
        self.__format = format      # ej: "3f" -> vec3 float, "2f" -> vec2 float
        self.__array = array        # datos (lista/np.array)

    @property
    def name(self) -> str:
        return self.__name

    @property
    def format(self) -> str:
        return self.__format

    @property
    def array(self) -> Sequence[Any]:
        return self.__array


class VertexLayout:
    def __init__(self):
        self.__attributes: List[Vertex] = []

    def add_attribute(self, name: str, format: str, array: Sequence[Any]) -> None:
        self.__attributes.append(Vertex(name, format, array))

    def get_attributes(self) -> List[Vertex]:
        return self.__attributes

    # atajo opcional
    def __iter__(self):
        return iter(self.__attributes)


class Model:
    def __init__(
        self,
        vertices: Optional[Sequence[Any]] = None,
        indices:  Optional[Sequence[int]] = None,
        colors:   Optional[Sequence[Any]] = None,
        normals:  Optional[Sequence[Any]] = None,
        texcoords: Optional[Sequence[Any]] = None,
    ):
        self.indices = indices
        self.vertex_layout = VertexLayout()

        if vertices is not None:
            self.vertex_layout.add_attribute("in_pos",   "3f", vertices)

        if colors is not None:
            self.vertex_layout.add_attribute("in_color", "3f", colors)

        if normals is not None:
            self.vertex_layout.add_attribute("in_normal","3f", normals)

        if texcoords is not None:
            self.vertex_layout.add_attribute("in_uv",    "2f", texcoords)

    # Helpers
    def attributes(self) -> List[Vertex]:
        return self.vertex_layout.get_attributes()

    def has_indices(self) -> bool:
        return self.indices is not None
