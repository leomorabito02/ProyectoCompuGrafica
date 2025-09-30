# Posiciona una cámara, administra los objetos y sus Graphics (VBO, VAO,
#ShaderProgram). Realiza transformaciones a los objetos que están en la escena y
#actualiza sus shaders. También actualiza viewport en on resize.
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
        self.time = 0
    def add_object(self, obj, shader_program=None):
        self.objects.append(obj)
        self.graphics[obj.name] = Graphics(self.ctx, shader_program, obj.vertices, obj.indices)
    

    def render(self):
        self.time += 0.01
        # la camara expone su view con view_matrix y 
        view = self.camera.get_view_matrix()
        # la proyeccion con get_perspective_matrix
        projection = self.camera.get_perspective_matrix()

        for obj in self.objects:
            obj.rotation.y += 0.57 # 0.01 radianes en grados
            obj.position.x += math.sin(self.time) * 0.01
            model = obj.get_model_matrix()
            mvp = projection * view * model
            sp = self.graphics[obj.name].shader_program
            sp.set_uniform("Mvp", mvp)

            self.graphics[obj.name].vao.render()
    
    def on_resize(self, width, height):
        self.ctx.viewport = (0,0,width,height)
        self.camera.projection = glm.perspective(glm.radians(45),width/height, 0.1 , 100.0 )
