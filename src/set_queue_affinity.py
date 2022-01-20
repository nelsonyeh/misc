#!/usr/bin/python3
import multiprocessing
import re

CPU_COUNT = multiprocessing.cpu_count()


def get_irqs():
    irqs = []
    reg = re.compile(r'\d+:.*virtio\d+-(\binput\b|\boutput\b).\d+$')
    with open('/proc/interrupts') as fp:
        for line in fp.readlines():
            if reg.match(line.strip()) is None:
                continue
            irqs.append(int(line.split(':')[0]))
    return irqs


def get_irq_affinity(irq):
    with open(f'/proc/irq/{irq}/smp_affinity_list') as fp:
        return fp.read().strip()


def set_irq_affinity(irq, value):
    print(f'Pin IRQ {irq} to CPUs {value}')
    with open(f'/proc/irq/{irq}/smp_affinity', 'w') as fp:
        return fp.write(value)


if __name__ == "__main__":
    irqs = get_irqs()
    print(irqs)
    for irq in irqs:
        cpu = get_irq_affinity(irq)
        print(f'Interrupt {irq} is allowed on CPUs {cpu}')

    irq_idx = 0
    for cnt in range(0, CPU_COUNT):
        mask = [0] * CPU_COUNT
        mask[CPU_COUNT - 1 - cnt] = 1
        bitmap = ''.join(str(i) for i in mask)
        print(f'Idx:{cnt} bitmap:{bitmap}')
        value = hex(int(bitmap, 2)).split('0x')[1]
        set_irq_affinity(irqs[irq_idx], value)
        set_irq_affinity(irqs[irq_idx + 1], value)
        irq_idx += 2

    for irq in irqs:
        cpu = get_irq_affinity(irq)
        print(f'Interrupt {irq} is allowed on CPUs {cpu}')
