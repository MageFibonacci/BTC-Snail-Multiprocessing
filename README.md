# BTC-Snail-Multiprocessing
This is a modified version of the Snail tool originally created by [iceland2k14](https://github.com/iceland2k14/snail). The modifications add support for KeyRange search, multiprocessing, a queue manager, and precalculation of sequential increments along with their h160 values.

## Features

- **KeyRange Search**: Specify a starting point (`--start`) and an endpoint (`--end`) for the keyspace to narrow down the search.
- **Multiprocessing**: Utilize multiple CPU cores for faster computation and enhanced performance.
- **Queue Manager**: Provides real-time progress tracking and key count updates across processes.
- **Precalculated Sequential Increments**: Improves efficiency by precalculating sequential public keys and their corresponding h160 hashes.

## Requirements

- Python 3.7 or higher


## Usage

Run the program using the following syntax:


```bash
python script.py -p unsolved.txt -n 1000000 --start 0x40000000000000000 --end 0x6ffffffffffffffff
```

### Arguments

- `-p`: Path to the file containing unsolved puzzles (default: `unsolved.txt`).
- `-n`: Number of sequential keys to search in one loop (default: `1000000`).
- `--start`: Starting point of the key range (in hexadecimal format).
- `--end`: Endpoint of the key range (in hexadecimal format).

### Example

To search in the range `0x40000000000000000` to `0x6FFFFFFFFFFFFFFFF`:

python script.py -p unsolved.txt -n 1000000 --start 0x40000000000000000 --end 0x6ffffffffffffffff


### Input File Format

The `unsolved.txt` file should list puzzles in the following format:
<bit_length> <address>

#### Example for Puzzle 67:
67 1BY8GQbnueYofwSuFAT3USAhGjPrkxDdW9

---

## Key Features in Detail

### KeyRange Search

The `--start` and `--end` parameters let you define a specific range in the keyspace to search for solutions. This is useful for focusing on smaller subsets of the keyspace.

### Multiprocessing

The program automatically detects the number of CPU cores available and distributes the workload across them for faster performance.

### Queue Manager

Real-time progress updates show:
- Current task and bit length being processed.
- Total keys checked.
- Approximate speed (keys per second).

### Precalculation of Sequential Keys

Sequential public keys and their h160 hashes are precalculated to improve search efficiency. This allows for faster checking of keys within the specified range.

---

## Tips

- Optimize the `-n` parameter based on your system's memory and CPU capabilities. Higher values may improve performance but require more memory.
- Use a smaller key range for faster testing and debugging.

---

## Original Credit

This project is based on [Snail by iceland2k14](https://github.com/iceland2k14/snail). The original implementation laid the foundation for solving Bitcoin puzzles using optimized techniques.

