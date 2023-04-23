import inspect

from calltrace import CallTrace


class A:
    def demo1(self):
        frame = inspect.currentframe()
        print("A.demo1")

    @staticmethod
    def demo2():
        frame = inspect.currentframe()
        pass


a = A()


def func1():
    _ = sorted([i for i in range(100)], key=lambda i: i)
    print('ok')
    a.demo1()
    a.demo2()


def func2():
    func1()


def func5():
    frame = inspect.currentframe()
    func1()


def func3():
    func2()


def func4():
    func3()
    for i in range(5):
        func5()


def file_filter(filename):
    if filename.find('calc') != -1:
        return True
    return False


if __name__ == '__main__':
    trace = CallTrace()
    trace.start(filter_func=lambda x: x.find('call_test') != -1)
    func4()
    trace.stop()
    trace.output()
