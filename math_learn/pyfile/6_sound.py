import pygame, pygame.sndarray
import numpy as np


def make_sinusoid(frequency, amplitude):
    def f(t):
        return amplitude * np.sin(2 * np.pi * frequency * t)

    return f


def sample(f, start, end, count):  # 输入是要被采样的函数f、采样的起点start和终点end，以及要采样多少个值count
    mapf = np.vectorize(f)  # 创建一个可以用于NumPy数组的f
    ts = np.arange(start, end, (end - start) / count)  # 在指定的范围上，创建等间距的值作为函数输入
    values = mapf(ts)  # 对NumPy数组的每个值应用函数f
    return values.astype(np.int16)  # 把结果数组转化为16位整数并返回


def apply_channels(*samples, channels=2):
    """
    将多个声音样本应用到指定的通道上
    :param samples: 声音样本
    :param channels: 通道数
    :return:
    """
    result_samples = []
    if channels == 1:
        for i in range(len(samples)):
            result_samples.append(samples[i].reshape(-1))
    else:
        for i in range(len(samples)):
            # 复制数据到两个通道
            result_samples.append(np.column_stack((samples[i], samples[i])))
    return result_samples


def play_sound(*sounds, channels=2):
    """
    播放声音
    :param sounds: 声音数组
    :return:
    """
    sounds = apply_channels(*sounds, channels=channels)
    sound_control_list = []
    for sound in sounds:
        sound_control = pygame.sndarray.make_sound(sound)
        sound_control_list.append(sound_control)
    for sound_control in sound_control_list:
        sound_control.play()


def run():
    pygame.mixer.init(
        frequency=44100,
        size=-16,  # −16表示位深为16，输入为16位有符号整数，从−32 768到32 767
        channels=1,
    )

    # 检查实际初始化的混音器通道数
    actual_channels = pygame.mixer.get_init()[2]
    print(f"混音器实际通道数: {actual_channels}")

    # 创建一维数组
    # sound_arr = np.random.randint(-10000, 10000, size=44100, dtype=np.int16)
    # sound_arr = np.repeat([10000, -10000], 80).astype(np.int16)
    # sound_arr = np.tile(sound_arr, 551)
    # sound_arr = sample(make_sinusoid(441, 9000), 0, 1, 44100)
    sample1 = sample(make_sinusoid(441, 9000), 0, 1, 44100)
    sample2 = sample(make_sinusoid(551, 9000), 0, 1, 44100)

    # play_sound(sample1, sample2, channels=actual_channels)
    play_sound(sample1 + sample2, channels=actual_channels)

    # 保持程序运行一段时间以听到声音
    # pygame.time.wait(2000)  # 等待1秒
    while pygame.mixer.get_busy():
        pygame.time.delay(100)  # 每100毫秒检查一次


if __name__ == '__main__':
    run()
    pygame.quit()
