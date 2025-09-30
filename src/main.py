#ejecuta el programa, crea un ventana window, un shaderprogram
#una scene, crea las instancias de los objetivos graficos (cube)
#crea la camra y la posiciona
#agrega los objetos en la escena y corre el loop principal

from window import Window
from shader_program import ShaderProgram
from cube import Cube
from camera import Camera
from scene import Scene


# ventana
window = Window(800, 600, "Basic Grapphic Engine")

# shader
shader_program = ShaderProgram(window.ctx , '../shaders/basic.vert', '../shaders/basic.frag')

# camara
camera = Camera((0,0,6), (0,0,0), (0,1,0), 45, window.width / window.height, 0.1, 100.0)

#objetos
cube1 = Cube ((-2,0,0), (0,45,0), (1,1,1), name="Cube1")
cube2 = Cube ((2,0,0), (0,45,0), (1,1,1), name="Cube2")


#escena
scene = Scene(window.ctx, camera)
scene.add_object(cube1, shader_program)
scene.add_object(cube2, shader_program)

#carga de la escena y ejecución del loop principal

window.set_scene(scene)
window.run()