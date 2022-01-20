#!/usr/bin/python3
import json
import getopt
import subprocess
import sys
from argparse import ArgumentParser


#CMD_IPERF3 = '/usr/bin/iperf3'
CMD_IPERF3 = 'D:\eclipses\eclipse-cpp-2020-03-R-incubation-win32-x86_64\Python3\iperf3.exe'
DEFAULT_PORT = 5201
DEFAULT_WORKERS = 1


def execute(args, run_async=False, env=None):
    if run_async:
        return subprocess.Popen(args, shell=False,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
    elif env is not None:
        p = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, env=env)
        (out, err) = p.communicate()
        ret = p.returncode
        return (ret, out, err)
    else:
        p = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        (out, err) = p.communicate()
        ret = p.returncode
        return (ret, out, err)


def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        '-t', '--time', help='time in seconds to transmit', type=int,
        dest='interval')
    parser.add_argument('-s', '--server',
                        help='run in server mode',
                        dest='is_server', action='store_true')
    parser.add_argument('-c', '--client',
                        help='run in client mode, connecting to <host>',
                        dest='host')
    parser.add_argument('-P', '--parallel',
                        help='number of parallel client streams to run',
                        dest='workers', type=int, default=DEFAULT_WORKERS)
    parser.add_argument('-n', '--count', help='loop count',
                        type=int, dest='count')
    parser.add_argument('-p', '--port',
                        help='server port to listen on/connect to',
                        dest='port', default=DEFAULT_PORT)
    return parser.parse_args()


def validate(args):
    assert not (args.is_server and args.host), 'Conflict options: -s -c'


class TestReport:
    def __init__(self, data):
        self.json = json.loads(data)

    @property
    def sender_info(self):
        return self.json.get('end', {}).get('sum_sent', {})

    @property
    def receiver_info(self):
        return self.json.get('end', {}).get('sum_received', {})

    @property
    def send_bandwidth(self):
        return self.sender_info.get('bits_per_second')

    @property
    def recv_bandwidth(self):
        return self.receiver_info.get('bits_per_second')


class Server:
    def __init__(self, port):
        self.port = port

    def run(self):
        '''
        process = execute([CMD_IPERF3, '-s', '-V'], run_async=True)
        while True:
            print('1' * 80)
            ret = process.poll()
            print('2' * 80)
            print(f'ret >>>>>>>>>>>>{ret}')
            yield ret
        '''

        #print(execute([CMD_IPERF3, '-s', '-V', '-D'], run_async=False))
        p = subprocess.run([CMD_IPERF3, '-s', '-J'],
                           capture_output=False, stdout=subprocess.PIPE)
        print('sss', p.stdout)
        TestReport(p.stdout)


class Client:
    EXECUTE_SUCCESS = 0

    def __init__(self, host, port, loop, interval, workers):
        self.server_host = host
        self.server_port = port
        self.loop = loop
        self.interval = interval
        self.workers = workers

    def run(self):
        count = 1
        reports = []
        while count <= self.loop:
            p = subprocess.run(
                [CMD_IPERF3, '-c', self.server_host,
                 '-p', str(self.server_port),
                 '-t', str(self.interval),
                 '-P', str(self.workers),
                 '-J', '-N'],
                capture_output=True, text=True)
            print(f'Loop {count} Result:{p.returncode}')
            if p.returncode != Client.EXECUTE_SUCCESS:
                break
            reports.append(TestReport(p.stdout))
            count += 1
        total_tx = total_rx = 0
        for report in reports:
            total_rx += report.recv_bandwidth
            print(report.recv_bandwidth)
            total_tx += report.send_bandwidth
        count = len(reports)
        print(f'Total times:{count}')
        print(f'Client TX bandwidth:{(total_tx/count)/10**9}')
        print(f'Client RX bandwidth:{(total_rx/count)/10**9}')


def get_runner(args):
    if args.is_server:
        return Server(args.port)
    return Client(args.host, args.port,
                  args.count, args.interval, args.workers)


def run_test(args):
    print(args)
    runner = get_runner(args)
    print(runner)
    try:
        runner.run()
    except Exception:
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    args = parse_args()
    validate(args)
    run_test(args)
