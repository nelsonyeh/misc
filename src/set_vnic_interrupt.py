#!/usr/bin/python3
import multiprocessing
import sys

CPU_COUNT = multiprocessing.cpu_count()


def set_rx(ifname):
    for cnt in range(0, CPU_COUNT):
        mask = [0] * CPU_COUNT
        path = f'/sys/class/net/{ifname}/queues/rx-{cnt}/rps_cpus'
        mask[CPU_COUNT - 1 - cnt] = 1
        bitmap = ''.join(str(i) for i in mask)
        print(f'Idx:{cnt} bitmap:{bitmap}')
        value = hex(int(bitmap, 2)).split('0x')[1]
        with open(path, 'w') as fp:
            fp.write(value)


def set_tx(ifname):
    for cnt in range(0, CPU_COUNT):
        mask = [0] * CPU_COUNT
        path = f'/sys/class/net/{ifname}/queues/tx-{cnt}/xps_cpus'
        mask[CPU_COUNT - 1 - cnt] = 1
        bitmap = ''.join(str(i) for i in mask)
        print(f'Idx:{cnt} bitmap:{bitmap}')
        value = hex(int(bitmap, 2)).split('0x')[1]
        with open(path, 'w') as fp:
            fp.write(value)


if __name__ == "__main__":
    ifname = sys.argv[1]
    set_rx(ifname)
    set_tx(ifname)
