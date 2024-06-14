import psutil
import platform
import argparse
import GPUtil
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
    
    usage_percent = psutil.cpu_percent(interval=1, percpu=False)
    if usage_percent <= 25:
        usage_str = f"[bold green]{usage_percent}%[/bold green]"
    elif usage_percent <= 50:
        usage_str = f"[bold blue]{usage_percent}%[/bold blue]"
    elif usage_percent <= 75:
        usage_str = f"[bold yellow]{usage_percent}%[/bold yellow]"
    else:
        usage_str = f"[bold red]{usage_percent}%[/bold red]"
        
    table.add_row(
        platform.processor(),
        str(psutil.cpu_count(logical=True)),
        str(psutil.cpu_count(logical=False)),
        str(usage_str)
    )
    
    return table

# Function to get RAM information
def get_ram_info():
    svmem = psutil.virtual_memory()
    
    table = Table(title="RAM Information")
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
                usage_str = f"[bold yellow]{usage_percent}%[/bold yellow]"
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
    gpu_info = GPUtil.getGPUs()
    table = Table(title="GPU Information")
    table.add_column("GPU", justify="start", style="cyan", no_wrap=True)
    table.add_column("Memory Total (GB)", justify="start", style="cyan")
    table.add_column("Memory Used (GB)", justify="start", style="magenta")
        
    for gpu in gpu_info:
        usage_percent = gpu.memoryUsed
        if usage_percent <= 25:
            usage_str = f"[bold green]{usage_percent}%[/bold green]"
        elif usage_percent <= 50:
            usage_str = f"[bold blue]{usage_percent}%[/bold blue]"
        elif usage_percent <= 75:
            usage_str = f"[bold yellow]{usage_percent}%[/bold yellow]"
        else:
            usage_str = f"[bold red]{usage_percent}%[/bold red]"
            
        table.add_row(
            gpu.name,
            str(gpu.memoryTotal),
            str(usage_str)
        )
    
    return table

# Function to get Network interface information
def get_network_info():
    network_info = {}
    
    table = Table(title="Network Interface Information")
    table.add_column("Interface", justify="start", style="cyan", no_wrap=True)
    table.add_column("IP Address", justify="start", style="cyan")
    
    for interface, addresses in psutil.net_if_addrs().items():
        ip_address = ", ".join([address.address for address in addresses])
        network_info[interface] = ip_address
        table.add_row(interface, ip_address)
        
    return table

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
        console.print("\n", get_os_info())
        console.print("\n", get_cpu_info())
        console.print("\n", get_ram_info())
        console.print("\n", get_disk_info())
        console.print("\n", get_gpu_info())
        console.print("\n", get_network_info())
        
    if args.os:
        console.print("\n", get_os_info())
    if args.cpu:
        console.print("\n", get_cpu_info())
    if args.ram:
        console.print("\n", get_ram_info())
    if args.disk:
        console.print("\n", get_disk_info())
    if args.gpu:
        console.print("\n", get_gpu_info())
    if args.network:
        console.print("\n", get_network_info())

if __name__ == "__main__":
    display_system_info(args)
