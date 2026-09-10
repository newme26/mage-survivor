import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


import pygame
import random


def spawn_wave(waves, monsters, WIDTH, wave_composition):

    for monster_class, amount in wave_composition.items():

        for i in range(amount):

            monster = monster_class(0, 0)

            monster.x = random.randint(0, WIDTH - monster.rect.width)
            monster.y = 0

            monster.rect.x = int(monster.x)
            monster.rect.y = int(monster.y)

            monsters.append(monster)


def upgrade_damage(fireball_damage):
    fireball_damage += 1
    return fireball_damage


def upgrade_max_hp(player_max_hp, player_hp):
    player_max_hp += 1
    player_hp += 1
    return player_max_hp, player_hp


def upgrade_speed(player_speed):
    player_speed += 1
    return player_speed


def upgrade_fireball_size(fireball_size):
    fireball_size += 2
    return fireball_size

def upgrade_attack_speed(fireball_cooldown):
    return max(200, fireball_cooldown - 200)


def get_player_image(player_sheet, column, row):
    image = player_sheet.subsurface((column * 16, row * 16, 16, 16))
    image = pygame.transform.scale(image, (64, 64))
    return image


def get_goblin_image(goblin_sheet, column, row):
    image = goblin_sheet.subsurface(
        (column * 16, row * 16, 16, 16)
    )
    image = pygame.transform.scale(image, (60, 60))
    return image


def get_bat_image(bat_sheet, column, row):
    image = bat_sheet.subsurface(
        (column * 16, row * 16, 16, 16)
    )
    image = pygame.transform.scale(image, (60, 60))
    return image


def get_slime_image(slime_sheet, column, row):
    image = slime_sheet.subsurface(
        (column * 32, row * 32, 32, 32)
    )
    image = pygame.transform.scale(image, (100, 100))
    return image


def get_skeleton_image(skeleton_sheet, column, row):
    image = skeleton_sheet.subsurface(
        (column * 16, row * 16, 16, 16)
    )
    image = pygame.transform.scale(image, (50, 50))
    return image


def get_boss_image(boss_sheet, column, row):
    image = boss_sheet.subsurface(
        (column * 48, row * 64, 48, 64)
    )
    image = pygame.transform.scale(image, (150, 150))
    return image


goblin_sheet = None
bat_sheet = None
slime_sheet = None
skeleton_sheet = None
boss_sheet = None


