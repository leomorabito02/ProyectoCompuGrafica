# ejecuta el programa, crea una ventana Window, un ShaderProgram,
# una Scene, crea las instancias de los objetos gráficos (Cube),
# crea la cámara y la posiciona, agrega los objetos y corre el loop.

import os
from window import Window
from shader_program import ShaderProgram
from cube import Cube
from camera import Camera
from scene import Scene

# --- ventana ---
window = Window(800, 600, "Basic Graphic Engine")

# --- shader ---
shader_program = ShaderProgram(window.ctx , '../shaders/basic.vert', '../shaders/basic.frag')

# --- cámara ---
camera = Camera((0, 0, 6), (0, 0, 0), (0, 1, 0), 45, window.width / window.height, 0.1, 100.0)

# --- objetos ---
cube1 = Cube((-2, 0, 0), (0, 45, 0), (1, 1, 1), name="Cube1")
cube2 = Cube(( 2, 0, 0), (0, 45, 0), (1, 0.5, 1), name="Cube2")  

# --- escena ---
scene = Scene(window.ctx, camera)
scene.add_object(cube1, shader_program)
scene.add_object(cube2, shader_program)

# --- carga y loop principal ---
window.set_scene(scene)
window.run()
