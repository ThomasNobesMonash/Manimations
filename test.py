from manim import *

class demoScene(Scene):
    def construct(self):
        astar_text = Tex(r"The A$^\ast$ Algorithm", font_size=92)
        astar_text.to_corner(UP + LEFT)
        self.play(Write(astar_text), run_time=1)
        
        # astar_text = Tex(r"The A$^\ast$ Algorithm")
        # astar_text.shift(UP)
        # descr_text  = Tex(r"Finds the shortest path efficiently")
        # descr_text .next_to(astar_text, DOWN)
        # self.play(Write(astar_text), run_time=2)
        # self.play(Write(descr_text ), run_time=2)
        # self.wait(1)
        
        # circle = Circle().set_color(BLUE)
        # square = Square().set_color(RED)
        # group = VGroup(circle, square).arrange(RIGHT, buff=1).next_to(descr_text, DOWN, buff=1)
        # self.play(FadeIn(group), run_time=1.5)
        # self.wait(1)
        # self.play(FadeOut(group), run_time=1)
