from manim import *

class Scene2D(Scene):
    def construct(self):
        slen = 2
        grid = VGroup(*[
            Square(side_length=slen).move_to(np.array([x, y, 0]))
            for y in [slen, 0, -slen]
            for x in [-slen, 0, slen]
        ])
        self.play(Create(grid), run_time=0.4)
        self.wait(0.5)
        
        start_node = grid[6]
        goal_node = grid[2]
        
        # Draw start and goal nodes with $S$ and $G$
        start_label = Tex("$S$").scale(slen).move_to(start_node.get_center())
        goal_label = Tex("$G$").scale(slen).move_to(goal_node.get_center())
        self.play(Write(start_label), Write(goal_label), run_time=0.4)
        self.wait(0.5)
        
