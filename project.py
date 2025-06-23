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
    class BSTNode:
        def __init__(self, task):
            self.task = task
            self.left = None
            self.right = None

    def insert_bst(self, root, task):
        if root is None:
            return self.BSTNode(task)
        if task.deadline < root.task.deadline:
            root.left = self.insert_bst(root.left, task)
        else:
            root.right = self.insert_bst(root.right, task)
        return root

    def delete_bst(self, root, deadline):
        if root is None:
            return None
        if deadline < root.task.deadline:
            root.left = self.delete_bst(root.left, deadline)
        elif deadline > root.task.deadline:
            root.right = self.delete_bst(root.right, deadline)
        else:
            if not root.left:
                return root.right
            if not root.right:
                return root.left
            min_larger_node = self.get_min(root.right)
            root.task = min_larger_node.task
            root.right = self.delete_bst(root.right, min_larger_node.task.deadline)
        return root

    def get_min(self, root):
        while root.left is not None:
            root = root.left
        return root

    def print_bst(self, root):
        if root:
            self.print_bst(root.left)
            print(root.task)
            self.print_bst(root.right)

    # -------------------------
    # Recursive Subtasks
    # -------------------------
    def add_subtask(self, parent_task, subtask):
        parent_task.subtasks.append(subtask)

    def print_subtasks(self, task):
        print(f"Subtasks of {task.name}:")
        self._print_subtasks_recursive(task.subtasks)

    def _print_subtasks_recursive(self, subtasks):
        for sub in subtasks:
            print(sub)
            self._print_subtasks_recursive(sub.subtasks)

    # -------------------------
    # Merge Sort Tasks
    # -------------------------
    def merge_sort_tasks(self, tasks, key):
        if len(tasks) > 1:
            mid = len(tasks) // 2
            L = tasks[:mid]
            R = tasks[mid:]

            self.merge_sort_tasks(L, key)
            self.merge_sort_tasks(R, key)

            i = j = k = 0

            while i < len(L) and j < len(R):
                if getattr(L[i], key) < getattr(R[j], key):
                    tasks[k] = L[i]
                    i += 1
                else:
                    tasks[k] = R[j]
                    j += 1
                k += 1

            while i < len(L):
                tasks[k] = L[i]
                i += 1
                k += 1

            while j < len(R):
                tasks[k] = R[j]
                j += 1
                k += 1

    def view_sorted_tasks(self, key):
        sorted_tasks = self.tasks.copy()
        self.merge_sort_tasks(sorted_tasks, key)
        for task in sorted_tasks:
            print(task)

# -----------------------------
# Run Example
# -----------------------------
if __name__ == "__main__":
    tm = TaskManager()

    while True:
        print("\n--- Task Manager ---")
        print("1. Add Task")
        print("2. View ALL Tasks")
        print("3. View Tasks by Category")
        print("4. View Priority Tasks")
        print("5. View Sorted Tasks (by Deadline)")
        print("6. View Task Schedule")
        print("7. Undo Last Action")
        print("8. Redo Last Action")
        print("9. Exit")

        choice = input("Enter your choice (1–9): ")

        if choice == '1':
            name = input("Enter task name: ")
            priority = int(input("Enter priority (lower is higher priority): "))
            deadline = int(input("Enter deadline (as integer): "))
            category = input("Enter category: ")
            task = Task(name, priority, deadline, category)
            tm.add_task(task)
            print(f"Task '{name}' added successfully!")
        elif choice == '2':
            tm.view_all_tasks()
        elif choice == '3':
            cat = input("Enter category to filter: ")
            tm.view_tasks_by_category(cat)
        elif choice == '4':
            tm.view_priority_tasks()
        elif choice == '5':
            tm.view_sorted_tasks('deadline')
        elif choice == '6':
            tm.view_schedule()
        elif choice == '7':
            tm.undo()
        elif choice == '8':
            tm.redo()
        elif choice == '9':
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")