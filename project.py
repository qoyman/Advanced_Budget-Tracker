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