class Monster:
    def __init__(self, x, y, hp=3, speed=1, monster_type="normal", size=60):
        self.x = float(x)
        self.y = float(y)
        self.rect = pygame.Rect(x, y, size, size)
        self.hitbox = pygame.Rect(0, 0, size, size)
        self.hitbox.center = self.rect.center
        self.max_hp = hp
        self.hp = hp
        self.speed = speed
        self.type = monster_type
        self.color = (255, 0, 0)
        self.can_shoot = False
        self.was_hit = False
        self.health_bar_visible = False
        self.hit_animation_frame = 0
        self.hit_animation_start = 0
        self.animation_frame = 0
        self.last_animation_time = 0
        self.animation_speed = 150
        self.direction = "right"
        self.image = None

        if monster_type == "normal":
            self.image = get_goblin_image(goblin_sheet, 0, 0)
            self.set_hitbox(35, 40)

        elif monster_type == "fast":
            self.image = get_bat_image(bat_sheet, 0, 0)


    def set_hitbox(self, width, height, offset_x=0, offset_y=0):
        self.hitbox = pygame.Rect(0, 0, width, height)
        self.hitbox.center = self.rect.center
        self.hitbox.x += offset_x
        self.hitbox.y += offset_y


    def move(self):
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        self.hitbox.center = self.rect.center


    def animate(self):
        current_time = pygame.time.get_ticks()

        if self.was_hit:

            if current_time - self.last_animation_time >= self.animation_speed:

                self.hit_animation_frame += 1
                self.last_animation_time = current_time

                if self.type == "boss":

                    if self.hit_animation_frame >= 3:
                        self.was_hit = False
                        self.hit_animation_frame = 0

                else:

                    if self.hit_animation_frame >= 4:
                        self.was_hit = False
                        self.hit_animation_frame = 0

                if self.was_hit:

                    if self.type == "normal":

                        if self.direction == "right":
                            self.image = get_goblin_image(
                                goblin_sheet,
                                self.hit_animation_frame,
                                4
                            )

                        elif self.direction == "left":
                            self.image = get_goblin_image(
                                goblin_sheet,
                                self.hit_animation_frame,
                                5
                            )

                    elif self.type == "fast":

                        if self.direction == "right":
                            self.image = get_bat_image(
                                bat_sheet,
                                self.hit_animation_frame,
                                4
                            )

                        elif self.direction == "left":
                            self.image = get_bat_image(
                                bat_sheet,
                                self.hit_animation_frame,
                                5
                            )

                    elif self.type == "tank":

                        if self.direction == "right":
                            self.image = get_slime_image(
                                slime_sheet,
                                self.hit_animation_frame,
                                4
                            )

                        elif self.direction == "left":
                            self.image = get_slime_image(
                                slime_sheet,
                                self.hit_animation_frame,
                                5
                            )

                    elif self.type == "shooter":

                        if self.direction == "right":
                            self.image = get_skeleton_image(
                                skeleton_sheet,
                                self.hit_animation_frame,
                                4
                            )

                        elif self.direction == "left":
                            self.image = get_skeleton_image(
                                skeleton_sheet,
                                self.hit_animation_frame,
                                5
                            )

                    elif self.type == "boss":

                        if self.direction == "right":
                            self.image = get_boss_image(
                                boss_sheet,
                                self.hit_animation_frame,
                                4
                            )

                        elif self.direction == "left":
                            self.image = get_boss_image(
                                boss_sheet,
                                self.hit_animation_frame,
                                5
                            )

            return

        if current_time - self.last_animation_time >= self.animation_speed:
            self.animation_frame += 1

            if self.type == "boss":

                if self.animation_frame > 4:
                    self.animation_frame = 0

            elif self.type == "fast":

                if self.animation_frame > 2:
                    self.animation_frame = 0

            elif self.animation_frame > 3:
                self.animation_frame = 0

            self.last_animation_time = current_time

            if self.type == "normal":

                if self.direction == "right":
                    self.image = get_goblin_image(
                            goblin_sheet,
                            self.animation_frame,
                            2
                        )

                elif self.direction == "left":
                    self.image = get_goblin_image(
                            goblin_sheet,
                            self.animation_frame,
                            3
                        )
                    
            elif self.type == "fast":

                if self.direction == "right":
                    self.image = get_bat_image(
                        bat_sheet,
                        self.animation_frame,
                        0
                    )

                elif self.direction == "left":
                    self.image = get_bat_image(
                        bat_sheet,
                        self.animation_frame,
                        1
                    )

            elif self.type == "tank":

                if self.direction == "right":
                    self.image = get_slime_image(
                        slime_sheet,
                        self.animation_frame,
                        2
                    )

                elif self.direction == "left":
                    self.image = get_slime_image(
                        slime_sheet,
                        self.animation_frame,
                        3
                    )

            elif self.type == "shooter":

                if self.direction == "right":
                    self.image = get_skeleton_image(
                        skeleton_sheet,
                        self.animation_frame,
                        2
                    )

                elif self.direction == "left":
                    self.image = get_skeleton_image(
                        skeleton_sheet,
                        self.animation_frame,
                        3
                    )

            elif self.type == "boss":

                if self.direction == "right":
                    self.image = get_boss_image(
                        boss_sheet,
                        self.animation_frame,
                        2
                    )

                elif self.direction == "left":
                    self.image = get_boss_image(
                        boss_sheet,
                        self.animation_frame,
                        3
                    )


    def follow_player(self, player):
        if self.x < player.x:
            self.dx = 1
            self.direction = "right"

        if self.x > player.x:
            self.dx = -1
            self.direction = "left"

        if self.y < player.y:
            self.dy = 1

        if self.y > player.y:
            self.dy = -1


