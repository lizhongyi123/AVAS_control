import struct
import numpy as np
np.set_printoptions(threshold=np.inf)

def read_field_1d(filename):
    with open(filename, "rb") as f:

        # --- 读头 ---
        nz = struct.unpack("i", f.read(4))[0]
        zmax = struct.unpack("d", f.read(8))[0]

        nx = struct.unpack("i", f.read(4))[0]
        xmin = struct.unpack("d", f.read(8))[0]
        xmax = struct.unpack("d", f.read(8))[0]

        ny = struct.unpack("i", f.read(4))[0]
        ymin = struct.unpack("d", f.read(8))[0]
        ymax = struct.unpack("d", f.read(8))[0]

        print("nz,nx,ny =", nz, nx, ny)
        print("zmax,xmin,xmax,ymin,ymax,norm =", zmax, xmin, xmax, ymin, ymax)
        norm = struct.unpack("d", f.read(8))[0]

        total = (nz + 1) * (ny + 1) * (nx + 1)

        # 👉 直接读成一维
        data = np.fromfile(f, dtype=np.float32, count=total)

    header = dict(
        nz=nz, zmax=zmax,
        nx=nx, xmin=xmin, xmax=xmax,
        ny=ny, ymin=ymin, ymax=ymax,
        norm=norm
    )

    return header, data


def write_field_1d(filename, header, data):
    with open(filename, "wb") as f:

        f.write(struct.pack(
            "i d i d d i d d d",
            header["nz"], header["zmax"],
            header["nx"], header["xmin"], header["xmax"],
            header["ny"], header["ymin"], header["ymax"],
            header["norm"]
        ))

        data.astype(np.float32).tofile(f)


def add_one_to_field(infile, outfile):
    header, data = read_field_1d(infile)

    # 👉 一维数组直接加
    data += 1.0

    write_field_1d(outfile, header, data)


def save_field_to_txt(txtfile, header, data):
    with open(txtfile, "w", encoding="utf-8") as f:
        # 头部
        f.write(f"{header['nz']:12d}{header['zmax']:24.15E}\n")
        f.write(f"{header['nx']:12d}{header['xmin']:24.15E}{header['xmax']:24.15E}\n")
        f.write(f"{header['ny']:12d}{header['ymin']:24.15E}{header['ymax']:24.15E}\n")
        f.write(f"{header['norm']:12.0f}\n")

        # 数据区：每行一个值
        for v in data:
            f.write(f"{v:16.8f}\n")

if __name__ == "__main__":

    # directory = "C:\Users\wangh\Desktop\0207_field"
    field_path = r"C:\Users\wangh\Desktop\324\64newb.bsz"
    header, data = read_field_1d(field_path)
    np.set_printoptions(threshold=np.inf)
    print(np.max(data), np.min(data))

    txt_path = r"C:\Users\wangh\Desktop\324\64new.bsz"
    save_field_to_txt(txt_path, header, data)
    print("已保存到:", txt_path)




# 使用
# add_one_to_field("field.bin", "field_plus1.bin")
