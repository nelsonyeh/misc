import threading


def loop():
    while True:
        pass


threads = []
for job in range(0, 4):
    thread = threading.Thread(target=loop)
    thread.daemon = True
    threads.append(thread)
    thread.start()
for thread in threads:
    thread.join()
