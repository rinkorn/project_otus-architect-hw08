# %%
import queue
import abc
import datetime as dt

from hw05 import Vector, Move, Rotate


class BaseCommand(abc.ABC):
    @abc.abstractmethod
    def execute(self):
        pass

class EmptyCommand(BaseCommand):
    def execute(self):
        pass

class SomeErrorExecutor(BaseCommand):
    def execute(self):
        # print("TRY EXECUTE SOMEONE")
        raise ValueError("Raise an error manually.")


class LogWriter(BaseCommand):
    def __init__(self, exception, path="log.txt", mode="w"):
        self.exception = exception
        self.path = path
        self.mode = mode

    def execute(self):
        # print(f"WRITE exception: {self.exception}")
        with open(self.path, self.mode) as f:
            # now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # f.write(f"Time to write: {repr(now)}\n")
            f.write(f"Exception: {repr(self.exception)}\n")


class Repeater(BaseCommand):
    def __init__(self, command):
        self.command = command

    def execute(self):
        # print(f"REPEAT COMMAND: {self.command}")
        self.command.execute()


class RepeaterTwice(BaseCommand):
    def __init__(self, command):
        self.command = command

    def execute(self):
        # print(f"REPEAT_TWICE COMMAND: {self.command}")
        self.command.execute()
        # print(f"REPEAT_TWICE COMMAND: {self.command}")
        self.command.execute()


# %%
class BaseEHandler(abc.ABC):
    @abc.abstractmethod
    def handle(self):
        pass


class LogWriterEHandler(BaseEHandler):
    def handle(self, command, exception):
        log_writer = LogWriter(exception)
        log_writer.execute()


class RepeaterEHandler(BaseEHandler):
    def __init__(self, queue):
        self.queue = queue

    def handle(self, command, exception):
        repeater = Repeater(command)
        self.queue.put(repeater)


class RepeaterTwiceEHandler(BaseEHandler):
    def __init__(self, queue):
        self.queue = queue

    def handle(self, command, exception):
        repeater = RepeaterTwice(command)
        self.queue.put(repeater)


class RepeaterLogWriterEHandler(BaseEHandler):
    def __init__(self, queue) -> None:
        self.queue = queue
        self.hash_table = {}

    def handle(self, command, exception):
        key = hash((hash(type(command)), hash(type(exception))))
        if key not in self.hash_table:
            handler = RepeaterEHandler(self.queue)
            self.hash_table[key] = handler.handle(command, exception)
        else:
            handler = LogWriterEHandler()
            handler.handle(command, exception)
            del self.hash_table[key]


class RepeaterTwiceLogWriterEHandler(BaseEHandler):
    def __init__(self, queue) -> None:
        self.queue = queue
        self.hash_table = {}

    def handle(self, command, exception):
        key = hash((hash(type(command)), hash(type(exception))))
        if key not in self.hash_table:
            handler = RepeaterTwiceEHandler(self.queue)
            self.hash_table[key] = handler.handle(command, exception)
        else:
            handler = LogWriterEHandler()
            handler.handle(command, exception)
            del self.hash_table[key]


# %%
if __name__ == "__main__":

    position = p = Vector([12, 5])
    velocity = v = Vector([-7, 3])
    move = Move(p, v)
    direction = d = 0
    angular_velocity = av = 0
    direction_numbers = dn = 8
    rotate = Rotate(d, av, dn)
    some_error = SomeErrorExecutor()

    q = queue.Queue()
    q.put(move)
    q.put(move)
    q.put(rotate)
    q.put(move)
    q.put(rotate)
    q.put(some_error)

    # handler = LogWriterEHandler()
    # handler = RepeaterEHandler(q)
    # handler = RepeaterLogWriterEHandler(q)
    handler = RepeaterTwiceLogWriterEHandler(q)

    i = 0
    while not q.empty():
        c = q.get()
        try:
            c.execute()
        except Exception as ex:
            i += 1
            # print(i)
            # print(c)
            handler.handle(c, ex)
        finally:
            q.task_done()

        if i == 100:
            break


# %%
