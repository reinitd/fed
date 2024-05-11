from ursina import Entity, camera, lerp, time, held_keys, mouse, Vec3, clamp, color
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.prefabs.health_bar import HealthBar

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
        self.turning_speed = 50
        
        self.health = 100
        self.__healthbar = HealthBar(max_value=100, value=self.health)

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
