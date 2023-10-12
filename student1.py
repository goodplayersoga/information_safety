import tkinter as tk
import time
from tkinter import messagebox as msg
m = 1
def P10(key):
    k = [None] + key
    return [k[3], k[5], k[2], k[7], k[4], k[10], k[1], k[9], k[8], k[6]]
def P8(key):
    k = [None] + key
    return [k[6], k[3], k[7], k[4], k[8], k[5], k[10], k[9]]

def Shift(value):
    return value[1:] + value[0:1]
def IP(value):
    k = [None] + value
    return [k[2], k[6], k[3], k[1], k[4], k[8], k[5], k[7]]

def IPinv(value):
    k = [None] + value
    return [k[4], k[1], k[3], k[5], k[7], k[2], k[8], k[6]]
def SW(value):
    return value[4:] + value[:4]
S0 = [[1, 0, 3, 2],
     [3, 2, 1, 0],
     [0, 2, 1, 3],
     [3, 1, 0, 2]]

S1 = [[0, 1, 2, 3],
     [2, 3, 1, 0],
     [3, 0, 1, 2],
     [2, 1, 0, 3]]
def F(value, key):
    val = lambda x, y: x * 2 + y
    def highLow(x):
        a = 1 if x & 0b10 > 0 else 0
        b = x & 0b01
        return a, b
    P = [[0, 0, 0, 0],
         [0, 0, 0, 0]]
    n = [None] + value
    k = [None] * 11 + key  # 这里前面空11无用的值None
    P[0][0] = n[4] ^ k[11]
    P[0][1] = n[1] ^ k[12]
    P[0][2] = n[2] ^ k[13]
    P[0][3] = n[3] ^ k[14]
    P[1][0] = n[2] ^ k[15]
    P[1][1] = n[3] ^ k[16]
    P[1][2] = n[4] ^ k[17]
    P[1][3] = n[1] ^ k[18]
    row0 = val(P[0][0], P[0][1])
    col0 = val(P[0][2], P[0][3])
    row1 = val(P[1][0], P[1][1])
    col1 = val(P[1][2], P[1][3])
    v1, v2 = highLow(S0[row0][col0])
    v3, v4 = highLow(S1[row1][col1])
    return [v2, v4, v3, v1]

def fK(value, key):
    L = value[:4]
    R = value[4:]
    return list(map(lambda x: x[0] ^ x[1], zip(L, F(R, key)))) + R
def sdesEncryptByte(value, key):
    K1 = P8(Shift(P10(key)))
    K2 = P8(Shift(Shift(P10(key))))
    fK1Value = fK(IP(value), K1)
    swValue = SW(fK1Value)
    fK2Value = fK(swValue, K2)
    return IPinv(fK2Value)
def sdesDecryptByte(value, key):
    K1 = P8(Shift(P10(key)))
    K2 = P8(Shift(Shift(P10(key))))
    fK2Value = fK(IP(value), K2)
    swValue = SW(fK2Value)
    fK1Value = fK(swValue, K1)
    return IPinv(fK1Value)
root = tk.Tk()
root.title("计算界面")
root.geometry("380x200")
root.configure(bg="#F9F9F9")
# 创建标签和输入框
label1 = tk.Label(root, text="输入明文:", font=("微软雅黑", 12), bg="#F9F9F9")
entry1 = tk.Entry(root,  font=("微软雅黑", 12), width=20, bd=2)
label2 = tk.Label(root, text="输入密钥:", font=("微软雅黑", 12), bg="#F9F9F9")
entry2 = tk.Entry(root, font=("微软雅黑", 12), width=20, bd=2)
label3 = tk.Label(root, text="输入密文:", font=("微软雅黑", 12), bg="#F9F9F9")
entry3 = tk.Entry(root,  font=("微软雅黑", 12), width=20, bd=2)
label4 = tk.Label(root, text="输入密钥:", font=("微软雅黑", 12), bg="#F9F9F9")
entry4 = tk.Entry(root, font=("微软雅黑", 12), width=20, bd=2)
label5 = tk.Label(root, text="输入明文:", font=("微软雅黑", 12), bg="#F9F9F9")
entry5 = tk.Entry(root,  font=("微软雅黑", 12), width=20, bd=2)
label6 = tk.Label(root, text="输入密文:", font=("微软雅黑", 12), bg="#F9F9F9")
entry6 = tk.Entry(root, font=("微软雅黑", 12), width=20, bd=2)

