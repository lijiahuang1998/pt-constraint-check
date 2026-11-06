"""The deterministic verifier: input and output checks for every tool call, and the verdict on the task."""

from contract import Task, Tool

from . import task, tools


def verify_input(tool, value):
    return tools.INPUT_CHECKS[Tool(tool)](value)


def verify_output(tool, input_value, output_value, workspace):
    return tools.OUTPUT_CHECKS[Tool(tool)](input_value, output_value, workspace)


def verify_task(name, arguments, output, reference, workspace):
    return VERDICTS[Task(name)](arguments, output, reference, workspace)


VERDICTS = {Task.CHECK_CONSTRAINTS: task.verify_task}
