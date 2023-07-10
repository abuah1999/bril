import json
import sys

TERMINATORS = 'jmp', 'br', 'ret'

def make_blocks(instrs):
    cur_block = []
    for instr in instrs:
        if 'op' in instr:
            cur_block.append(instr)
            # check if terminator
            if instr['op'] in TERMINATORS:
                yield cur_block
                cur_block = []
        else:
            # instr is a label
            if cur_block: yield cur_block
            cur_block = [instr]
    if cur_block: yield cur_block

def make_cfg(named_blocks):
    cfg = {}
    for i, (name, block) in enumerate(named_blocks):
        cfg[name] = []
        if block[-1].get('op') in ['jmp', 'br']:
            cfg[name] = block[-1]['labels']
        elif block[-1].get('op') == 'ret':
            continue
        elif i < len(named_blocks)-1:
            next_name, _ = named_blocks[i+1]
            cfg[name].append(next_name)
    return cfg

            

def name_blocks(blocks):
    out = []
    for block in blocks:
        if 'label' in block[0]:
            name = block[0]['label']
            block = block[1:]
        else:
            name = 'b{}'.format(len(out))
        out.append((name, block))

    return out


def mycfg():
    prog = json.load(sys.stdin)
    for func in prog['functions']:
        print('digraph {} {{'.format(func['name']))
        blocks = make_blocks(func['instrs'])

        named_blocks = name_blocks(blocks)
        for name, _ in named_blocks:
            print('  {};'.format(name))

        cfg = make_cfg(named_blocks)
        for node in cfg:
            for val in cfg[node]:
                print('  {} -> {};'.format(node, val))
        print('}')

if __name__ == "__main__":
    mycfg()
