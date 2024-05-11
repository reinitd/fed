from ursina import Entity, camera, lerp, time, Text, held_keys, mouse, curve, Vec3, clamp, color, Button, window, Default, Quad, Grid
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.scripts.property_generator import generate_properties_for_class

@generate_properties_for_class()
class HealthBar(Button):

    def __init__(self, max_value=100, value=Default, roundness=.25, animation_duration=.1, show_text=True, show_lines=False, text_size=.7, origin=(-.5,.5), **kwargs):
        super().__init__(
            position=(-.49*window.aspect_ratio,.48),
            scale=(Text.size*7.25,Text.size),
            origin=origin,
            color=color.black,
            text='Health: hp / max hp',
            text_size=text_size,
            radius=roundness,
            ignore=True
        )

        # self.bar = Entity(parent=self, model=Quad(radius=roundness), origin=origin, z=-.005, color=color.red.tint(-.2), ignore=True)
        # self.lines = Entity(parent=self.bar, y=-1, color=color.black33, ignore=True, enabled=show_lines, z=-.05)

        self.max_value = max_value
        self.clamp = False
        self.roundness = roundness
        self.animation_duration = animation_duration
        self.show_lines = show_lines
        self.show_text = show_text
        self.value = self.max_value if value == Default else value

        for key, value in kwargs.items():
            setattr(self, key, value)

        self.text_entity.enabled = show_text


    def value_setter(self, n):
        if self.clamp:
            n = clamp(n, 0, self.max_value)

        self._value = n
        self.text_entity.text = f'Health: {n} / {self.max_value}'

    def show_text_getter(self):
        return self.text_entity.enabled
    def show_text_setter(self, value):
        self.text_entity.enabled = value

    def __setattr__(self, name, value):
        if 'scale' and hasattr(self, 'model') and self.model:
            self.model.aspect = self.world_scale_x / self.world_scale_y
            self.model.generate()
            if hasattr(self, 'text_entity') and self.text_entity:
                self.text_entity.world_scale = 25 * self.text_size

        super().__setattr__(name, value)

class Player(Entity):
    def __init__(self, **kwargs):
        self.controller = FirstPersonController(
            jump_height = 5,
            jump_up_duration = .55,
            gravity = .75,
            **kwargs
        )
        self.defaultSpeed = 20
        self.defaultFov = 100
        self.defaultSensitivity = (100,100)
        self.defaultCameraPivotY = 3
        self.targetSpeed = self.defaultSpeed
        self.targetFov = self.defaultFov
        self.slide_speed = 0
        self.slide_acceleration = 0.1
        self.turn_speed = 100
        self.is_sliding = False
        self.target_rotation = self.controller.rotation_y
        self.target_camera_pivot_y = self.defaultCameraPivotY
        self.turning_speed = 75
        
        self.health = 100
        self.__healthbar = HealthBar(max_value=100, value=self.health, roundess=.25)

        self.controller.speed = self.defaultSpeed
        self.controller.mouse_sensitivity = self.defaultSensitivity
        camera.fov = self.defaultFov
        super().__init__(
            parent=self.controller
            )

    
    def input(self,key):        
        # sprint
        if key == 'left shift':
            self.targetSpeed = self.defaultSpeed + 20
            self.targetFov = self.defaultFov + 10
        elif key == 'left shift up':
            self.targetSpeed = self.defaultSpeed
            self.targetFov = self.defaultFov
    
        # slide
        if key == 'e':
            self.slide_speed = self.controller.speed
            # self.controller.camera_pivot.y = 1
            self.target_camera_pivot_y = self.defaultCameraPivotY / 2
            self.is_sliding = True
        elif key == 'e up':
            self.slide_speed = 0
            # self.controller.camera_pivot.y = 2
            self.target_camera_pivot_y = self.defaultCameraPivotY
            self.is_sliding = False
        
        # slow walk
        if key == 'x':
            camera.fov = 90
            self.controller.speed = 3
        elif key == 'x up':
            camera.fov = self.defaultFov
            self.controller.speed = self.defaultSpeed
        
        # zoom
        if key == '1':
            self.targetFov = 20
            self.controller.mouse_sensitivity = (10,10)
        elif key == '1 up':
            self.targetFov = self.defaultFov
            self.controller.mouse_sensitivity = self.defaultSensitivity

    
    def update(self):
        if self.controller.y < -1:
            self.controller.position = (0, 10, 0)

        
        if self.__healthbar: self.__healthbar.value = self.health


        self.controller.speed = lerp(self.controller.speed, self.targetSpeed, time.dt * 10)
        camera.fov = lerp(camera.fov, self.targetFov, time.dt * 10)
        self.controller.camera_pivot.y = lerp(
            self.controller.camera_pivot.y,
            self.target_camera_pivot_y,
            time.dt * 10
        )
        
        
        if self.is_sliding:
            self.controller.speed = self.slide_speed
            self.slide_speed -= 0.2  # Deceleration

            mouse_movement = mouse.velocity[0]
            turn_amount = self.turning_speed * mouse_movement
            self.controller.camera_pivot.rotation_z = lerp(
                self.controller.camera_pivot.rotation_z,
                turn_amount,
                time.dt * 10
            )
        else:
            self.controller.camera_pivot.rotation_z = lerp(
                self.controller.camera_pivot.rotation_z,
                0,
                time.dt * 10
            )
