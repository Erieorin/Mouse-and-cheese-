import pygame
import random
pygame.init()
pygame.mixer.init()
# цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
# размеры экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Мышка и сыр")
# изображения
mouse_img = pygame.image.load('mouse.png')
cheese_img = pygame.image.load('cheese.png')
trap_img = pygame.image.load('trap.png')
cat_img = pygame.image.load('cat.png')
heart_img = pygame.image.load('heart.png')
background_start_img = pygame.image.load('background_start.png')
background_game_img = pygame.image.load('background_game.png')
background_end_img = pygame.image.load('background_end.png')
background_pause_img = pygame.image.load('background_pause.png')
# музыка и звуки
pygame.mixer.music.load('background_music.ogg')
cheese_sound = pygame.mixer.Sound('cheese_sound.ogg')
trap_sound = pygame.mixer.Sound('trap_sound.ogg')
cat_sound = pygame.mixer.Sound('cat_sound.ogg')
heart_sound = pygame.mixer.Sound('heart_sound.ogg')
# размеры изображений
mouse_width, mouse_height = mouse_img.get_size()
cheese_width, cheese_height = cheese_img.get_size()
trap_width, trap_height = trap_img.get_size()
cat_width, cat_height = cat_img.get_size()
heart_width, heart_height = heart_img.get_size()

# классы для игрока, сыра, ловушки, кота и сердечка
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = mouse_img
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 50
        self.lives = 3
        self.invincible = False
        self.invincible_start_time = 0
        self.invincible_duration = 2000  # 2 секунды неуязвимости

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        if keys[pygame.K_UP]:
            self.rect.y -= 5
        if keys[pygame.K_DOWN]:
            self.rect.y += 5

        # ограничение перемещения игрока рамками экрана
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

        # неуязвимость
        if self.invincible:
            current_time = pygame.time.get_ticks()
            if current_time - self.invincible_start_time > self.invincible_duration:
                self.invincible = False

class Cheese(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = cheese_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)

class Trap(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = trap_img
        self.rect = self.image.get_rect()
        self.respawn()

    def respawn(self):
        safe_zone = pygame.Rect(player.rect.x - 100, player.rect.y - 100, 200, 200)
        while True:
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)
            if not self.rect.colliderect(safe_zone):
                break

class Cat(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = cat_img
        self.rect = self.image.get_rect()
        self.respawn()
        self.speed_x = random.choice([-3, 3])
        self.speed_y = random.choice([-3, 3])

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Изменение направления при столкновении с краями экрана
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.speed_x = -self.speed_x
        if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            self.speed_y = -self.speed_y

    def respawn(self):
        safe_zone = pygame.Rect(player.rect.x - 100, player.rect.y - 100, 200, 200)
        while True:
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)
            if not self.rect.colliderect(safe_zone):
                break

class Heart(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = heart_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)

# группы спрайтов
all_sprites = pygame.sprite.Group()
cheese_group = pygame.sprite.Group()
trap_group = pygame.sprite.Group()
cat_group = pygame.sprite.Group()
heart_group = pygame.sprite.Group()

# создание игрока
player = Player()
all_sprites.add(player)

# отображение текста
def draw_text(surface, text, size, x, y, color=BLACK):
    font = pygame.font.SysFont("comicsansms", size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_surface, text_rect)

# начальное меню
def show_start_screen():
    pygame.mixer.music.play(-1)  # Играть музыку в цикле
    screen.blit(background_start_img, (0, 0))
    draw_text(screen, "Мышка и сыр", 65, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4, YELLOW)
    draw_text(screen, "Выберите уровень сложности", 35, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50, YELLOW)
    draw_text(screen, "Легкий", 35, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, GREEN)
    draw_text(screen, "Средний", 35, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50, BLUE)
    draw_text(screen, "Тяжелый", 35, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 100, RED)
    draw_text(screen, "Выход", 35, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 150, RED)
    pygame.display.flip()
    waiting = True
    difficulty = None
    global running
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
                waiting = False
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                if SCREEN_WIDTH / 2 - 50 < mouse_pos[0] < SCREEN_WIDTH / 2 + 50:
                    if SCREEN_HEIGHT / 2 - 20 < mouse_pos[1] < SCREEN_HEIGHT / 2 + 20:
                        difficulty = "easy"
                        waiting = False
                    elif SCREEN_HEIGHT / 2 + 30 < mouse_pos[1] < SCREEN_HEIGHT / 2 + 70:
                        difficulty = "medium"
                        waiting = False
                    elif SCREEN_HEIGHT / 2 + 80 < mouse_pos[1] < SCREEN_HEIGHT / 2 + 120:
                        difficulty = "hard"
                        waiting = False
                    elif SCREEN_HEIGHT / 2 + 130 < mouse_pos[1] < SCREEN_HEIGHT / 2 + 170:
                        pygame.quit()
                        running = False
                        waiting = False
    return difficulty

