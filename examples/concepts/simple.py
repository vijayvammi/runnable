"""
A simple pipeline with a simple function that just prints "Hello World!".

Run this pipeline by:
    python examples/concepts/simple.py
"""

from runnable import Pipeline, PythonTask


def simple_function():
    """
    A simple function that just prints "Hello World!".
    """
    print("Hello World!")


def main():
    simple_task = PythonTask(
        name="simple",
        function=simple_function,
        terminate_with_success=True,
    )

    pipeline = Pipeline(
        steps=[simple_task],
        add_terminal_nodes=True,
    )

    pipeline.execute()  # (1)

    return pipeline


if __name__ == "__main__":
    main()
