from biomorph import Biomorph
from biomorph_rendererer import Biomorph_Renderer
import pygame
from math import sin, cos, pi, floor

WINDOW_SIZE = (1200, 800)
PARENT_SIZE_DIVISOR = 8
CHILD_SIZE_DIVISOR = 20
CHILD_RADIUS_DIVISOR = 3.75
CENTRE_OFFSET_DIVISOR = 1.6
PARENT_RENDER_SIZE = (WINDOW_SIZE[0] /PARENT_SIZE_DIVISOR, WINDOW_SIZE[0] / PARENT_SIZE_DIVISOR)
CHILD_RENDER_SIZE = (WINDOW_SIZE[0] / CHILD_SIZE_DIVISOR, WINDOW_SIZE[0] / CHILD_SIZE_DIVISOR)
CHILD_DISTANCE_FROM_CENTRE = WINDOW_SIZE[0] / CHILD_RADIUS_DIVISOR


class Game:

    def __init__(self):
        # Create the initial parent
        self.parent = Biomorph()
        self.parent.randomise()

        # And a surface to render it
        self.parent_surface = pygame.Surface(PARENT_RENDER_SIZE)
        self.parent_position = (WINDOW_SIZE[0] / CENTRE_OFFSET_DIVISOR - PARENT_RENDER_SIZE[0] / 2, WINDOW_SIZE[1] / 2 - PARENT_RENDER_SIZE[1] / 2)

        # Render it to the surface
        self.render_biomorph_to_surface(self.parent, self.parent_surface)

        # Now to the same for the offspring
        self.child_surfaces = []
        self.child_positions = []
        self.offspring_hints = []
        self.offspring = self.parent.generate_offspring_standard()
        num_offspring = len(self.offspring)
        for index, child in enumerate(self.offspring):
            self.child_surfaces.append(pygame.Surface(CHILD_RENDER_SIZE))
            self.render_biomorph_to_surface(child, self.child_surfaces[index])
            self.offspring_hints.append(
                self.parent.all_genes[floor(index /2)].name + ' (+)' if index % 2 == 0 else
                self.parent.all_genes[floor((index - 1) /2)].name + ' (-)')
            self.child_positions.append(self.calculate_child_position(index, num_offspring))

    def calculate_child_position(self, index, num_offspring):
        child_angle = index * 2 * pi / num_offspring
        child_x = WINDOW_SIZE[0] / CENTRE_OFFSET_DIVISOR + CHILD_DISTANCE_FROM_CENTRE * cos(child_angle) - CHILD_RENDER_SIZE[0] / 2
        child_y = WINDOW_SIZE[1] / 2 + CHILD_DISTANCE_FROM_CENTRE * sin(child_angle) - CHILD_RENDER_SIZE[1] / 2
        return child_x, child_y


    def render_biomorph_to_surface(self, biomorph, surface):
        # Render the biomorph to an abstract space
        renderer = Biomorph_Renderer(biomorph)
        renderer.generate()
        # Grab the biomorph's extent and lines
        # extent is a tuple - (min_x, min_x, max_x, max_y) in the abstract space
        extent = renderer.extent
        # lines are an array of lines in the abstract space (start_x, start_y, end_x, end_y, colour)
        # colour itself it a tuple (r,g,b)
        lines = renderer.lines

        # Scale the biomorph and render it to the supplied surface
        surface_width = surface.get_width()
        surface_height = surface.get_height()

        abstract_width = max(extent[2] - extent[0], 100)
        abstract_height = max(extent[3] - extent[1], 100)

        # Determine the scale factor - making sure we maintain aspect ratio
        scale_width = surface_width / abstract_width
        scale_height = surface_height / abstract_height
        scale = min(scale_height, scale_width)

        translate_x = surface_width / 2
        translate_y = surface_height / 2

        surface.fill((0, 0, 0))

        for line in lines:
            # transform line to surface by scaling and translating
            (start_x, start_y, end_x, end_y, colour) = line

            start_x = translate_x + start_x * scale
            end_x = translate_x + end_x * scale
            start_y = translate_y + start_y * scale
            end_y = translate_y + end_y * scale

            pygame.draw.line(surface, colour, (start_x, start_y), (end_x, end_y), 1)

    def run(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("Biomorphs")
        self.window = pygame.display.set_mode(WINDOW_SIZE)

        self.gameloop()

    def render_text(self, text, position):
        font = pygame.font.Font(None, 18)
        self.window.blit(font.render(text, True, (255, 255, 255), (0, 0, 0)), position)

    def render_parent_info(self):
        text_x = 20
        text_y = 20

        for gene in self.parent.all_genes:
            self.render_text(gene.short_str(),
                             (text_x, text_y))
            text_y += 20

    def gameloop(self):

        done = False
        offspring_hint = ''
        while not done:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.MOUSEMOTION:
                    pos = pygame.mouse.get_pos()
                    offspring_hint = ''
                    for index, cp in enumerate(self.child_positions):
                        if cp[0] <= pos[0] <= cp[0] + CHILD_RENDER_SIZE[0] and \
                                cp[1] <= pos[1] <= cp[1] + CHILD_RENDER_SIZE[1]:
                            offspring_hint = self.offspring_hints[index]
                            break;
                elif event.type == pygame.MOUSEBUTTONUP:
                    if self.parent_position[0] <= pos[0] <= self.parent_position[0] + PARENT_RENDER_SIZE[0] and \
                       self.parent_position[1] <= pos[1] <= self.parent_position[1] + PARENT_RENDER_SIZE[1]:
                        pass # parent clicked on
                    else:
                        for index, cp in enumerate(self.child_positions):
                            if cp[0] <= pos[0] <= cp[0] + CHILD_RENDER_SIZE[0] and \
                               cp[1] <= pos[1] <= cp[1] + CHILD_RENDER_SIZE[1]:
                                self.parent = self.offspring[index]
                                self.render_biomorph_to_surface(self.parent, self.parent_surface)
                                self.offspring = self.parent.generate_offspring_standard()
                                for idx, child in enumerate(self.offspring):
                                    self.render_biomorph_to_surface(child, self.child_surfaces[idx])
                                break

            self.window.fill((0,0,0))

            self.window.blit(self.parent_surface, self.parent_position)
            for index, surface in enumerate(self.child_surfaces):
                self.window.blit(surface, self.child_positions[index])

            self.render_parent_info()

            self.render_text(offspring_hint, (20, 260))

            pygame.display.flip()


