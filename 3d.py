from ursina import *
import math
window.position = (0,25)
window.size = (800, 600)
leg1 = 0  # 摄像机高度偏移
me = True
ua = Ursina()
cube1=open("cube1.cube")
cube_list = eval(cube1.read())
player_speed = 0.09
# 创建方块
player = Entity(
    model='cube', 
    color= color.gray,
    position=(0, 1.5, 0),
    scale=(1, 2, 1),
    texture='img/sg1/gd1.png',
    collider='box'
) 

for i in cube_list:
    Entity(
    model='cube',
    color=color.gray,
    collider='box',
    position=(i[0],i[1],i[2]),
    scale=(1, 1, 1),
    texture='img/sg1/gd2.png'
    )

# 视角模式：True为主视角，False为第三人称
first_person = True
camera_distance = 0.5  # 主视角距离
third_distance = 6     # 第三人称距离

camera.rotation_x = 0
camera.rotation_y = 0
mouse_sensitivity = 40

mouse.locked = me


# 添加跳跃相关变量
is_jumping = False
jump_velocity = 1
gravity = -0.5 # 重力加速度，值越小重力越大

def update():
    global me, is_jumping, jump_velocity

    # 鼠标移动控制视角
    if me:
        camera.rotation_y += mouse.velocity[0] * mouse_sensitivity
        camera.rotation_x -= mouse.velocity[1] * mouse_sensitivity
        camera.rotation_x = clamp(camera.rotation_x, -90, 90)

    # 计算前后左右方向
    yaw_rad = math.radians(camera.rotation_y)
    forward = Vec3(math.sin(yaw_rad), 0, math.cos(yaw_rad))
    right = Vec3(math.sin(yaw_rad + math.pi/2), 0, math.cos(yaw_rad + math.pi/2))

    # 摄像机跟随 player
    if first_person:
        camera.position = player.position
        camera.look_at(player.position + Vec3(0, leg1, 0))

    # WASD移动
    if held_keys['w']:
        player.position += forward * player_speed
        if held_keys['ctrl']:
            player.position += forward * player_speed * 2
    if held_keys['s']:
        player.position -= forward * player_speed
        if held_keys['ctrl']:
            player.position -= forward * player_speed * 2
    if held_keys['a']:
        player.position -= right * player_speed
        if held_keys['ctrl']:
            player.position -= right * player_speed * 2
    if held_keys['d']:
        player.position += right * player_speed
        if held_keys['ctrl']:
            player.position += right * player_speed * 2

    # 跳跃逻辑
    if held_keys['space'] and not is_jumping:
        is_jumping = True
        jump_velocity = 1  # 跳跃初速度

    # 重力与跳跃
    if is_jumping:
        player.position += Vec3(0, jump_velocity, 0)
        jump_velocity += gravity * time.dt
        # 检查是否落地
        hit_info = player.intersects()
        if hit_info.hit and jump_velocity < 0:
            
            jump_velocity = 0
            # 修正落地高度
            player.position += Vec3(0,1.5,0)
            is_jumping = False
        else:
            player.position -= Vec3(0, 0.5, 0)
    if held_keys['escape']:
        me = False
        mouse.locked = me
    if held_keys['`']:
        me = True
        mouse.locked = me
    if player.position.y < -100:
        player.position = Vec3(0, 1.5, 0)
print(507171)    
ua.run()