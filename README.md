
# Sysinfo

This is a tool that gives you detailed information about the operating system and hardware components. This information includes the operating system, CPU, RAM, hard drives, graphics card, and network interface.

## Author

- [@mobin-ghanbarpour](https://github.com/mobin-gpr/)


## Run Project
Clone the project

```bash
git clone https://github.com/mobin-gpr/fox-web-api.git
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
usage: main.py [-h] [--all] [--os] [--cpu] [--ram] [--disk] [--gpu] [--network]

Display system information

options:
  -h, --help  show this help message and exit
  --all       Display All information
  --os        Display OS information
  --cpu       Display CPU information
  --ram       Display RAM information
  --disk      Display Disk information
  --gpu       Display GPU information
  --network   Display Network interface information
```

## License

[MIT](https://choosealicense.com/licenses/mit/)
