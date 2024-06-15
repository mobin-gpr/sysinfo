# Sysinfo

This is a tool that gives you detailed information about the operating system and hardware components. This information includes the OS, CPU, RAM, Disks, GPU Network interface & ...

## Author

- [@mobin-ghanbarpour](https://github.com/mobin-gpr/)


## Run Project
Clone the project

```bash
git clone https://github.com/mobin-gpr/sysinfo.git
```

Go to the project directory

```bash
cd sysinfo
```

Install dependencies

```bash
pip install -r requirements.txt
```

Show helps

```bash
python main.py --help
```

## Guide


```text
usage: main.py [-h] [--all] [--os] [--cpu]
               [--ram] [--disk] [--gpu]
               [--network] [--process]
               [--uptime] [--network_usage]
               [--user] [--temperature]

Display system information

optional arguments:
  -h, --help       show this help message and
                   exit
  --all            Display All information
  --os             Display OS information
  --uptime         Display System Uptime
  --cpu            Display CPU information
  --ram            Display RAM information
  --disk           Display Disk information
  --gpu            Display GPU information
  --network        Display Network interface
                   information
  --process        Display Process information
  --network_usage  Display Network Usage
  --user           Display User Information
  --temperature    Display System Temperature
```

## License

[MIT](https://choosealicense.com/licenses/mit/)
