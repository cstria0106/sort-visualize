from random import shuffle

import pygame

import sort


class Bar:
    def __init__(self, n):
        self.n = n
        self.color = (255, 255, 255)


def put_random(bars, n):
    for i in range(n):
        bars.append(Bar(i))
    shuffle(bars)


def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    clock = pygame.time.Clock()
    fps = 60

    black = (0, 0, 0)

    bars = []

    size = 1
    delay = 0.01
    skip = 10
    sorter = sort.Sorter(bars, delay, skip)
    samples = 600

    put_random(bars, samples)

    while True:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if sorter.sorting:
                    sorter.stop()
                    while not sorter.complete:
                        pass
                quit()
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if sorter.sorting:
                        sorter.stop()
                        while not sorter.complete:
                            pass
                    else:
                        sorter.run()

                elif event.key == pygame.K_r:
                    sorter.stop()
                    bars.clear()
                    put_random(bars, samples)
                elif event.key == pygame.K_LEFT:
                    if size > 1:
                        size -= 1
                elif event.key == pygame.K_RIGHT:
                    size += 1
                elif event.key == pygame.K_UP:
                    samples += 10
                    put_random(bars, 10)
                elif event.key == pygame.K_DOWN:
                    if samples > 10:
                        del bars[-11:-1]
                        samples -= 10

        screen.fill(black)
        for i, bar in enumerate(bars):
            rect = pygame.Rect((i * size, 600 - bar.n * size), (0, 0))
            image = pygame.Surface((size, bar.n * size))
            image.fill(bar.color)
            screen.blit(image, rect)

        pygame.display.update()
    pass


if __name__ == '__main__':
    main()
