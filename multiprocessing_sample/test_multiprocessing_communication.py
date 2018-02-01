from multiprocessing import freeze_support, Process, Array, Value, Queue, Pipe, Event, Semaphore
import time

num_tile = 4
max_cycles = 10

IS_SINGLE_THREAD_VERSION = False

tile_instructions = {
    0: ['dummy', 'send', 'dummy'] + ['dummy']*(max_cycles-3),
    1: ['dummy', 'dummy', 'rcv'] + ['dummy']*(max_cycles-3),
    2: ['dummy', 'send', 'dummy'] + ['dummy']*(max_cycles-3),
    3: ['dummy', 'dummy', 'rcv'] + ['dummy']*(max_cycles-3),
}

class Tile():

    def __init__ (self, id, queue, parent_pipe):
        self.tile_halt = 0
        self.counter = 0
        self.id = id
        self.queue = queue
        self.parent_pipe = parent_pipe

    def tile_run(self, cycle):
        #START SOME COMPUTATION
        aba = []
        for i in range(10000):
            aba.append(i ** 10 + (i * 10) ** 10 + (i * 10) ** 10)
        #END SOME COMPUTATION

        fake_instruction = tile_instructions[self.id][cycle]
        if not IS_SINGLE_THREAD_VERSION:
            if fake_instruction == 'send':
                target = self.id + 1
                print "\t[tile_id={}] Sending date to tile_id={}".format(self.id, target)
                self.queue.put({'target' : target, 'source': self.id, 'buffer': [0,1,2,3,4]})
            elif fake_instruction == 'rcv':
                received_data = self.parent_pipe.recv()
                source = received_data['source']
                print "\t[tile_id={}] Receiving date from tile_id={} -> data='{}'".format(self.id, source, received_data)

        # Halting tiles using some logic
        self.counter += 1
        #Logic: [0,2] will halted at cycle=2 and [1,3] will be halted in the last cycle - 1
        if self.id in [0,2] and cycle == 2:
            self.tile_halt = 1
        elif self.counter == max_cycles - 1:
            self.tile_halt = 1

class TileProcess(Process):

    def __init__ (self, tile, run_tile_event, tile_run_finished_semaphore):
        super(TileProcess, self).__init__()
        self.tile = tile
        self.run_tile_event = run_tile_event
        self.cycle = 0
        self.tile_run_finished_semaphore = tile_run_finished_semaphore
        self.tile_halt = Value('i', 0)

    def run(self):
        while self.tile.tile_halt != 1:
            self.run_tile_event.wait() # Wait for the next cycle execution
            self.tile.tile_run(self.cycle)
            self.cycle += 1
            if self.tile.tile_halt == 1:
                self.tile_halt.value = 1
            self.tile_run_finished_semaphore.release() #Just sinalizing that the current execution ends

    def get_halt(self):
        return self.tile_halt.value

class Node(object):
    def __init__(self):
        self.queue_list = [Queue() for _ in range(num_tile)]
        self.pipes_list = [Pipe() for _ in range(num_tile)]
        self.tile_list = [Tile(i, self.queue_list[i], self.pipes_list[i][1] ) for i in range(num_tile)]
        self.tile_halt_list = [0 for _ in range(num_tile)]
        self.run_tile_event = Event()
        self.tile_run_finished_semaphore = Semaphore(0)

        self.process_list = []
        for i in range(num_tile):
            p = TileProcess(self.tile_list[i], self.run_tile_event, self.tile_run_finished_semaphore)
            p.daemon = True
            p.start()
            self.process_list.append(p)

    def node_run_process(self, cycle):
        self.run_tile_event.set()
        self.run_tile_event.clear()

        # Waiting tiles execution to finish (like process.join())
        tiles_to_wait = self.tile_halt_list.count(0)
        for i in xrange(tiles_to_wait):
            self.tile_run_finished_semaphore.acquire()

        # Updating the tiles halted
        for i in xrange(num_tile):
            self.tile_halt_list[i] = self.process_list[i].get_halt()

        for i in xrange(num_tile):
            if not self.queue_list[i].empty():
                received_data = self.queue_list[i].get()
                target = received_data['target']
                print "\tThere is something on the queue {} -> {}".format(i, received_data)
                parent_conn, _ = self.pipes_list[target]
                parent_conn.send(received_data)

        print "Cycle: {} All Halted? {} - {}".format(cycle, self.halt(), self.tile_halt_list)

    def node_run_single(self, cycle):
        for i in range(num_tile):
            self.tile_list[i].tile_run (cycle)
            self.tile_halt_list[i] = self.tile_list[i].tile_halt

        print "Cycle: {} All Halted? {} - {}".format(cycle, self.halt(), self.tile_halt_list)

    def halt(self):
        return all(self.tile_halt_list)

def run_process():
    node = Node()
    cycle = 0
    time.sleep(2)
    while (not node.halt() and cycle < max_cycles):
        node.node_run_process(cycle)
        cycle += 1

def run_sync():
    global IS_SINGLE_THREAD_VERSION
    IS_SINGLE_THREAD_VERSION= True

    node = Node()
    cycle = 0
    time.sleep(2)
    while (not node.halt() and cycle < max_cycles):
        node.node_run_single(cycle)
        cycle += 1

if __name__ == '__main__':
    freeze_support()
    print 'Tiles {}'.format(num_tile)

    start = time.time()
    run_process()
    end = time.time()
    print ('time process: ' + str(end-start) + 'secs')

    start = time.time()
    run_sync()
    end = time.time()
    print ('time original: ' + str(end-start) + 'secs')

