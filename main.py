import pygame
import math
import sys
import random

pygame.init()

WIDTH, HEIGHT = 1000, 600
FPS = 60
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fortress Duel")

bq2 = pygame.image.load('background.png')
springBq = pygame.image.load('spring.png')
summerBq = pygame.image.load('summer.png')
autumnBq = pygame.image.load('fall.png')
winterBq = pygame.image.load('winter.png')
springBlock = pygame.image.load('springBlock.png')
summerBlock = pygame.image.load('summerBlock.png')
autumnBlock = pygame.image.load('fallBlock.png')
winterBlock = pygame.image.load('winterBlock.png')

springChar = pygame.image.load('SpringChar.png')
summerChar = pygame.image.load('SummerChar.png')
autumnChar = pygame.image.load('FallChar.png')
winterChar = pygame.image.load('WinterChar.png')
c = pygame.image.load('cannon.png')
c = pygame.transform.scale(c, (50, 50))

bulletSound = pygame.mixer.Sound("bullet.mp3")
hitSound = pygame.mixer.Sound("hit.mp3")

start_time = pygame.time.get_ticks()
game_duration = 60000
font = pygame.font.SysFont(None, 50)
font2 = pygame.font.SysFont(None, 36)

#choose game mode-single or multi
def mode():
    single_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 80, 300, 60)
    multi_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 20, 300, 60)
    while True:
        screen.blit(bq2, (0, 0))
        title = font.render("Choose Game Mode", True, (255, 255, 255))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        for button, text, mode in [
            (single_button, "Single Player", "single"),
            (multi_button, "Two Players", "two")
        ]:
            color = (0, 255, 0) if button.collidepoint(mouse) else (100, 100, 100)
            pygame.draw.rect(screen, color, button)
            btn_text = font2.render(text, True, (0, 0, 0))
            screen.blit(btn_text, (button.x + button.width // 2 - btn_text.get_width() // 2,
                                   button.y + button.height // 2 - btn_text.get_height() // 2))
            if click[0] and button.collidepoint(mouse):
                return mode

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        pygame.display.flip()
        clock.tick(60)

#choose the background
def choose_background():
    options = [("Spring", springBq, springBlock, springChar), ("Summer", summerBq, summerBlock, summerChar),
               ("Autumn", autumnBq, autumnBlock, autumnChar), ("Winter", winterBq, winterBlock, winterChar)]
    buttons = [pygame.Rect(100 + i * 200, HEIGHT // 2 - 50, 150, 60) for i in range(4)]

    while True:
        screen.blit(bq2, (0, 0))
        title = font.render("Choose Background", True, (255, 255, 255))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        for i, (label, _, _, _) in enumerate(options):
            color = (0, 200, 0) if buttons[i].collidepoint(mouse) else (100, 100, 100)
            pygame.draw.rect(screen, color, buttons[i])
            text = font2.render(label, True, (0, 0, 0))
            screen.blit(text, (buttons[i].x + buttons[i].width // 2 - text.get_width() // 2,
                               buttons[i].y + buttons[i].height // 2 - text.get_height() // 2))

            if click[0] and buttons[i].collidepoint(mouse):
                return (
                    pygame.transform.scale(options[i][1], (WIDTH, HEIGHT)),
                    pygame.transform.scale(options[i][2], (30, 30)),
                    options[i][3]
                )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        pygame.display.flip()
        clock.tick(60)

#instructions for single player mode
def instruction_single():
    lines = [
        "Fortress Duel!",
        "Destroy your opponent's castle blocks.",
        "Player uses 'A' to move left, 'D' to move right, and 'W' to jump",
        "Player uses 'S' to shoot.",
        "Player has 10 bullets.",
        "The game lasts 1 minute.",
        "The player with more blocks left wins.",
        "Click 'Continue' to start."
    ]
    continue_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 100, 200, 50)

    while True:
        screen.blit(bq2, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if continue_button.collidepoint(event.pos):
                    return
        for i, line in enumerate(lines):
            font_used = font if i == 0 else font2
            text = font_used.render(line, True, (0, 0, 0))
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 50 + i * 40))

        mouse_pos = pygame.mouse.get_pos()
        color = (0, 250, 0) if continue_button.collidepoint(mouse_pos) else (0, 255, 0)
        pygame.draw.rect(screen, color, continue_button)
        button_text = font2.render("Continue", True, (0, 0, 0))
        screen.blit(button_text, (continue_button.x + continue_button.width // 2 - button_text.get_width() // 2,
                                  continue_button.y + continue_button.height // 2 - button_text.get_height() // 2))

        pygame.display.flip()
        clock.tick(60)

#instructions for multi player mode
def instruction_multi():
    lines = [
        "Fortress Duel!",
        "Destroy your opponent's castle blocks.",
        "Player 1 uses 'A' to move left, 'D' to move right, 'W' to jump, and 'S' to shoot",
        "Player 2 uses left arrow to move left, right arrow to move right,",
        "up arrow to jump, and 'L' to shoot",
        "Players have 10 bullets.",
        "The game lasts 1 minute.",
        "The player with more blocks left wins.",
        "Click 'Continue' to start."
    ]
    continue_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 100, 200, 50)

    while True:
        screen.blit(bq2, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if continue_button.collidepoint(event.pos):
                    return

        for i, line in enumerate(lines):
            font_used = font if i == 0 else font2
            text_ = font_used.render(line, True, (0, 0, 0))
            screen.blit(text_, (WIDTH // 2 - text_.get_width() // 2, 50 + i * 40))

        mouse_pos = pygame.mouse.get_pos()
        color = (0, 250, 0) if continue_button.collidepoint(mouse_pos) else (0, 255, 0)
        pygame.draw.rect(screen, color, continue_button)
        button_text = font2.render("Continue", True, (0, 0, 0))
        screen.blit(button_text, (continue_button.x + continue_button.width // 2 - button_text.get_width() // 2,
                                  continue_button.y + continue_button.height // 2 - button_text.get_height() // 2))

        pygame.display.flip()
        clock.tick(60)

#single mode AI control
def ai():
    current_time = pygame.time.get_ticks()
    ai_center = p2.x + p2.width // 2
    cannon_x, cannon_y = p2.cannon_pos

    if current_time - p2.last_shot_time < p2.shot_cooldown:
        return

    def obstacle_ahead():
        future_rect = pygame.Rect(p2.x + 5, p2.y, p2.width, p2.height)
        for block in castle2:
            block_rect = pygame.Rect(block.x, block.y, block.width, block.height)
            if future_rect.colliderect(block_rect):
                return True
        return False

    if not p2.cannon_enable():
        step = 1
        if ai_center < cannon_x:
            p2.x += step
        elif ai_center > cannon_x:
            p2.x -= step

        if p2.is_on_ground and obstacle_ahead():
            p2.jump()

    else:
        if not p2.is_charging and p2.can_shoot and p2.cannonballs_left > 0:
            p2.is_charging = True

    if p2.is_charging:
        charge_rate = 0.5
        p2.shoot_power = min(p2.shoot_power + charge_rate, p2.max_power)

        if p2.shoot_power >= p2.max_power or p2.shoot_power > 60:
            variation = random.uniform(-10, 10)
            power = min(max(p2.shoot_power + variation, 30), p2.max_power)
            new_ball = shoot(p2.cannon_pos, -1, power)
            cannonballs.append(new_ball)
            bulletSound.play()
            p2.cannonballs_left -= 1
            p2.last_shot_time = current_time
            p2.is_charging = False
            p2.shoot_power = 0


class player:
    def __init__(self, x, y, image, width, height, cannon_pos):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(image, (width, height))
        self.velocity = 0
        self.gravity = 0.5
        self.vy = 0
        self.speed = 5
        self.jump_strength = -9
        self.is_jumping = False
        self.cannonballs_left = 10
        self.can_shoot = True
        self.is_on_ground = True
        self.cannon_pos = cannon_pos
        self.cannon_range = 50
        self.health = 2
        self.spawn_x = x
        self.spawn_y = y
        self.shoot_power = 0
        self.max_power = 100
        self.power_increase = 2
        self.is_charging = False
        self.last_shot_time = 0
        self.shot_cooldown = 2000

    def update(self, blocks):
        if not self.is_on_ground:
            self.vy += self.gravity

        self.y += self.vy
        initial_ground_y = HEIGHT - 30
        if self.y > initial_ground_y - self.height:
            self.y = initial_ground_y - self.height
            self.vy = 0
            self.is_jumping = False
            self.is_on_ground = True
            return

        self.is_on_ground = False

        for block in blocks:
            block_rect = pygame.Rect(block.x, block.y, block.width, block.height)
            player_rect = pygame.Rect(self.x, self.y, self.width, self.height)

            if player_rect.colliderect(block_rect):
                if self.vy >= 0 and player_rect.bottom > block_rect.top and player_rect.top < block_rect.top:
                    self.y = block_rect.top - self.height
                    self.vy = 0
                    self.is_jumping = False
                    self.is_on_ground = True

                elif self.vy < 0 and player_rect.top < block_rect.bottom and player_rect.bottom > block_rect.bottom:
                    self.y = block_rect.bottom
                    self.vy = 0

                elif player_rect.right > block_rect.left and player_rect.left < block_rect.left:
                    self.x = block_rect.left - self.width

                elif player_rect.left < block_rect.right and player_rect.right > block_rect.right:
                    self.x = block_rect.right

    def jump(self):
        if self.is_on_ground:
            self.vy = self.jump_strength
            self.is_jumping = True
            self.is_on_ground = False

    def cannon_enable(self):
        dx = self.x + self.width / 2 - self.cannon_pos[0]
        dy = self.y + self.height / 2 - self.cannon_pos[1]
        distance = math.sqrt(dx * dx + dy * dy)
        return distance < self.cannon_range

    def respawn(self):
        self.x = self.spawn_x
        self.y = self.spawn_y
        self.vy = 0
        self.is_jumping = False
        self.is_on_ground = True


class Block:
    def __init__(self, x, y, width, height, image=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.health = 1
        self.image = image


cannonballs = []
cannon_radius = 5
cannon_speed = 7


def create_castle(x, y, block_image, left=True):
    blocks = []
    layers = [14, 12, 10, 8, 6, 4, 2]
    for row, width in enumerate(layers):
        x_offset = (max(layers) - width) * 15
        for col in range(width):
            blocks.append(Block(
                x + x_offset + col * 30,
                y - row * 30,
                30, 30, block_image
            ))
    top_blocks = [b for b in blocks if b.y == y - (len(layers) - 1) * 30]
    cannon_block = sorted(top_blocks, key=lambda b: b.x)[len(top_blocks) // 2]
    cannon_pos = (
        cannon_block.x + cannon_block.width // 2,
        cannon_block.y - 35
    )
    return blocks, cannon_pos


def shoot(cannon_pos, direction, power):
    total_power = (power / 100) * 0.7 * 2
    return {
        'x': cannon_pos[0],
        'y': cannon_pos[1],
        'vx': 7 * direction * total_power,
        'vy': -10 * total_power,
        'power': power
    }


def block_collision():
    global cannonballs, castle1, castle2
    new_cannonballs = []
    for ball in cannonballs:
        hit = False
        for castle in [castle1, castle2]:
            for block in castle:
                if block.x < ball['x'] < block.x + block.width and block.y < ball['y'] < block.y + block.height:
                    block.health -= 1
                    hitSound.play()
                    if block.health == 0:
                        castle.remove(block)
                    hit = True
                    break
            if hit:
                break
        if not hit and 0 <= ball['x'] <= WIDTH and 0 <= ball['y'] <= HEIGHT:
            new_cannonballs.append(ball)
    cannonballs = new_cannonballs


def player_collision(player):
    global cannonballs
    new_cannonballs = []
    for ball in cannonballs:
        if player.x < ball['x'] < player.x + player.width and player.y < ball['y'] < player.y + player.height:
            hitSound.play()
            player.health -= 1
            player.respawn()
            if player.health == 0:
                print(f"{player} defeated!")
                return True
            continue
        new_cannonballs.append(ball)
    cannonballs = new_cannonballs


running = True
clock = pygame.time.Clock()

game_mode = mode()
if game_mode == "single":
    instruction_single()
else:
    instruction_multi()
bq, b, character = choose_background()
castle1, cannon11 = create_castle(30, HEIGHT - 70, b, True)
castle2, cannon22 = create_castle(WIDTH - 450, HEIGHT - 70, b, False)
p1 = player(450, HEIGHT - 20, character, 30, 30, cannon11)
p2 = player(WIDTH - 490, HEIGHT - 30, character, 30, 30, cannon22)

#main game loop
while running:
    current_time = pygame.time.get_ticks()
    elapsed_time = current_time - start_time
    if elapsed_time >= game_duration:
        running = False
        break
    clock.tick(FPS)
    screen.blit(bq, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s and p1.can_shoot and p1.cannon_enable():
                p1.is_charging = True
            if event.key == pygame.K_l and p2.can_shoot and p2.cannon_enable():
                p2.is_charging = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_s and p1.is_charging:
                if p1.cannonballs_left > 0:
                    bulletSound.play()
                    power = min(p1.shoot_power, p1.max_power)
                    new_ball = shoot(cannon11, 1, power)
                    cannonballs.append(new_ball)
                    p1.cannonballs_left -= 1
                p1.is_charging = False
                p1.shoot_power = 0

            if event.key == pygame.K_l and p2.is_charging:
                if p2.cannonballs_left > 0:
                    bulletSound.play()
                    power = min(p2.shoot_power, p2.max_power)
                    new_ball = shoot(cannon22, -1, power)
                    cannonballs.append(new_ball)
                    p2.cannonballs_left -= 1
                p2.is_charging = False
                p2.shoot_power = 0

    keys = pygame.key.get_pressed()

    if keys[pygame.K_a] and p1.x > 0:
        p1.x -= p1.speed
    if keys[pygame.K_d] and p1.x < WIDTH - p1.width:
        p1.x += p1.speed
    if keys[pygame.K_w]:
        p1.jump()

    if game_mode == "two":
        if keys[pygame.K_LEFT] and p2.x > 0:
            p2.x -= p2.speed
        if keys[pygame.K_RIGHT] and p2.x < WIDTH - p2.width:
            p2.x += p2.speed
        if keys[pygame.K_UP]:
            p2.jump()

    else:
        ai()

    p1.update(castle1)
    p2.update(castle2)

    if p1.is_charging and p1.can_shoot:
        p1.shoot_power = min(p1.shoot_power + p1.power_increase, p1.max_power)
    if p2.is_charging and p2.can_shoot:
        p2.shoot_power = min(p2.shoot_power + p2.power_increase, p2.max_power)

    if p1.is_charging:
        pygame.draw.rect(screen, (100, 100, 100), (p1.x, p1.y - 20, 100, 10))
        pygame.draw.rect(screen, (255, 0, 0), (p1.x, p1.y - 20, p1.shoot_power, 10))

    if p2.is_charging:
        pygame.draw.rect(screen, (100, 100, 100), (p2.x, p2.y - 20, 100, 10))
        pygame.draw.rect(screen, (255, 0, 0), (p2.x, p2.y - 20, p2.shoot_power, 10))

    for ball in cannonballs:
        ball['x'] += ball['vx']
        ball['y'] += ball['vy']
        ball['vy'] += 0.3

    block_collision()
    player_collision(p1)
    player_collision(p2)

    for ball in cannonballs:
        pygame.draw.circle(screen, (0, 0, 0), (int(ball['x']), int(ball['y'])), cannon_radius)

    for block in castle1:
        screen.blit(b, (block.x, block.y))
    for block in castle2:
        screen.blit(b, (block.x, block.y))

    screen.blit(p1.image, (p1.x, p1.y))
    screen.blit(p2.image, (p2.x, p2.y))

    if castle1:
        screen.blit(c, (cannon11[0] - c.get_width() // 2, cannon11[1]))

    if castle2:
        screen.blit(c, (cannon22[0] - c.get_width() // 2, cannon22[1]))

    time_left = max(0, (game_duration - elapsed_time) // 1000)
    time_text = font2.render(f" Time Left: {time_left}s", True, (255, 255, 255))
    screen.blit(time_text, (WIDTH // 2 - time_text.get_width() // 2, 10))

    p1_bullets = font2.render(f"Player 1 bullets: {p1.cannonballs_left}", True, (255, 255, 255))
    p2_bullets = font2.render(f"Player 2 bullets: {p2.cannonballs_left}", True, (255, 255, 255))
    screen.blit(p1_bullets, (10, 10))
    screen.blit(p2_bullets, (WIDTH - p2_bullets.get_width() - 10, 10))

    pygame.display.flip()

screen.blit(bq, (0, 0))

#game result
if len(castle1) > len(castle2):
    text = font.render("Player 1 wins!", True, (0, 128, 0))
elif len(castle1) < len(castle2):
    text = font.render("Player 2 wins!", True, (0, 128, 0))
else:
    text = font.render("It's a draw!", True, (0, 128, 0))

screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
pygame.display.flip()
pygame.time.delay(4000)

pygame.quit()