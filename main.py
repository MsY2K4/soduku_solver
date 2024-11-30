import time
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, Frame
from tkinter.ttk import Style

# Node class
class Node:
    def __init__(self, state, parent=None, action=None):
        self.state = state
        self.parent = parent
        self.action = action
        self.children = []

# Problem class
class Problem:
    def __init__(self, initial_state):
        self.initial_state = initial_state

    def goal_test(self, state):
        return all(0 not in row for row in state) and self.is_valid(state)

    def is_valid(self, state):
        for i in range(9):
            if not self.valid_group([state[i][j] for j in range(9)]) or \
               not self.valid_group([state[j][i] for j in range(9)]):
                return False
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                subgrid = [state[x][y] for x in range(i, i + 3) for y in range(j, j + 3)]
                if not self.valid_group(subgrid):
                    return False
        return True

    def valid_group(self, group):
        nums = [n for n in group if n != 0]
        return len(nums) == len(set(nums))

# SudokuSolver class
class SudokuSolver:
    def __init__(self, problem):
        self.problem = problem

    def dfs(self, state):
        if self.problem.goal_test(state):
            return state

        for x, y in self.find_empty(state):
            for num in range(1, 10):
                state[x][y] = num
                if self.problem.is_valid(state):
                    solution = self.dfs(state)
                    if solution:
                        return solution
                state[x][y] = 0
        return None

    def bfs(self):
        from collections import deque

        initial_state = self.problem.initial_state
        queue = deque([initial_state])

        while queue:
            current_state = queue.popleft()
            if self.problem.goal_test(current_state):
                return current_state

            for x, y in self.find_empty(current_state):
                for num in range(1, 10):
                    new_state = [row[:] for row in current_state]
                    new_state[x][y] = num
                    if self.problem.is_valid(new_state):
                        queue.append(new_state)

        return None

    def dls(self, state, limit):
        return self._dls_recursive(state, limit)

    def _dls_recursive(self, state, limit):
        if limit == 0:
            return None
        if self.problem.goal_test(state):
            return state

        for x, y in self.find_empty(state):
            for num in range(1, 10):
                state[x][y] = num
                if self.problem.is_valid(state):
                    solution = self._dls_recursive(state, limit - 1)
                    if solution:
                        return solution
                state[x][y] = 0
        return None

    def find_empty(self, state):
        for i in range(9):
            for j in range(9):
                if state[i][j] == 0:
                    return [(i, j)]
        return []

# SudokuApp class
class SudokuApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Sudoku Solver")
        self.master.configure(bg="#F4F4F9")
        self.grid = [[3, 0, 9, 4, 0, 7, 5, 0, 8],
                     [7, 0, 6, 0, 0, 5, 0, 0, 0],
                     [4, 0, 2, 6, 0, 3, 1, 9, 0],
                     [9, 7, 4, 1, 3, 0, 0, 0, 0],
                     [2, 0, 0, 0, 0, 0, 7, 0, 0],
                     [8, 3, 0, 7, 6, 0, 0, 1, 9],
                     [0, 0, 0, 0, 7, 0, 0, 2, 6],
                     [0, 0, 7, 0, 0, 0, 0, 5, 0],
                     [1, 0, 0, 0, 0, 6, 4, 7, 3]]
        self.entries = [[None for _ in range(9)] for _ in range(9)]
        self.create_widgets()

    def create_widgets(self):
        # Frame for the grid
        frame = Frame(self.master, bg="#F4F4F9")
        frame.grid(row=0, column=0, padx=20, pady=20)

        for i in range(9):
            for j in range(9):
                bg_color = "#D6EAF8" if (i // 3 + j // 3) % 2 == 0 else "#FDEBD0"
                entry = Entry(frame, width=2, justify='center', bg=bg_color, font=("Arial", 14))
                entry.grid(row=i, column=j, padx=2, pady=2)
                if self.grid[i][j] != 0:
                    entry.insert(0, self.grid[i][j])
                    entry.config(state="disabled")  # Disable preset values
                self.entries[i][j] = entry

        # Buttons for algorithms
        button_frame = Frame(self.master, bg="#F4F4F9")
        button_frame.grid(row=1, column=0, pady=10)

        dfs_button = Button(button_frame, text="Solve with DFS", command=self.solve_dfs, bg="#85C1E9", font=("Arial", 12))
        dfs_button.grid(row=0, column=0, padx=10)

        bfs_button = Button(button_frame, text="Solve with BFS", command=self.solve_bfs, bg="#85C1E9", font=("Arial", 12))
        bfs_button.grid(row=0, column=1, padx=10)

        dls_button = Button(button_frame, text="Solve with DLS", command=self.solve_dls, bg="#85C1E9", font=("Arial", 12))
        dls_button.grid(row=0, column=2, padx=10)

        clear_button = Button(button_frame, text="Clear Grid", command=self.clear_grid, bg="#E74C3C", font=("Arial", 12), fg="white")
        clear_button.grid(row=0, column=3, padx=10)

    def solve_dfs(self):
        self.solve("DFS")

    def solve_bfs(self):
        self.solve("BFS")

    def solve_dls(self):
        self.solve("DLS")

    def solve(self, algorithm):
        try:
            puzzle = [[int(self.entries[i][j].get() or 0) for j in range(9)] for i in range(9)]
            problem = Problem(puzzle)
            solver = SudokuSolver(problem)
            start_time = time.time()

            if algorithm == "DFS":
                solution = solver.dfs(puzzle)
            elif algorithm == "BFS":
                solution = solver.bfs()
            elif algorithm == "DLS":
                solution = solver.dls(puzzle, limit=50)
            else:
                solution = None

            elapsed_time = time.time() - start_time
            if solution:
                for i in range(9):
                    for j in range(9):
                        if self.grid[i][j] == 0:  # Only update non-preset values
                            self.entries[i][j].delete(0, "end")
                            self.entries[i][j].insert(0, solution[i][j])
                messagebox.showinfo("Success", f"Sudoku solved in {elapsed_time:.2f} seconds!")
            else:
                messagebox.showwarning("Failure", "No solution found.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def clear_grid(self):
        """Clear all values that were not preset."""
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:  # Only clear non-preset values
                    self.entries[i][j].delete(0, "end")
# Run the application
if __name__ == "__main__":
    root = Tk()
    app = SudokuApp(root)
    root.mainloop()
