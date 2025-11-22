#!/bin/bash
# Rebuild ChampSim with tuned CRISP parameters

cd /home/pratik/project_arch/crisp-champsim/ChampSim

echo "=== Rebuilding ChampSim with tuned CRISP ==="
./config.sh my_config.json
make clean
make -j8

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Build successful!"
    echo ""
    echo "Run tests with:"
    echo "  ./bin/champsim --warmup-instructions 15000000 --simulation-instructions 50000000 traces/LimitOrderBook_trace.champsimtrace.xz > limitorder_tuned.txt"
    echo "  ./bin/champsim --warmup-instructions 20000000 --simulation-instructions 50000000 traces/bfs-14.trace.gz > bfs_tuned.txt"
else
    echo "❌ Build failed!"
    exit 1
fi
