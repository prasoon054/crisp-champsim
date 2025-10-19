# Setup system
sudo sysctl kernel.perf_event_paranoid=1
sudo sysctl kernel.kptr_restrict=0

# if reverseLinkedList absent compile it
if [ ! -f ./reverseLinkedList ]; then
    g++ -o reverseLinkedList reverseLinkedList.cpp -O2
fi

# Run perf for mem load profiling
sudo perf record -t load ./reverseLinkedList
