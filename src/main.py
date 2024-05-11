from entities.player import Player
from direct.stdpy import thread
from ursina import (AmbientLight, Button, EditorCamera, Entity, PointLight,
                    Sky, SmoothFollow, Ursina, Vec3, Vec2, application, camera,
                    color, destroy, mouse, random, scene, Text)


def loadLevel():
    Sky()

    PointLight(
        parent=camera,
        color=color.white,
        position=(0, 10, -1.5)
    )

    AmbientLight(
        color=color.rgba(100, 100, 100, .1)
    )

    size = 150
    height = 25
    ground = Entity(model='plane', scale=(size, 1, size), texture='floor', texture_scale=Vec2(24,24), collider='box', color=color.gray)

    wall_1 = Entity(model='cube', scale=(size, height, 1), position=(0, 1, -size/2), texture='brick', texture_scale=Vec2(22,7), collider='mesh', color=color.gray)
    wall_2 = Entity(model='cube', scale=(size, height, 1), position=(0, 1, size/2), texture='brick', texture_scale=Vec2(22,7), collider='mesh', color=color.gray)
    wall_3 = Entity(model='cube', scale=(1, height, size), position=(-size/2, 1, 0), texture='brick', texture_scale=Vec2(22,7), collider='mesh', color=color.gray)
    wall_4 = Entity(model='cube', scale=(1, height, size), position=(size/2, 1, 0), texture='brick', texture_scale=Vec2(22,7), collider='mesh', color=color.gray)
    
    block = Entity(model='cube', scale=(12, 4, 12), position=((size/2)-6, 1.75, (size/2)-6), texture='light_floor', collider='mesh', color=color.gray)
    ramp = Entity(model='cube', rotation_z = -10, scale=(32, 2, 12), position=((size/2)-27.5, 0, (size/2)-6), texture='light_floor', texture_scale=Vec2(2,1), collider='mesh', color=color.gray)
    ramp_2 = Entity(model='cube', rotation_x = -10, scale=(12, 2, 32), position=((size/2)-6, 0, (size/2)-27.5), texture='light_floor', texture_scale=Vec2(1,2), collider='mesh', color=color.gray)

    spawn_pad = Entity(model='cube', scale=(10,10,10), position=(0, -2.5, 0), texture='light_floor', texture_scale=Vec2(3,3), collider='mesh', color=color.gray)
    spawn_pad_ramp   = Entity(model='cube', rotation_z = -10, scale=(15,10,10), position=(-11.5, -3.75, 0), texture='light_floor', texture_scale=Vec2(4,3), collider='mesh', color=color.gray)
    spawn_pad_ramp_1 = Entity(model='cube', rotation_z = 10, scale=(15,10,10), position=(11.5, -3.75, 0), texture='light_floor', texture_scale=Vec2(4,3), collider='mesh', color=color.gray)
    spawn_pad_ramp_2 = Entity(model='cube', rotation_x = -10, scale=(10,10,15), position=(0, -3.75, -11.5), texture='light_floor', texture_scale=Vec2(3,4), collider='mesh', color=color.gray)
    spawn_pad_ramp_3 = Entity(model='cube', rotation_x = 10, scale=(10,10,15), position=(0, -3.75, 11.5), texture='light_floor', texture_scale=Vec2(3,4), collider='mesh', color=color.gray)

    global png

    png.add_script(
        SmoothFollow(
            target=player,
            offset=(2, 2, 2),
            speed=1.5,
            rotation_speed=25
        )
    )


def update():
    global png
    global player
    if player.health > 0:
        distance = (png.world_position - player.world_position).length()
        if distance < 4:
            player.health -= 1
    else:
        Text("GAME OVER\nPress 'esc' to quit.", size=2, origin=(0,0))
        destroy(png)
        destroy(player)
        destroy(camera)

def beginLevel():
    global play
    destroy(play)
    thread.start_new_thread(function=loadLevel, args='')

def showMenu():
    global play
    play = Button(
        '''Run from the glow in the dark CIA guys.

Click to play.

  Controls:

WASD - Move
E - Slide
L Shift - Sprint

1 - Zoom

Escape - Quit
        ''',
        scale=3,
        on_click=beginLevel
    )


def input(key):
    if key == 'escape':
        application.quit()

eC = EditorCamera(enabled=False)

if __name__ == '__main__':
    app = Ursina(
        icon="cia",
        vsync=True,
        title="Run from the CIA.",
        show_ursina_splash = False,
        borderless = False
        )

    global png
    png = Entity(
        model='cube',
        scale=Vec3(2, 2, 0),
        texture='cia',
        double_sided=True,
        collision=True,
        position=Vec3(10, 10, 10),
        collider='box'
    )

    global player
    player = Player(
        position=Vec3(0, 7, 0),
        speed=5,
        model='cube',
        collider='mesh'
    )

    showMenu()

    app.run()