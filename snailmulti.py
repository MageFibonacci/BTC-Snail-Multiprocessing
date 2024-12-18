# -*- coding: utf-8 -*-
import secp256k1 as ice
import time
import os
import sys
import random
import argparse
from multiprocessing import Pool, cpu_count, Manager

# ==============================================================================
parser = argparse.ArgumentParser(description='Optimized BTC puzzle search with multiprocessing and accurate progress display.',
                                 epilog='Enjoy the program! :)')
parser.version = '02052023'
parser.add_argument("-p", help="Unsolved Puzzles file. default=unsolved.txt", action="store")
parser.add_argument("-n", help="Total sequential search in 1 loop. default=1000000", action='store')

args = parser.parse_args()
# ==============================================================================

seq = int(args.n) if args.n else 1000000  # 1 Million
p_file = args.p if args.p else 'unsolved.txt'  # 'unsolved.txt'

if not os.path.isfile(p_file):
    print('File {} not found'.format(p_file))
    sys.exit()

puzz = {int(line.split()[0]): line.split()[1] for line in open(p_file, 'r')}
puzz_bits = list(puzz.keys())
puzz_h160 = set(bytes.fromhex(ice.address_to_h160(line)) for line in puzz.values())  # Set for fast lookup
# ==============================================================================

def print_success(my_key):
    print('\n============== KEYFOUND ==============')
    print(f'Puzzle FOUND PrivateKey: {hex(my_key)}   Address: {ice.privatekey_to_address(0, True, my_key)}')
    print('======================================')
    with open('KEYFOUNDKEYFOUND.txt', 'a') as fw:
        fw.write('Puzzle_FOUND_PrivateKey ' + hex(my_key) + '\n')
    sys.exit()

def randk(bits):
    return random.SystemRandom().randint(2**(bits-1), 2**bits - 1)

def precalculate_keys(seq, base_point):
    """ Precalculate sequential increments and their h160 """
    precomputed_h160 = []
    for t in chunks(ice.point_sequential_increment(seq, base_point)):
        precomputed_h160.append(ice.pubkey_to_h160(0, True, t))
    return precomputed_h160

def chunks(s):
    for start in range(0, 65 * seq, 65):
        yield s[start: start + 65]

def worker(task_id, progress_queue, key_counter):
    """ Worker function for multiprocessing """
    keys_checked = 0
    key_int = randk(160)
    for cbits in puzz_bits:
        bitkey = int('1' + bin(key_int)[2:][(1 + 160 - cbits):], 2)
        base_point = ice.scalar_multiplication(bitkey)
        keys_checked += 1

        if ice.pubkey_to_h160(0, True, base_point) in puzz_h160:
            print_success(bitkey)

        # Precalculate sequential keys and check
        precomputed_h160 = precalculate_keys(seq, base_point)
        for cnt, curr160 in enumerate(precomputed_h160):
            keys_checked += 1
            if curr160 in puzz_h160:
                print_success(bitkey + cnt + 1)

        # Update global counter and progress
        key_counter.value += keys_checked
        progress_queue.put((task_id, cbits, key_counter.value))

# ==============================================================================

def display_progress(progress_queue, start_time, key_counter):
    """ Function to display progress from workers """
    while True:
        try:
            task_id, cbits, total_keys = progress_queue.get(timeout=2)
            elapsed = time.time() - start_time
            speed = total_keys / elapsed
            print(f'[Task: {task_id}] [Puzzle: {cbits} bit] [Speed: {speed:.2f} keys/s] [Checked: {total_keys}]', end='\r')
        except:
            continue

if __name__ == "__main__":
    print('\n[+] Starting Program.... Please Wait !')
    print(f'[+] Search Mode: Sequential Random with multiprocessing. seq={seq}')
    print(f'[+] Total Unsolved: {len(puzz_bits)} Puzzles in the bit range [{min(puzz_bits)}-{max(puzz_bits)}]')

    manager = Manager()
    progress_queue = manager.Queue()
    key_counter = manager.Value('i', 0)  # Shared counter for total keys
    start_time = time.time()

    try:
        with Pool(cpu_count()) as pool:
            # Start progress display in a separate process
            pool.apply_async(display_progress, (progress_queue, start_time, key_counter))

            # Run workers
            while True:
                pool.starmap(worker, [(i, progress_queue, key_counter) for i in range(cpu_count())])

    except (KeyboardInterrupt, SystemExit):
        elapsed = time.time() - start_time
        print(f'\nProgram terminated. Total time elapsed: {elapsed:.2f} seconds')
        print(f'Total Keys Checked: {key_counter.value}')
        sys.exit()
