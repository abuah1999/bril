import json
import sys

def main():
    prog = json.load(sys.stdin)
    count = 0
    for func in prog["functions"]:
        br_cnt = sum([1 if instr.get('op') == 'br' else 0 for instr in func['instrs']])
        count += br_cnt
    print(count)

if __name__ == "__main__":
    main()
