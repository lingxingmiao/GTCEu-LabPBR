import multiprocessing as mp
import shutil
import random
import cupy as np
from functools import partial
from PIL import Image as img
from tqdm import tqdm
from Mpbr import Mpbr
from pathlib import Path
def 随机16进制字符串():
    return '-'.join([f'{random.randint(0, 0xFFFF):04X}' for _ in range(4)])
def 构建单个图像(fp):
    try:
        法线图像 = Mpbr.image1normal2map(Mpbr.open(f"{Path(fp).parent}/{Path(fp).name.replace('_n.png', '.png')}"), Mpbr.image2normal(fp, eazy_mode="decimal", eazy=16, ao_int=1.2), zoom=True)
        法线图像.save(f"{Path(fp).parent}/{Path(fp).name.replace('_n.png', '.png')}") 
    except Exception as e:
        print(f"处理图像 {fp} 时发生错误: {e}")
def 构建(path: str):
    缓存文件夹 = 随机16进制字符串()
    缓存路径 = str((Path("./cache") / 缓存文件夹).resolve())
    shutil.copytree(path, 缓存路径, dirs_exist_ok=True)
    未构建法线纹理图像 = [str(index) for index in Path(缓存路径).rglob('*_n.png')]
    线程数 = mp.cpu_count() // 2
    with mp.Pool(processes=线程数) as 池:
        处理函数 = partial(构建单个图像)
        list(tqdm(池.imap(处理函数, 未构建法线纹理图像), total=len(未构建法线纹理图像), desc="构建法线"))
    for index in 未构建法线纹理图像 + [str(index) for index in Path(缓存路径).rglob('*_s.png')]:
        Path(index).unlink(missing_ok=True)
    return 缓存路径

if __name__ == '__main__':
    输出路径 = 构建(r"./格雷科技PBR未构建")
    目标路径对象 = Path(r"C:\Users\FengMang\AppData\Roaming\PrismLauncher\instances\Cleanroom-MMC-instance-0.3.0-alpha\minecraft\resourcepacks\GregTech PBR测试3")
    """if 目标路径对象.exists():
        shutil.rmtree(目标路径对象)"""
    shutil.copytree(输出路径, 目标路径对象, dirs_exist_ok=True)