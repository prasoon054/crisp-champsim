# CRISP Simulator Project
## _Critical Slice Prefetcher_

## Setup Steps

### Angr Setup
```sh
python -m venv angr-env
source angr-env/bin/activate
pip install -r requirements.txt
```

### Perf Setup
- Temporarily set perf_event_paranoid to 1
```sudo sysctl kernel.perf_event_paranoid=1```
- Set /proc/sys/kernel/kptr_restrict to 0, allowing kernel addresses to be shown
```sudo sysctl kernel.kptr_restrict=0```

### Intel vtune Setup
- [Install vtune](https://www.intel.com/content/www/us/en/docs/vtune-profiler/installation-guide/2023-1/package-managers.html)
- Temporarily set the ptrace scope to allow profiling
```sudo sysctl -w kernel.yama.ptrace_scope=0```
- Build missing sampling drivers (SEP/PAX) for precise events like uncore/memory bandwidth
```cd /opt/intel/oneapi/vtune/latest/sepdk/src```
```sudo ./build-driver -ni```
- Install the drivers
```sudo ./insmod-sep -r -g <user_group>```
- Check if drivers are installed
```sudo ./insmod-sep -q```
- Enable the debug repository and install
```sh
sudo apt install ubuntu-dbgsym-keyring
echo "Types: deb
URIs: http://ddebs.ubuntu.com/
Suites: $(lsb_release -cs) $(lsb_release -cs)-updates $(lsb_release -cs)-proposed 
Components: main restricted universe multiverse
Signed-by: /usr/share/keyrings/ubuntu-dbgsym-keyring.gpg" | sudo tee /etc/apt/sources.list.d/ddebs.sources
sudo apt update
sudo apt install linux-image-$(uname -r)-dbgsym
```
- Check if vtune has been setup successfully
```/opt/intel/oneapi/vtune/latest/bin64/vtune-self-checker.sh```
- Activate vtune
```source /opt/intel/oneapi/setvars.sh```

## Running Various Tools

### Running perf
```sh
sudo perf mem record -t load -- ./reverseLinkedList
```

### Running vtune vtune-profiler
```./pipeline.sh```  
This will generate the raw ```loads.csv```

## Steps
- Start angr venv ```source angr-env/bin/activate```