# 创建按钮来触发函数
def encry_result():

    # 获取输入的参数值
    param1 = entry1.get()
    param2 = entry2.get()
    if m == 0:
        param1_list = [int(bit) for bit in param1]
        param2_list = [int(bit) for bit in param2]
        result = sdesEncryptByte(param1_list, param2_list)
        encry_label.config(text=f"结果: {result}")
    else:
        # 初始化一个空的列表来存储二进制位
        param1_list = []

        # 处理字符串中的每个字符
        for char in param1:
            if char.isalpha():  # 如果字符是字母
                # 将字符转换为二进制
                param1_list.extend([int(bit) for bit in format(ord(char), '08b')])
            elif char.isdigit():  # 如果字符是数字
                # 将数字字符转换为整数，然后转换为二进制
                param1_list.extend([int(bit) for bit in format(int(char), '08b')])
        # 转换为列表
        param2_list = [int(bit) for bit in param2]

        result0 = []
        for i in range(0, len(param1_list), 8):
            # 取出8位作为参数调用函数
            eight_bits = param1_list[i:i + 8]
            result0.append(sdesEncryptByte(eight_bits, param2_list))
        # 遍历每个子列表，将二进制数字转换为整数，并将整数解释为ASCII字符

        # ascii_characters = [chr(int("".join(map(str, sublist), 2)) for sublist in result0)]

        # 将ASCII字符连接成一个字符串0
        result = ''.join([chr(int(''.join(map(str, sublist)), 2)) for sublist in result0])

        # 显示结果
        encry_label.config(text=f"结果: {result}")

def viocrack():
    param1 = entry5.get()
    param2 = entry6.get()
    result = []
    start_time = time.time()
    for i in range(1024):
        # 将整数转换为二进制字符串
        binary_string = bin(i)[2:]  # [2:] 是为了去除 '0b' 前缀

        # 添加零位填充到10位
        if len(binary_string) < 10:
            binary_string = '0' * (10 - len(binary_string)) + binary_string
        binary_list = [int(bit) for bit in binary_string]
        if m == 0:
            param1_list = [int(bit) for bit in param1]
            param2_list = [int(bit) for bit in param2]
            result0 = sdesEncryptByte(param1_list, binary_list)
            if result0 == param2_list:
                binary0 = "".join(str(binary_list))
                result.append(binary0)
        else:
            # 初始化一个空的列表来存储二进制位
            param1_list = []

            # 处理字符串中的每个字符
            for char in param1:
                if char.isalpha():  # 如果字符是字母
                    # 将字符转换为二进制
                    param1_list.extend([int(bit) for bit in format(ord(char), '08b')])
                elif char.isdigit():  # 如果字符是数字
                    # 将数字字符转换为整数，然后转换为二进制
                    param1_list.extend([int(bit) for bit in format(int(char), '08b')])

            result0 = []
            for i in range(0, len(param1_list), 8):
                # 取出8位作为参数调用函数
                eight_bits = param1_list[i:i + 8]
                result0.append(sdesEncryptByte(eight_bits, binary_list))
            # 遍历每个子列表，将二进制数字转换为整数，并将整数解释为ASCII字符

            # 将ASCII字符连接成一个字符串0
            results = ''.join([chr(int(''.join(map(str, sublist)), 2)) for sublist in result0])
            if results == param2:
                result.append(binary_list)
    end_time = time.time()
    strs = "\n密钥：".join(result) + "\n用时："+str(end_time-start_time)
    tk.Tk().withdraw()
    msg.showinfo("全部可能密钥", strs)
    # break_label.config(text=f"密钥：{result}\n用时：{end_time-start_time}")


