from calltrace import CallTrace


def func1():
    print('ok')


def func2():
    func1()


def func5():
    func1()


def func3():
    func2()


def func4():
    func3()
    func5()


def file_filter(filename):
    if filename.find('calc') != -1:
        return True
    return False


trace = CallTrace()
trace.start(filter_func=lambda x: x.find('call_test') != -1)
func4()
trace.stop()
trace.output()
