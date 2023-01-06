from math import atan, pi, sqrt
import random
import pyglet

collision = False
tracing = False

planets_mass = 5
planets_scale_factor = 8
planets_num = 0
planets_clr = (0, 0, 0, 0)

update_dt = 0.02

planets_obj = []
planets_shp = []
traces_shp = []

planets_obj_len = 0
traces_shp_len = 0

# window + clear
clear_r = 30
clear_g = 30
clear_b = 30
clear_a = 255

win = pyglet.window.Window(1800, 800)
pyglet.gl.glClearColor(clear_r/255, clear_g/255, clear_b/255, clear_a/200)

clear_recs_shp = []

# launch
launch_x = -1
launch_y = -1
launch_x2 = 0
launch_y2 = 0
launch_line = pyglet.shapes.Line(
    launch_x, 
    launch_y, 
    launch_x2, 
    launch_y2,
    3)

@win.event
def on_draw():

    global traces_shp, planets_num, planets_obj_len, traces_shp_len

    win.clear()

    launch_line.draw()
    
    if tracing:
        for t in traces_shp:
            t.draw()

    if tracing:
        for s in planets_shp:

            if traces_shp_len > (planets_obj_len) * 100:
                del traces_shp[:planets_obj_len]
                traces_shp_len -= planets_obj_len
            
            tmp = list(s.color)
            tmp[3] = 10
            trace_clr = tmp
            traces_shp.append(pyglet.shapes.Circle(s.x, s.y, s.radius * 0.8, 8, trace_clr))
            traces_shp_len += 1

    for s in planets_shp:
        s.draw()

@win.event
def on_mouse_press(x, y, button, modifiers):
    pass

@win.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):

    global launch_x, launch_y, launch_x2, launch_y2, planets_scale_factor, planets_mass

    if launch_x == -1 and launch_y == -1:
        launch_x = x
        launch_y = y

    length = sqrt((x - launch_x)**2 + (y - launch_y)**2)

    launch_line.x = launch_x
    launch_line.y = launch_y
    launch_line.x2 = x
    launch_line.y2 = y
    launch_x2 = x
    launch_y2 = y

    launch_line.color = (round(atan(length/50)*240/(pi/2)), 186 - round(atan(length/50)*186/(pi/2)), 255 - round(atan(length/50)*230/(pi/2)), 255)

@win.event
def on_mouse_release(x, y, button, modifier):

    global launch_x, launch_y, launch_x2, launch_y2, planets_obj_len, traces_shp_len

    obj_x = launch_x
    obj_y = launch_y
    force_x = launch_x - launch_x2
    force_y = launch_y - launch_y2

    if launch_x == -1 and launch_y == -1:
        obj_x = x
        obj_y = y
        force_x = 0
        force_y = 0

    obj = Obj(
        obj_x,
        obj_y,
        planets_mass,
        planets_scale_factor * ((planets_mass/pi)*(3/4)) ** (1/3),
        Force(force_x / 20, force_y / 20))

    launch_x = -1
    launch_y = -1
    launch_line.color = (0, 0, 0, 0)

    planets_obj.append(obj)
    planets_shp.append(pyglet.shapes.Circle(obj.x, obj.y, obj.r, 16, planets_clr))
    planets_obj_len += 1

@win.event
def on_key_press(symbol, modifiers):

    global planets_obj, planets_shp, traces_shp, planets_mass, planets_obj_len, traces_shp_len, tracing

    if symbol == pyglet.window.key.X:
        planets_obj = []
        planets_obj_len = 0
        planets_shp = []
        traces_shp = []
        traces_shp_len = 0
    
    if symbol == pyglet.window.key.T:
        
        if tracing == False:
            tracing = True
        else:
            tracing = False

    if symbol == pyglet.window.key._1:
        planets_mass = 1
    
    if symbol == pyglet.window.key._2:
        planets_mass = 2
    
    if symbol == pyglet.window.key._3:
        planets_mass = 3
    
    if symbol == pyglet.window.key._4:
        planets_mass = 4

    if symbol == pyglet.window.key._5:
        planets_mass = 5

    if symbol == pyglet.window.key._6:
        planets_mass = 6

    if symbol == pyglet.window.key._7:
        planets_mass = 7

    if symbol == pyglet.window.key._8:
        planets_mass = 8

    if symbol == pyglet.window.key._9:
        planets_mass = 9

def update(dt):

    for star in planets_obj:
        for planet in planets_obj:
            if (star != planet):
                add_force(planet, star)

    for o, s in zip(planets_obj, planets_shp):
        o.x += o.force.x
        o.y += o.force.y
        s.color = (round(atan(o.force.val/2)*240/(pi/2)), 186 - round(atan(o.force.val/2)*186/(pi/2)), 255 - round(atan(o.force.val/2)*230/(pi/2)), 255)

    for s, o in zip(planets_shp, planets_obj):
        s.x = o.x
        s.y = o.y

if __name__ == '__main__':

    middle_x = win.width / 2
    middle_y = win.height / 2

    class Obj:
        def __init__(self, x, y, mass, r, force):
            self.x = x
            self.y = y
            self.mass = mass
            self.r = r
            self.force = force

    class Force:
        def __init__(self, x, y):
            self.x = x
            self.y = y

        @property
        def val(self):
            return sqrt(self.x**2 + self.y**2)

    def add_force(obj_p, obj_s):

        d_x = obj_s.x - obj_p.x
        d_y = obj_s.y - obj_p.y

        if d_x == 0:
            d_x = 1
        if d_y == 0:
            d_y = 1

        d_xy = sqrt(d_x**2 + d_y**2)

        if not collision or d_xy > obj_p.r + obj_s.r:
            obj_p.force.x += d_x * obj_s.mass / d_xy**2
            obj_p.force.y += d_y * obj_s.mass / d_xy**2
        else:
            obj_p.x += (d_xy - (obj_p.r + obj_s.r)) * d_x
            obj_p.y += (d_xy - (obj_p.r + obj_s.r)) * d_y
            obj_s.force.x += obj_p.force.x
            obj_s.force.y += obj_p.force.y
            obj_p.force.x = 0
            obj_p.force.y = 0

    for p in range(planets_num):

        obj = Obj(
            win.width * (random.random() * 0.5 + 0.25),
            win.height * (random.random() * 0.5 + 0.25),
            planets_mass,
            planets_scale_factor * ((planets_mass/pi)*(3/4)) ** (1/3),
            Force(0, 0))

        planets_obj.append(obj)
        planets_shp.append(pyglet.shapes.Circle(obj.x, obj.y, obj.r, 32, planets_clr))
        planets_obj_len += 1

    pyglet.clock.schedule_interval(update, update_dt)
    pyglet.app.run()
