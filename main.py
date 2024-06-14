import psutil
import platform
import tabulate
import argparse

from rich.console import Console
from rich.table import Table
console = Console()


# Function to get OS information
def get_os_info():    
    table = Table(title="Operating System Information")
    table.add_column("System", justify="center", style="cyan", no_wrap=True)    
    table.add_column("OS Release", justify="center", style="cyan")
    table.add_column("OS Version", justify="center", style="magenta")
    
    table.add_row(
        platform.system(),
        str(platform.release()), 
        str(platform.version()), 
    )
    
    return table


# Function to get CPU information
def get_cpu_info():        
    table = Table(title="CPU Information")
    table.add_column("Processor", justify="start", style="cyan", no_wrap=True)    
    table.add_column("Core count", justify="start", style="cyan")
    table.add_column("Physical cores", justify="start", style="magenta")
    table.add_column("CPU Usage (%)", justify="start", style="green")
    
    table.add_row(
        platform.processor(),
        str(psutil.cpu_count(logical=True)), 
        str(psutil.cpu_count(logical=False)), 
        str(psutil.cpu_percent(interval=1, percpu=False))
    )
    
    return table


# Function to get RAM information
def get_ram_info():
    svmem = psutil.virtual_memory()    
    
    table = Table(title="CPU Information")
    table.add_column("Total memory (GB)", justify="center", style="cyan", no_wrap=True)    
    table.add_column("Available memory (GB)", justify="center", style="cyan")
    table.add_column("Used memory (%)", justify="center", style="magenta")
    
    table.add_row(
        str(round(svmem.total / (1024**3), 2)), 
        str(round(svmem.available / (1024**3), 2)), 
        str(svmem.percent)
    )
    
    return table


# Function to get Disk information
def get_disk_info():
    partitions = psutil.disk_partitions()
    
    table = Table(title="Disk Information")
    table.add_column("Device", justify="start", style="cyan", no_wrap=True)    
    table.add_column("Total size (GB)", justify="start", style="cyan")
    table.add_column("Used size (GB)", justify="start", style="magenta")
    table.add_column("Free size (GB)", justify="start", style="green")
    table.add_column("Usage (%)", justify="start")

    for partition in partitions:
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
            device = partition.device
            total = round(partition_usage.total / (1024**3), 2)
            used = round(partition_usage.used / (1024**3), 2)
            free = round(partition_usage.free / (1024**3), 2)
            usage_percent = partition_usage.percent
            
            if usage_percent <= 25:
                usage_str = f"[bold green]{usage_percent}%[/bold green]"
            elif usage_percent <= 50:
                usage_str = f"[bold blue]{usage_percent}%[/bold blue]"
            elif usage_percent <= 75:
                usage_str = f"[bold #f5a629]{usage_percent}%[/]"
            else:
                usage_str = f"[bold red]{usage_percent}%[/bold red]"
                
            
            table.add_row(
                device,
                str(total), 
                str(used), 
                str(free),
                usage_str
            )
        except PermissionError:
            continue
        
    return table


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
os_table = get_os_info()
cpu_table = get_cpu_info()
ram_table = get_ram_info()
disk_table = get_disk_info()
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
        print("\n")
        console.print(os_table)
    if args.cpu:
        print("\n")
        console.print(cpu_table)
    if args.ram:
        print("\n")
        console.print(ram_table)
    if args.disk:
        print("\n")
        console.print(disk_table)
    if args.gpu:
        print("\nGPU Information:")
        print(gpu_table if gpu_table else "GPUs not available")
    if args.network:
        print("\nNetwork Interface Information:")
        print(network_table)
    
        
        
if __name__ == "__main__":
    display_system_info(args)
