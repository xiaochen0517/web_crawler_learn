import numpy as np

def dot_product(vector_a, vector_b, mode="error"):
    """
    计算两个向量的点积，可处理不同维度的情况
    
    参数:
        vector_a (list or numpy.ndarray): 第一个向量
        vector_b (list or numpy.ndarray): 第二个向量
        mode (str): 处理不同维度向量的模式:
            - "error": 维度不同时抛出错误(默认)
            - "pad_zeros": 用零填充较短的向量
            - "truncate": 截断较长的向量以匹配较短的向量
            - "min_dims": 只考虑两个向量共有的维度
    
    返回:
        float: 两个向量的点积结果
    """
    # 转换为numpy数组以确保兼容性
    a = np.array(vector_a)
    b = np.array(vector_b)
    
    # 检查维度是否匹配
    if a.shape != b.shape:
        if mode == "error":
            raise ValueError("两个向量的维度不同，无法直接计算点积")
        elif mode == "pad_zeros":
            # 用零填充较短的向量
            max_len = max(len(a), len(b))
            a = np.pad(a, (0, max_len - len(a)), 'constant')
            b = np.pad(b, (0, max_len - len(b)), 'constant')
        elif mode == "truncate":
            # 截断较长的向量
            min_len = min(len(a), len(b))
            a = a[:min_len]
            b = b[:min_len]
        elif mode == "min_dims":
            # 只计算共有维度的点积
            min_len = min(len(a), len(b))
            a = a[:min_len]
            b = b[:min_len]
        else:
            raise ValueError("无效的模式。可选值: 'error', 'pad_zeros', 'truncate', 'min_dims'")
    
    # 使用numpy的dot函数计算点积
    return np.dot(a, b)

def cross_product(vector_a, vector_b, mode="error"):
    """
    计算两个向量的叉积，可处理不同维度的情况
    
    参数:
        vector_a (list or numpy.ndarray): 第一个向量
        vector_b (list or numpy.ndarray): 第二个向量
        mode (str): 处理不同维度向量的模式:
            - "error": 维度不同时抛出错误(默认)
            - "pad_zeros": 用零填充向量至3维
            - "truncate": 截断向量至3维或2维
            - "force_3d": 强制将向量转为3维(填充0或截断)
            - "force_2d": 强制将向量转为2维(填充0或截断)
    
    返回:
        numpy.ndarray 或 float: 两个向量的叉积结果
    
    注意:
        - 标准叉积只在3维空间中定义
        - 对于2维向量，返回的是它们张成的平行四边形的有向面积(标量)
    """
    # 转换为numpy数组
    a = np.array(vector_a)
    b = np.array(vector_b)
    
    # 检查维度
    if len(a) != len(b):
        if mode == "error":
            raise ValueError("两个向量的维度不同，无法直接计算叉积")
        elif mode == "pad_zeros":
            # 用零填充至3维
            a = np.pad(a, (0, max(0, 3 - len(a))), 'constant')
            b = np.pad(b, (0, max(0, 3 - len(b))), 'constant')
        elif mode == "truncate":
            # 截断至共有维度，但最多3维
            min_len = min(len(a), len(b), 3)
            a = a[:min_len]
            b = b[:min_len]
        elif mode == "force_3d":
            # 强制转为3维
            a = np.pad(a, (0, max(0, 3 - len(a))), 'constant')[:3]
            b = np.pad(b, (0, max(0, 3 - len(b))), 'constant')[:3]
        elif mode == "force_2d":
            # 强制转为2维
            a = np.pad(a, (0, max(0, 2 - len(a))), 'constant')[:2]
            b = np.pad(b, (0, max(0, 2 - len(b))), 'constant')[:2]
        else:
            raise ValueError("无效的模式。可选值: 'error', 'pad_zeros', 'truncate', 'force_3d', 'force_2d'")
    
    # 根据维度计算叉积
    if len(a) == 2:
        # 2维向量的叉积（结果是标量，表示有向面积）
        return a[0]*b[1] - a[1]*b[0]
    elif len(a) == 3:
        # 3维向量的标准叉积
        return np.cross(a, b)
    else:
        raise ValueError("处理后的向量维度必须是2或3，目前为: " + str(len(a)))

# 演示用法
if __name__ == "__main__":
    # 示例向量（不同维度）
    v1 = [1, 2]         # 2维向量
    v2 = [4, 5, 6]      # 3维向量
    v3 = [1, 2, 3, 4]   # 4维向量
    
    print("==== 不同维度向量的点积计算 ====")
    
    # 使用零填充模式计算点积
    dot_result1 = dot_product(v1, v2, mode="pad_zeros")
    print(f"向量 {v1} 和 {v2} 的点积(零填充): {dot_result1}")  # [1,2,0]·[4,5,6] = 1*4 + 2*5 + 0*6 = 14
    
    # 使用截断模式计算点积
    dot_result2 = dot_product(v3, v2, mode="truncate")
    print(f"向量 {v3} 和 {v2} 的点积(截断): {dot_result2}")  # [1,2,3]·[4,5,6] = 1*4 + 2*5 + 3*6 = 32
    
    # 使用最小维度模式计算点积
    dot_result3 = dot_product(v1, v3, mode="min_dims")
    print(f"向量 {v1} 和 {v3} 的点积(最小维度): {dot_result3}")  # [1,2]·[1,2] = 1*1 + 2*2 = 5
    
    print("\n==== 不同维度向量的叉积计算 ====")
    
    # 使用填充模式计算叉积
    cross_result1 = cross_product(v1, v2, mode="pad_zeros")
    print(f"向量 {v1} 和 {v2} 的叉积(零填充): {cross_result1}")  # [1,2,0]×[4,5,6] = [12,-6,-3]
    
    # 强制转为2维后计算叉积
    cross_result2 = cross_product(v3, v2, mode="force_2d")
    print(f"向量 {v3} 和 {v2} 的叉积(强制2维): {cross_result2}")  # [1,2]×[4,5] = 1*5 - 2*4 = -3
    
    # 强制转为3维后计算叉积
    cross_result3 = cross_product(v1, v3, mode="force_3d")
    print(f"向量 {v1} 和 {v3} 的叉积(强制3维): {cross_result3}")  # [1,2,0]×[1,2,3] = [6,-3,0]