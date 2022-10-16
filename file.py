import pygame


def main():
    
    # activate the pygame library .
    pygame.init()
    
    # create the display surface object
    # of specific dimension..e(X, Y).
    scrn = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    
    # set the pygame window name
    pygame.display.set_caption('image')
    
    # create a surface object, image is drawn on it.
    imp = pygame.image.load("./all_files/0000197c9ddf7fff.jpg").convert()
    #imp = pygame.transform.scale(imp, (1280, 720))
    print(imp)
    
    # Using blit to copy content from one surface to other
    scrn.blit(imp, (0, 0))
    
    # paint screen one time
    pygame.display.flip()
    status = True
    while (status):
    
    # iterate over the list of Event objects
    # that was returned by pygame.event.get() method.
        for i in pygame.event.get():
    
            # if event object type is QUIT
            # then quitting the pygame
            # and program both.
            if i.type == pygame.QUIT:
                status = False
    
    # deactivates the pygame library
    pygame.quit()


if __name__ == '__main__':
    main()