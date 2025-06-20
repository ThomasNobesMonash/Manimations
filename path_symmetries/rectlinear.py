from manim import *

class Scene2D(MovingCameraScene):
    def construct(self):
        slen = 2
        grid_dims = 3
        
        # Construct square grid
        grid = VGroup(*[
            Square(side_length=slen).move_to(
            np.array([
                x * slen,
                y * slen,
                0
            ])
            )
            for y in range(grid_dims)
            for x in range(grid_dims)
        ])
        self.camera.frame.move_to(grid.get_center())
        self.play(Create(grid), run_time=0.4)
        self.wait(0.5)
        
        start_node = grid[0]
        goal_node = grid[8]
        
        # Draw start and goal nodes with $S$ and $G$
        start_label = Tex("$S$").scale(slen).move_to(start_node.get_center())
        goal_label = Tex("$G$").scale(slen).move_to(goal_node.get_center())
        self.play(Write(start_label), Write(goal_label), run_time=0.4)
        self.wait(0.5)
        
        # Define path as a sequence of (dx, dy) moves from the start node (top-left)
        dx, dy = 2, 2
        top_moves = [(0, 0, 0), (0, dy, 0), (dx, 0, 0), (0, 0, 0)]
        top_moves2 = [(0, 0, 0), (0, dy/2, 0), (dx, 0, 0), (dx/2, 0, 0), (0, dy/2, 0), (0, 0, 0)]
        bot_moves = [(0, 0, 0), (dx, 0, 0), (0, dy, 0), (0, 0, 0)]
        bot_moves2 = [(0, 0, 0), (dx/2, 0, 0), (0, dy/2, 0), (dx/2, 0, 0), (0, dy/2, 0), (0, 0, 0)]

        # Convert moves to grid indices
        def add_move(curr, move):
            x, y, z = curr + move
            return x, y, z

        def animate_line(moves, COLOUR=YELLOW):
            # Yellow line
            curr_pos = start_node.get_center()
            path_indices = []
            for move in moves:
                curr_pos = add_move(np.array(curr_pos), np.array(move))
                idx = int(curr_pos[1]) * grid_dims + int(curr_pos[0])
                path_indices.append(idx)
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
        
            # Offset the first point towards the second, and the last towards the second-to-last
            offset_points = [offset_point(path_points[0], path_points[1], offset)]
            for i in range(1, len(path_points) - 2):
                offset_points.append(path_points[i])
            offset_points.append(offset_point(path_points[-2], path_points[-3], offset))

            # Create lines between consecutive offset points
            lines = VGroup(*[
                Line(offset_points[i], offset_points[i + 1], color=COLOUR, stroke_width=8)
                for i in range(len(offset_points) - 1)
            ])
            self.play(Create(lines), run_time=0.5)
            
        animate_line(top_moves, YELLOW)
        animate_line(bot_moves, GREEN)
        animate_line(bot_moves2, ORANGE)
        
        
        self.wait(0.5)
        self.wait(1)
