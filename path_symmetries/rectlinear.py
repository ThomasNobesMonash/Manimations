from manim import *
from itertools import permutations
from manim.utils.color import interpolate_color

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
        bot_moves = [(0, 0, 0), (dx, 0, 0), (0, dy, 0), (0, 0, 0)]
        bot_moves2 = [(0, 0, 0), (dx/2, 0, 0), (0, dy/2, 0), (dx/2, 0, 0), (0, dy/2, 0), (0, 0, 0)]
        bot_moves3 = [(0, 0, 0), (dx/2, 0, 0), (0, dy, 0), (dx/2, 0, 0), (0, 0, 0)]

        # Convert moves to grid indices
        def add_move(curr, move):
            x, y, z = curr + move
            return x, y, z

        def animate_line(moves, COLOUR=YELLOW):
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
            return lines
            
        self.play(Create(animate_line(bot_moves, GREEN), run_time=0.5))
        self.play(Create(animate_line(top_moves, YELLOW), run_time=0.5))
        self.play(Create(animate_line(bot_moves2, ORANGE), run_time=0.5))
        self.play(Create(animate_line(bot_moves3, BLUE), run_time=0.5))
        self.wait(1)
        
        # Fade out all lines and groups of lines
        lines_to_fade = [m for m in self.mobjects if isinstance(m, VGroup) or isinstance(m, Line)]
        # Do not fade out the grid or the start/goal labels
        lines_to_fade = [
            m for m in self.mobjects
            if (isinstance(m, VGroup) or isinstance(m, Line))
            and m not in [grid, start_label, goal_label]
        ]
        self.play(*[FadeOut(line) for line in lines_to_fade])
        self.wait(1)
        
        # Define paths for all permutations of moves between S and G
        # These paths iterate through every perumtation of adding x, y in range (0, 3)
        moves = []
        for _ in range(grid_dims * grid_dims):
            moves.append([(0, 0, 0)])  # Each list is a distinct object
        
        move_steps = [(1, 0, 0)] * 2 + [(0, 1, 0)] * 2
        all_paths = list(permutations(move_steps))
        moves.clear()
        for path in all_paths:
            moves.append([(0, 0, 0)] + list(path))
        for move in moves:
            move.append((0, 0, 0))
        print("Generated moves:")
        for move in moves:
            print(move)
        # Remove duplicate paths from moves
        unique_moves = []
        seen = set()
        for move in moves:
            move_tuple = tuple(move)
            if move_tuple not in seen:
                unique_moves.append(move)
                seen.add(move_tuple)
        moves = unique_moves
        
        # Animate all paths
        num_paths = len(moves)
        # Generate a unique color for each path using a color gradient
        base_colors = [interpolate_color(RED, BLUE, alpha) for alpha in np.linspace(0, 1, num_paths)]
        def get_unique_color(i, total):
            # Interpolate between base colors
            idx = i * (len(base_colors) - 1) / max(1, total - 1)
            low = int(idx)
            high = min(low + 1, len(base_colors) - 1)
            frac = idx - low
            return interpolate_color(base_colors[low], base_colors[high], frac)

        for i, move in enumerate(moves):
            color = get_unique_color(i, num_paths)
            line = animate_line(move, color)
            self.play(Create(line), run_time=0.3)
            self.play(FadeOut(line), run_time=0.2)

        self.wait(1)
