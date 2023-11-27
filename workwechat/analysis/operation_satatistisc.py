import os
import pprint
import datetime
from datetime import datetime
import numpy as np

date_start = ''
date_end = ''

t_gap = 15  # 设定同一连续操作中的常规时间延迟为15秒

list_host_name = ['RPA-4', 'U37U5LH', 'XIAOLUO', 'XIAOYU', 'ZHANGLEI1', 'zhuli08']

log_smr = 'smr.log'
log_smr_task = 'smr_task.log'
log_smr_1224 = 'smr2021-12-24.log'
dict_ref_smr = {
    'ToastWindow': '已发送弹窗',
    '错': '出错',
    'error': '出错',
    'ERROR': '出错'
}

dict_ref_smr_task = {

    '已发送一次群发消息': '点击发送'

}


def calculate_datetime_delta(list_input, gap_threshold):
    list_output = []
    for i in range(0, len(list_input)-1):
        time_delta = (datetime.strptime(
            list_input[i + 1], "%Y-%m-%d %H:%M:%S,%f"
        ) - datetime.strptime(list_input[i], "%Y-%m-%d %H:%M:%S,%f") ).total_seconds()
        if time_delta < gap_threshold:
            list_output.append(time_delta)
    return list_output


def fill_in_dict(contents, dict_ref, dict_):
    for i in range(len(contents) - 1):
        l_smr = contents[i].strip()
        if l_smr[0].isdigit():
            str_time_stamp = l_smr[:23]
            for key in dict_ref.keys():
                if key in contents[i + 1].strip():
                    dict_[str_time_stamp] = [dict_ref[key], contents[i + 1].strip()]
                elif key in l_smr[26:]:
                    dict_[str_time_stamp] = [dict_ref[key], l_smr[26:]]


def fill_in_dict_process(path_base, log_file, dict_ref, dict_):
    path_smr = os.path.join(path_base, log_file)
    if os.path.isfile(path_smr):
        f_smr = open(path_smr, encoding='utf-8')
        c_smr = f_smr.readlines()
        fill_in_dict(c_smr, dict_ref, dict_)


