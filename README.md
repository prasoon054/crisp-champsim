# CRISP Simulator Project
## _Critical Slice Prefetcher_

## Setup Steps

### angr setup
```sh
python -m venv angr
source angr/bin/activate
pip install -r requirements.txt
```

### perf setup
```sh
# Allow temporary access of various hardwares

# lowering perf_event_paranoid to 1
sudo sysctl kernel.perf_event_paranoid=1

# set /proc/sys/kernel/kptr_restrict to 0, allowing kernel addresses to be shown
sudo sysctl kernel.kptr_restrict=0
```

## Running perf
```sh
sudo perf mem record -t load -- ./reverseLinkedList
```
