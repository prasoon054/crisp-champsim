#!/bin/bash
bin/champsim --warmup-instructions 26000000 --simulation-instructions 25000000 traces/648.exchange2_s-1712B.champsimtrace.xz  > results/exchange_base
bin/champsim --warmup-instructions 26000000 --simulation-instructions 25000000 traces/bfs-14.trace.gz  > results/bfs_base
bin/champsim --warmup-instructions 26000000 --simulation-instructions 25000000 traces/LimitOrderBook_trace.champsim.xz > results/LimitOrderBook_base
bin/champsim --warmup-instructions 26000000 --simulation-instructions 25000000 traces/reverseLinkedList_trace.champsim.xz > results/reverseLL_base
bin/champsim --warmup-instructions 26000000 --simulation-instructions 25000000 traces/sssp-14.trace.gz > results/sssp_base
