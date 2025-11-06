"""
Pygame interactive gallery

- Shows 5 items (emoji placeholders). Click an item to animate it to the screen center and scale it to 120%.
- Other items will fade to 40% opacity ("变淡60%") while the clicked item remains fully opaque.
- Click the selected item again (or press ESC) to return to the normal layout.

How to run:
    python pygame_gallery.py

Dependencies:
    pip install pygame

How to replace emoji with images:
- Put image files in an "assets/" folder next to this script.
- When creating items, pass image_path="assets/name.png" instead of leaving emoji text.

"""

import os
import sys
import math
import pygame
from pygame import Rect

# Configuration
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 640
BG_COLOR = (245, 247, 250)
ITEM_BASE_WIDTH = 180
ITEM_BASE_HEIGHT = 220
ANIMATION_TIME = 0.35  # seconds
FPS = 60
POSITION_SAVE_FILE = 'positions.json'

# Utility lerp
def lerp(a, b, t):
    return a + (b - a) * t

class Item:
    def __init__(self, id_, emoji, pos, image_path=None, font=None):
        self.id = id_
        self.emoji = emoji
        self.orig_pos = pygame.Vector2(pos)
        self.pos = pygame.Vector2(pos)
        self.image_path = image_path
        self.font = font

        # Surface that represents the content (emoji or image)
        self.base_surf = self._create_base_surface()
        self.base_rect = self.base_surf.get_rect(center=self.pos)

        # animation state
        self.current_scale = 1.0
        self.target_scale = 1.0
        self.current_alpha = 255
        self.target_alpha = 255
        self.current_pos = pygame.Vector2(self.pos)
        self.target_pos = pygame.Vector2(self.pos)
        self.anim_progress = 1.0  # 0..1

    def _create_base_surface(self):
        # If image path exists, load image, else render emoji text on white card
        if self.image_path and os.path.isfile(self.image_path):
            try:
                img = pygame.image.load(self.image_path).convert_alpha()
                # fit into base box
                img_w, img_h = img.get_size()
                max_w, max_h = ITEM_BASE_WIDTH - 24, ITEM_BASE_HEIGHT - 40
                scale = min(max_w / img_w, max_h / img_h, 1.0)
                new_w = int(img_w * scale)
                new_h = int(img_h * scale)
                img = pygame.transform.smoothscale(img, (new_w, new_h))
                surf = pygame.Surface((ITEM_BASE_WIDTH, ITEM_BASE_HEIGHT), pygame.SRCALPHA)
                surf.fill((255,255,255,255))
                surf.blit(img, img.get_rect(center=surf.get_rect().center))
                # draw small title area
                return surf
            except Exception as e:
                print('Failed loading image', self.image_path, e)
        # fallback: draw emoji in center with light card
        surf = pygame.Surface((ITEM_BASE_WIDTH, ITEM_BASE_HEIGHT), pygame.SRCALPHA)
        surf.fill((255,255,255,255))
        # card border shadow
        # draw emoji
        if self.font:
            emoji_surf = self.font.render(self.emoji, True, (17,24,39))
            emoji_rect = emoji_surf.get_rect(center=(ITEM_BASE_WIDTH//2, ITEM_BASE_HEIGHT//2 - 12))
            surf.blit(emoji_surf, emoji_rect)
        # title area will be rendered separately by caller when needed
        return surf

    def set_target(self, pos=None, scale=None, alpha=None):
        if pos is not None:
            self.target_pos = pygame.Vector2(pos)
        if scale is not None:
            self.target_scale = scale
        if alpha is not None:
            self.target_alpha = alpha
        self.anim_progress = 0.0

    def update(self, dt):
        if self.anim_progress < 1.0:
            self.anim_progress = min(1.0, self.anim_progress + (dt / ANIMATION_TIME))
            t = self.ease_out_cubic(self.anim_progress)
            self.current_scale = lerp(self.current_scale, self.target_scale, t)
            self.current_pos.x = lerp(self.current_pos.x, self.target_pos.x, t)
            self.current_pos.y = lerp(self.current_pos.y, self.target_pos.y, t)
            self.current_alpha = int(lerp(self.current_alpha, self.target_alpha, t))
        else:
            # ensure exact
            self.current_scale = self.target_scale
            self.current_pos = pygame.Vector2(self.target_pos)
            self.current_alpha = int(self.target_alpha)

    def ease_out_cubic(self, x):
        return 1 - pow(1 - x, 3)

    def draw(self, surface, title_text=None, title_font=None):
        # scale base_surf
        sw, sh = self.base_surf.get_size()
        scaled_w = max(1, int(sw * self.current_scale))
        scaled_h = max(1, int(sh * self.current_scale))
        scaled = pygame.transform.smoothscale(self.base_surf, (scaled_w, scaled_h))
        # set alpha
        scaled.set_alpha(self.current_alpha)
        # compute blit position centered at current_pos
        blit_rect = scaled.get_rect(center=(int(self.current_pos.x), int(self.current_pos.y)))
        surface.blit(scaled, blit_rect)
        # draw title below the emoji/image within the item card (if provided)
        if title_text and title_font:
            # draw a small semi-bold label with opacity
            title_surf = title_font.render(title_text, True, (55,65,81))
            title_surf.set_alpha(self.current_alpha)
            # anchor at bottom center of the drawn scaled card
            title_rect = title_surf.get_rect(center=(blit_rect.centerx, blit_rect.bottom - 18))
            surface.blit(title_surf, title_rect)

    def get_current_rect(self):
        sw, sh = self.base_surf.get_size()
        scaled_w = int(sw * self.current_scale)
        scaled_h = int(sh * self.current_scale)
        rect = Rect(0,0,scaled_w, scaled_h)
        rect.center = (int(self.current_pos.x), int(self.current_pos.y))
        return rect

    def contains_point(self, p):
        # inflate hit area slightly for accessibility
        r = self.get_current_rect().inflate(24, 24)
        return r.collidepoint(p)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Pygame Zoom Gallery')
    clock = pygame.time.Clock()

    # fonts
    try:
        emoji_font = pygame.font.Font(None, 72)
        title_font = pygame.font.Font(None, 20)
    except Exception:
        emoji_font = pygame.font.SysFont('arial', 72)
        title_font = pygame.font.SysFont('arial', 20)

    # items initial positions (spread horizontally)
    center_y = SCREEN_HEIGHT // 2
    gap = SCREEN_WIDTH // 6
    start_x = gap
    ids = ['it1','it2','it3','it4','it5']
    emojis = ['🎸','🎹','🎻','🎷','🥁']
    titles = ['吉他','钢琴','小提琴','萨克斯','鼓']

    items = []
    for i in range(5):
        pos = (start_x + i * gap, center_y)
        items.append(Item(ids[i], emojis[i], pos, image_path=None, font=emoji_font))

    selected_id = None
    show_positions = False  # press P to toggle
    move_mode = False  # press M to toggle move mode for selected item

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # deselect if any
                    if selected_id is not None:
                        selected_id = None
                        # reset targets
                        for it in items:
                            it.set_target(pos=it.orig_pos, scale=1.0, alpha=255)
                elif event.key == pygame.K_q:
                    running = False
                elif event.key == pygame.K_p:
                    show_positions = not show_positions
                elif event.key == pygame.K_m:
                    # toggle move mode only if an item is selected
                    if selected_id is not None:
                        move_mode = not move_mode
                elif event.key == pygame.K_s:
                    # save current orig_pos for items
                    try:
                        import json
                        save = {it.id: [it.orig_pos.x, it.orig_pos.y] for it in items}
                        with open(POSITION_SAVE_FILE, 'w', encoding='utf-8') as f:
                            json.dump(save, f, ensure_ascii=False, indent=2)
                        print('Saved positions to', POSITION_SAVE_FILE)
                    except Exception as e:
                        print('Failed to save positions', e)
                # quick select via number keys 1..5
                elif event.unicode in ('1','2','3','4','5'):
                    idx = int(event.unicode) - 1
                    if 0 <= idx < len(items):
                        clicked = items[idx]
                        if selected_id == clicked.id:
                            # deselect
                            selected_id = None
                            for it in items:
                                it.set_target(pos=it.orig_pos, scale=1.0, alpha=255)
                        else:
                            selected_id = clicked.id
                            for it in items:
                                if it.id == selected_id:
                                    center_pos = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                                    it.set_target(pos=center_pos, scale=1.8, alpha=255)
                                else:
                                    it.set_target(pos=it.orig_pos, scale=1.0, alpha=int(255 * 0.4))
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                clicked = None
                # iterate reversed so topmost selected is prioritized
                for it in reversed(items):
                    if it.contains_point((mx, my)):
                        clicked = it
                        break
                if clicked:
                    if selected_id == clicked.id:
                        # deselect
                        selected_id = None
                        for it in items:
                            it.set_target(pos=it.orig_pos, scale=1.0, alpha=255)
                    else:
                        selected_id = clicked.id
                        # set targets: selected moves to center and scales to 1.2
                        for it in items:
                            if it.id == selected_id:
                                center_pos = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                                it.set_target(pos=center_pos, scale=1.8, alpha=255)
                            else:
                                it.set_target(pos=it.orig_pos, scale=1.0, alpha=int(255 * 0.4))

        # update
        for it in items:
            it.update(dt)

        # handle keyboard nudging when in move_mode
        if move_mode and selected_id is not None:
            keys = pygame.key.get_pressed()
            dx = 0; dy = 0
            if keys[pygame.K_LEFT]:
                dx = -int(300 * dt)
            if keys[pygame.K_RIGHT]:
                dx = int(300 * dt)
            if keys[pygame.K_UP]:
                dy = -int(300 * dt)
            if keys[pygame.K_DOWN]:
                dy = int(300 * dt)
            if dx or dy:
                for it in items:
                    if it.id == selected_id:
                        it.orig_pos += pygame.Vector2(dx, dy)
                        # update targets immediately so it moves with animation
                        it.set_target(pos=it.orig_pos, scale=1.0 if selected_id is None else it.target_scale, alpha=it.target_alpha)
                        break

        # draw
        screen.fill(BG_COLOR)
        for idx, it in enumerate(items):
            it.draw(screen, title_text=titles[idx], title_font=title_font)

        # overlay: show positions and indexes
        if show_positions:
            for idx, it in enumerate(items):
                rect = it.get_current_rect()
                # draw small circular badge with number at top-left of rect
                badge_pos = (rect.left + 12, rect.top + 12)
                pygame.draw.circle(screen, (17,24,39), badge_pos, 14)
                num_surf = title_font.render(str(idx+1), True, (255,255,255))
                num_rect = num_surf.get_rect(center=badge_pos)
                screen.blit(num_surf, num_rect)
                # draw coordinates text below the badge
                coord_text = f"({int(it.orig_pos.x)},{int(it.orig_pos.y)})"
                coord_surf = title_font.render(coord_text, True, (31,41,55))
                screen.blit(coord_surf, (rect.left + 34, rect.top + 6))

        # show status line
        status = 'P: toggle positions | 1-5 select | M: move mode | S: save positions | Esc: reset'
        if move_mode:
            status = 'MOVE MODE (use arrow keys) - press M to exit | ' + status
        status_surf = title_font.render(status, True, (75,85,99))
        screen.blit(status_surf, (16, 16))

        # small instruction
        info_surf = title_font.render('点击一个元素放大到中心，按 Esc 或再次点击回到原位', True, (75,85,99))
        screen.blit(info_surf, (16, 16))

        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()
