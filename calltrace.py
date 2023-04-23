import inspect
import sys
from collections import defaultdict
from dataclasses import dataclass
from inspect import FrameInfo


@dataclass(unsafe_hash=True)
class CallInfo:
    frame: FrameInfo
    info: None
    stack: None
    trace: None
    current: None
    arg: None


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
        self.call_events = defaultdict(int)
        self.call_infos = []
        self.filter = None

    def __call__(self, frame, event, arg):
        if event == "call":
            self.stack_level += 1

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
            txt = "{: <40} # {}:{}, {}:{}".format(
                func_name,
                frame.f_code.co_filename,
                frame.f_lineno,
                frame_back.f_code.co_filename,
                frame_back.f_lineno,
            )
            if txt not in self.call_events:
                call_info = CallInfo(
                    frame=frame,
                    info=inspect.getframeinfo(frame),
                    trace=inspect.trace(),
                    stack=inspect.stack(),
                    current=inspect.currentframe(),
                    arg=arg,
                )
                self.call_infos.append(call_info)
            self.call_events[txt] += 1

        elif event == "return":
            self.stack_level -= 1

    def start(self, filter_func=None):
        if filter_func:
            FileFilter.filter = filter_func

        self.stack_level = 0
        self.call_events.clear()
        sys.setprofile(self)

    def output(self):
        for txt, i in self.call_events.items():
            if i > 1:
                print(f"{txt}({i})")
            else:
                print(txt)
        self.call_events.clear()

    def stop(self):
        FileFilter.filter = FileFilter.old_filter
        sys.setprofile(None)
