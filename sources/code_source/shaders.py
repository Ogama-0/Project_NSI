import pygame,sys,moderngl
from array import array
class shader_None :
    def __init__(self):

        self.ctx = moderngl.create_context()
        self.quad_buffer = self.ctx.buffer(data = array('f',[
        -1.0, 1.0, 0.0, 0.0,    # upleft
        1.0, 1.0, 1.0, 0.0,     # up rignt
        -1.0, -1.0, 0.0, 1.0,   # bottom left
        1.0, -1.0, 1.0, 1.0,    # bottom right
        ]))
        ver_shaders = '''
        # version 330 core

        in vec2 vert;
        in vec2 texcoord;
        out vec2 uvs;

            void main() {
            uvs = texcoord;
            gl_Position = vec4(vert.x, vert.y, 0.0, 1.0);
        } 
        '''
        frag_shader = '''
        # version 330 core

        uniform sampler2D tex;
        uniform float time;

        in vec2 uvs;
        out vec4 f_color;

        void main() {
            vec2 sample_pos = vec2(uvs.x + time * 0, uvs.y); 
            f_color = vec4(texture(tex, sample_pos).rgb, 1.0);
        }
        '''
        self.program = self.ctx.program(vertex_shader=ver_shaders, fragment_shader=frag_shader)
        self.render_object = self.ctx.vertex_array(self.program, [(self.quad_buffer,'2f 2f','vert','texcoord')])# 2f 2f c'est la spécification du format(donc 2float et 2float) et donc le premier 2f s'appelle 'vert' et le deuxième s'appelle 'texcoord', Ca fait allusion au buffer du debut mathox1Modeste

    def surf_to_texture(self,surf : pygame.surface.Surface) :
        tex = self.ctx.texture(surf.get_size(), 4)# 4 c'est le nombre de canneaux de couleurs donc ici rgb et Alpha
        tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
        tex.swizzle = 'BGRA'
        tex.write(surf.get_view('1'))# 1 c'est le format souhaiter
        return tex


class Shader_eau:
    def __init__(self):

        self.ctx = moderngl.create_context()
        self.quad_buffer = self.ctx.buffer(data = array('f',[
        -1.0, 1.0, 0.0, 0.0,    # upleft
        1.0, 1.0, 1.0, 0.0,     # up rignt
        -1.0, -1.0, 0.0, 1.0,   # bottom left
        1.0, -1.0, 1.0, 1.0,    # bottom right
        ]))
        ver_shaders = '''
        # version 330 core

        in vec2 vert;
        in vec2 texcoord;
        out vec2 uvs;

            void main() {
            uvs = texcoord;
            gl_Position = vec4(vert.x, vert.y, 0.0, 1.0);
        } 
        '''
        frag_shader = '''
        # version 330 core

        uniform sampler2D tex;
        uniform float time;

        in vec2 uvs;
        out vec4 f_color;

        void main() {
            vec2 sample_pos = vec2(uvs.x + cos(uvs.y * 10 + time * 0.04)*0.01, uvs.y); 
            f_color = vec4(texture(tex, sample_pos).rg,texture(tex, sample_pos).b*1.4, 1.0);
        }
        '''
        self.program = self.ctx.program(vertex_shader=ver_shaders, fragment_shader=frag_shader)
        self.render_object = self.ctx.vertex_array(self.program, [(self.quad_buffer,'2f 2f','vert','texcoord')])# 2f 2f c'est la spécification du format(donc 2float et 2float) et donc le premier 2f s'appelle 'vert' et le deuxième s'appelle 'texcoord', Ca fait allusion au buffer du debut mathox1Modeste

    def surf_to_texture(self,surf : pygame.surface.Surface) :
        tex = self.ctx.texture(surf.get_size(), 4)# 4 c'est le nombre de canneaux de couleurs donc ici rgb et Alpha
        tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
        tex.swizzle = 'BGRA'
        tex.write(surf.get_view('1'))# 1 c'est le format souhaiter
        return tex
    


if __name__ == '__main__' :
    pygame.init()
    screen = pygame.display.set_mode((700,700),pygame.OPENGL | pygame.DOUBLEBUF)
    display = pygame.Surface(screen.get_size())
    clock = pygame.time.Clock()
    img = pygame.transform.scale(pygame.image.load("img.png"),screen.get_size())


    shaders = Shader_eau()

    t = 0
    while True :
        t += 1
        display.fill((0,0,0))
        display.blit(img,(0,0))

        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                pygame.quit()
                sys.exit()

        

        frame_tex = shaders.surf_to_texture(display)
        frame_tex.use(0)
        shaders.program['tex'] = 0
        shaders.program['time'] = t
        shaders.render_object.render(mode=moderngl.TRIANGLE_STRIP)

        pygame.display.flip()
        frame_tex.release()
        clock.tick(60)


