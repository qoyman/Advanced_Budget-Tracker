import heapq
from collections import deque, defaultdict
from datetime import datetime

# -----------------------------
# Task Class Definition
# -----------------------------
class Task:
    def __init__(self, name, priority, deadline, category):
        self.name = name
        self.priority = priority  # lower = higher priority
        self.deadline = deadline
        self.category = category
        self.status = 'incomplete'
        self.subtasks = []

    def __lt__(self, other):
        return self.priority < other.priority

    def __repr__(self):
        return f"Task: {self.name}, Priority: {self.priority}, Deadline: {self.deadline}, Status: {self.status}"

# -----------------------------
# Task Manager Definition
# -----------------------------
class TaskManager:
    def __init__(self):
        self.tasks = []  # Dynamic array (list)
        self.priority_queue = []  # Min-Heap
        self.schedule_queue = deque()  # Queue by deadline
        self.category_map = defaultdict(list)  # Hash Table by category
        self.undo_stack = []  # Undo Stack
        self.redo_stack = []  # Redo Stack
        self.bst_root = None  # BST for task hierarchy

    # -------------------------
    # Add Task
    # -------------------------
    def add_task(self, task):
        self.tasks.append(task)
        heapq.heappush(self.priority_queue, task)
        self.schedule_queue.append(task)
        self.category_map[task.category].append(task)
        self.undo_stack.append(('add', task))
        self.bst_root = self.insert_bst(self.bst_root, task)

    # -------------------------
    # Undo / Redo
    # -------------------------
    def undo(self):
        if not self.undo_stack:
            print("Nothing to undo.")
            return
        action, task = self.undo_stack.pop()
        if action == 'add':
            self.tasks.remove(task)
            self.priority_queue.remove(task)
            heapq.heapify(self.priority_queue)
            self.schedule_queue.remove(task)
            self.category_map[task.category].remove(task)
            self.bst_root = self.delete_bst(self.bst_root, task.deadline)
            self.redo_stack.append(('add', task))
            print(f"Undo: Removed task '{task.name}'")
        elif action == 'remove':
            self.add_task(task)
            print(f"Undo: Re-added task '{task.name}'")

    def redo(self):
        if not self.redo_stack:
            print("Nothing to redo.")
            return
        action, task = self.redo_stack.pop()
        if action == 'add':
            self.add_task(task)
            print(f"Redo: Re-added task '{task.name}'")

    # -------------------------
    # View Tasks
    # -------------------------
    def view_all_tasks(self):
        for task in self.tasks:
            print(task)

    def view_tasks_by_category(self, category):
        for task in self.category_map[category]:
            print(task)

    def view_priority_tasks(self):
        sorted_pq = sorted(self.priority_queue)
        for task in sorted_pq:
            print(task)

    def view_schedule(self):
        sorted_schedule = sorted(self.schedule_queue, key=lambda t: t.deadline)
        for task in sorted_schedule:
            print(task)

    # -------------------------
    # BST for Hierarchy
    # -------------------------
    