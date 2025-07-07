import asyncio
import pygame
from constants import WIDTH, HEIGHT
from game import Game

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hexagonal 2048")

game = Game(screen)


async def main():
    await game.run()


if __name__ == "__main__":
    asyncio.run(main())
    pygame.quit()
