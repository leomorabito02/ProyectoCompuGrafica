# crea el VBO, IBO y VAO con el shaderprogram  y el format
# implementa el metodo render para renderizar el vao

class Graphics:
    def __init__(self, ctx, shader_program, vertices, indices):
        self.ctx = ctx
        self.shader_program = shader_program

        #VBO IBO Y VAO
        #VBO --> vertex buffer object: almacena los datos de los vertices
        self.vbo = ctx.buffer(vertices.tobytes())
        # IBO --> index buffer object: almacena los indices para dibujar los vertices
        self.ibo = ctx.buffer(indices.tobytes())
        # VAO --> vertex array object: combina el vbo e ibo y define el formato de los datos
        self.vao = ctx.vertex_array(shader_program.prog, [(
            self.vbo, '3f 3f', 'in_pos', 'in_color')
        ], self.ibo)

    def set_shader(self, shader_program):
        self.shader_program = shader_program.prog

    def set_uniform(self, name, value):
        self.shader_program.set_uniform(name, value)