import sys, trace


def _log(a, path):
    if path:
        with open(path, 'a') as file:
            file.write('{0}\n'.format(a))
    else:
        print(a)

def trace_log(f, path):
    code = f.__code__
    filename = code.co_filename
    with open(filename, 'r') as file:
        source = file.read().split('\n')
    def trace_lines(frame, event, arg):
        co = frame.f_code
        func_name = co.co_name
        if func_name != f.__name__:
            return
        elif event == 'call':
            return trace_lines
        elif event != 'line':
            return
        co = frame.f_code
        func_name = co.co_name
        func_line_no = frame.f_lineno
        _log('def %s:%d %s' % (f.__name__, func_line_no, source[func_line_no - 1]), path)
        return trace_lines
    return trace_lines

def log(path=None):
    def wrapper(f):
        def decorator(*args, **kwargs):
            sys.settrace(trace_log(f, path))
            f(*args, **kwargs)
            sys.settrace(None)
        return decorator
    return wrapper

# def log(path=None):
#     def wrapper(f):
#         code = f.__code__
#         filename = code.co_filename
#         with open(filename, 'r') as file:
#             source = file.read().split('\n')
        
#         instructions = list(dis.get_instructions(f))
#         new_names = code.co_names + ('print',)
#         print_index = len(new_names) - 1
#         new_consts = list(code.co_consts)
#         new_code = []
#         offset = 0
#         new_offset = 0
        
#         for h, i in enumerate(instructions):
#             change = True
        
#             if i.starts_line:
#                 a = 'def %s:%d %s' % (f.__name__, i.starts_line, source[i.starts_line - 1])
#                 new_consts.append(a)
#                 new_code.append(dis.Instruction('LOAD_GLOBAL', 116, print_index, 0, 'print', offset, i.starts_line, i.is_jump_target))
#                 offset += 3
#                 new_code.append(dis.Instruction('LOAD_CONST', 100, len(new_consts) - 1, 0, a, offset, None, False))
#                 offset += 3
#                 new_code.append(dis.Instruction('CALL_FUNCTION', 131, 1, 0, '', offset, None, False))
#                 offset += 3
#                 new_code.append(dis.Instruction('POP_TOP', 1, 0, 0, '', offset, None, False))
#                 offset += 1
#                 new_offset += 10
#                 change = False
            
#             new_code.append(dis.Instruction(i.opname, i.opcode, i.arg, i.argval, i.argrepr, i.offset + new_offset, i.starts_line if change else None, i.is_jump_target if change else False))
#             if h < len(instructions) - 1:
#                 offset = instructions[h + 1].offset + new_offset
#         print('\n'.join(map(str, new_code)))
#         def decorator(*args, **kwargs):
#             print(0)
#         return decorator
#     print(path)
#     return wrapper

# @log()
# def z(s):
#     e = 2
#     s = 4
#     y(s)
#     1/0

# def y(s):
#     print(s)

# z(2)

