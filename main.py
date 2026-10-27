import pygame
import sys
import random
import math 
import os 

pygame.init()
pygame.mixer.init() # Ovoz tizimini ishga tushirish

# Ekran o'lchami
W, H = 1080, 2340
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Sky Rider - Ovozlar")

# Ranglar
WHITE = (255, 255, 255)
BLUE = (135, 206, 235)
YELLOW = (255, 255, 0)
RED = (200, 0, 0)
GRAY = (150, 150, 150)
ORANGE = (255, 100, 0)
DARK_RED = (139, 0, 0) 
GREEN = (0, 255, 0)

# --- RASMLARNI YUKLASH ---
try:
    menu_img = pygame.image.load("menu.png").convert_alpha()
    menu_img = pygame.transform.scale(menu_img, (W, H))
except:
    menu_img = None

try:
    bg_img = pygame.image.load("fon.png").convert()
    bg_img = pygame.transform.scale(bg_img, (W, H))
except:
    bg_img = None

try:
    player_img = pygame.image.load("qizil.png").convert_alpha()
    player_img = pygame.transform.scale(player_img, (250, 250))
except:
    player_img = None

try:
    enemy_img = pygame.image.load("qora.png").convert_alpha()
    enemy_img = pygame.transform.scale(enemy_img, (130, 130))
except:
    enemy_img = None

try:
    bullet_img = pygame.image.load("oq.png").convert_alpha()
    bullet_img = pygame.transform.scale(bullet_img, (30, 60)) 
except:
    bullet_img = None

try:
    enemy_bullet_img = pygame.image.load("dushman_oq.png").convert_alpha()
    enemy_bullet_img = pygame.transform.scale(enemy_bullet_img, (20, 40))
except:
    enemy_bullet_img = None

try:
    bomb_img = pygame.image.load("bomba.png").convert_alpha()
    bomb_img = pygame.transform.scale(bomb_img, (40, 80)) 
except:
    bomb_img = None

try:
    gameover_img = pygame.image.load("gameover.png").convert_alpha()
    gameover_img = pygame.transform.scale(gameover_img, (W, H))
except:
    gameover_img = None

try:
    coin_panel = pygame.image.load("coin_panel.png").convert_alpha()
    coin_panel = pygame.transform.scale(coin_panel, (450, 120)) 
except:
    coin_panel = None

try:
    ticket_panel = pygame.image.load("ticket_panel.png").convert_alpha()
    ticket_panel = pygame.transform.scale(ticket_panel, (450, 120)) 
except:
    ticket_panel = None

try:
    powerup_img = pygame.image.load("powerup.png").convert_alpha()
    powerup_img = pygame.transform.scale(powerup_img, (120, 120)) 
except:
    powerup_img = None

try:
    settings_bg = pygame.image.load("settings_oynasi.png").convert_alpha()
    settings_bg = pygame.transform.scale(settings_bg, (800, 800)) 
except:
    settings_bg = None

# --- OVOZLARNI YUKLASH VA SOZLASH ---
try:
    pygame.mixer.music.load("bg_music.mp3")
    pygame.mixer.music.set_volume(0.2) # Fon musiqasi sal pastroq
    pygame.mixer.music.play(-1) # Cheksiz qo'yish
except:
    print("XATO: bg_music.mp3 topilmadi!")

try:
    shoot_sound = pygame.mixer.Sound("shoot.wav")
    shoot_sound.set_volume(0.4)
except:
    shoot_sound = None
    print("XATO: shoot.wav topilmadi!")

try:
    explosion_sound = pygame.mixer.Sound("explosion.wav")
    explosion_sound.set_volume(0.7)
except:
    explosion_sound = None
    print("XATO: explosion.wav topilmadi!")

# --- O'YIN O'ZGARUVCHILARI ---
player_width = 250 
player_height = 250
player_hp = 20

line_y = H - 250
line_start_x = 50
line_end_x = W - 50
handle_x = W // 2
handle_radius = 80
is_dragging = False

bullet_width = 30 
bullet_height = 60
bullet_speed = 35 
shoot_delay = 250 

enemy_width = 130
enemy_height = 130
base_enemy_speed = 4 
enemy_hp = 4 

