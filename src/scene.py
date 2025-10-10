# Posiciona una cámara, administra los objetos y sus Graphics (VBO, VAO,
# ShaderProgram). Realiza transformaciones a los objetos que están en la escena y
# actualiza sus shaders. También actualiza viewport en on_resize.

from graphics import Graphics
import glm
import math
from raytracer import RayTracer


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
    
    def start(self):
        print("Startt!!!!!")

    # --- NUEVA FIRMA: recibimos model (objeto) y material ---
    def add_object(self, model, material):
        self.objects.append(model)
        # Graphics ahora se crea con (ctx, model, material)
        self.graphics[model.name] = Graphics(self.ctx, model, material)

    def render(self):
        self.time += 0.01 
        for obj in self.objects:
            if (obj.animated):
                # Rotaciones por frame (X, Y, Z)
                obj.rotation += glm.vec3(0.8, 0.6, 0.4)
                # Pequeño desplazamiento en X con el tiempo
                obj.position.x = math.sin(self.time) * 0.01

            model = obj.get_model_matrix()
            mvp = self.projection * self.view * model
            self.graphics[obj.name].render({'Mvp': mvp})

    def on_mouse_click(self, u, v):
        ray = self.camera.raycast(u, v)

        hit_any = False
        for obj in self.objects:
            if hasattr(obj, "check_hit") and callable(getattr(obj, "check_hit")):
                if obj.check_hit(ray.origin, ray.direction):
                    print(f"¡Golpeaste al objeto {obj.name}!")
                    hit_any = True

        if not hit_any:
            print("No golpeaste ningún objeto.")

    def on_resize(self, width, height):
        # Actualizar viewport de OpenGL
        self.ctx.viewport = (0, 0, width, height)

        # Actualizar parámetros de cámara y su matriz de proyección
        self.camera.aspect = width / max(1, height)
        self.projection = self.camera.get_perspective_matrix()

class RayScene(Scene):
    def __init__(self, ctx, camera, width, height):
        super().__init__(ctx, camera)
        self.raytracer= RayTracer(camera, width, height)
    
    def start(self):
        self.raytracer.render_frame(self.objects)
        if "Sprite" in self.graphics:
            self.graphics["Sprite"].update_texture("u_texture", self.raytracer.get_texture())
        
    def render(self):
        super().render()

    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.raytracer= RayTracer(self.camera, width, height)
        self.start()