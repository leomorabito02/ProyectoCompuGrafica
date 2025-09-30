import glm

#datos de una camara simple
# Útil para obtener las coordenadas de la cámara y su proyección
class Camera:
    def __init__(self, position, target, up, fov, aspect, near, far):
        self.position = glm.vec3(*position)
        self.target = glm.vec3(*target)
        self.up = glm.vec3(*up)
        self.fov = fov
        self.aspect = aspect
        self.near = near
        self.far = far


    def get_perspective_matrix(self):
        return glm.perspective(glm.radians(self.fov), self.aspect, self.near, self.far)

    def get_view_matrix(self):
        return glm.lookAt(self.position, self.target, self.up)

