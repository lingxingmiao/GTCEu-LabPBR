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
    法线图像 = Mpbr.image2normal(fp, ao=False, eazy_mode="decimal", eazy=16)
    法线图像.save(fp) 
def 构建(path: str):
    缓存文件夹 = 随机16进制字符串()
    缓存路径 = str((Path("./cache") / 缓存文件夹).resolve())
    shutil.copytree(path, 缓存路径, dirs_exist_ok=True)
    未构建法线纹理图像 = [str(index) for index in Path(缓存路径).rglob('*_n.png')]
    _emissive发光纹理路径 = [str(index) for index in Path(缓存路径).rglob('*_emissive.png')]
    for index in tqdm(_emissive发光纹理路径, desc="发光图像"):
        _emissive发光纹理单路径 = Path(index)
        _emissive发光纹理数组 = np.array(img.open(index).convert('L'))
        _emissive发光纹理数组 += (254 - _emissive发光纹理数组.max())
        高, 宽 = _emissive发光纹理数组.shape[:2]
        _emissive发光纹理图像 = np.zeros((高, 宽, 4), dtype=np.uint8)
        _emissive发光纹理图像[:, :, 0] = 0      # R 通道
        _emissive发光纹理图像[:, :, 1] = 0      # G 通道  
        _emissive发光纹理图像[:, :, 2] = 255    # B 通道
        _emissive发光纹理图像[:, :, 3] = _emissive发光纹理数组  # A 通道
        _emissive发光纹理图像 = img.fromarray(_emissive发光纹理图像.get(), mode='RGBA')
        _emissive发光纹理图像.save(Path(f"{_emissive发光纹理单路径.parent}/{_emissive发光纹理单路径.stem}_s.png"))
    未构建法线纹理外图像 = [str(index)  for index in Path(缓存路径).rglob('*.png')  if not index.name.endswith('_n.png')]
    for index in tqdm(未构建法线纹理外图像, desc="放大图像"):
        原图 = img.open(index)
        宽, 高 = 原图.size
        放大图 = 原图.resize((宽 * 8, 高 * 8), img.NEAREST)
        放大图.save(index)
    线程数 = mp.cpu_count() // 2
    with mp.Pool(processes=线程数) as 池:
        处理函数 = partial(构建单个图像)
        list(tqdm(池.imap(处理函数, 未构建法线纹理图像), total=len(未构建法线纹理图像), desc="构建法线"))
    return 缓存路径

if __name__ == '__main__':
    输出路径 = 构建(r"./")
    目标路径对象 = Path(r"./构建文件夹")
    """if 目标路径对象.exists():
        shutil.rmtree(目标路径对象)"""
    shutil.copytree(输出路径, 目标路径对象, dirs_exist_ok=True)
