# PiedPiper Volatility3 Plugin

The PiedPiper plugin is a custom plugin for the Volatility3 framework that targets Windows systems. It allows you to enumerate the named pipes for specified processes and displays their creation dates.

## Installation

1. Make sure you have Volatility3 framework installed. Refer to the official [Volatility3 documentation](https://github.com/volatilityfoundation/volatility3) for installation instructions.

2. Clone this repository or download the `piedpiper.py` file.

## Usage

To run the PiedPiper plugin, follow these steps:

1. Open a terminal or command prompt.

2. Navigate to the directory where Volatility3 is installed.

3. Run the PiedPiper plugin using the `vol.py` command:

   ```shell
   vol.py -f <path_to_memory_dump> piedpiper --pid_list <list_of_process_ids>
   ```
Replace <path_to_memory_dump> with the path to your memory dump file, and <list_of_process_ids> with the space-separated list of process IDs for which you want to enumerate named pipes.
  
  ```shell
  vol.py -f memory.dmp piedpiper --pid_list 1234 5678 9012
  ```
4. The plugin will output the process name, process ID, named pipes, and their creation dates sorted by creation date using the TreeGrid format.

## Requirements 
- Volatility3 framework (compatible with Python 3.x)
- Memory dump of a Windows system (obviously)

## Licence
This project is licensed under the MIT License.
Pipis Pipa
