import sys


class FileFilter:
    @staticmethod
    def filter(filename):
        return True

    @staticmethod
    def old_filter(filename):
        return False


class CallTrace:
    def __init__(self):
        self.stack_level = 0
        self.call_events = []
        self.filter = None

    def __call__(self, frame, event, arg):
        if event == "call":
            self.stack_level += 1

            unique_id = frame.f_code.co_filename + str(frame.f_lineno)

            # Part of filename MUST be in white list.
            if "self" in frame.f_locals:
                class_name = frame.f_locals["self"].__class__.__name__
                func_name = class_name + "." + frame.f_code.co_name
            else:
                func_name = frame.f_code.co_name

            func_name = "{indent}{name}".format(
                indent=self.stack_level * 2 * "-", name=func_name
            )

            if not FileFilter.filter(frame.f_code.co_filename):
                return

            frame_back = frame.f_back  # 获取调用函数时的信息
            txt = "{: <40} # {}, {}, {}, {}".format(
                func_name,
                frame.f_code.co_filename,
                frame.f_lineno,
                frame_back.f_code.co_filename,
                frame_back.f_lineno,
            )

            self.call_events.append(txt)

        elif event == "return":
            self.stack_level -= 1

    def start(self, filter_func=None):
        if filter_func:
            FileFilter.filter = filter_func

        self.stack_level = 0
        self.call_events.clear()
        sys.setprofile(self)

    def output(self):
        for text in self.call_events:
            print(text)

        self.call_events.clear()

    def stop(self):
        FileFilter.filter = FileFilter.old_filter
        sys.setprofile(None)
