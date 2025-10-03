import glm
import math

class Hit:
    def __init__(self, get_model_matrix, hittable: bool = True):
        self.__get_model_matrix = get_model_matrix
        self.hittable = hittable  # nuevo flag

    @property
    def model_matrix(self) -> glm.mat4:
        return self.__get_model_matrix()

    @property
    def position(self) -> glm.vec3:
        m = self.model_matrix
        return glm.vec3(m[3].x, m[3].y, m[3].z)

    @property
    def scale(self) -> glm.vec3:
        m = self.model_matrix
        return glm.vec3(
            glm.length(glm.vec3(m[0])),
            glm.length(glm.vec3(m[1])),
            glm.length(glm.vec3(m[2])),
        )

    def check_hit(self, origin, direction) -> bool:
        raise NotImplementedError("Subclasses should implement this method.")


class HitBoxOBB(Hit):
    def __init__(self, get_model_matrix, hittable: bool = True):
        super().__init__(get_model_matrix, hittable)

    def check_hit(self, origin, direction) -> bool:
        # Si no es hiteable, cortar
        if not self.hittable:
            return False

        # Normalizar datos de entrada
        origin = glm.vec3(origin)
        direction = glm.normalize(glm.vec3(direction))

        # Transformar a espacio local del OBB
        inv_model = glm.inverse(self.model_matrix)
        local_origin4 = inv_model * glm.vec4(origin, 1.0)
        local_dir4    = inv_model * glm.vec4(direction, 0.0)

        local_origin = glm.vec3(local_origin4)
        local_dir    = glm.normalize(glm.vec3(local_dir4))

        # AABB unitario en espacio local
        min_bounds = glm.vec3(-1.0, -1.0, -1.0)
        max_bounds = glm.vec3( 1.0,  1.0,  1.0)

        tmin = -math.inf
        tmax =  math.inf
        eps = 1e-8

        # X
        if abs(local_dir.x) < eps:
            if local_origin.x < min_bounds.x or local_origin.x > max_bounds.x:
                return False
        else:
            tx1 = (min_bounds.x - local_origin.x) / local_dir.x
            tx2 = (max_bounds.x - local_origin.x) / local_dir.x
            if tx1 > tx2: tx1, tx2 = tx2, tx1
            tmin = max(tmin, tx1)
            tmax = min(tmax, tx2)
            if tmin > tmax: return False

        # Y
        if abs(local_dir.y) < eps:
            if local_origin.y < min_bounds.y or local_origin.y > max_bounds.y:
                return False
        else:
            ty1 = (min_bounds.y - local_origin.y) / local_dir.y
            ty2 = (max_bounds.y - local_origin.y) / local_dir.y
            if ty1 > ty2: ty1, ty2 = ty2, ty1
            tmin = max(tmin, ty1)
            tmax = min(tmax, ty2)
            if tmin > tmax: return False

        # Z
        if abs(local_dir.z) < eps:
            if local_origin.z < min_bounds.z or local_origin.z > max_bounds.z:
                return False
        else:
            tz1 = (min_bounds.z - local_origin.z) / local_dir.z
            tz2 = (max_bounds.z - local_origin.z) / local_dir.z
            if tz1 > tz2: tz1, tz2 = tz2, tz1
            tmin = max(tmin, tz1)
            tmax = min(tmax, tz2)
            if tmin > tmax: return False

        return tmax >= 0.0


class HitBox(Hit):
    def __init__(self, get_model_matrix, hittable: bool = True):
        super().__init__(get_model_matrix, hittable)

    def check_hit(self, origin, direction) -> bool:
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
