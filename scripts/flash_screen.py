#!/usr/bin/env python
# coding=utf-8
import logging
import pygame
import time

log = logging.getLogger(__name__)

FLASH_INC = 0.01
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
clock = pygame.time.Clock()


def warning(screen, width, height):
    """
    Display a warning
    """
    done = False

    while not done:
        screen.fill(BLACK)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return False

            if e.type is pygame.KEYDOWN:
                # increase the flash time
                if e.key == pygame.K_y:
                    return True
                if e.key == pygame.K_n or e.key == pygame.K_q:
                    return False

        # draw some instructions
        font = pygame.font.Font(None, 36)
        text1 = font.render("WARNING! The program is designed to flash the screen at ", 1, WHITE)
        screen.blit(text1, text1.get_rect(centerx=width / 2, centery=height * 0.4))

        text2 = font.render(u"frequencies between 1Hz and 100Hz", 1, WHITE)
        screen.blit(text2, text2.get_rect(centerx=width / 2, centery=height * 0.45))

        text3 = font.render("Type Y to continue, or type Q or N to quit! ", 1, WHITE)
        screen.blit(text3, text3.get_rect(centerx=width / 2, centery=height * 0.55))

        clock.tick(120)
        pygame.display.update()


def flash_screen(screen, width, height):
    """
    Flash the screen
    """

    flash = False
    sflash = False
    done = False
    flash_i = 1
    flash_t = 0
    flash_time = time.time()

    while not done:
        for e in pygame.event.get():
            done = (e.type == pygame.QUIT) or (e.type is pygame.KEYDOWN and e.key == pygame.K_q)

            if e.type is pygame.KEYDOWN:
                # increase the flash time
                if e.key == pygame.K_z:
                    flash_i = min(100, flash_i + 1)
                # decrease the flash time
                if e.key == pygame.K_x:
                    flash_i = max(1, flash_i - 1)
                if e.key == pygame.K_SPACE:
                    sflash ^= True
                    if sflash:
                        flash_t = FLASH_INC * flash_i

        if sflash:
            # keep the screen WHITE until the flash time expires
            if time.time() > flash_time:
                flash_time = time.time() + flash_t
                flash ^= True

        screen.fill(WHITE if flash and sflash else BLACK)

        # draw some instructions
        font = pygame.font.Font(None, 36)
        text1 = font.render("Press SPACE to flash on/off for {:.2f}s".format(flash_i * FLASH_INC), 1, WHITE)
        screen.blit(text1, text1.get_rect(centerx=width / 2, centery=height * 0.85))

        text2 = font.render("Press Z to increase flash time and X to decrease it", 1, WHITE)
        screen.blit(text2, text2.get_rect(centerx=width / 2, centery=height * 0.9))

        clock.tick(120)
        pygame.display.update()

def main():
    pygame.init()
    pygame.font.init()
    width, height = 1024, 720
    screen = pygame.display.set_mode((width, height))

    if warning(screen, width, height):
        flash_screen(screen, width, height)


if __name__ == "__main__":
    main()
