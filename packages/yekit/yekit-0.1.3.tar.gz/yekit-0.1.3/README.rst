工具介绍
========

本工具是看了\ `ShichaoMa <https://github.com/ShichaoMa/toolkit>`__\ 的项目写出来的，因为我觉得有很多功能，用装饰器的方式会更好。

函数介绍
========

kit.py
------

timer
~~~~~

装饰器函数，用于计算func运行耗时，并将运行时间输出至屏幕上，结果保留小数点后3位。

::

    from yekit import kit.timer as timer

    @timer
    def process():
        some operations...

    process()

输出结果会将process的运行时间打印到console中。
