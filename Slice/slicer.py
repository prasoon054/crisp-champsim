import angr
import sys
import lief

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 slicer.py <binary> <target_runtime_addr>")
        return

    BINARY_PATH = sys.argv[1]
    TARGET_RUNTIME_ADDR = int(sys.argv[2], 16)

    print(f"[*] Loading binary: {BINARY_PATH}")
    proj = angr.Project(BINARY_PATH, auto_load_libs=False)

    # === Detect PIE and compute static offset ===
    binary = lief.parse(BINARY_PATH)
    base_addr = 0

    if binary.is_pie:
        base_addr = proj.loader.main_object.mapped_base
        print(f"[*] Detected PIE binary. Base load address: {hex(base_addr)}")
    else:
        print("[*] Non-PIE binary detected (fixed base address).")

    TARGET_STATIC_ADDR = TARGET_RUNTIME_ADDR - base_addr
    print(f"[*] Runtime address: {hex(TARGET_RUNTIME_ADDR)} → Adjusted static address: {hex(TARGET_STATIC_ADDR)}")

    # === Step 1: Build CFG ===
    print("[*] Building Control Flow Graph (CFG)...")
    cfg = proj.analyses.CFGEmulated(
        keep_state=True,
        state_add_options=angr.sim_options.refs,
        context_sensitivity_level=2
    )
    print("[*] CFG build complete.")

    # === Step 2: Build Dependence Graphs ===
    print("[*] Building Control Dependence Graph (CDG)...")
    cdg = proj.analyses.CDG(cfg)
    print("[*] Building Data Dependence Graph (DDG)...")
    ddg = proj.analyses.DDG(cfg)
    print("[*] Dependence graphs complete.")

    # === Step 3: Find the target node and statement ===
    target_node = cfg.model.get_any_node(TARGET_STATIC_ADDR)
    if target_node is None:
        print(f"[!] Could not find CFG node for address {hex(TARGET_STATIC_ADDR)}")
        return

    stmt_idx = -1
    block = proj.factory.block(target_node.addr, size=target_node.size)
    for i, stmt in enumerate(block.vex.statements):
        if stmt.tag == 'Ist_IMark' and stmt.addr == TARGET_STATIC_ADDR:
            stmt_idx = i
            break

    if stmt_idx == -1:
        print(f"[!] Could not find statement for {hex(TARGET_STATIC_ADDR)} in block.")
        return

    print(f"[*] Found target node at {hex(target_node.addr)}, stmt index {stmt_idx}")

    # === Step 4: Backward Slice ===
    print("[*] Running backward slice...")
    bs = proj.analyses.BackwardSlice(
        cfg,
        cdg=cdg,
        ddg=ddg,
        targets=[(target_node, stmt_idx)]
    )
    print("[*] Slice complete.")

    # === Step 5: Display slice ===
    print("\n" + "=" * 30)
    print("      CRITICAL SLICE BLOCKS")
    print("=" * 30)

    for addr in sorted(bs.chosen_statements.keys()):
        print(f"\n--- Block at {hex(addr)} ---")
        try:
            proj.factory.block(addr).capstone.pp()
        except Exception as e:
            print(f"Could not disassemble block: {e}")

if __name__ == "__main__":
    main()
