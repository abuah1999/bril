import json
import sys
import mycfg

def glb_dce(instrs):
    used = []
    defined = {}
    instr_index = []
    for i, instr in enumerate(instrs):
        instr_index.append((i, instr))
        dest = instr.get("dest")
        if dest: defined[dest] = i
        args = instr.get("args")
        if args: used.extend(args)

    for var in defined:
        if var not in used: 
            instr_index = [(i, _) for (i, _) in instr_index if i != defined[var]]

    return [instr for (_, instr) in instr_index]

def glb_dce_runner(instrs):
    last_instrs = instrs
    while(True):
        new_instrs = glb_dce(last_instrs)
        if new_instrs == last_instrs: return new_instrs;
        last_instrs = new_instrs

def loc_dce(block):
    last_def = {}
    block_index = []
    #new_block = block.copy()
    for i, instr in enumerate(block):
        block_index.append((i, instr))
        if "args" in instr:
            for arg in instr["args"]:
                if arg in last_def: del last_def[arg]
        if "dest" in instr:
            if instr["dest"] in last_def: 
                block_index = [(i,_) for (i,_) in block_index if i != last_def[instr["dest"]]]
            last_def[instr["dest"]] = i
    new_block = [instr for (_,instr) in block_index]
    return new_block

def loc_dce_runner(block):
    last_block = block
    while(True):
        new_block = loc_dce(last_block)
        if new_block == last_block: return new_block;
        last_block = new_block

def main():
    prog = json.load(sys.stdin)
    for func in prog["functions"]:
       new_instrs_1 = glb_dce_runner(func["instrs"])
       func["instrs"] = new_instrs_1
       new_instrs_2 = []
       for block in mycfg.make_blocks(func["instrs"]):
           new_block = loc_dce_runner(block)
           new_instrs_2.extend(new_block)
       func["instrs"] = new_instrs_2

        
    print(json.dumps(prog, indent=1))

if __name__ == "__main__":
    main()