# меню паузы
def show_pause_screen():
    screen.blit(background_pause_img, (0, 0))
    draw_text(screen, "Пауза", 65, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4, YELLOW)
    draw_text(screen, "Продолжить", 35, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, GREEN)
    draw_text(screen, "Главное меню", 35, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50, BLUE)
    draw_text(screen, "Выход", 35, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 100, RED)
    pygame.display.flip()
    waiting = True
    action = None
    global running
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
                waiting = False
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                if SCREEN_WIDTH / 2 - 50 < mouse_pos[0] < SCREEN_WIDTH / 2 + 50:
                    if SCREEN_HEIGHT / 2 - 20 < mouse_pos[1] < SCREEN_HEIGHT / 2 + 20:
                        action = "continue"
                        waiting = False
                    elif SCREEN_HEIGHT / 2 + 30 < mouse_pos[1] < SCREEN_HEIGHT / 2 + 70:
                        action = "menu"
                        waiting = False
                    elif SCREEN_HEIGHT / 2 + 80 < mouse_pos[1] < SCREEN_HEIGHT / 2 + 120:
                        pygame.quit()
                        running = False
                        waiting = False
    return action

# экран окончания игры
def show_game_over_screen(score):
    pygame.mixer.music.stop()
    screen.blit(background_end_img, (0, 0))
    draw_text(screen, "Игра окончена", 65, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4, RED)
    draw_text(screen, f"Счёт: {score}", 35, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, YELLOW)
    draw_text(screen, "Главное меню", 35, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50, BLUE)
    draw_text(screen, "Выход", 35, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 100, RED)
    pygame.display.flip()
    waiting = True
    action = None
    global running
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
                waiting = False
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                if SCREEN_WIDTH / 2 - 50 < mouse_pos[0] < SCREEN_WIDTH / 2 + 50:
                    if SCREEN_HEIGHT / 2 + 30 < mouse_pos[1] < SCREEN_HEIGHT / 2 + 70:
                        action = "menu"
                        waiting = False
                    elif SCREEN_HEIGHT / 2 + 80 < mouse_pos[1] < SCREEN_HEIGHT / 2 + 120:
                        pygame.quit()
                        running = False
                        waiting = False
    return action

# основной игровой цикла
def game_loop(difficulty):
    # очистка групп спрайтов
    all_sprites.empty()
    cheese_group.empty()
    trap_group.empty()
    cat_group.empty()
    heart_group.empty()

    # добавление игрока
    all_sprites.add(player)
    player.rect.x, player.rect.y = 50, 50
    player.lives = 3

    # сложность
    if difficulty == "easy":
        num_traps = 3
        num_cats = 1
    elif difficulty == "medium":
        num_traps = 5
        num_cats = 2
    elif difficulty == "hard":
        num_traps = 7
        num_cats = 3

    # создание сыра
    for _ in range(5):  # Создаём сразу 5 кусков сыра
        cheese = Cheese()
        all_sprites.add(cheese)
        cheese_group.add(cheese)

    # создание ловушек
    for _ in range(num_traps):
        trap = Trap()
        all_sprites.add(trap)
        trap_group.add(trap)

    # создание котов
    for _ in range(num_cats):
        cat = Cat()
        all_sprites.add(cat)
        cat_group.add(cat)

    score = 0
    clock = pygame.time.Clock()
    game_active = True
    global running
    while game_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_active = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                result = show_pause_screen()
                if result == "menu":
                    game_active = False
                elif result == "continue":
                    continue

        if not running:
            break

        # обновление спрайтов
        all_sprites.update()

        # проверка на столкновения с сыром
        if pygame.sprite.spritecollide(player, cheese_group, True):
            score += 1
            cheese_sound.play()
            new_cheese = Cheese()
            all_sprites.add(new_cheese)
            cheese_group.add(new_cheese)

        # проверка на столкновение с ловушками
        if pygame.sprite.spritecollide(player, trap_group, False) and not player.invincible:
            trap_sound.play()
            player.lives -= 1
            player.invincible = True
            player.invincible_start_time = pygame.time.get_ticks()
            for trap in trap_group:
                if trap.rect.colliderect(player.rect):
                    trap.respawn()
            if player.lives <= 0:
                result = show_game_over_screen(score)
                if result == "menu":
                    game_active = False
                else:
                    running = False
                    game_active = False

        # проверка на столкновение с котами
        if pygame.sprite.spritecollide(player, cat_group, False) and not player.invincible:
            cat_sound.play()
            player.lives -= 1
            player.invincible = True
            player.invincible_start_time = pygame.time.get_ticks()
            if player.lives <= 0:
                result = show_game_over_screen(score)
                if result == "menu":
                    game_active = False
                else:
                    running = False
                    game_active = False

        # проверка на столкновение с сердечками
        if pygame.sprite.spritecollide(player, heart_group, True):
            heart_sound.play()
            player.lives += 1

        if not game_active:
            break

        # очистка экрана и отображение фона
        screen.blit(background_game_img, (0, 0))

        # отрисовка спрайтов
        all_sprites.draw(screen)

        # счёт и жизни
        draw_text(screen, f"Счёт: {score}", 35, 70, 20, YELLOW)
        draw_text(screen, f"Жизни: {player.lives}", 35, 70, 60, YELLOW)
        draw_text(screen, "Нажмите P для паузы", 25, SCREEN_WIDTH - 150, 20, YELLOW)

        # рандомный спаун сердечка
        if random.random() < 0.001:  # 0.1% шанс спауна сердечка каждый кадр
            heart = Heart()
            all_sprites.add(heart)
            heart_group.add(heart)

        # обновление экрана
        pygame.display.flip()

        # ограничение кадров в секунду
        clock.tick(30)

# основной цикл
running = True
while running:
    difficulty = show_start_screen()
    if difficulty:
        game_loop(difficulty)

pygame.quit()