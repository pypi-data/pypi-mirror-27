# -*- coding: utf-8 -*-
#author: myvyang#gmail.com

import threading
import Queue

__all__ = ["ThreadPool"]


class ThreadPool(object):

    """
    简单的线程池实现,只支持函数的多线程
    inputs = [(x,x,x), ...]
    p = Pool(func, inputs, 10)
    p.start()
    p.outputs # [x,x,x, ...]
    """

    def __init__(self, func, inputs, number = 10, print_result = False):

        self.print_result = print_result

        self.runable = True
        self.error = ""
        # 检查参数合法性
        if not callable(func):
            self.runable = False
            self.error = "first params is not a callable function"
        elif not isinstance(inputs, list):
            self.runable = False
            self.error = "second params is not a list"
        elif not isinstance(number, int):
            print type(number)
            self.runable = False
            self.error = "thrid params is not a int value"

        if not self.runable:
            raise TypeError, self.error

        self.__func = func
        self.inputs = inputs  # 输入列表
        self.queue_len = len(inputs)  # 输入量， 一般比线程数要大
        if self.queue_len < number:
            self.__number = self.queue_len
        else:
            self.__number = number  # 线程数
        self.threads = [None] * number  # 线程容器
        self.outputs = [None] * self.queue_len  # 输入列表长度(即输入队列长度)

        # 建立一个queue, 用于多线程中提供参数。
        # queue -> [(args, i), ...]
        # 通过添加 i 保证 outputs 中元素和 inputs 对应
        self.queue = Queue.Queue()
        for i in xrange(self.queue_len):
            self.queue.put((self.inputs[i], i))

    def __callable_func(self, func):
        while True:
            try:
                item = self.queue.get_nowait()
            except Queue.Empty:
                break

            args = item[0]
            index = item[1]

            #兼容多个参数和单个参数
            if isinstance(args, list) or isinstance(args, tuple):
                returned = func(*args)
            else:
                returned = func(args)
            
            self.outputs[index] = returned

            if self.print_result and returned != None:
                print(returned)

    def start(self):
        for i in xrange(self.__number):
            t = threading.Thread(
                target=self.__callable_func, args=([self.__func]))
            t.start()
            self.threads[i] = t
        for i in xrange(self.__number):
            self.threads[i].join()


def test_Pool():
    def func(a, b, c):
        return a + b + c
    inputs = [(1, 2, 3), (4, 5, 6), (7, 8, 9)] * 10
    p = ThreadPool(func, inputs, 10)
    p.start()
    print p.outputs


def test_Pool_error():
    func = 1
    inputs = [(1, 2, 3), (4, 5, 6), (7, 8, 9)] * 10
    p = ThreadPool(func, inputs, 10)
    p.start()
    print p.outputs

if __name__ == "__main__":
    test_Pool()
