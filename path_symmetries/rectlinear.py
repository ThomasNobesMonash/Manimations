from manim import *

class Scene2D(Scene):
    def construct(self):
        slen = 2
        grid_dims = 3
        
        # Construct square grid
        grid = VGroup(*[
            Square(side_length=slen).move_to(
                np.array([
                    (x - (grid_dims - 1) / 2) * slen,
                    (y - (grid_dims - 1) / 2) * slen,
                    0
                ])
            )
            for y in range(grid_dims)
            for x in range(grid_dims)
        ])
        self.play(Create(grid), run_time=0.4)
        self.wait(0.5)
        
        start_node = grid[0]
        goal_node = grid[8]
        
        # Draw start and goal nodes with $S$ and $G$
        start_label = Tex("$S$").scale(slen).move_to(start_node.get_center())
        goal_label = Tex("$G$").scale(slen).move_to(goal_node.get_center())
        self.play(Write(start_label), Write(goal_label), run_time=0.4)
        self.wait(0.5)
        
        # Animate a colored line from node 0 -> 6 -> 8, offsetting to avoid overlap with S/G
        path_indices = [0, 6, 8]
        path_points = [grid[i].get_center() for i in path_indices]

        # Offset amount (fraction of square side length)
        offset_frac = 0.35
        offset = slen * offset_frac

        # Calculate direction vectors for offsetting
        def offset_point(p1, p2, amount):
            direction = (p2 - p1)
            direction[2] = 0
            direction = direction / np.linalg.norm(direction)
            return p1 + direction * amount

        # Offset start and end points
        start = offset_point(path_points[0], path_points[1], offset)
        mid = path_points[1]
        end = offset_point(path_points[2], path_points[1], offset)

        path_line = Line(start, mid, color=YELLOW, stroke_width=8)
        path_line2 = Line(mid, end, color=YELLOW, stroke_width=8)
        self.play(Create(path_line), run_time=0.5)
        self.play(Create(path_line2), run_time=0.5)
        # Bring start and goal labels to the front
        self.bring_to_front(start_label, goal_label)
        self.wait(0.5)