def decry_result():

    # 获取输入的参数值
    param1 = entry3.get()
    param2 = entry4.get()
    if m == 0:
        param1_list = [int(bit) for bit in param1]
        param2_list = [int(bit) for bit in param2]
        result = sdesDecryptByte(param1_list, param2_list)
        decry_label.config(text=f"结果: {result}\n")
    else:
        # 初始化一个空的列表来存储二进制位
        param1_list = []

        # 处理字符串中的每个字符
        for char in param1:
            if char.isalpha():  # 如果字符是字母
                # 将字符转换为二进制
                param1_list.extend([int(bit) for bit in format(ord(char), '08b')])
            elif char.isdigit():  # 如果字符是数字
                # 将数字字符转换为整数，然后转换为二进制
                param1_list.extend([int(bit) for bit in format(int(char), '08b')])
        # 转换为列表
        param2_list = [int(bit) for bit in param2]

        result0 = []
        for i in range(0, len(param1_list), 8):
            # 取出8位作为参数调用函数
            eight_bits = param1_list[i:i + 8]
            result0.append(sdesDecryptByte(eight_bits, param2_list))
        # 遍历每个子列表，将二进制数字转换为整数，并将整数解释为ASCII字符

        # 将ASCII字符连接成一个字符串0
        result = ''.join([chr(int(''.join(map(str, sublist)), 2)) for sublist in result0])

        # 显示结果
        decry_label.config(text=f"结果: {result}\n")


# 0：字符串； 1：二进制
def changeturn():
    global m
    if m == 0:
        m = 1
    else:
        m = 0


# 加密
encry_button = tk.Button(root, text="加密", font=(
    "微软雅黑", 12), bg="#000080", fg="#FFFFFF", command=encry_result)
encry_label = tk.Label(root, text="结果: ", font=("微软雅黑", 12), bg="#F9F9F9")
# 布局管理
label1.grid(row=0, column=0, padx=20, pady=10)
entry1.grid(row=0, column=1, padx=20, pady=10)
label2.grid(row=1, column=0, padx=20, pady=10)
entry2.grid(row=1, column=1, padx=20, pady=10)
encry_button.grid(row=2, column=0, padx=20, pady=10)
encry_label.grid(row=2, column=1, padx=20, pady=10)

# 解密
decry_button = tk.Button(root, text="解密", font=(
    "微软雅黑", 12), bg="#000080", fg="#FFFFFF", command=decry_result)
decry_label = tk.Label(root, text="结果: ", font=("微软雅黑", 12), bg="#F9F9F9")
# 布局管理
label3.grid(row=3, column=0, padx=20, pady=10)
entry3.grid(row=3, column=1, padx=20, pady=10)
label4.grid(row=4, column=0, padx=20, pady=10)
entry4.grid(row=4, column=1, padx=20, pady=10)
decry_button.grid(row=5, column=0, padx=20, pady=10)
decry_label.grid(row=5, column=1, padx=20, pady=10)

# 破解
break_button = tk.Button(root, text="暴力破解", font=(
    "微软雅黑", 12), bg="#000080", fg="#FFFFFF", command=viocrack)
break_label = tk.Label(root, text="结果: ", font=("微软雅黑", 12), bg="#F9F9F9")

# 布局管理
label5.grid(row=6, column=0, padx=20, pady=10)
entry5.grid(row=6, column=1, padx=20, pady=10)
label6.grid(row=7, column=0, padx=20, pady=10)
entry6.grid(row=7, column=1, padx=20, pady=10)
break_button.grid(row=8, column=0, padx=20, pady=10)
# break_label.grid(row=8, column=1, padx=20, pady=10)

# 切换二进制输入和字符串输入
change_button = tk.Button(root, text="切换（二进制/字符串）", font=(
    "微软雅黑", 12), bg="#000080", fg="#FFFFFF", command=changeturn)
change_button.grid(row=9, column=0, padx=20, pady=10)

# 设置窗口大小和位置
window_width = 500
window_height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# 启动主循环
root.mainloop()