class FastMonster(Monster):
    def __init__(self, x ,y):
        super().__init__(x, y, 2, 2, "fast", 60)
        self.color = (0, 100, 255)
        self.image = get_bat_image(bat_sheet, 0, 0)
        self.set_hitbox(30, 25)


class TankMonster(Monster):
    def __init__(self, x, y):
        super().__init__(x, y, 15, 0.7, "tank", 100)
        self.color = (100, 150, 50)
        self.image = get_slime_image(slime_sheet, 0, 0)
        self.animation_speed = 250
        self.set_hitbox(60, 50, 0, 20)


class ShooterMonster(Monster):
    def __init__(self, x, y):
        super().__init__(x, y, 5, 1, "shooter", 50)
        self.color = (180, 0, 180)
        self.shoot_cooldown = 2000
        self.last_shot_time = 0
        self.can_shoot = True
        self.image = get_skeleton_image(skeleton_sheet, 0, 0)
        self.set_hitbox(30, 40)


class BossMonster(Monster):
    def __init__(self, x, y):
        super().__init__(x, y, 100, 1, "boss", 150)
        self.color = (255, 100, 0)
        self.shoot_cooldown = 1000
        self.last_shot_time = 0
        self.can_shoot = True
        self.image = get_boss_image(boss_sheet, 0, 0)
        self.animation_speed = 250
        self.set_hitbox(100, 80, 0, 20)


wave_compositions = [
    {Monster : 3},

    {Monster : 2, 
     FastMonster : 2},

    {Monster : 2,
     FastMonster : 2,
     TankMonster : 1},

    {FastMonster : 2,
     ShooterMonster : 2},

    {ShooterMonster : 2,
     TankMonster : 1},

    {ShooterMonster : 2,
     FastMonster : 1,
     TankMonster : 1},

    {Monster : 1,
     ShooterMonster : 1,
     TankMonster : 2,
     FastMonster : 2},

    {FastMonster : 2,
     ShooterMonster : 3,
     Monster : 2},

    {ShooterMonster : 4,
     TankMonster : 2},

    {BossMonster : 1}
]

def restart_game(
        game_over, 
        PLAYER_MAX_HP, 
        PLAYER_HP, player, 
        monsters, 
        wave_cleared, 
        game_started, 
        waves, 
        fireballs, 
        monster_projectiles, 
        FIREBALL_DAMAGE, 
        PLAYER_SPEED, 
        FIREBALL_SIZE, 
        FIREBALL_COOLDOWN):
    
    player.x = 375
    player.y = 275

    monsters.clear()
    fireballs.clear()
    monster_projectiles.clear()

    wave_cleared = False
    game_started = False
    waves = 1

    game_over = False

    PLAYER_HP = PLAYER_MAX_HP
    FIREBALL_DAMAGE = 1
    PLAYER_SPEED = 5
    FIREBALL_SIZE = 8
    FIREBALL_COOLDOWN = 1000

    return game_over, PLAYER_MAX_HP, PLAYER_HP, wave_cleared, game_started, waves, FIREBALL_DAMAGE, PLAYER_SPEED, FIREBALL_SIZE, FIREBALL_COOLDOWN

