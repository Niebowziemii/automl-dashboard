# Contribution guide
This guide provides rules and examples for writing clean and consistent Python code. Following these guidelines 
will help ensure code readability, maintainability, and collaboration within a development team.

## Code Organization
Well-organized code is easier to navigate and understand. Consider the following guidelines:

* Separate different concerns into modules, classes, and functions.
* Keep each function or method focused on a single task.
* Group related functions or methods within classes or modules.
* Use meaningful file and directory names to reflect the purpose of the code.

## Branching Strategy
Adopting a consistent branching strategy promotes collaboration and code isolation. Follow the structure 
```feature/{task_id}-{task_name}``` for each new task branch. For example:

```feature/123-add-user-authentication```

This structure allows for easy identification of the task and ensures a clear separation of code changes.
Furthermore there are several important things to remeber:

* main branch should be reserved for a production-ready version of the code
* develop branch should contain latest stable version
* each merge request should be performed with squash and deletion of the source branch

## Docstring Format
Writing clear and concise docstrings helps others understand your code's purpose and usage. Follow the Google Style 
Python Docstrings format, which includes sections for the summary, parameters, return values, and more. 
Here's an example:
```py 
def calculate_sum(a, b):
    """Calculate the sum of two numbers.

    Args:
        a (int): The first number.
        b (int): The second number.

    Returns:
        int: The sum of the two numbers.
    """
    return a + b
```

Using a consistent docstring format improves code documentation and helps generate accurate API documentation automatically.