enemy_bullet_width = 20
enemy_bullet_height = 40
base_enemy_bullet_speed = 10 

bomb_width = 40 
bomb_height = 80
bomb_speed = 12 

double_shot_timer = 0 
kill_count = 0 
powerups = [] 

game_state = "menu" 
show_settings = False 
sound_on = True
music_on = True

score = 0 
speed_multiplier = 1.0
max_speed_multiplier = 3.0
start_time = pygame.time.get_ticks()

bullets = []
enemies = []
enemy_bullets = []
bombs = []

# --- SAVE TIZIMI ---
total_coins = 0 
total_tickets = 5
SAVE_FILE = "save_data.txt"

if os.path.exists(SAVE_FILE):
    try:
        with open(SAVE_FILE, "r") as f:
            data = f.read().split(",")
            total_coins = int(data[0])
            total_tickets = int(data[1])
    except:
        pass
else:
    with open(SAVE_FILE, "w") as f:
        f.write(f"{total_coins},{total_tickets}")

def save_data():
    with open(SAVE_FILE, "w") as f:
        f.write(f"{total_coins},{total_tickets}")

def reset_game():
    global player_x, player_y, player_hp, bullets, enemies, enemy_bullets, bombs, score, start_time, speed_multiplier
    global enemy_spawn_timer, enemy_shoot_timer, bomb_timer, last_shot_time, double_shot_timer, kill_count, powerups
    
    player_x = (W // 2) - (player_width // 2)
    player_y = H - 650 
    player_hp = 20 
    
    bullets.clear()
    enemies.clear()
    enemy_bullets.clear()
    bombs.clear()
    powerups.clear()
    
    score = 0
    start_time = pygame.time.get_ticks()
    speed_multiplier = 1.0
    
    enemy_spawn_timer = 0
    enemy_shoot_timer = 0
    bomb_timer = 0
    last_shot_time = 0
    double_shot_timer = 0
    kill_count = 0

# --- TUGMALAR ---
btn_start_game = pygame.Rect(250, 1450, 580, 160)
btn_settings = pygame.Rect(250, 1670, 580, 160)
btn_restart = pygame.Rect(200, 1300, 680, 180) 
btn_home = pygame.Rect(200, 1550, 680, 180)

btn_buy_ticket = pygame.Rect(370, 195, 95, 90) 

btn_close_settings = pygame.Rect(825, 690, 100, 100) 
btn_toggle_sound = pygame.Rect(640, 1110, 200, 80) 
btn_toggle_music = pygame.Rect(640, 1270, 200, 80) 

# Shriftlar
main_font = pygame.font.SysFont("Arial", 50, bold=True)
hp_font = pygame.font.SysFont("Arial", 30, bold=True)
panel_font = pygame.font.SysFont("Arial", 60, bold=True) 

reset_game()

clock = pygame.time.Clock()
running = True

while running:
    current_time = pygame.time.get_ticks()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            save_data()
            
        if show_settings:
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.FINGERDOWN:
                mouse_x = event.pos[0] if hasattr(event, 'pos') else event.x * W
                mouse_y = event.pos[1] if hasattr(event, 'pos') else event.y * H
                
                if btn_close_settings.collidepoint(mouse_x, mouse_y): 
                    show_settings = False
                    
                if btn_toggle_sound.collidepoint(mouse_x, mouse_y): 
                    sound_on = not sound_on
                    if not sound_on: pygame.mixer.stop() # Ovozlarni o'chirish
                    
                if btn_toggle_music.collidepoint(mouse_x, mouse_y):
                    music_on = not music_on
                    if music_on: pygame.mixer.music.unpause()
                    else: pygame.mixer.music.pause()

        elif game_state == "menu":
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.FINGERDOWN:
                mouse_x = event.pos[0] if hasattr(event, 'pos') else event.x * W
                mouse_y = event.pos[1] if hasattr(event, 'pos') else event.y * H
                
                if btn_buy_ticket.collidepoint(mouse_x, mouse_y):
                    if total_coins >= 200 and total_tickets < 20:
                        total_coins -= 200
                        total_tickets += 1
                        save_data()

                if btn_start_game.collidepoint(mouse_x, mouse_y):
                    if total_tickets > 0:
                        total_tickets -= 1
                        save_data()
                        reset_game()
                        game_state = "playing"
                    else:
                        print("Chipta yetarli emas!") 
                        
                elif btn_settings.collidepoint(mouse_x, mouse_y):
                    show_settings = True 

        elif game_state == "game_over":
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.FINGERDOWN:
                mouse_x = event.pos[0] if hasattr(event, 'pos') else event.x * W
                mouse_y = event.pos[1] if hasattr(event, 'pos') else event.y * H
                
                if btn_restart.collidepoint(mouse_x, mouse_y):
                    if total_tickets > 0:
                        total_tickets -= 1
                        save_data()
                        show_settings = False
                        reset_game()
                        game_state = "playing"
                        
                if btn_home.collidepoint(mouse_x, mouse_y):
                    total_coins += score
                    save_data()
                    show_settings = False
                    game_state = "menu" 

        elif game_state == "playing":
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.FINGERDOWN:
                mouse_x = event.pos[0] if hasattr(event, 'pos') else event.x * W
                mouse_y = event.pos[1] if hasattr(event, 'pos') else event.y * H
                if (mouse_x - handle_x)**2 + (mouse_y - line_y)**2 <= handle_radius**2:
                    is_dragging = True
            elif event.type == pygame.MOUSEBUTTONUP or event.type == pygame.FINGERUP:
                is_dragging = False
            elif event.type == pygame.MOUSEMOTION or event.type == pygame.FINGERMOTION:
                if is_dragging:
                    mouse_x = event.pos[0] if hasattr(event, 'pos') else event.x * W
                    handle_x = max(line_start_x, min(mouse_x, line_end_x))
                    player_x = handle_x - (player_width // 2)

    # --- O'YIN LOGIKASI ---
    if game_state == "playing" and not show_settings:
        seconds_elapsed = (current_time - start_time) / 1000
        speed_multiplier = 1.0 + (seconds_elapsed // 10) * 0.25
        if speed_multiplier > max_speed_multiplier:
            speed_multiplier = max_speed_multiplier
        
        if player_x < -50: player_x = -50
        if player_x > W - player_width + 50: player_x = W - player_width + 50

        # O'Q UZISH VA OVOZ
        if current_time - last_shot_time > shoot_delay:
            bullets.append([player_x + 75, player_y + 30]) 
            bullets.append([player_x + player_width - 90, player_y + 30]) 
            
            if double_shot_timer > 0:
                bullets.append([player_x + 20, player_y + 50]) 
                bullets.append([player_x + player_width - 40, player_y + 50]) 
            
            last_shot_time = current_time
            if shoot_sound and sound_on: 
                shoot_sound.play() # Ovozni chalinishi

        if double_shot_timer > 0:
            double_shot_timer -= 16.6 

        for bullet in bullets[:]:
            bullet[1] -= bullet_speed 
            if bullet[1] < -bullet_height:
                bullets.remove(bullet)

        if current_time - enemy_spawn_timer > 2000:
            random_x = random.randint(0, W - enemy_width)
            enemies.append([random_x, -150, enemy_hp]) 
            enemy_spawn_timer = current_time

        if current_time - enemy_shoot_timer > 2500:
            for enemy in enemies:
                enemy_bullets.append([enemy[0] + enemy_width//2 - enemy_bullet_width//2, enemy[1] + enemy_height])
            enemy_shoot_timer = current_time

        for enemy in enemies[:]:
            enemy[1] += base_enemy_speed * speed_multiplier 
            
            dodge_speed = 5 
            for bullet in bullets:
                if abs(bullet[0] - (enemy[0] + enemy_width//2)) < 250 and (enemy[1] < bullet[1] < enemy[1] + 600):
                    if enemy[0] + enemy_width//2 < bullet[0]: 
                        enemy[0] -= dodge_speed
                    else: 
                        enemy[0] += dodge_speed
                    break 
                    
            if enemy[0] < 0: enemy[0] = 0
            if enemy[0] > W - enemy_width: enemy[0] = W - enemy_width

            if enemy[1] > H:
                enemies.remove(enemy)

        for e_bullet in enemy_bullets[:]:
            e_bullet[1] += base_enemy_bullet_speed * speed_multiplier 
            if e_bullet[1] > H:
                enemy_bullets.remove(e_bullet)

        if score >= 10 and score % 10 == 0:
            if current_time - bomb_timer > 2000:
                for enemy in enemies:
                    if enemy[1] < 800:
                        b_start_x = enemy[0] + enemy_width//2 - bomb_width//2
                        b_start_y = enemy[1] + enemy_height
                        
                        target_x = player_x + player_width // 2
                        target_y = player_y + player_height // 2
                        
                        dx = target_x - (b_start_x + bomb_width//2)
                        dy = target_y - (b_start_y + bomb_height//2)
                        distance = math.hypot(dx, dy)
                        
                        if distance > 0:
                            vel_x = (dx / distance) * bomb_speed
                            vel_y = (dy / distance) * bomb_speed
                            bombs.append([b_start_x, b_start_y, vel_x, vel_y])
                bomb_timer = current_time

        for bomb in bombs[:]:
            bomb[0] += bomb[2] * speed_multiplier
            bomb[1] += bomb[3] * speed_multiplier
            if bomb[1] > H or bomb[0] < -50 or bomb[0] > W + 50:
                bombs.remove(bomb)

        for p_up in powerups[:]:
            p_up[1] += 5 
            if p_up[1] > H:
                powerups.remove(p_up)

        # --- URILISHLAR ---
        for bullet in bullets[:]:
            b_x, b_y = bullet
            for enemy in enemies[:]:
                e_x, e_y = enemy[0], enemy[1]
                if (b_x < e_x + enemy_width and b_x + bullet_width > e_x and
                    b_y < e_y + enemy_height and b_y + bullet_height > e_y):
                    bullets.remove(bullet) 
                    enemy[2] -= 1 
                    if enemy[2] <= 0:
                        enemies.remove(enemy) 
                        score += 5 
                        kill_count += 1
                        
                        # PORTLASH OVOZI
                        if explosion_sound and sound_on: 
                            explosion_sound.play()
                        
                        if kill_count >= 10:
                            powerups.append([random.randint(100, W-220), -100]) 
                            kill_count = 0
                    break 

        for e_bullet in enemy_bullets[:]:
            eb_x, eb_y = e_bullet
            if (eb_x < player_x + player_width - 60 and eb_x + enemy_bullet_width > player_x + 60 and
                eb_y < player_y + player_height - 50 and eb_y + enemy_bullet_height > player_y + 50):
                enemy_bullets.remove(e_bullet)
                player_hp -= 1 

        for bomb in bombs[:]:
            b_x, b_y = bomb[0], bomb[1]
            if (b_x < player_x + player_width - 60 and b_x + bomb_width > player_x + 60 and
                b_y < player_y + player_height - 50 and b_y + bomb_height > player_y + 50):
                bombs.remove(bomb)
                player_hp -= 3 

        for p_up in powerups[:]:
            if (p_up[0] < player_x + player_width - 40 and p_up[0] + 120 > player_x + 40 and
                p_up[1] < player_y + player_height - 40 and p_up[1] + 120 > player_y + 40):
                powerups.remove(p_up)
                double_shot_timer = 6000 

        if player_hp <= 0:
            game_state = "game_over"
            is_dragging = False

    # --- CHIZISH QISMI ---
    if game_state == "menu":
        if menu_img: screen.blit(menu_img, (0, 0))
        else: screen.fill(BLUE)
        
        if coin_panel:
            screen.blit(coin_panel, (30, 30)) 
            coin_text = panel_font.render(f"{total_coins}", True, WHITE)
            screen.blit(coin_text, coin_text.get_rect(center=(240, 90))) 
            
        if ticket_panel:
            screen.blit(ticket_panel, (30, 160)) 
            ticket_text = panel_font.render(f"{total_tickets}", True, WHITE)
            screen.blit(ticket_text, ticket_text.get_rect(center=(240, 220))) 

    elif game_state == "playing":
        if bg_img: screen.blit(bg_img, (0, 0))
        else: screen.fill(BLUE)

        if enemy_img:
            for enemy in enemies:
                screen.blit(enemy_img, (enemy[0], enemy[1]))
                hp_text = hp_font.render(f"{enemy[2]}", True, RED)
                screen.blit(hp_text, (enemy[0] + 55, enemy[1] + 50))
        else:
            for enemy in enemies:
                pygame.draw.rect(screen, (0,0,0), (enemy[0], enemy[1], enemy_width, enemy_height))

        if bullet_img:
            for bullet in bullets:
                screen.blit(bullet_img, (bullet[0], bullet[1]))
        else:
            for bullet in bullets:
                pygame.draw.rect(screen, YELLOW, (bullet[0], bullet[1], bullet_width, bullet_height))
            
        if enemy_bullet_img:
            for e_bullet in enemy_bullets:
                screen.blit(enemy_bullet_img, (e_bullet[0], e_bullet[1]))
        else:
            for e_bullet in enemy_bullets:
                pygame.draw.rect(screen, ORANGE, (e_bullet[0], e_bullet[1], enemy_bullet_width, enemy_bullet_height))

        if bomb_img:
            for bomb in bombs:
                screen.blit(bomb_img, (bomb[0], bomb[1]))
        else:
            for bomb in bombs:
                pygame.draw.rect(screen, DARK_RED, (bomb[0], bomb[1], bomb_width, bomb_height))

        if powerup_img:
            for p_up in powerups:
                screen.blit(powerup_img, (p_up[0], p_up[1]))
        else:
            for p_up in powerups:
                pygame.draw.rect(screen, GREEN, (p_up[0], p_up[1], 120, 120))

        if player_img: 
            screen.blit(player_img, (player_x, player_y))
            if double_shot_timer > 0:
                pygame.draw.circle(screen, GREEN, (int(player_x + player_width//2), int(player_y + player_height//2)), 140, 5)
        else: 
            pygame.draw.rect(screen, RED, (player_x, player_y, player_width, player_height))

        pygame.draw.line(screen, GRAY, (line_start_x, line_y), (line_end_x, line_y), 15)
        handle_color = WHITE if is_dragging else GRAY
        pygame.draw.circle(screen, handle_color, (int(handle_x), int(line_y)), handle_radius)
        pygame.draw.circle(screen, BLUE, (int(handle_x), int(line_y)), 25)

        if coin_panel:
            screen.blit(coin_panel, (30, 30)) 
            coin_text = panel_font.render(f"{total_coins + score}", True, WHITE)
            screen.blit(coin_text, coin_text.get_rect(center=(240, 90))) 

        player_hp_text = main_font.render(f"HP: {player_hp}", True, RED)
        screen.blit(player_hp_text, (50, 160)) 
        
        speed_text = main_font.render(f"Speed: {speed_multiplier:.1f}x", True, WHITE)
        screen.blit(speed_text, (W - 350, 50))

    elif game_state == "game_over":
        if gameover_img: screen.blit(gameover_img, (0, 0))
        else: screen.fill((20, 20, 20)) 
        
        if coin_panel:
            screen.blit(coin_panel, (30, 30)) 
            coin_text = panel_font.render(f"{total_coins + score}", True, WHITE)
            screen.blit(coin_text, coin_text.get_rect(center=(240, 90))) 

    # --- SOZLAMALAR OYNASINI CHIZISH ---
    if show_settings:
        s = pygame.Surface((W, H))
        s.set_alpha(150)
        s.fill((0, 0, 0))
        screen.blit(s, (0, 0))
        
        if settings_bg: 
            screen.blit(settings_bg, (140, 700))
            
        if sound_on:
            pygame.draw.rect(screen, GREEN, (640, 1110, 115, 55), border_radius=25)
        else:
            pygame.draw.rect(screen, RED, (640, 1110, 115, 55), border_radius=25)

        if music_on:
            pygame.draw.rect(screen, GREEN, (640, 1270, 115, 55), border_radius=25)
        else:
            pygame.draw.rect(screen, RED, (640, 1270, 115, 55), border_radius=25)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()