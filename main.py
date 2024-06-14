import psutil
import platform
import tabulate
import argparse


# Function to get OS information
def get_os_info():
    os_info = {}
    os_info["System"] = platform.system()
    os_info["OS Release"] = platform.release()
    os_info["OS Version"] = platform.version()
    return os_info


# Function to get CPU information
def get_cpu_info():
    cpu_info = {}
    cpu_info["Processor"] = platform.processor()
    cpu_info["Core count"] = psutil.cpu_count(logical=True)
    cpu_info["Physical cores"] = psutil.cpu_count(logical=False)
    cpu_info["CPU Usage (%)"] = psutil.cpu_percent(interval=1, percpu=False)
    return cpu_info


# Function to get RAM information
def get_ram_info():
    ram_info = {}
    svmem = psutil.virtual_memory()
    ram_info["Total memory (GB)"] = round(svmem.total / (1024**3), 2)
    ram_info["Available memory (GB)"] = round(svmem.available / (1024**3), 2)
    ram_info["Used memory (%)"] = svmem.percent
    return ram_info


# Function to get Disk information
def get_disk_info():
    disk_info = {}
    partitions = psutil.disk_partitions()
    for partition in partitions:
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
            disk_info[partition.device] = {
                "Total size (GB)": round(partition_usage.total / (1024**3), 2),
                "Used size (GB)": round(partition_usage.used / (1024**3), 2),
                "Free size (GB)": round(partition_usage.free / (1024**3), 2),
                "Usage (%)": partition_usage.percent,
            }
        except PermissionError:
            continue
    return disk_info


# Function to get GPU information
def get_gpu_info():
    try:
        import GPUtil

        gpu_info = GPUtil.getGPUs()
        return [
            {
                "GPU": gpu.name,
                "GPU Memory Total (GB)": gpu.memoryTotal,
                "GPU Memory Used (GB)": gpu.memoryUsed,
            }
            for gpu in gpu_info
        ]
    except ImportError:
        return []


# Function to get Network interface information
def get_network_info():
    network_info = {}
    for interface, addresses in psutil.net_if_addrs().items():
        network_info[interface] = [address.address for address in addresses]
    return network_info


# Display system information in tabulated tables
os_table = tabulate.tabulate(get_os_info().items(), tablefmt="grid")
cpu_table = tabulate.tabulate(get_cpu_info().items(), tablefmt="grid")
ram_table = tabulate.tabulate(get_ram_info().items(), tablefmt="grid")
disk_table = tabulate.tabulate(get_disk_info().items(), headers="keys", tablefmt="grid")
gpu_table = tabulate.tabulate(get_gpu_info(), headers="keys", tablefmt="grid")
network_table = tabulate.tabulate(
    get_network_info().items(),
    headers=["Network Interface", "IP Address"],
    tablefmt="grid",
)


# Add command line argument parser
parser = argparse.ArgumentParser(description="Display system information")
parser.add_argument("--all", action="store_true", help="Display All information")
parser.add_argument("--os", action="store_true", help="Display OS information")
parser.add_argument("--cpu", action="store_true", help="Display CPU information")
parser.add_argument("--ram", action="store_true", help="Display RAM information")
parser.add_argument("--disk", action="store_true", help="Display Disk information")
parser.add_argument("--gpu", action="store_true", help="Display GPU information")
parser.add_argument("--network", action="store_true", help="Display Network interface information")

args = parser.parse_args()

# Function to display system information based on user input
def display_system_info(args):
    if args.all:
        print("\nOperating System Information:")
        print(os_table)
        print("\nCPU Information:")
        print(cpu_table)
        print("\nRAM Information:")
        print(ram_table)
        print("\nDisk Information:")
        print(disk_table)
        print("\nGPU Information:")
        print(gpu_table if gpu_table else "GPUs not available")
        print("\nNetwork Interface Information:")
        print(network_table)
    if args.os:
        print("\nOperating System Information:")
        print(os_table)
    if args.cpu:
        print("\nCPU Information:")
        print(cpu_table)
    if args.ram:
        print("\nRAM Information:")
        print(ram_table)
    if args.disk:
        print("\nDisk Information:")
        print(disk_table)
    if args.gpu:
        print("\nGPU Information:")
        print(gpu_table if gpu_table else "GPUs not available")
    if args.network:
        print("\nNetwork Interface Information:")
        print(network_table)
    
        
        
if __name__ == "__main__":
    display_system_info(args)
