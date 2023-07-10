import json
import sys
import mycfg
from collections import OrderedDict

def lvn(block):
    table = OrderedDict()
    var2num = {}
    new_block = []
    fresh_num = 0

    for i, instr in enumerate(block):
        # effect operations
        if ('dest' not in instr or
            instr['op'] == "call"):
            value = ()
        else:
            value = (instr['op'],)
            # constant literals
            if instr['op'] == "const":
                value += (instr['value'],)
            # value operations
            else:
                for arg in instr['args']:
                    #if arg not in var2num: continue
                    value += (var2num[arg],)

        if value in table:
            # The value has been computed before; reuse it.
            num, var = table[value]
            new_instr = {
                    'dest': instr['dest'],
                    'op': 'id',
                    'args': [var]
                    }
            new_block.append(new_instr)
        else:
            new_instr = instr.copy()
            if value != ():
                # A newly computed value
                num = len(table)

                dest = instr["dest"]
                defined = [inst_.get("dest") for inst_ in block]
                if dest in defined[i+1:]:
                    dest = 'x{}'.format(fresh_num)
                    fresh_num += 1
                    while dest in defined:
                        dest = 'x{}'.format(fresh_num)
                        fresh_num += 1
                    new_instr['dest'] = dest
                else:
                    dest = instr['dest']

                table[value] = (num, dest)
            if 'args' in instr:
                new_args = []
                for arg in instr["args"]:
                    new_args.append(list(table.values())[var2num[arg]])
                new_args = [var for (_,var) in new_args]
                new_instr["args"] = new_args
            new_block.append(new_instr)
        if 'dest' in instr: var2num[instr['dest']] = num
    #print(table)
    #print(json.dumps(var2num, indent=1))
    
    return new_block


def main():
    prog = json.load(sys.stdin)
    for func in prog["functions"]:
        new_instrs = []
        for block in mycfg.make_blocks(func["instrs"]):
            new_block = lvn(block)
            new_instrs.extend(new_block)
        func["instrs"] = new_instrs
    print(json.dumps(prog, indent=1))

if __name__ == "__main__":
    main()
