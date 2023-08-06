#!/usr/bin/python
# -*- coding: utf-8 -*-
# Github: https://github.com/SarbazVatan/wcolors
# Email: soldier.of.iran.dev@gmail.com
# Coded By @Soldier_of_iran
# [Sarbaz_Vatan]

from ctypes import windll


class WIN:
    def __init__(self):
        std_output_handle = -11
        self.stdout_handle = windll.kernel32.GetStdHandle(std_output_handle)

    def control(self, num):
        windll.kernel32.SetConsoleTextAttribute(self.stdout_handle, num)

    def green(self):
        self.control(10)

    def red(self):
        self.control(12)

    def white(self):
        self.control(15)

    def blue(self):
        self.control(11)

    def pink(self):
        self.control(13)

    def yellow(self):
        self.control(14)

    def dark_green(self):
        self.control(2)

    def dark_red(self):
        self.control(4)

    def dark_white(self):
        self.control(7)

    def dark_blue(self):
        self.control(3)

    def dark_pink(self):
        self.control(5)

    def dark_yellow(self):
        self.control(6)