def run(host_name_):
    path_base_ = os.path.join(r'E:\Working_Space\scrmrobot-service\workwechat\analysis', host_name_)
    f_report = open(os.path.join(path_base_, host_name_ + '_report.txt'), 'w', encoding='utf-8')
    dict_all = {}
    fill_in_dict_process(path_base_, log_smr, dict_ref_smr, dict_all)
    fill_in_dict_process(path_base_, log_smr_task, dict_ref_smr_task, dict_all)
    fill_in_dict_process(path_base_, log_smr_1224, dict_ref_smr, dict_all)
    # pprint.pprint(dict_all)
    num_click_pop_pairs = 0
    k_last = None
    list_time_send = []      # 记录 点击发送 的时间戳
    list_time_pop_send = []  # 记录 已发送弹窗 的时间戳
    list_time_response = []  # 记录 点击发送 - 已发送弹窗 响应时间
    list_stop_run = []       # 记录 运行和停止时间
    i = 0
    for k, v in sorted(dict_all.items(), key=lambda x: x[0]):
        if v[0] == '已发送弹窗':
            list_time_pop_send.append(k)
            if k_last:
                t_tmp = (datetime.strptime(k, "%Y-%m-%d %H:%M:%S,%f") - datetime.strptime(
                    k_last, "%Y-%m-%d %H:%M:%S,%f")).total_seconds()
                if t_tmp < t_gap:
                    list_time_response.append(t_tmp)
                    num_click_pop_pairs += 1
        k_last = None
        if v[0] == '点击发送':
            k_last = k
            list_time_send.append(k)
        # 统计 运行-出错
        if (i == 0 or (list_stop_run and list_stop_run[-1][1] == '出错')) and v[0] != '出错':
            list_stop_run.append([k, v[0], v[1]])
        if v[0] == '出错':
            if list_stop_run and list_stop_run[-1][1] != '出错':
                list_stop_run.append([k, v[0], v[1]])
        i += 1
    print('%s 运行结果：\n' % host_name_)
    f_report.write('%s 运行结果：\n' % host_name_)
    # 运行时长
    print('list_stop_run = ', list_stop_run)
    print('运行时间段：')
    f_report.write('\n运行时间段：')
    for j in range(0, len(list_stop_run)):
        if list_stop_run[j][1] != '出错':
            if j < len(list_stop_run) - 1 and list_stop_run[j+1][1] == '出错':
                print('\t%21s\t开始: %s, 结束: %s 出错原因: %s' % (str(
                    (datetime.strptime(list_stop_run[j + 1][0], "%Y-%m-%d %H:%M:%S,%f") - datetime.strptime(
                        list_stop_run[j][0], "%Y-%m-%d %H:%M:%S,%f"))),
                                                           list_stop_run[j][0],
                                                           list_stop_run[j + 1][0],
                                                           list_stop_run[j + 1][2]))
                f_report.write('\n\t%21s\t\t开始: %s, 结束: %s 出错原因: %s' % (str(
                    (datetime.strptime(list_stop_run[j + 1][0], "%Y-%m-%d %H:%M:%S,%f") - datetime.strptime(
                        list_stop_run[j][0], "%Y-%m-%d %H:%M:%S,%f"))),
                                                                        list_stop_run[j][0],
                                                                        list_stop_run[j + 1][0],
                                                                        list_stop_run[j + 1][2]))
            else:
                print('\n\t%17s\t\t开始: %s' % ('持续运行中', list_stop_run[j][0]))
                f_report.write('\n\t%17s\t\t开始: %s' % ('持续运行中', list_stop_run[j][0]))
    if not list_stop_run:
        f_report.write('未检测到报错记录（可能一直运行 or 漏记了 ERROR）')

    # 点击发送
    num_click_send = sum(value[0] == '点击发送' for value in dict_all.values())
    print('\n点击发送 次数：%d' % num_click_send)
    f_report.write('\n\n点击发送 次数：%d' % num_click_send)
    t_delta_send = calculate_datetime_delta(list_time_send, t_gap)
    if t_delta_send:
        print('点击发送\t\t\t\t\t\t（假设正常情况下连续点击在 %d 以内） '
              '\n\t平均发生周期 %f 秒\n\t最大 %f 秒\n\t最小 %f 秒'
              % (t_gap, np.average(t_delta_send), max(t_delta_send), min(t_delta_send)))
        f_report.write('\t\t\t\t\t（假设正常情况下连续点击在 %d 以内） '
                       '\n\t平均发生周期 %f 秒\n\t最大 %f 秒\n\t最小 %f 秒'
                       % (t_gap, np.average(t_delta_send), max(t_delta_send), min(t_delta_send)))
    # 已发送弹窗
    num_pop_send = sum(value[0] == '已发送弹窗' for value in dict_all.values())
    print('\n已发送弹窗 次数：%d' % num_pop_send)
    f_report.write('\n\n已发送弹窗 次数：%d' % num_pop_send)
    t_delta_pop_send = calculate_datetime_delta(list_time_pop_send, t_gap)
    if t_delta_pop_send:
        print('已发送弹窗\t\t\t\t\t\t（假设正常情况下连续弹窗在 %d 以内） '
              '\n\t平均发生周期 %f 秒\n\t最大 %f 秒\n\t最小 %f 秒'
              % (t_gap, np.average(t_delta_pop_send), max(t_delta_pop_send), min(t_delta_pop_send)))
        f_report.write('\t\t\t\t\t（假设正常情况下连续弹窗在 %d 以内） '
                       '\n\t平均发生周期 %f 秒\n\t最大 %f 秒\n\t最小 %f 秒'
                       % (t_gap, np.average(t_delta_pop_send), max(t_delta_pop_send), min(t_delta_pop_send)))
    # 点击发送 - 已发送弹窗
    print('\n\n点击发送-已发送弹窗 对数：%d\t（假设正常情况下连续时间击在 %d 以内）' % (num_click_pop_pairs, t_gap))
    f_report.write('\n\n点击发送-已发送弹窗 对数：%d\t\t\t（假设正常情况下连续时间击在 %d 以内）' % (num_click_pop_pairs, t_gap))
    if list_time_response:
        print('响应时间 \n\t平均发生周期 %f 秒\n\t最大 %f 秒\n\t最小 %f 秒'
              % (np.average(list_time_response), max(list_time_response), min(list_time_response)))
        f_report.write('\n\t平均发生周期（响应时间） %f 秒\n\t最大 %f 秒\n\t最小 %f 秒'
                       % (np.average(list_time_response), max(list_time_response), min(list_time_response)))
    if num_click_send > 0:
        print('点击发送-已发送弹窗 完成率（点击发送-已发送弹窗的对数/点击发送次数）：\n\t%f' % (
                float(num_click_pop_pairs) / float(num_click_send)))
        f_report.write('\n\n\t点击发送-已发送弹窗 完成率（点击发送-已发送弹窗的对数/点击发送次数）：\n\t%f' % (
                float(num_click_pop_pairs) / float(num_click_send)))
    else:
        print('未查到 点击发送-已发送弹窗 记录...')
        f_report.write('未查到 点击发送-已发送弹窗 记录...')


for host_name in list_host_name:
    run(host_name)






"""

1. 为什么在前
    ['已发送弹窗',
        '—— 当前顶部窗口为ToastWindow,大小为150x50,屏幕缩放比例为1.25 ——'],



"""
