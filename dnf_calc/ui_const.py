#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------
# File   : ui_const
# Date   : 2020/5/24 0024
# Author : Chen Ji
# Email  : fzls.zju@gmail.com
# -------------------------------


main_window_width = 710
main_window_height = 720
main_window_x_offset = 0
main_window_y_offset = 0

other_window_x_offset = main_window_x_offset + main_window_width + 10

result_window_width = 585
result_window_readable_result_area_height = 18 * 3
result_window_height = 402 + result_window_readable_result_area_height
result_window_x_offset = other_window_x_offset
result_window_y_offset = main_window_y_offset + (main_window_height - result_window_height) // 2

custom_window_width = 620
custom_window_height = 400
custom_window_x_offset = other_window_x_offset
custom_window_y_offset = main_window_y_offset + (main_window_height - custom_window_height) // 2

res_txt_readable_result_center_x = result_window_width // 2
res_txt_readable_result_center_y = result_window_height - result_window_readable_result_area_height // 2

