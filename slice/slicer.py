import angr
import sys

# --- Configuration ---
# 1. TODO: Accept binary path as a command-line argument
BINARY_PATH = sys.argv[1] if len(sys.argv) > 1 else None
# 2. TODO: Accept target load address as a command-line argument
TARGET_LOAD_ADDR = int(sys.argv[2], 16) if len(sys.argv) > 2 else None
TARGET_LOAD_ADDR = 0x401b60  # 2. TODO: Change this to your delinquent load address

def main():
    if not BINARY_PATH or not TARGET_LOAD_ADDR:
        print("Please set BINARY_PATH and TARGET_LOAD_ADDR in the script.")
        return

    print(f"[*] Loading binary: {BINARY_PATH}")
    # auto_load_libs=False makes it faster by not loading shared libraries
    proj = angr.Project(BINARY_PATH, auto_load_libs=False)

    # === Step 1: Build the Control Flow Graph (CFG) ===
    # We use CFGEmulated for accuracy. This is the key part:
    # - keep_state=True: Saves the state at the end of each block.
    # - state_add_options=angr.sim_options.refs: This is CRITICAL.
    #   It tells angr to record all register and memory accesses (refs),
    #   which is necessary for building an accurate Data Dependence Graph.
    print("[*] Building accurate Control Flow Graph (CFG). This may take time...")
    cfg = proj.analyses.CFGEmulated(
        keep_state=True,
        state_add_options=angr.sim_options.refs,
        context_sensitivity_level=2  # A good default
    )
    print("[*] CFG build complete.")

    # === Step 2: Build Dependence Graphs (CDG & DDG) ===
    # These graphs are built on top of the CFG.
    print("[*] Building Control Dependence Graph (CDG)...")
    cdg = proj.analyses.CDG(cfg)
    print("[*] Building Data Dependence Graph (DDG). This is the slow part...")
    ddg = proj.analyses.DDG(cfg)
    print("[*] Dependence graphs complete.")

    # === Step 3: Find the Slicing Target ===
    # We need to find the *exact statement* in the VEX IR (angr's intermediate
    # representation) that corresponds to our assembly instruction.
    
    # First, find the CFG node that contains our target address
    target_node = cfg.model.get_any_node(TARGET_LOAD_ADDR)
    if target_node is None:
        print(f"[!] Could not find CFG node for address {hex(TARGET_LOAD_ADDR)}")
        return

    # Now, find the *statement index* within that block.
    # We iterate through the VEX statements and find the 'IMark' (Instruction Mark)
    # that matches our address. The actual load (e.g., 'LDle') will follow it.
    # We slice from the *end* of the instruction, so we find the *last* VEX
    # statement that belongs to our assembly instruction.
    
    stmt_idx = -1
    block = proj.factory.block(target_node.addr, size=target_node.size)
    
    # Find the VEX statement index for our specific instruction
    for i, stmt in enumerate(block.vex.statements):
        if stmt.tag == 'Ist_IMark':
            if stmt.addr == TARGET_LOAD_ADDR:
                stmt_idx = i
                
    # If our load isn't the last instruction, find its end
    if stmt_idx != -1:
        # Find the *next* IMark to get the range of statements for our instruction
        for i in range(stmt_idx + 1, len(block.vex.statements)):
            if block.vex.statements[i].tag == 'Ist_IMark':
                stmt_idx = i - 1 # Target the statement just *before* the next instruction
                break
        else:
            # It's the last instruction, so target the end of the block
            stmt_idx = len(block.vex.statements) - 1

    if stmt_idx == -1:
        print(f"[!] Could not find statement for {hex(TARGET_LOAD_ADDR)} in block.")
        return

    print(f"[*] Found target: Node {hex(target_node.addr)}, Stmt Index {stmt_idx}")

    # === Step 4: Run the Backward Slice ===
    print("[*] Running backward slice...")
    # The 'targets' list is a tuple of (CFGNode, statement_index)
    bs = proj.analyses.BackwardSlice(
        cfg,
        cdg=cdg,
        ddg=ddg,
        targets=[(target_node, stmt_idx)]
    )
    print("[*] Slice complete.")

    # === Step 5: Print the Results ===
    # The result 'bs.chosen_statements' is a dict of:
    # { block_address: [list_of_critical_statement_indices] }
    
    # For a user-friendly view, we'll just print all assembly blocks
    # that contain *any* critical statements.
    
    print("\n" + "="*30)
    print("      CRITICAL SLICE BLOCKS")
    print("="*30)

    # Get all unique block addresses from the slice
    slice_block_addrs = sorted(bs.chosen_statements.keys())

    for addr in slice_block_addrs:
        print(f"\n--- Block at {hex(addr)} ---")
        # Lift the block again, this time to print its disassembly
        try:
            block = proj.factory.block(addr)
            block.capstone.pp()  # .pp() pretty-prints the Capstone disassembly
        except Exception as e:
            print(f"Could not disassemble block: {e}")

if __name__ == "__main__":
    main()
