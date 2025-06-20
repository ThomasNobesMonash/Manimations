from manim import *
from itertools import permutations
from manim.utils.color import interpolate_color

def create_grid(slen, grid_dims):
    """Create a square grid of squares with given side length and dimensions."""
    return VGroup(*[
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


class MultipleGridsScene2D(MovingCameraScene):
    def construct(self):
        slen = 2
        grid_dims = 3
        grid = create_grid(slen, grid_dims)
        
        self.camera.frame.move_to(grid.get_center())
        self.add(grid)
        
        start_node = grid[0]
        goal_node = grid[8]
        
        # Draw start and goal nodes with $S$ and $G$
        start_label = Tex("$S$").scale(slen).move_to(start_node.get_center())
        goal_label = Tex("$G$").scale(slen).move_to(goal_node.get_center())
        self.add(start_label)
        self.add(goal_label)
        self.wait(0.5)

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
            
        def get_all_moves(lgrid_dims):
            # Define paths for all permutations of moves between S and G
            # These paths iterate through every perumtation of adding x, y in range (0, 3)
            moves = []
            for _ in range(lgrid_dims * lgrid_dims):
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
            return moves
        
        moves = get_all_moves(3)
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

        # Highlight that these symmetries scale with grid size
        # Zoom out and shift grid to the far left, keeping it vertically centered
        frame = self.camera.frame
        grid_width = grid_dims * slen
        frame_width = frame.get_width()
        # Calculate new center: move grid to far left, keep vertical center
        left_x = 2.7*(grid.get_center()[0] + (frame_width / 2 - grid_width / 2))
        new_center = np.array([left_x, grid.get_center()[1], 0])
        self.play(
            frame.animate.set(width=frame_width * 3).move_to(new_center),
            run_time=1
        )
        
        # Create a 4x4 and a 5x5 grid
        # Calculate spacing based on frame width and number of grids
        num_grids = 3
        spacing = frame_width * 0.9 / (num_grids)
        base_x = grid.get_center()[0]

        # Get bottom y of the first grid
        base_y = grid.get_bottom()[1]

        grid2 = create_grid(slen, 4)
        # Align bottom of grid2 to base_y
        grid2.move_to(np.array([base_x + spacing * np.sqrt(len(grid)), 0, 0]))
        grid2.shift([0, base_y - grid2.get_bottom()[1], 0])

        grid3 = create_grid(slen, 5)
        # Align bottom of grid3 to base_y
        grid3.move_to(np.array([base_x * spacing * np.sqrt(len(grid)) + np.sqrt(len(grid2)), 0, 0]))
        grid3.shift([0, base_y - grid3.get_bottom()[1], 0])
        
        assemble_time = 1

        self.play(
            Create(grid2),
            run_time=assemble_time
        )
        self.play(
            Create(grid3),
            run_time=assemble_time
        )
        
        # Add Respective start and goal labels for each grid
        start_label2 = Tex("$S$").scale(slen).move_to(grid2[0].get_center())
        goal_label2 = Tex("$G$").scale(slen).move_to(grid2[15].get_center())
        start_label3 = Tex("$S$").scale(slen).move_to(grid3[0].get_center())
        goal_label3 = Tex("$G$").scale(slen).move_to(grid3[24].get_center())
        self.play(
            Write(start_label2), Write(goal_label2),
            Write(start_label3), Write(goal_label3),
            run_time=0.8
        )
        
        # generate all moves for each grid
        moves2 = get_all_moves(4)
        print("moves:", moves)
        print("moves2:", moves2)
        moves3 = get_all_moves(5)
        # animate all paths for each grid
            
        for i, move in enumerate(moves):
            num_paths = len(moves)
            color = get_unique_color(i, num_paths)
            line = animate_line(move, color)
            self.play(Create(line), run_time=0.3)
            self.play(FadeOut(line), run_time=0.2)
        
        for i, move in enumerate(moves2):
            num_paths = len(moves2)
            color = get_unique_color(i, num_paths)
            line = animate_line(move, color)
            self.play(Create(line), run_time=0.3)
            self.play(FadeOut(line), run_time=0.2)
        
        for i, move in enumerate(moves3):
            num_paths = len(moves3)
            color = get_unique_color(i, num_paths)
            line = animate_line(move, color)
            self.play(Create(line), run_time=0.3)
            self.play(FadeOut(line), run_time=0.2)  

        self.wait(1)
