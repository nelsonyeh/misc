import signal
import time

def signal_handler(signum, frame):
    print('Received signal: ', signum)
    print 'Signal start:', time.time()
    time.sleep(5)
    print 'Signal end:', time.time()

def signal_handler2(signum, frame):
    print('Received signal2: ', signum)
    print 'Signal2 start:', time.time()
    time.sleep(5)
    print 'Signal2 end:', time.time()

def step(i):
    print('%s...%s' %(i, time.time()))
    time.sleep(5)
    print('%s...%s' %(i, time.time()))

    
while True:
    signal.signal(signal.SIGUSR1, signal_handler) # 14
    signal.signal(signal.SIGUSR2, signal_handler2) # 14
    while True:
        i=1
        step(i)
        i=2
        step(i)
        i=3
        step(i)
        i=4
        step(i)
        i=5
        step(i)
        print('---------------------------------------------\n')

        
# kill -USR1 $PID
# kill -USR2 $PID
