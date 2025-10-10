import glm
import math

class Hit:
    def __init__(self, get_model_matrix, hittable = True):
        self.__model_matrix = get_model_matrix
        self.hittable = hittable

    @property
    def model_matrix(self):
        return self.__model_matrix()

    @property
    def position(self):
        m = self.model_matrix
        return glm.vec3(m[3].x, m[3].y, m[3].z)

    @property
    def scale(self):
        m = self.model_matrix
        return glm.vec3(
            glm.length(glm.vec3(m[0])),
            glm.length(glm.vec3(m[1])),
            glm.length(glm.vec3(m[2])),
        )

    def check_hit(self, origin, direction) -> bool:
        raise NotImplementedError("Subclasses should implement this method.")


class HitBoxOBB(Hit):
    def __init__(self, get_model_matrix, hittable = True):
        super().__init__(get_model_matrix, hittable)

    def check_hit(self,origin,direction):
        if (not self.hittable):
            return False
        
        origin = glm.vec3(origin)
        direction = glm.normalize(glm.vec3(direction))

        #con la inversa, transformamos el rayo en sus componentes locales
        inv_model = glm.inverse(self.model_matrix)
        #multiplicamos el origen del rayo por la inversa usando coordenadas homogéneas w = 1.0 (porque es un punto)
        local_origin = inv_model * glm.vec4(origin, 1.0)
        #multiplicamos la dirección por la misma inversa con w = 0.0,  no debe verse afectada por la traslación
        local_dir = inv_model * glm.vec4(direction, 0.0)

        # convertimos el resultado a vec3 (local_origin, local_dir)
        local_origin = glm.vec3(local_origin)

        #normalizamos local_dir para obtener una dirección unitaria en el espacio local.
        local_dir = glm.normalize(glm.vec3(local_dir))

        # calculamos los limites de la cajausando las variables transformadas al espacio total
        mix_bounds = glm.vec3(-1,-1,-1)
        max_bounds = glm.vec3(1,1,1)

        # para cada eje, se despeja el valor de t de la ecuación usando como origen los planos de min y max
        # entrada del rayo en ese eje
        tmin = (mix_bounds - local_origin) / local_dir
        #salida del rayo en ese eje
        tmax = (max_bounds - local_origin) / local_dir

        # como no sabemos los valores, reorganizamos los valores para que t1 siempre sea la entrada
        t1 = glm.min(tmin,tmax)
        t2 = glm.max(tmin,tmax)

        t_near = max(t1.x, t1.y, t1.z)
        t_far = min(t2.x, t2.y, t2.z)

        return t_near <= t_far and t_far >= 0


class HitBox(Hit):
    def __init__(self, get_model_matrix, hittable = True):
        super().__init__(get_model_matrix, hittable)

    def check_hit(self, origin, direction):
        # Si no es hiteable, cortar
        if not self.hittable:
            return False

        origin = glm.vec3(origin)
        direction = glm.normalize(glm.vec3(direction))

        min_bounds = self.position - self.scale
        max_bounds = self.position + self.scale

        tmin = (min_bounds - origin) / direction
        tmax = (max_bounds - origin) / direction

        t1 = glm.min(tmin, tmax)
        t2 = glm.max(tmin, tmax)

        t_near = max(t1.x, t1.y, t1.z)
        t_far  = min(t2.x, t2.y, t2.z)

        return t_near <= t_far and t_far >= 0.0
