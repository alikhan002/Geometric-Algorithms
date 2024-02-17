import tkinter as tk
import time
from math import atan2  # For Graham Scan
from itertools import combinations  # For Quick Elimination


def merge(hull1, hull2):
    # Simplified merging logic for two convex hulls
    hull = hull1 + hull2  # Placeholder, implement proper merging logic here
    return hull

def divide_and_conquer_convex_hull(points):
    if len(points) <= 3:
        return points  # A direct computation for small number of points

    mid = len(points) // 2
    left_hull = divide_and_conquer_convex_hull(sorted(points[:mid], key=lambda p: p[0]))
    right_hull = divide_and_conquer_convex_hull(sorted(points[mid:], key=lambda p: p[0]))

    return merge(left_hull, right_hull)


def orientation(p, q, r):
    """Calculate the orientation of the triplet (p, q, r)."""
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0: return 0  # collinear
    return 1 if val > 0 else 2  # clock or counterclockwise


def convex_hull_jarvis_march(points):
    if len(points) < 3:
        return points

    def leftmost_point(pts):
        return min(pts, key=lambda p: (p[0], p[1]))

    hull = [leftmost_point(points)]

    while True:
        endpoint = points[0]  # Start with an arbitrary point in the set
        for j in range(1, len(points)):
            # Check if the current point is more counterclockwise than the endpoint
            # In other words, check if the line segment from hull[-1] to points[j]
            # is on the left side of the line segment from hull[-1] to endpoint
            if orientation(hull[-1], points[j], endpoint) == 2 or endpoint == hull[-1]:
                endpoint = points[j]

        # Avoid duplicate points in the hull
        if endpoint != hull[0]:
            hull.append(endpoint)
        else:
            break  # We have wrapped around to the first point

    return hull


def graham_scan(points):
    if len(points) < 3:
        return points

    # Find the bottom-most point (and left-most if there are ties)
    bottom_most = min(points, key=lambda p: (p[1], p[0]))

    # Sort the points based on the polar angle with bottom_most
    def polar_angle(p0, p1):
        return atan2(p1[1] - p0[1], p1[0] - p0[0])

    sorted_points = sorted(points, key=lambda p: (polar_angle(bottom_most, p), -p[1], p[0]))

    # Initialize the hull with the first three points
    hull = sorted_points[:3]

    for p in sorted_points[3:]:
        while len(hull) >= 2 and orientation(hull[-2], hull[-1], p) != 2:
            hull.pop()
        hull.append(p)

    return hull


def quick_elimination(points):
    if len(points) < 3:
        return points

    # Filter points that are not part of the hull
    def is_inside(p, q, r, s):
        # Check if point 's' is inside the triangle formed by 'p', 'q', 'r'
        pass  # Implement the logic

    filtered_points = []
    for p in points:
        if not any(is_inside(q, r, s, p) for q, r, s in combinations(points, 3)):
            filtered_points.append(p)

    # Apply a convex hull algorithm (like Graham Scan) to the filtered points
    return graham_scan(filtered_points)








def convex_hull_brute_force(points):
    n = len(points)
    if n < 3:
        return points

    def on_same_side(p1, p2, a, b):
        # Check if points p1 and p2 are on the same side of the line segment a-b
        cp1 = (b[0] - a[0]) * (p1[1] - a[1]) - (b[1] - a[1]) * (p1[0] - a[0])
        cp2 = (b[0] - a[0]) * (p2[1] - a[1]) - (b[1] - a[1]) * (p2[0] - a[0])
        return cp1 * cp2 >= 0

    hull = []
    for i in range(n):
        for j in range(n):
            if i != j:
                external = True
                for k in range(n):
                    if k != i and k != j and not on_same_side(points[i], points[j], points[k], points[(k+1)%n]):
                        external = False
                        break
                if external:
                    hull.append(points[i])
                    hull.append(points[j])

    # Remove duplicates and return
    return list(set(hull))





class ConvexHullApp:
    def __init__(self, root):
        self.root = root
        self.points = []
        self.canvas = tk.Canvas(root, width=600, height=600, bg="white")
        self.canvas.pack(side=tk.LEFT)
        self.canvas.bind("<Button-1>", self.add_point)

        self.algorithm_var = tk.StringVar(root)
        self.algorithm_var.set("Brute Force")
        self.algorithm_menu = tk.OptionMenu(root, self.algorithm_var, "Brute Force", "Jarvis March", "Graham Scan", "Quick Elimination","Divide and Conquer")
        self.algorithm_menu.pack()

        self.run_button = tk.Button(root, text="Run Convex Hull", command=self.calculate_convex_hull)
        self.run_button.pack()

        self.time_label = tk.Label(root, text="")
        self.time_label.pack()

        self.clear_button = tk.Button(root, text="Clear", command=self.clear_canvas)
        self.clear_button.pack()

    def add_point(self, event):
        point = (event.x, event.y)
        self.points.append(point)
        self.canvas.create_oval(point[0]-2, point[1]-2, point[0]+2, point[1]+2, fill="black")

    def calculate_convex_hull(self):
        start_time = time.time()
        selected_algorithm = self.algorithm_var.get()
        
        if selected_algorithm == "Brute Force":
            hull = convex_hull_brute_force(self.points)
        elif selected_algorithm == "Jarvis March":
            hull = convex_hull_jarvis_march(self.points)
        elif selected_algorithm == "Graham Scan":
            hull = graham_scan(self.points)
        elif selected_algorithm == "Quick Elimination":
            hull = quick_elimination(self.points)  
        elif selected_algorithm == "Divide and Conquer":
            hull = divide_and_conquer_convex_hull(self.points) 

        end_time = time.time()
        self.display_hull(hull)
        self.display_execution_time(end_time - start_time)

    def display_hull(self, hull):
        if len(hull) < 3:
            return
        for i in range(len(hull)):
            self.canvas.create_line(hull[i][0], hull[i][1], hull[(i+1)%len(hull)][0], hull[(i+1)%len(hull)][1], fill="red", width=2)

    def display_execution_time(self, execution_time):
        self.time_label.config(text=f"Execution Time: {execution_time:.6f} seconds")

    def clear_canvas(self):
        self.canvas.delete("all")
        self.points = []
        self.time_label.config(text="")

# Main application setup
root = tk.Tk()
root.title("Convex Hull Visualization")
app = ConvexHullApp(root)
root.mainloop()
