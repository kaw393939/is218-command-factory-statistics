"""Optional conversion experiment; not a claim about hardware mispredictions."""
import random
from timeit import repeat


def eafp(text):
    try:
        return int(text)
    except ValueError:
        return None


def lbyl(text):
    if text and text.isascii() and text.isdecimal():
        return int(text)
    return None


def main():
    print('Restricted workload: unsigned ASCII integers or invalid alphabetic text.')
    print('Valid input % | EAFP seconds | LBYL seconds (best of 3; 100 batches)')
    for percent in (100, 99, 50, 0):
        inputs = ['123'] * (percent * 10) + ['bad'] * ((100 - percent) * 10)
        random.Random(218).shuffle(inputs)
        assert [eafp(value) for value in inputs] == [lbyl(value) for value in inputs]
        timings = [min(repeat(lambda: [method(value) for value in inputs], number=100, repeat=3))
                   for method in (eafp, lbyl)]
        print(f'{percent:13} | {timings[0]:.6f} | {timings[1]:.6f}')
    print('These measurements apply to this workload and interpreter. They do not measure branch prediction.')


if __name__ == '__main__':
    main()
