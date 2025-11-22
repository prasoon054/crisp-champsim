#!/bin/bash
bin/champsim --warmup-instructions 26000000 --simulation-instructions 25000000 traces/648.exchange2_s-1712B.champsimtrace.xz  > results/crisp/exchange_crisp
bin/champsim --warmup-instructions 26000000 --simulation-instructions 25000000 traces/bfs-14.trace.gz  > results/crisp/bfs_crisp
bin/champsim --warmup-instructions 26000000 --simulation-instructions 25000000 traces/LimitOrderBook_trace.champsim.xz > results/crisp/LimitOrderBook_crisp
bin/champsim --warmup-instructions 26000000 --simulation-instructions 25000000 traces/reverseLinkedList_trace.champsim.xz > results/crisp/reverseLL_crisp
bin/champsim --warmup-instructions 26000000 --simulation-instructions 25000000 traces/sssp-14.trace.gz > results/crisp/sssp_crisp
