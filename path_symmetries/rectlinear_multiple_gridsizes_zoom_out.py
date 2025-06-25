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
   

class MultGridsZoomOutScene2D(MovingCameraScene):
    def construct(self):
        myTemplate = TexTemplate()
        myTemplate.add_to_preamble(r"\usepackage{mathdots}")
        
        slen = 2
        grid = create_grid(slen, 3)
        
        # Calculate spacing based on frame width and number of grids
        num_grids = 3
        base_x = grid.get_center()[0]
        base_y = grid.get_bottom()[1]
        # Highlight that these symmetries scale with grid size
        # Zoom out and shift grid to the far left, keeping it vertically centered
        frame = self.camera.frame
        grid_width = slen * int(np.sqrt(len(grid)))
        frame_width = frame.get_width()
        
        spacing = frame_width * 0.9 / (num_grids)
        
        grid2 = create_grid(slen, 4)
        new_x = grid.get_center()[0] + grid.width / 2 + spacing + grid2.width / 2
        grid2.move_to(np.array([new_x, 0, 0]))
        grid2.shift([0, base_y - grid2.get_bottom()[1], 0])

        grid3 = create_grid(slen, 5)
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
        grid_label3 = Tex("5x5").scale(2).next_to(grid3, UP, buff=0.5)
        
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
        self.add(number)
        digit_width = Integer(1).scale(2).get_width()
        number = Integer(20, color=BLUE_B).scale(2).next_to(grid2, DOWN, buff=0.5).shift([- digit_width / 2, 0, 0])
        self.add(number)
        digit_width = Integer(1).scale(2).get_width()
        number = Integer(70, color=BLUE_B).scale(2).next_to(grid3, DOWN, buff=0.5).shift([- digit_width / 2, 0, 0])
        self.add(number)

        self.wait(1)
        
        self.play(
            FadeOut(start_label),
            FadeOut(goal_label),
            FadeOut(start_label2),
            FadeOut(goal_label2),
            FadeOut(start_label3),
            FadeOut(goal_label3),
            run_time=1
        )
        
        all_grids = [grid, grid2, grid3]
        base_x = grid.get_center()[0]
        base_y = grid.get_bottom()[1]
        # Create and add more grids up to NxN
        max_grid_size = 10
        for n in range(6, max_grid_size + 1):
            new_grid = create_grid(slen, n)
            # Position each grid to the right of the previous one
            prev_grid = all_grids[-1]
            # Calculate new_x by summing widths and spacing of all previous grids
            new_x = all_grids[0].get_center()[0]
            # Position new_grid to the right of the previous grid with even spacing
            prev_grid = all_grids[-1]
            new_x = prev_grid.get_center()[0] + prev_grid.width / 2 + spacing + new_grid.width / 2
            new_grid.move_to(np.array([new_x, 0, 0]))
            # Align bottom
            new_grid.shift([0, base_y - new_grid.get_bottom()[1], 0])
            if n == 6:
                self.play(
                    Create(new_grid),
                    run_time=1)
            else:
                self.add(new_grid)
            all_grids.append(new_grid)
        
        self.wait(1.5)
        all_grid_labels = [grid_label, grid_label2, grid_label3]
        for i, grid in enumerate(all_grids):
            if i < 3:
                continue
            self.add(grid)
            number = Text("?", color=BLUE_B).scale(2).next_to(grid, DOWN, buff=0.5)
            self.add(number)
            grid_label = Tex(f"{int(np.sqrt(len(grid)))}$\\times${int(np.sqrt(len(grid)))}", color=WHITE).scale(2).next_to(grid, UP, buff=0.5)
            all_grid_labels.append(grid_label)
            self.add(grid_label)
        
        left_x = (all_grids[0].get_left()[0] + all_grids[-1].get_right()[0]) / 2
        new_center = np.array([left_x, grid.get_center()[1], 0])
        total_width = all_grids[-1].get_right()[0] - all_grids[0].get_left()[0] + slen  # Add slen for padding
        # Gradually speed up, then slow down at the end using rate_func
        self.play(
            frame.animate.set(width=total_width * 1.1).move_to(new_center),
            run_time=2,
            rate_func=lambda t: smooth(t, inflection=0.7)  # Much faster at start, snappier
        )
        
        self.wait(2)
        # Shift camera frame down so grids are near the top
        # top_y = all_grids[0].get_top()[1]
        # frame_height = self.camera.frame.get_height()
        # # Place the top of the grids a bit below the top of the frame (e.g., 10% margin)
        # target_y = top_y - frame_height * 0.2
        # self.play(
        #     self.camera.frame.animate.move_to([new_center[0], target_y, 0]),
        #     run_time=1
        # )
        
        # Emphasize (flash/grow) each number below the grid
        for i, grid in enumerate(all_grids):
            # Find the number object below this grid
            if i == 0:
                number = Integer(1, color=BLUE_B).scale(2).next_to(grid, DOWN, buff=0.5)
            elif i == 1:
                number = Integer(20, color=BLUE_B).scale(2).next_to(grid, DOWN, buff=0.5).shift([-digit_width / 2, 0, 0])
            elif i == 2:
                number = Integer(70, color=BLUE_B).scale(2).next_to(grid, DOWN, buff=0.5).shift([-digit_width / 2, 0, 0])
            else:
                number = Text("?", color=BLUE_B).scale(2).next_to(grid, DOWN, buff=0.5)
        
        # Fade out all grids except the first, second, and last, along with their grid_labels and numbers
        grids_to_fade = [g for i, g in enumerate(all_grids) if i not in (0, 1, len(all_grids) - 1)]
        grid_labels_to_fade = []
        numbers_to_fade = [
            n for i, g in enumerate(all_grids)
            for n in self.mobjects
            if (isinstance(n, Text) or isinstance(n, Integer))
            and n.get_center()[1] < g.get_bottom()[1]
            and i not in [0, 1, len(all_grids) - 1]
        ]
        for i, g in enumerate(all_grids):
            if i not in [0, 1, len(all_grids) - 1]:
                # Find the grid label above this grid
                label = next((m for m in self.mobjects if isinstance(m, Tex) and m.get_center()[0] == g.get_center()[0] and m.get_center()[1] > g.get_top()[1]), None)
                if label:
                    grid_labels_to_fade.append(label)
        # Remove grids at indices not in (0, 1, len(all_grids) - 1)
        for i in sorted([i for i in range(len(all_grids)) if i not in [0, 1, len(all_grids) - 1]], reverse=True):
            del all_grids[i]
        number1 = Integer(6, color=BLUE_B).scale(2).next_to(all_grids[0], DOWN, buff=0.5)
        number2 = Integer(20, color=BLUE_B).scale(2).next_to(all_grids[1], DOWN, buff=0.5)
        self.add(number1)
        self.add(number2)
        last_number = Text("?", color=BLUE_B).scale(2).next_to(all_grids[-1], DOWN, buff=0.5)
        self.add(last_number)
        # Fade out all numbers
        self.play(
            *[FadeOut(g) for g in grids_to_fade],
            *[FadeOut(l) for l in grid_labels_to_fade],
            *[FadeOut(n) for n in numbers_to_fade],
            run_time=1
        )
        
        self.wait(1)
        
        # Move all_grids[-1] (the largest grid), its label, and its number to be next to all_grids[1]
        # Calculate the new x position: to the right of all_grids[1] with same spacing
        right_grid = all_grids[1]
        moved_grid = all_grids[-1]
        new_grid = create_grid(slen, 6)
        new_x = right_grid.get_center()[0] + right_grid.width / 2 + spacing + new_grid.width / 2
        new_grid.move_to(np.array([new_x, new_grid.get_center()[1], 0]))
        new_label= Tex("$NxN$").scale(2).next_to(new_grid, UP, buff=0.5)
        new_label.next_to(new_grid, UP, buff=0.5)
        new_number = Text("?", color=BLUE_B).scale(2).next_to(new_grid, DOWN, buff=0.5)
        # Add dots along last row and column
        n = 6
        dots = []
        for i in range(n - 1):
            idx = (n - 1) * n + i
            dot = Tex(r"$\vdots$").scale(1.5).move_to(new_grid[idx].get_center())
            dots.append(dot)
        for i in range(n - 1):
            idx = i * n + (n - 1)
            dot = Tex(r"$\dots$").scale(1.5).move_to(new_grid[idx].get_center())
            dots.append(dot)
        dots.append(Tex(r"$\iddots$", tex_template=myTemplate).scale(1.5).move_to(new_grid[n * n - 1].get_center()))
        moved_label = all_grid_labels[-1]
        # Animate transition from moved_grid to new_grid
        self.play(
            Transform(moved_grid, new_grid),
            Transform(moved_label, new_label),
            Transform(last_number, new_number),
            run_time=1
        )

        # Zoom in camera to fit the three grids
        left_x = all_grids[0].get_left()[0]
        right_x = all_grids[2].get_right()[0]
        new_center = np.array([(left_x + right_x) / 2, all_grids[0].get_center()[1], 0])
        total_width = right_x - left_x + slen  # Add slen for padding

        self.play(
            self.camera.frame.animate.set(width=total_width * 1.1).move_to(new_center),
            run_time=1
        )
        # Add dots to the scene
        self.play(*[FadeIn(dot) for dot in dots], run_time=0.5)
        
        outline = Square(side_length=slen * n, color=YELLOW, stroke_width=10)
        outline.move_to(new_grid.get_center())
        numbers = [number1, number2, last_number]
        for i, number in enumerate(numbers):
            scale_up_time = max(0.15, 0.3 - i * 0.02)
            scale_down_time = max(0.1, 0.2 - i * 0.015)
            self.play(
                number.animate.scale(1.5).set_color(YELLOW),
                run_time=scale_up_time
            )
            if i < 2:
                self.play(
                    number.animate.scale(2/3).set_color(BLUE_B),
                    run_time=scale_down_time
                )
            else:
                self.play(
                    number.animate.scale(2/3).set_color(YELLOW),
                    # Animate a yellow outline square around the last grid
                    run_time=scale_down_time
                )
                # Animate outline creation starting from the bottom-left corner
                outline.set_stroke(opacity=0)  # Hide initially
                self.add(outline)
                # Get the four corners in order: bottom-left, bottom-right, top-right, top-left
                corners = [
                    outline.get_corner(DL),
                    outline.get_corner(DR),
                    outline.get_corner(UR),
                    outline.get_corner(UL),
                    outline.get_corner(DL)
                ]
                animated_outline = VMobject()
                animated_outline.set_stroke(color=YELLOW, width=10)
                animated_outline.set_points_as_corners([corners[0], corners[0]])
                self.add(animated_outline)
                def update_outline(mob, alpha):
                    n = len(corners) - 1
                    total_length = sum(np.linalg.norm(corners[i+1] - corners[i]) for i in range(n))
                    target_length = total_length * alpha
                    points = [corners[0]]
                    length = 0
                    for i in range(n):
                        seg = corners[i+1] - corners[i]
                        seg_len = np.linalg.norm(seg)
                        if length + seg_len < target_length:
                            points.append(corners[i+1])
                            length += seg_len
                        else:
                            remain = target_length - length
                            if seg_len > 0:
                                points.append(corners[i] + seg / seg_len * remain)
                            break
                    mob.set_points_as_corners(points)
                self.play(UpdateFromAlphaFunc(animated_outline, update_outline), run_time=2)
                outline.set_stroke(opacity=1)
                self.remove(animated_outline)

        self.wait(1)
