from multiprocessing import Process, Queue

def finger_tracking(q):
    q.put([[0,0] for x in range(10)])

def gesture_recognition(q):
    while True:
        pos = q.get()
        print "got positions: {}".format(pos)


def main():
    q = Queue()
    t = Process(target=finger_tracking, args=(q,))
    t.start()
    g = Process(target=gesture_recognition, args=(q,))
    g.start()
    while True:
        pass


if __name__ == '__main__':
    main()
