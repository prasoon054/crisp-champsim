# Setup system
sudo sysctl kernel.perf_event_paranoid=1
sudo sysctl kernel.kptr_restrict=0
sudo sysctl -w kernel.yama.ptrace_scope=0

binary="reverseLinkedList"

# if reverseLinkedList absent compile it
if [ ! -f ./reverseLinkedList ]; then
    g++ -g -o $binary reverseLinkedList.cpp -O3 -march=native
fi

# Run perf for mem load profiling
# sudo perf mem record -t load ./reverseLinkedList

# Run vtune profiling for memory access analysis
sudo /opt/intel/oneapi/vtune/latest/bin64/vtune -collect memory-access \
    -knob analyze-mem-objects=true \
    -knob sampling-interval=0.1ms \
    -result-dir ./memacc \
    -- taskset -c 0-5 ./$binary

# Generate report from vtune results
sudo /opt/intel/oneapi/vtune/latest/bin64/vtune -report hotspots -r ./memacc -group-by address -format csv -report-output loads.csv
sudo rm -rf ./memacc
