from math import pi, sin, cos

# This class renders a biomorph as a collection of lines in an abstract space.
# The resulting collection of lines can be scaled and drawn onto a real space.
class Biomorph_Renderer:

    def __init__(self, biomorph):
        self.biomorph = biomorph

    # A static helper method to determine if a heading is pointed 'upwards' or 'downwards'
    @staticmethod
    def heading_up(heading):
        return False if (1.5 * pi <= heading <= 2.0 * pi) or \
                        (0.0 <= heading <= 0.5 * pi) else True

    def generate(self):
        self.lines = []
        self.abstract_render()
        self.extent = self.find_min_max_x_y()


    # Draws a biomorph into an abstract space (a collection of lines centred on (0, 0))
    def abstract_render(self, ):
        self.abstract_render_step(self.biomorph.iterations.value(),
                                  self.biomorph.branch_length_up.value(), self.biomorph.branch_length_down.value(),
                                  self.biomorph.branch_length_delta_up.value(), self.biomorph.branch_length_delta_down.value(),
                                  self.biomorph.branch_angle_up.value(), self.biomorph.branch_angle_down.value(),
                                  self.biomorph.branch_angle_delta_up.value(), self.biomorph.branch_angle_delta_down.value(),
                                  self.biomorph.aspect_ratio.value(),
                                  (0, 0), pi)

    def abstract_render_step(self,
                             iterations_remaining,
                             branch_length_up, branch_length_down,
                             branch_length_delta_up, branch_length_delta_down,
                             branch_angle_up, branch_angle_down,
                             branch_angle_delta_up, branch_angle_delta_down,
                             aspect_ratio,
                             origin, heading):

        # Check if our current heading is 'upwards'
        up = Biomorph_Renderer.heading_up(heading)

        # Draw a new line and determine the next origin by returning it's end point
        new_origin = self.generate_abstract_line(branch_length_up, origin, heading, aspect_ratio) if up else \
            self.generate_abstract_line(branch_length_down, origin, heading, aspect_ratio)

        iterations_remaining -= 1
        if iterations_remaining > 0:

            # Determine the headings for our next two branches
            if up:
                heading_left = heading - branch_angle_up
                heading_right = heading + branch_angle_up
            else:
                heading_left = heading - branch_angle_down
                heading_right = heading + branch_angle_down

            # Update lengths and angles by the delta
            if up:
                branch_length_up += branch_length_delta_up
                branch_angle_up += branch_angle_delta_up
            else:
                branch_length_down += branch_length_delta_down
                branch_angle_down += branch_angle_delta_down

            # And render our next two branches recursively
            self.abstract_render_step(iterations_remaining,
                                      branch_length_up, branch_length_down,
                                      branch_length_delta_up, branch_length_delta_down,
                                      branch_angle_up, branch_angle_down,
                                      branch_angle_delta_up, branch_angle_delta_down,
                                      aspect_ratio,
                                      new_origin, heading_left)

            self.abstract_render_step(iterations_remaining,
                                      branch_length_up, branch_length_down,
                                      branch_length_delta_up, branch_length_delta_down,
                                      branch_angle_up, branch_angle_down,
                                      branch_angle_delta_up, branch_angle_delta_down,
                                      aspect_ratio,
                                      new_origin, heading_right)



    # Calculates (and stores) a line.
    # The coordinates of the new end point are returned.
    def generate_abstract_line(self, line_length, origin, heading, aspect_ratio):
        target_x = origin[0] + line_length * sin(heading)
        target_y = origin[1] + line_length * cos(heading)

        # Apply the aspect ratio
        target_x *= aspect_ratio

        self.lines.append((origin[0], origin[1], target_x, target_y, (128, 128, 128)))

        return target_x, target_y

    # Iterate through all the lines, determining the max and min X and Y
    def find_min_max_x_y(self, margin = 0.1):
        min_x = min_y = max_x = max_y = None

        for line in self.lines: # line is a tuple of start_x, start_y, end_x, end_y
            min_x = min(line[0], line[2]) if min_x is None else min(min_x, line[0], line[2])
            min_y = min(line[1], line[3]) if min_y is None else min(min_y, line[1], line[3])

            max_x = max(line[0], line[2]) if max_x is None else max(max_x, line[0], line[2])
            max_y = max(line[1], line[3]) if max_y is None else max(max_y, line[1], line[3])

        return min_x * (1+margin), min_y * (1+margin), max_x * (1+margin), max_y * (1+margin)



