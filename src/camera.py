import glm
from ray import Ray

# Datos de una cámara simple
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

    def raycast(self, u, v):
        # Ajuste por FOV
        fov_adjustment = glm.tan(glm.radians(self.fov) / 2)

        # NDC (Normalised Device Coordinates) en [-1,1]
        ndc_x = (2 * u - 1) * self.aspect * fov_adjustment
        ndc_y = (2 * v - 1) * fov_adjustment

        # Dirección en espacio cámara
        ray_dir_camera = glm.vec3(ndc_x, ndc_y, -1.0)
        ray_dir_camera = glm.normalize(ray_dir_camera)

        # Transformar a espacio mundo
        view = self.get_view_matrix()
        inv_view = glm.inverse(view)
        ray_dir_world = glm.vec3(inv_view * glm.vec4(ray_dir_camera, 0.0))

        return Ray(self.position, ray_dir_world)
