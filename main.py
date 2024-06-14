import psutil
import platform
import argparse
import GPUtil
import os
import time
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
        str(usage_str),
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
        str(svmem.percent),
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

            table.add_row(device, str(total), str(used), str(free), usage_str)
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

        table.add_row(gpu.name, str(gpu.memoryTotal), str(usage_str))

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


# Function to get Process information
def get_process_info():
    processes = []
    for process in psutil.process_iter():
        processes.append(
            {
                "PID": process.pid,
                "Name": process.name(),
                "CPU Usage (%)": process.cpu_percent(),
                "Memory Usage (MB)": round(
                    process.memory_info().rss / (1024 * 1024), 2
                ),
            }
        )

    table = Table(title="Process Information")
    for key in processes[0].keys():
        table.add_column(key, justify="start", style="cyan")

    for process in processes:
        table.add_row(*[str(value) for value in process.values()])

    return table


# Function to get System Uptime
def get_system_uptime():
    table = Table(title="System Uptime")
    table.add_column("Uptime", justify="start", style="cyan")

    uptime = round(time.time() - psutil.boot_time())
    days, remainder = divmod(uptime, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    uptime_str = f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds"
    table.add_row(uptime_str)

    return table


# Function to get Network Usage
def get_network_usage():
    net_io = psutil.net_io_counters()

    table = Table(title="Network Usage")
    table.add_column("Total Bytes Sent", justify="start", style="cyan")
    table.add_column("Total Bytes Received", justify="start", style="magenta")

    table.add_row(str(net_io.bytes_sent), str(net_io.bytes_recv))

    return table


# Function to get User Information
def get_user_info():
    table = Table(title="User Information")
    table.add_column("Username", justify="start", style="cyan")
    table.add_column("Home Directory", justify="start", style="magenta")

    username = os.getlogin()
    home_directory = os.path.expanduser("~")

    table.add_row(username, home_directory)

    return table


# Function to get System Temperature
def get_system_temperature():
    sensors = psutil.sensors_temperatures()

    table = Table(title="System Temperature")
    for sensor, data in sensors.items():
        table.add_column(sensor, justify="start", style="cyan")
        sensor_data = " | ".join([f"{item.label}: {item.current}°C" for item in data])

    table.add_row(sensor_data)

    return table


# Add command line argument parser
parser = argparse.ArgumentParser(description="Display system information")
parser.add_argument("--all", action="store_true", help="Display All information")
parser.add_argument("--os", action="store_true", help="Display OS information")
parser.add_argument("--cpu", action="store_true", help="Display CPU information")
parser.add_argument("--ram", action="store_true", help="Display RAM information")
parser.add_argument("--disk", action="store_true", help="Display Disk information")
parser.add_argument("--gpu", action="store_true", help="Display GPU information")
parser.add_argument(
    "--network", action="store_true", help="Display Network interface information"
)
parser.add_argument(
    "--process", action="store_true", help="Display Process information"
)
parser.add_argument("--uptime", action="store_true", help="Display System Uptime")
parser.add_argument(
    "--network_usage", action="store_true", help="Display Network Usage"
)
parser.add_argument("--user", action="store_true", help="Display User Information")
parser.add_argument(
    "--temperature", action="store_true", help="Display System Temperature"
)

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
        console.print("\n", get_process_info())
        console.print("\n", get_system_uptime())
        console.print("\n", get_network_usage())
        console.print("\n", get_user_info())
        console.print("\n", get_system_temperature())

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
    if args.process:
        console.print("\n", get_process_info())
    if args.uptime:
        console.print("\n", get_system_uptime())
    if args.network_usage:
        console.print("\n", get_network_usage())
    if args.user:
        console.print("\n", get_user_info())
    if args.temperature:
        console.print("\n", get_system_temperature())


if __name__ == "__main__":
    display_system_info(args)
