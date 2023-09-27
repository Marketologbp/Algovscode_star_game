from pygame import *
from random import *
import time as my_time


init()

class GameSprite(sprite.Sprite):
    def __init__(self, sprite_width, sprite_height, sprite_picture, sprite_speed, sprite_x, sprite_y):
        super().__init__()
        self.sprite_picture = sprite_picture
        self.image = transform.scale(image.load(sprite_picture), (sprite_width, sprite_height))
        self.sprite_speed = sprite_speed
        self.rect = self.image.get_rect()
        self.rect.x = sprite_x
        self.rect.y = sprite_y

    def show_sprite(self):
        main_window.blit(self.image, (self.rect.x, self.rect.y))


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.sprite_speed
        if self.rect.y <= -60:
            self.kill()


class Player(GameSprite):
    def update(self):
        buttons_pressed = key.get_pressed()
        if buttons_pressed[K_LEFT] and self.rect.x >= 0:
            self.rect.x -= self.sprite_speed
        if buttons_pressed[K_RIGHT] and self.rect.x <= 640:
            self.rect.x += self.sprite_speed

    def shoot(self):
        bullet = Bullet(20, 30, 'bullet.png', 10, self.rect.centerx - 10, self.rect.top)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.sprite_speed
        global run
        if self.rect.y >= 520:
            self.rect.y = randint(-120, -40)
            self.rect.x = randint(0, 640)
            self.sprite_speed = randint(1, 2)
            if self.sprite_picture == 'ufo.png':
                run += 1

def draw_scene():
    main_window.blit(space, (0, 0))
    main_window.blit(waiting, (250, 400))
    main_window.blit(run_aliiens, (0, 0))
    main_window.blit(kill_aliiens, (0, 40))
    main_window.blit(lifes_count, (620, 0)) 
    spaceship.show_sprite()
    aliens.draw(main_window)
    asteroids.draw(main_window)
    bullets.draw(main_window)

size = [700, 500]
main_window = display.set_mode(size)
display.set_caption('Звёздные войны')

space = transform.scale(image.load('galaxy.jpg'), (size))
spaceship = Player(60, 80, 'rocket.png', 10, 400, 420)

aliens = sprite.Group()
asteroids = sprite.Group()
bullets = sprite.Group()

for i in range(5):
    ufo = Enemy(70, 40, 'ufo.png', randint(1, 2), randint(0, 630), randint(-360, -120))
    aliens.add(ufo)

for i in range(5):
    asteroid = Enemy(60, 60, 'asteroid.png', randint(1, 4), randint(0, 640), randint(-360, -120))
    asteroids.add(asteroid)

mixer.init()
mixer.music.load('space.ogg')
shot = mixer.Sound('fire.ogg')
mixer.music.play()

font.init()
font_game = font.SysFont('Arial', 30)
font_result = font.SysFont('Arial', 80)

clock = time.Clock()
FPS = 60

game_exit = True
finish = True
reload_bullet = False
bullet_count = 5
run = 0
killed = 0
lifes = 3
waiting = font_game.render('', True, (0, 0, 0))

while game_exit:
    for game_event in event.get():
        if game_event.type == QUIT:
           game_exit = False
        if game_event.type == KEYDOWN:
            if game_event.key == K_SPACE and finish:
                if not reload_bullet:
                    spaceship.shoot()
                    shot.play()
                    bullet_count -= 1

    if finish:
        spaceship.update()
        bullets.update()
        aliens.update()
        asteroids.update()
        run_aliiens = font_game.render('Пропущено: ' + str(run), True, (255, 255, 255))
        kill_aliiens = font_game.render('Убито: ' + str(killed), True, (255, 255, 255))
        lifes_count = font_result.render(str(lifes), True, (255, 255, 255))

        if not reload_bullet:
            if bullet_count <= 0:
                reload_bullet = True
                time_begin = my_time.time()              
        else:
            time_end = my_time.time()
            if time_end - time_begin >= 1:
                reload_bullet = False
                bullet_count = 5
                waiting = font_game.render('', True, (0, 0, 0))
            else:
                waiting = font_game.render('Орудие перезаряжается...', True, (255, 255, 255))

        draw_scene()

        collide_ufo = sprite.spritecollide(spaceship, aliens, True)
        collide_asteroid = sprite.spritecollide(spaceship, asteroids, True)
        collide_bullet = sprite.groupcollide(aliens, bullets, True, True)

        for collide in collide_bullet:
            new_ufo = Enemy(70, 40, 'ufo.png', randint(1, 2), randint(0, 640), randint(-120, -40))
            aliens.add(new_ufo)
            killed += 1
            kill_aliiens = font_game.render('Убито: ' + str(killed), True, (255, 255, 255))
            main_window.blit(kill_aliiens, (0, 40))
            draw_scene()

        for collide in collide_ufo:
            lifes -= 1
            lifes_count = font_result.render(str(lifes), True, (255, 255, 255))
            draw_scene()

        for collide in collide_asteroid :
            lifes -= 1
            lifes_count = font_result.render(str(lifes), True, (255, 255, 255))
            draw_scene()

        if lifes <= 0:
            finish = False
            game_over = font_result.render('You lose!', True, (255, 0, 0))
            main_window.blit(game_over, (200, 250))

        if run >= 3:
            finish = False
            game_over = font_result.render('You lose!', True, (255, 0, 0))
            main_window.blit(game_over, (200, 250))

        if killed >= 20:
            finish = False
            game_win = font_result.render('You win!', True, (0, 255, 0))
            main_window.blit(game_win, (200, 250))

    display.update()
    clock.tick(FPS)