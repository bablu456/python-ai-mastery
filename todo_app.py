"""
Welcome to Python! 
Since you already know C and Java, you will find Python to be very expressive and concise.
This is a simple To-Do List Command Line Application.

It demonstrates:
1. Classes and Object-Oriented Programming in Python
2. Exception Handling
3. File I/O (Saving and loading data)
4. List comprehensions (A very "Pythonic" feature)
"""

import os # Importing modules is like #include in C or import in Java
import json # json is part of the standard library, used for saving our tasks

# In Python, we don't need to declare types, but we can use "Type Hints" for better readability.
# We define a class using the 'class' keyword. No curly braces {}, Python uses indentation!
class TodoList:
    # __init__ is the constructor in Python, similar to public TodoList() in Java.
    # 'self' is equivalent to 'this' in Java or C++. It must be the first parameter in instance methods.
    def __init__(self, filename="tasks.json"):
        self.filename = filename # Instance variables are created dynamically when assigned
        self.tasks = []          # This is a Python list, similar to ArrayList in Java
        self.load_tasks()        # Call a method to load existing tasks

    def load_tasks(self):
        """Loads tasks from a JSON file if it exists."""
        # This is a docstring, used for documenting methods/classes.
        
        # os.path.exists checks if the file exists on the disk
        if os.path.exists(self.filename):
            # 'with' statement is a context manager. It automatically closes the file after the block finishes,
            # somewhat similar to try-with-resources in Java, without needing explicit .close()
            try:
                with open(self.filename, 'r') as file:
                    self.tasks = json.load(file) 
            except json.JSONDecodeError:
                # If the file is empty or corrupted, we start with an empty list
                self.tasks = []

    def save_tasks(self):
        """Saves current tasks to the JSON file."""
        # 'w' mode opens the file for writing. It will be created if it doesn't exist.
        with open(self.filename, 'w') as file:
            json.dump(self.tasks, file, indent=4)

    def add_task(self, description):
        """Adds a new task to the list."""
        # Python dictionaries are like HashMaps in Java or structs in C, but dynamic.
        task = {
            "id": len(self.tasks) + 1,
            "description": description,
            "completed": False
        }
        # append() adds to the end of the list (like add() in Java ArrayList)
        self.tasks.append(task)
        self.save_tasks()
        print(f"Task '{description}' added successfully!") # This is an f-string, similar to String.format or printf

    def view_tasks(self):
        """Displays all tasks."""
        if not self.tasks:
            print("Your To-Do list is empty!")
            return

        print("\n--- Your To-Do List ---")
        # A simple for loop in Python iterates over elements directly, like a foreach loop in Java
        for task in self.tasks:
            # We use a ternary operator to set the status mark. 
            # Syntax: [value_if_true] if [condition] else [value_if_false]
            status = "[X]" if task["completed"] else "[ ]"
            print(f"{task['id']}. {status} {task['description']}")
        print("-----------------------\n")

    def mark_completed(self, task_id):
        """Marks a task as completed."""
        # Here we use a standard loop. Let's find the task.
        for task in self.tasks:
            if task["id"] == task_id:
                task["completed"] = True
                self.save_tasks()
                print(f"Task {task_id} marked as completed!")
                return
        print(f"Error: Task with ID {task_id} not found.")

    def delete_task(self, task_id):
        """Deletes a task from the list."""
        # List comprehension - a very Pythonic way to filter lists.
        # This creates a new list with all tasks EXCEPT the one we want to delete.
        original_length = len(self.tasks)
        self.tasks = [task for task in self.tasks if task["id"] != task_id]
        
        if len(self.tasks) < original_length:
            # Re-assign IDs to keep them sequential
            for index, task in enumerate(self.tasks):
                # enumerate gives us both the index and the item
                task["id"] = index + 1
            
            self.save_tasks()
            print(f"Task {task_id} deleted successfully!")
        else:
            print(f"Error: Task with ID {task_id} not found.")

# This block is like 'public static void main(String[] args)' in Java or 'int main()' in C.
# It ensures this code only runs if the script is executed directly (not imported as a module).
if __name__ == "__main__":
    app = TodoList() # Instantiating an object (no 'new' keyword in Python!)
    
    # A while True loop is typical for CLI apps (like while(1) in C)
    while True:
        print("\n--- To-Do List Menu ---")
        print("1. View tasks")
        print("2. Add a task")
        print("3. Mark task as completed")
        print("4. Delete a task")
        print("5. Exit")
        
        # input() reads a line from the console (returns a string)
        choice = input("\nEnter your choice (1-5): ")
        
        if choice == '1':
            app.view_tasks()
        elif choice == '2':
            # strip() removes leading/trailing whitespace (like trim() in Java)
            task_desc = input("Enter task description: ").strip()
            if task_desc:
                app.add_task(task_desc)
            else:
                print("Task description cannot be empty.")
        elif choice == '3':
            try:
                # We must cast the input string to an integer
                # If parsing fails, it throws a ValueError
                task_id = int(input("Enter task ID to mark as completed: "))
                app.mark_completed(task_id)
            except ValueError:
                print("Invalid input. Please enter a valid number.")
        elif choice == '4':
            try:
                task_id = int(input("Enter task ID to delete: "))
                app.delete_task(task_id)
            except ValueError:
                print("Invalid input. Please enter a valid number.")
        elif choice == '5':
            print("Goodbye!")
            break # Breaks out of the while loop
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")
