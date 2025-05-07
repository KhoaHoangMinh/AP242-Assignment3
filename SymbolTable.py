from StaticError import *
from Symbol import *
from functools import *

def check_identifier(identifier):
    if not identifier:
        return True

def helper(commands, cmd_list, result, lst):
    if not commands:
        # print("symtbl: " + ", ".join([f"({var}, {var_type})" for var, var_type in lst]))
        if len(lst) > 1:
            raise UnclosedBlock(len(lst) - 1)
        return result
    head, *tail = commands
    tokens = head.split()

    if tokens[0] == cmd_list[0]:    # INSERT
        # print("INSERT", tokens[1])
        var, var_type = tokens[1], tokens[2]
        if var in [item[0] for item in lst[-1]]:  # Check only the current scope
            raise Redeclared(head)
        updated_scope = lst[-1] + [(var, var_type)]
        return helper(tail, cmd_list, result + ["success"], lst[:-1] + [updated_scope])
        # lst[:-1]: lst with last element excluded
        # [[lst[-1] + [var, var_type]]: innermost block with new element inserted

    elif tokens[0] == cmd_list[1]:  # ASSIGN
        # print("ASSIGN")
        var, value = tokens[1], tokens[2]

        # Check if the variable exists in any scope
        var_type = next((item[1] for scope in reversed(lst) for item in scope if item[0] == var), None)
        if var_type is None:
            raise Undeclared(head)

        if value.isdigit():
            if var_type != "number":
                raise TypeMismatch(head)
        elif value.startswith("'") and value.endswith("'") and all(
                c.isalnum() or c.isspace() for c in value[1:-1]):  # String constant
            if var_type != "string":
                raise TypeMismatch(head)
        else:
            if next((item[1] for scope in reversed(lst) for item in scope if item[0] == value), None) is None:
                raise Undeclared(head)

        return helper(tail, cmd_list, result + ["success"], lst)

    elif tokens[0] == cmd_list[2]:  # BEGIN
        # print("BEGIN")
        return helper(tail, cmd_list, result, lst + [[]])

    elif tokens[0] == cmd_list[3]: # END
        # print("END")
        if len(lst) == 1:
            raise UnknownBlock()
        return helper(tail, cmd_list, result, lst[:-1])

    elif tokens[0] == cmd_list[4]:
        # print("LOOKUP")
        helper(tail, cmd_list, result, lst)

    elif tokens[0] == cmd_list[5]:
        # print("PRINT")
        helper(tail, cmd_list, result, lst)

    elif tokens[0] == cmd_list[6]:
        # print("RPRINT")
        helper(tail, cmd_list, result, lst)

    else:
        raise Exception("Unknown command")


def simulate(list_of_commands):
    """
    Executes a list of commands and processes them sequentially.

    Args:
        list_of_commands (list[str]): A list of commands to be executed.

    Returns:
        list[str]: A list of return messages corresponding to each command.
    """
    cmd_list = ["INSERT", "ASSIGN", "BEGIN", "END", "LOOKUP", "PRINT", "RPRINT"]
    return helper(list_of_commands, cmd_list, [], [[]])
    # helper(list_of_commands, cmd_list, [])
    # try:
    #     results = helper(list_of_commands, cmd_list, [])
    #     return results
    # except Redeclared as e:
    #     # print(e)  # This will print the error message like "Redeclared: INSERT x string"
    #     return str(e)
    # return ["success", "success"]
