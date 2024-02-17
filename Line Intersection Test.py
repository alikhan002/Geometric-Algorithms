import tkinter as tk
from tkinter import messagebox

# Functions for intersection checking
def orientation(p, q, r):
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0: return 0  # Collinear
    return 1 if val > 0 else 2  # Clockwise or counterclockwise

def on_segment(p, q, r):
    return (q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and
            q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1]))

def do_intersect(p1, q1, p2, q2):
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    if o1 != o2 and o3 != o4:
        return True

    if o1 == 0 and on_segment(p1, p2, q1): return True
    if o2 == 0 and on_segment(p1, q2, q1): return True
    if o3 == 0 and on_segment(p2, p1, q2): return True
    if o4 == 0 and on_segment(p2, q1, q2): return True

    return False

def cross_product(p1, p2, p3):
    return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])

def check_intersection_cross_product(p1, q1, p2, q2):
    if cross_product(p1, p2, q1) * cross_product(p1, q2, q1) < 0 and \
       cross_product(p2, p1, q2) * cross_product(p2, q1, q2) < 0:
        return True
    return False

# Initialize the main application window
app = tk.Tk()
app.title("Line Intersection Checker")

# Create a canvas for drawing line segments
canvas = tk.Canvas(app, width=400, height=400)
canvas.pack()

# Global variables to store line segment points
current_segment = []
segments = []

def on_canvas_click(event):
    global current_segment
    if len(current_segment) < 2:
        current_segment.append((event.x, event.y))
        if len(current_segment) == 2:
            canvas.create_line(current_segment[0][0], current_segment[0][1],
                               current_segment[1][0], current_segment[1][1])
            segments.append(current_segment)
            current_segment = []

canvas.bind("<Button-1>", on_canvas_click)

# Variable to store the selected method
method_var = tk.StringVar(value="orientation")

# Radio buttons for method selection
orientation_rb = tk.Radiobutton(app, text="Orientation Method", variable=method_var, value="orientation")
cross_product_rb = tk.Radiobutton(app, text="Cross Product Method", variable=method_var, value="cross_product")

orientation_rb.pack()
cross_product_rb.pack()

def check_intersection():
    if len(segments) >= 2:
        seg1, seg2 = segments[-2], segments[-1]
        intersects = False
        if method_var.get() == "orientation":
            intersects = do_intersect(seg1[0], seg1[1], seg2[0], seg2[1])
        elif method_var.get() == "cross_product":
            intersects = check_intersection_cross_product(seg1[0], seg1[1], seg2[0], seg2[1])
        result_text = "Intersect" if intersects else "Do not intersect"
        messagebox.showinfo("Intersection Result", result_text)

check_button = tk.Button(app, text="Check Intersection", command=check_intersection)
check_button.pack()

app.mainloop()
