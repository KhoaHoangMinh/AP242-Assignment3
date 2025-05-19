from StaticError import *
from Symbol import *
from functools import *

def check_identifier(cmd):
    tokens = cmd.split()
    if not tokens:
        raise InvalidInstruction(cmd)

    code = tokens[0]
    valid_codes = ["INSERT", "ASSIGN", "BEGIN", "END", "LOOKUP", "PRINT", "RPRINT"]

    if code not in valid_codes:
        raise InvalidInstruction(cmd)

    if code in ["BEGIN", "END", "PRINT", "RPRINT"] and len(tokens) != 1:
        raise InvalidInstruction(cmd)

    if code == "LOOKUP" and len(tokens) != 2:
        raise InvalidInstruction(cmd)

    if code in ["INSERT", "ASSIGN"] and len(tokens) != 3:
        raise InvalidInstruction(cmd)

    # Ensure no extra spaces or invalid delimiters
    if "  " in cmd or cmd.strip() != cmd:
        raise InvalidInstruction(cmd)

    if code == "ASSIGN":
        identifier, value = tokens[1], tokens[2]

        # Validate identifier name (must follow rules in 3.5.1)
        if not identifier.isidentifier() or not identifier[0].islower():
            raise InvalidInstruction(cmd)

        # Validate value
        if not (value.isdigit() or  # Number constant
                (value.startswith("'") and value.endswith("'") and  # String constant
                 all(c.isalnum() or c.isspace() for c in value[1:-1])) or
                (value.isidentifier() and value[0].islower())):  # Valid identifier
            raise InvalidInstruction(cmd)

    if code == "INSERT":
        identifier, var_type = tokens[1], tokens[2]

        # Validate identifier name
        if not identifier.isidentifier() or not identifier[0].islower():
            raise InvalidInstruction(cmd)

        # Validate type (must be either 'number' or 'string')
        if var_type not in ["number", "string"]:
            raise InvalidInstruction(cmd)

    if code == "LOOKUP":
        identifier = tokens[1]

        # Validate identifier name
        if not identifier.isidentifier() or not identifier[0].islower():
            raise InvalidInstruction(cmd)

def helper(commands, cmd_list, result, lst):
    if not commands:
        # print("symtbl: " + ", ".join([f"({var}, {var_type})" for var, var_type in lst]))
        if len(lst) > 1:
            raise UnclosedBlock(len(lst) - 1)
        return result
    head, *tail = commands
    check_identifier(head)
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
            # value is an identifier, check its existence and type
            value_type = next((item[1] for scope in reversed(lst) for item in scope if item[0] == value), None)
            if value_type is None:
                raise Undeclared(head)
            if value_type != var_type:
                raise TypeMismatch(head)

        return helper(tail, cmd_list, result + ["success"], lst)

    elif tokens[0] == cmd_list[2]:  # BEGIN
        # print("BEGIN")
        return helper(tail, cmd_list, result, lst + [[]])

    elif tokens[0] == cmd_list[3]: # END
        # print("END")
        if len(lst) == 1:
            raise UnknownBlock()
        return helper(tail, cmd_list, result, lst[:-1])

    elif tokens[0] == cmd_list[4]:  # LOOKUP
        # print("LOOKUP")
        # helper(tail, cmd_list, result, lst)
        var = tokens[1]

        level = next(
            (len(lst) - 1 - idx for idx, scope in enumerate(reversed(lst)) if var in [item[0] for item in scope]),
            None
        )

        if level is None:
            raise Undeclared(head)

        return helper(tail, cmd_list, result + [str(level)], lst)

    elif tokens[0] == cmd_list[5]:  # PRINT
        # print("PRINT")
        # helper(tail, cmd_list, result, lst)

        # Add the formatted string to the result
        return helper(tail, cmd_list, result + [" ".join(
            [f"{var}//{level}" for var, level in reduce(
            lambda acc, scope_level: [
                                         (var, scope_level[1]) for var, _ in scope_level[0] if
                                         var not in [v[0] for v in acc]
                                     ] + acc,
            zip(reversed(lst), range(len(lst) - 1, -1, -1)),  # Traverse from innermost to outermost
            []
        )]
        )], lst)

    elif tokens[0] == cmd_list[6]:
        # print("RPRINT")
        # helper(tail, cmd_list, result, lst)

        # Format the identifiers and their levels in reverse order

        # Add the formatted string to the result
        return helper(tail, cmd_list, result + [" ".join(
            [f"{var}//{level}" for var, level in reversed(reduce(
            lambda acc, scope_level: [
                                         (var, scope_level[1]) for var, _ in scope_level[0] if
                                         var not in [v[0] for v in acc]
                                     ] + acc,
            zip(reversed(lst), range(len(lst) - 1, -1, -1)),  # Traverse from innermost to outermost
            []
        )
            )]
        )], lst)

    else:
        raise InvalidInstruction(head)


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
