import json
import sys

def glb_dce(instrs):
    used = []
    defined = {}
    for i, instr in enumerate(instrs):
        dest = instr.get("dest")
        if dest: defined[dest] = i
        args = instr.get("args")
        if args: used.extend(args)

    for var in defined:
        if var not in used: instrs.pop(defined[var])

def glb_dce_runner(instrs):
    while(True):
        temp = instrs.copy()
        glb_dce(instrs)
        if temp == instrs: break;



def main():
    prog = json.load(sys.stdin)
    for func in prog["functions"]:
       glb_dce_runner(func["instrs"])
        
    print(json.dumps(prog, indent=1))

if __name__ == "__main__":
    main()
