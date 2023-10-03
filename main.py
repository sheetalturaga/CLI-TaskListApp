# using  the 'Command Line Interface creation kit"

#!/usr/bin/env python
import click


@click.group
def mycommands():
    pass


@click.command()
@click.option("--name", prompt="Enter you name ", help="The name of the user ")
def hello(name):
    click.echo(f"Hello, {name}!")


PRIORITIES = {
    "ninu": "Not Important - Not Urgent",
    "inu": "Important - Not Urgent",
    "iu": "Important - Urgent",
    "niu": "Not Important - Urgent",
}


@click.command()  # used to register the following function into a command
@click.argument("priority", type=click.Choice(PRIORITIES.keys()), default="a")
@click.argument("taskfile", type=click.Path(exists=False), required=0)
@click.option("-n", "--name", prompt="Enter the task name", help="The name of the task")
@click.option(
    "-d", "--description", prompt="Enter the description", help="Describe the task"
)
def add_task(name, description, priority, taskfile):
    file = taskfile if taskfile is not None else "mytasks.txt"

    # write to exisiting file else create a new one "append+"
    with open(file, "a+") as f:
        f.write(f"{name}: {description} [Priority: {PRIORITIES[priority]}]\n")


@click.command()
@click.argument("idx", type=int, required=1)
def delete_task(idx):
    with open("mytasks.txt", "r") as f:
        task_list = f.read().splitlines()
        task_list.pop(idx)

    with open("mytasks.txt", "w") as f:
        f.write("\n".join(task_list))
        f.write("\n")


@click.command()
@click.option("-p", "--priority", type=click.Choice(PRIORITIES.keys()))
@click.argument("taskfile", type=click.Path(exists=True), required=0)
def list_tasks(priority, taskfile):
    filename = taskfile if taskfile is not None else "mytasks.txt"

    with open(filename, "r") as f:
        tasklist = f.read().splitlines()

    if priority is None:
        for idx, task in enumerate(tasklist):
            print(f"({idx}) - {task}")
    else:
        for idx, task in enumerate(tasklist):
            if f"[Priority: {PRIORITIES[priority]}]" in task:
                print(f"({idx}) - {task}")


mycommands.add_command(hello)
mycommands.add_command(add_task)
mycommands.add_command(delete_task)
mycommands.add_command(list_tasks)

if __name__ == "__main__":
    mycommands()
