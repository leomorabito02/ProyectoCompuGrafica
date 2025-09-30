# Posiciona una cámara, administra los objetos y sus Graphics (VBO, VAO,
# ShaderProgram). Realiza transformaciones a los objetos que están en la escena y
# actualiza sus shaders. También actualiza viewport en on_resize.

from graphics import Graphics
import glm
import math

class Scene:
    def __init__(self, ctx, camera):
        self.ctx = ctx
        self.objects = []
        self.graphics = {}
        self.camera = camera
        self.model = glm.mat4(1)
        self.view = camera.get_view_matrix()
        self.projection = camera.get_perspective_matrix()
        self.time = 0  # en el constructor definir self.time = 0

    def add_object(self, obj, shader_program=None):
        self.objects.append(obj)
        self.graphics[obj.name] = Graphics(self.ctx, shader_program, obj.vertices, obj.indices)

    def render(self):
        self.time += 0.01  # avanzar el tiempo

        # Actualizar matrices de cámara y usarlas directo (como en la imagen)
        self.view = self.camera.get_view_matrix()
        self.projection = self.camera.get_perspective_matrix()

        for obj in self.objects:
            # --- Código de la imagen: rotar en X, Y, Z ---
            obj.rotation.x += 0.8   # rotar en X
            obj.rotation.y += 0.6   # rotar en Y
            obj.rotation.z += 0.4   # rotar en Z

            # Pequeño desplazamiento en X con el tiempo
            obj.position.x += math.sin(self.time) * 0.01

            # Calcular matrices y pasar uniformes
            model = obj.get_model_matrix()
            mvp = self.projection * self.view * model

            sp = self.graphics[obj.name].shader_program
            sp.set_uniform("Mvp", mvp)

            self.graphics[obj.name].vao.render()

    def on_mouse_click(self, u, v):
        """u, v en [0,1] desde Window.on_mouse_press"""
        ray = self.camera.raycast(u, v)

        hit_any = False
        for obj in self.objects:
            if hasattr(obj, "check_hit") and callable(getattr(obj, "check_hit")):
                if obj.check_hit(ray.origin, ray.direction):
                    print(f"¡Golpeaste al objeto {obj.name}!")
                    hit_any = True
                    # break  # descomentá si querés cortar en el primer hit

        if not hit_any:
            print("No golpeaste ningún objeto.")

    def on_resize(self, width, height):
        # Actualizar viewport de OpenGL
        self.ctx.viewport = (0, 0, width, height)

        # Actualizar parámetros de cámara y su matriz de proyección
        self.camera.aspect = width / max(1, height)
        self.projection = self.camera.get_perspective_matrix()