def main():

    clock = pygame.time.Clock()

    pygame.init()

    WIDTH = 800
    HEIGHT = 600

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    pygame.display.set_caption("Mage Survivor")

    player = pygame.Rect(375, 275, 50, 50)

    player_hitbox = pygame.Rect(0, 0, 30, 50)


    player_sheet = pygame.image.load(resource_path("assets/mage.png")).convert_alpha()
    player_image = get_player_image(player_sheet, 0, 0)


    global goblin_sheet, bat_sheet, slime_sheet, skeleton_sheet, boss_sheet

    goblin_sheet = pygame.image.load(resource_path("assets/SGQ_Enemies/normal/16x16/goblin.png")).convert_alpha()

    bat_sheet = pygame.image.load(resource_path("assets/SGQ_Enemies/normal/16x16/bat.png")).convert_alpha()

    slime_sheet = pygame.image.load(resource_path("assets/SGQ_Enemies/normal/32x32/medium_slime.png")).convert_alpha()

    skeleton_sheet = pygame.image.load(resource_path("assets/SGQ_Enemies/normal/16x16/skeleton.png")).convert_alpha()

    boss_sheet = pygame.image.load(resource_path("assets/SGQ_Enemies/bosses/slime_king.png")).convert_alpha()


    player_direction = ""
    animation_frame = 0
    last_animation_time = 0 
    ANIMATION_SPEED = 150
    
    fireballs = []
    monster_projectiles = []


    PLAYER_SPEED = 5

    PLAYER_MAX_HP = 3
    PLAYER_HP = PLAYER_MAX_HP


    FIREBALL_SPEED = 8
    FIREBALL_DAMAGE = 1
    FIREBALL_SIZE = 8
    FIREBALL_COOLDOWN = 1000


    last_fire_time = 0
    wave_start_time = pygame.time.get_ticks()


    monsters = []

    waves = 1
    wave_cleared = False


    font = pygame.font.Font(None, 24)

    wave_cleared_font = pygame.font.Font(None, 40)

    game_over_font = pygame.font.Font(None, 72)

    restart_font = pygame.font.Font(None, 50)

    victory_font = pygame.font.Font(None, 80)


    last_hit_time = 0

    running = True

    game_over = False
    game_won = False
    game_started = False

    restart = False

    player_invicible = True

    upgrade_chosen = False


    upgrades = [
    "damage",
    "max_hp",
    "speed",
    "fireball_size",
    "attack_speed"
    ]

    chosen_upgrades = []

    upgrade_functions = {
        "damage" : upgrade_damage,
        "max_hp" : upgrade_max_hp,
        "speed" : upgrade_speed,
        "fireball_size" : upgrade_fireball_size,
        "attack_speed" : upgrade_attack_speed
    }

    upgrade_names = {
        "damage" : "+1 Fireball Damage",
        "max_hp" : "+1 HP MAX, +1 HP",
        "speed" : "+1 Speed",
        "fireball_size" : "+1 Fireball Size",
        "attack_speed" : "+1 Attack Speed"
    }


    while running:

        clock.tick(60)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and game_over:

                if event.key == pygame.K_r:
                    game_over, PLAYER_MAX_HP, PLAYER_HP, wave_cleared, game_started, waves, FIREBALL_DAMAGE, PLAYER_SPEED, FIREBALL_SIZE, FIREBALL_COOLDOWN = restart_game(
                        game_over, PLAYER_MAX_HP, PLAYER_HP, player, monsters, wave_cleared, game_started, waves, fireballs, monster_projectiles, FIREBALL_DAMAGE, PLAYER_SPEED, FIREBALL_SIZE, FIREBALL_COOLDOWN
                        )

            if event.type == pygame.KEYDOWN and not game_over and not game_won:

                    if not game_started:

                        if event.key == pygame.K_SPACE:

                            game_started = True
                            wave_cleared = False

                            wave_start_time = pygame.time.get_ticks()
                            player_invicible = True

                            wave_composition = wave_compositions[waves - 1]
                            spawn_wave(waves, monsters, WIDTH, wave_composition)

                    elif wave_cleared:

                        if event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:

                            choice_index = event.key - pygame.K_1

                            chosen_upgrade = chosen_upgrades[choice_index]

                            upgrade_function = upgrade_functions[chosen_upgrade]

                            if chosen_upgrade == "damage":
                                FIREBALL_DAMAGE = upgrade_function(FIREBALL_DAMAGE)

                            elif chosen_upgrade == "speed":
                                PLAYER_SPEED = upgrade_function(PLAYER_SPEED)

                            elif chosen_upgrade == "max_hp":
                                PLAYER_MAX_HP, PLAYER_HP = upgrade_function(PLAYER_MAX_HP, PLAYER_HP)

                            elif chosen_upgrade == "fireball_size":
                                FIREBALL_SIZE = upgrade_function(FIREBALL_SIZE)

                            elif chosen_upgrade == "attack_speed":
                                FIREBALL_COOLDOWN = upgrade_function(FIREBALL_COOLDOWN)

                            upgrade_chosen = True


                        if upgrade_chosen:

                                wave_cleared = False
                                waves += 1

                                wave_start_time = pygame.time.get_ticks()
                                player_invicible = True

                                wave_composition = wave_compositions[waves - 1]
                                spawn_wave(waves, monsters, WIDTH, wave_composition)

                                upgrade_chosen = False

                    else:

                        current_time = pygame.time.get_ticks()

                        if current_time - last_fire_time >= FIREBALL_COOLDOWN:

                            if event.key == pygame.K_SPACE:

                                fireball = {
                                    "x" : player.centerx,
                                    "y" : player.centery,
                                    "direction" : player_direction
                                }
                                fireballs.append(fireball)

                                last_fire_time = current_time


        if not game_over and not game_won and game_started:

            player_moving = False

            keys = pygame.key.get_pressed()

            if keys[pygame.K_RIGHT]:

                player_direction = "right"
                player.x += PLAYER_SPEED
                if player.x > 750:
                    player.x = 750
                player_moving = True

            if keys[pygame.K_LEFT]:

                player_direction = "left"
                player.x -= PLAYER_SPEED
                if player.x < 0:
                    player.x = 0
                player_moving = True

            if keys[pygame.K_UP]:

                player_direction = "up"
                player.y -= PLAYER_SPEED
                if player.y < 0:
                    player.y = 0
                player_moving = True

            if keys[pygame.K_DOWN]:

                player_direction = "down"
                player.y += PLAYER_SPEED
                if player.y > 550:
                    player.y = 550
                player_moving = True


            current_time = pygame.time.get_ticks()

            if player_moving and current_time - last_animation_time >= ANIMATION_SPEED:
                animation_frame += 1

                if animation_frame > 3:
                    animation_frame = 0

                last_animation_time = current_time


            if player_direction == "down":
                player_image = get_player_image(player_sheet, animation_frame, 0)

            elif player_direction == "up":
                player_image = get_player_image(player_sheet, animation_frame + 4, 0)

            elif player_direction == "right":
                player_image = get_player_image(player_sheet, animation_frame, 1)

            elif player_direction == "left":
                player_image = get_player_image(player_sheet, animation_frame + 4, 1)


            current_time = pygame.time.get_ticks()
            if current_time - wave_start_time >= 2000:
                player_invicible = False

            for monster in monsters:

                monster.follow_player(player)

                for other_monster in monsters:

                    if monster != other_monster:

                        if monster.rect.colliderect(other_monster.rect):

                            if monster.rect.x < other_monster.rect.x:
                                monster.dx = -1

                            if monster.rect.x > other_monster.rect.x:
                                monster.dx = 1

                            if monster.rect.y < other_monster.rect.y:
                                monster.dy = -1
                                
                            if monster.rect.y > other_monster.rect.y:
                                monster.dy = 1

                  
                monster.move()

                monster.animate()

                player_hitbox.center = player.center

                if monster.hitbox.colliderect(player_hitbox):

                    if not player_invicible:
                        current_time = pygame.time.get_ticks()

                        if current_time - last_hit_time >= 2000:
                            PLAYER_HP -= 1
                            last_hit_time = current_time


                current_time = pygame.time.get_ticks()

                if monster.can_shoot:

                    if current_time - monster.last_shot_time >= monster.shoot_cooldown:

                        dx = player.centerx - monster.rect.centerx
                        dy = player.centery - monster.rect.centery

                        distance = (dx ** 2 + dy ** 2) ** 0.5

                        projectile = {
                            "x" : monster.rect.centerx,
                            "y" : monster.rect.centery,
                            "dx" : dx / distance,
                            "dy" : dy / distance
                        }

                        monster_projectiles.append(projectile)

                        monster.last_shot_time = current_time


            for projectile in monster_projectiles:

                projectile["x"] += projectile["dx"] * 5
                projectile["y"] += projectile["dy"] * 5

                projectile_rect = pygame.Rect(
                    projectile["x"] - 6,
                    projectile["y"] - 6,
                    12,
                    12
                )

                if projectile_rect.colliderect(player):

                    monster_projectiles.remove(projectile)

                    if not player_invicible:

                        PLAYER_HP -= 1


            for fireball in fireballs[:]:
                
                if fireball["direction"] == "right":
                    fireball["x"] += FIREBALL_SPEED

                if fireball["direction"] == "left":
                    fireball["x"] -= FIREBALL_SPEED

                if fireball["direction"] == "up":
                    fireball["y"] -= FIREBALL_SPEED

                if fireball["direction"] == "down":
                    fireball["y"] += FIREBALL_SPEED

                if fireball["x"] > WIDTH:
                    fireballs.remove(fireball)

                if fireball["x"] < 0:
                    fireballs.remove(fireball)

                if fireball["y"] > HEIGHT:
                    fireballs.remove(fireball)

                if fireball["y"] < 0:
                    fireballs.remove(fireball)


            for fireball in fireballs[:]:

                fireball_rect = pygame.Rect(
                    fireball["x"] - 8,
                    fireball["y"] - 8,
                    16,
                    16
                )

                for monster in monsters[:]:

                    if fireball_rect.colliderect(monster.hitbox):

                        monster.hp -= FIREBALL_DAMAGE

                        monster.was_hit = True
                        monster.health_bar_visible = True
                        monster.hit_animation_frame = 0
                        monster.hit_animation_start = pygame.time.get_ticks()

                        if fireball in fireballs:
                            fireballs.remove(fireball)

                        if monster.hp <= 0:
                            monsters.remove(monster)
                            break


        if len(monsters) == 0 and not wave_cleared and game_started:

            if waves == len(wave_compositions):

                game_won = True
                wave_cleared = False

            else:

                wave_cleared = True

                available_upgrades = upgrades.copy()

                if FIREBALL_COOLDOWN <= 200:
                    available_upgrades.remove("attack_speed")

                chosen_upgrades = random.sample(available_upgrades, 3)


        if PLAYER_HP <= 0:
            game_over = True


        screen.fill((80, 42, 42))

        player_image_rect = player_image.get_rect(center = player.center)

        screen.blit(player_image, player_image_rect)


        if wave_cleared and game_started: 

            wave_cleared_text = wave_cleared_font.render(
                """               WAVE CLEARED. 

            Choose an upgrade :""", 
            True, (255, 255, 255)
            )
            screen.blit(wave_cleared_text, (150, 100))

            
            upgrade_1_text = wave_cleared_font.render("1 - " + upgrade_names[chosen_upgrades[0]], True, (255, 255, 255))
            screen.blit(
                upgrade_1_text,
                (250, 250))

            upgrade_2_text = wave_cleared_font.render("2 - " + upgrade_names[chosen_upgrades[1]], True, (255, 255, 255))
            screen.blit(
                upgrade_2_text,
                (250, 300))

            upgrade_3_text = wave_cleared_font.render("3 - " + upgrade_names[chosen_upgrades[2]], True, (255, 255, 255))
            screen.blit(
                upgrade_3_text,
                (250, 350))


        if game_over:

            game_over_text = game_over_font.render(
                "GAME OVER",
                True,
                (255, 0, 255)
            )
            screen.blit(
                game_over_text,
                (220, 250)
            )
            restart_text = restart_font.render(
                "Press R to restart",
                True,
                (255, 255, 255)
            )
            screen.blit(
                restart_text,
                (250, 350)
            )


        player_hp_text = font.render(f'HP : {PLAYER_HP} / {PLAYER_MAX_HP}', True, (250, 30, 30))
        screen.blit(player_hp_text, (10, 10))

        speed_text = font.render(f'SPEED : {PLAYER_SPEED}', True, (255, 230, 0))
        screen.blit(speed_text, (10, 30))

        fireball_dammage_text = font.render(f'FIREBALL DAMAGE : {FIREBALL_DAMAGE}', True, (255, 100, 0))
        screen.blit(fireball_dammage_text, (600, 10))

        """fireball_size_text = font.render(f'FIREBALL SIZE : {FIREBALL_SIZE}', True, (255, 100, 0))
        screen.blit(fireball_size_text, (600, 30))"""

        attack_speed_text = font.render(f'COOLDOWN : {FIREBALL_COOLDOWN}ms', True, (255, 100, 0))
        screen.blit(attack_speed_text, (600, 30))


        for monster in monsters:

            if monster.image:
                screen.blit(monster.image, monster.rect)
            else:
                pygame.draw.rect(screen, monster.color, monster.rect)


            if monster.health_bar_visible:

                bar_width = monster.rect.width
                bar_height = 6

                bar_x = monster.rect.x
                bar_y = monster.rect.y - 10

                hp_ratio = monster.hp / monster.max_hp

                pygame.draw.rect(
                    screen,
                    (80, 80, 80),
                    (bar_x, bar_y, bar_width, bar_height)
                )

                pygame.draw.rect(
                    screen,
                    (0, 255, 0),
                    (bar_x, bar_y, bar_width * hp_ratio, bar_height)
                )


        for fireball in fireballs:

            pygame.draw.circle(
                screen,
                (255, 100, 0),
                (fireball["x"], fireball["y"]),
                FIREBALL_SIZE
            )


        for projectile in monster_projectiles:

            pygame.draw.circle(
                screen,
                (255, 255, 0),
                (projectile["x"], projectile["y"]),
                6
            )

        if game_won:

            victory_text = victory_font.render(
                "VICTORY !",
                True,
                (255, 215, 0)
            )

            screen.blit(
                victory_text,
                (WIDTH // 2 - victory_text.get_width() // 2,
                 HEIGHT // 2 - victory_text.get_height() // 2)
            )


        if not game_started:

            title_text = victory_font.render(
                "MAGE SURVIVOR",
                True,
                (255, 255, 255)
            )

            start_text = font.render(
                "Press SPACE to start",
                True,
                (255, 255, 255)
            )

            screen.blit(
                title_text,
                (
                    WIDTH // 2 - title_text.get_width() // 2,
                    HEIGHT // 2 - title_text.get_height() - 40
                )
            )

            screen.blit(
                start_text,
                (
                    WIDTH // 2 - start_text.get_width() // 2,
                    HEIGHT // 2 + 50
                )
            )


        if game_started and not game_won and not game_over:

            if waves == len(wave_compositions):
                wave_text = font.render(
                    "BOSS",
                    True,
                    (255, 255, 255)
                )
            else:
                wave_text = font.render(
                    f"WAVE {waves}",
                    True,
                    (255, 255, 255)
                )

            screen.blit(
                wave_text,
                (
                    WIDTH // 2 - wave_text.get_width() // 2,
                    10
                )
            )

        pygame.display.flip()

    pygame.quit()

main()