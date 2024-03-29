"""
An example pipeline to demonstrate the use of file-system catalog.

Run this pipeline by:
    python examples/concepts/catalog_simple.py

"""

from runnable import Catalog, Pipeline, ShellTask


def main():
    # Make the data folder if it does not exist
    set_up = ShellTask(name="Setup", command="mkdir -p data")

    # create a catalog instruction to put a file into the catalog
    create_catalog = Catalog(put=["data/hello.txt"])
    # This task will create a file in the data folder and attaches the instruction
    # to put the file into the catalog.
    create = ShellTask(
        name="Create Content",
        command='echo "Hello from runnable" >> data/hello.txt',
        catalog=create_catalog,
        terminate_with_success=True,
    )

    pipeline = Pipeline(
        steps=[set_up, create],
        add_terminal_nodes=True,
    )

    # override the default configuration to use file-system catalog.
    pipeline.execute(configuration_file="examples/configs/fs-catalog.yaml")

    return pipeline


if __name__ == "__main__":
    main()
