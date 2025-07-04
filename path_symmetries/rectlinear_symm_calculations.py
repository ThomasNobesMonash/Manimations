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


# Convert moves to grid indices
def add_move(curr, move):
    x, y, z = curr + move
    return x, y, z


# Calculate direction vectors for offsetting
def offset_point(p1, p2, amount):
    direction = (p2 - p1)
    direction[2] = 0
    direction = direction / np.linalg.norm(direction)
    return p1 + direction * amount


def animate_line(lgrid, moves, snode, COLOUR=YELLOW, slen=2):
    curr_pos = (0, 0, 0)
    path_indices = []
    grid_dims = int(np.sqrt(len(lgrid)))  # Assuming grid is square
    for move in moves:
        curr_pos = add_move(np.array(curr_pos), np.array(move))
        x_idx, y_idx = int(curr_pos[1]), int(curr_pos[0])
        idx =  y_idx * grid_dims + x_idx
        path_indices.append(idx)
    path_points = [lgrid[i].get_center() for i in path_indices]
    
    # Add snode.get_center() to all path_points
    # for i in range(len(path_points)):
    #     path_points[i] += snode.get_center()

    # Offset amount (fraction of square side length)
    offset_frac = 0.35
    offset = slen * offset_frac

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
    
    move_steps = [(1, 0, 0)] * (lgrid_dims - 1) + [(0, 1, 0)] * (lgrid_dims - 1)
    all_paths = list(permutations(move_steps))
    moves.clear()
    for path in all_paths:
        moves.append([(0, 0, 0)] + list(path))
    for move in moves:
        move.append((0, 0, 0))
    
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


def get_unique_color(base_colors, i, total):
            # Interpolate between base colors
            idx = i * (len(base_colors) - 1) / max(1, total - 1)
            low = int(idx)
            high = min(low + 1, len(base_colors) - 1)
            frac = idx - low
            return interpolate_color(base_colors[low], base_colors[high], frac)
   

class SymmCalcsScene2D(MovingCameraScene):
    def construct(self):
        myTemplate = TexTemplate()
        myTemplate.add_to_preamble(r"\usepackage{mathdots}")
        
        slen = 2
        grid = create_grid(slen, 3)
        init_grid = grid
        
        # Calculate spacing based on frame width and number of grids
        num_grids = 3
        base_y = grid.get_bottom()[1]
        # Highlight that these symmetries scale with grid size
        # Zoom out and shift grid to the far left, keeping it vertically centered
        frame = self.camera.frame
        frame_width = frame.get_width()
        
        spacing = frame_width * 0.9 / (num_grids)
        
        grid2 = create_grid(slen, 4)
        new_x = grid.get_center()[0] + grid.width / 2 + spacing + grid2.width / 2
        grid2.move_to(np.array([new_x, 0, 0]))
        grid2.shift([0, base_y - grid2.get_bottom()[1], 0])

        grid3 = create_grid(slen, 6)
        new_x = grid2.get_center()[0] + grid2.width / 2 + spacing + grid3.width / 2
        grid3.move_to(np.array([new_x, 0, 0]))
        grid3.shift([0, base_y - grid3.get_bottom()[1], 0])
        
        self.camera.frame.move_to(grid.get_center())
        self.add(grid)
        
        start_node = grid[0]
        goal_node = grid[8]
        
        # Add Respective start and goal labels for each grid
        start_label = Tex("$S$").scale(slen).move_to(start_node.get_center())
        goal_label = Tex("$G$").scale(slen).move_to(goal_node.get_center())
        start_label2 = Tex("$S$").scale(slen).move_to(grid2[0].get_center())
        goal_label2 = Tex("$G$").scale(slen).move_to(grid2[-1].get_center())
        start_label3 = Tex("$S$").scale(slen).move_to(grid3[0].get_center())
        goal_label3 = Tex("$G$").scale(slen).move_to(grid3[-1].get_center())
        self.add(start_label)
        self.add(goal_label)
        grid_label = Tex("3x3").scale(2).next_to(grid, UP, buff=0.5)
        grid_label2 = Tex("4x4").scale(2).next_to(grid2, UP, buff=0.5)
        grid_label3 = Tex("NxN").scale(2).next_to(grid3, UP, buff=0.5)
        
        moves = get_all_moves(3)
        
        # Calculate new center: move grid to far left, keep vertical center
        # Center camera so that all three grids are centered in the screen
        left_x = (grid.get_left()[0] + grid3.get_right()[0]) / 2
        new_center = np.array([left_x, grid.get_center()[1], 0])
        self.camera.frame.move_to(new_center)
        self.camera.frame.set(width=frame_width * 3)
        
        self.add(grid2)
        self.add(grid3)
        
        self.add(grid_label, grid_label2, grid_label3)
        self.add(start_label2, goal_label2, start_label3, goal_label3)
        
        number = Integer(6, color=BLUE_B).scale(2).next_to(grid, DOWN, buff=0.5)
        digit_width = Integer(1).scale(2).get_width()
        number2 = Integer(20, color=BLUE_B).scale(2).next_to(grid2, DOWN, buff=0.5).shift([- digit_width / 2, 0, 0])
        number3 = Text("?", color=BLUE_B).scale(2).next_to(grid3, DOWN, buff=0.5)
        self.add(number, number2, number3)
    
        # Add dots along last row and column
        n = 6
        dots = []
        for i in range(n - 1):
            idx = (n - 1) * n + i
            dot = Tex(r"$\vdots$").scale(1.5).move_to(grid3[idx].get_center())
            dots.append(dot)
        for i in range(n - 1):
            idx = i * n + (n - 1)
            dot = Tex(r"$\dots$").scale(1.5).move_to(grid3[idx].get_center())
            dots.append(dot)
        dots.append(Tex(r"$\iddots$", tex_template=myTemplate).scale(1.5).move_to(grid3[n * n - 1].get_center()))

        # Zoom in camera to fit the three grids
        all_grids = [grid, grid2, grid3]
        left_x = all_grids[0].get_left()[0]
        right_x = all_grids[2].get_right()[0]
        new_center = np.array([(left_x + right_x) / 2, all_grids[0].get_center()[1], 0])
        
        outline = Square(side_length=slen * n, color=YELLOW, stroke_width=10)
        outline.move_to(grid3.get_center())
        numbers = [number, number2, number3]
        for i, number in enumerate(numbers):
            self.add(outline)
                
        self.wait(1)
        
        word_eq = Tex("Number of paths = ?").scale(1.5).move_to(init_grid.get_bottom() + [0, -6, 0])
        self.play(
            Write(word_eq),
            run_time=1
        )
