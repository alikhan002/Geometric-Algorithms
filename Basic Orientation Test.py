import tkinter as tk
from tkinter import messagebox
import time

def orientation(p, q, r):
    """Calculate the orientation of the triplet (p, q, r)."""
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0: return 0  # collinear
    return 1 if val > 0 else 2  # clock or counterclockwise

def do_intersect(p1, q1, p2, q2):
    """Check if line segments (p1, q1) and (p2, q2) intersect."""
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    if o1 != o2 and o3 != o4: return True

    return False

def simple_sweeping_line_algorithm(segment1, segment2):
    """A simplified sweeping line algorithm to check intersection."""
    return do_intersect(segment1[0], segment1[1], segment2[0], segment2[1])

class LineSegmentApp:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=600, height=600)
        self.canvas.pack()

        self.segment_start = None
        self.segments = []

        self.algorithm_var = tk.StringVar(root)
        self.algorithm_var.set("Basic Orientation Test")
        self.algorithm_menu = tk.OptionMenu(root, self.algorithm_var, "Basic Orientation Test", "Simple Sweeping Line")
        self.algorithm_menu.pack()

        self.check_button = tk.Button(root, text="Check Intersection", command=self.check_intersection)
        self.check_button.pack()

        self.clear_button = tk.Button(root, text="Clear", command=self.clear_canvas)
        self.clear_button.pack()

        self.text_panel = tk.Text(root, height=10, width=50)
        self.text_panel.pack()

        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def on_canvas_click(self, event):
        if not self.segment_start:
            self.segment_start = (event.x, event.y)
        else:
            segment_end = (event.x, event.y)
            self.segments.append((self.segment_start, segment_end))
            self.canvas.create_line(self.segment_start[0], self.segment_start[1], segment_end[0], segment_end[1])
            self.segment_start = None

    def check_intersection(self):
        start_time = time.time()
        selected_algorithm = self.algorithm_var.get()
        for i in range(len(self.segments)):
            for j in range(i+1, len(self.segments)):
                intersect = False
                if selected_algorithm == "Basic Orientation Test":
                    intersect = do_intersect(self.segments[i][0], self.segments[i][1], self.segments[j][0], self.segments[j][1])
                elif selected_algorithm == "Simple Sweeping Line":
                    intersect = simple_sweeping_line_algorithm(self.segments[i], self.segments[j])

                if intersect:
                    end_time = time.time()
                    self.text_panel.insert(tk.END, f"Segments intersect using {selected_algorithm}!\n")
                    self.text_panel.insert(tk.END, f"Execution Time: {end_time - start_time:.6f} seconds\n")
                    self.text_panel.see(tk.END)
                    return

        end_time = time.time()
        self.text_panel.insert(tk.END, f"No intersection found using {selected_algorithm}.\n")
        self.text_panel.insert(tk.END, f"Execution Time: {end_time - start_time:.6f} seconds\n")
        self.text_panel.see(tk.END)

    def clear_canvas(self):
        self.canvas.delete("all")
        self.segments.clear()
        self.text_panel.delete("1.0", tk.END)

# Main window setup
root = tk.Tk()
root.title("Line Segment Intersection Checker")
app = LineSegmentApp(root)
root.mainloop()
