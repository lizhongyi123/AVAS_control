import struct

def density_file_reading(path):
    res = {}
    data_dict_lis = []
    moy_lis = []  #平均值, x, y, phase, e,r, z, dp/p
    moy2_lis = [] #平方值
    maxb_lis = [] #最大偏移
    minb_lis = [] #最小偏移

    maxR_lis = [] #最大光束尺寸或颗粒的最小值
    minR_lis = [] #最小尺寸的最大值

    rms_size_lis = [] #rms尺寸
    rms_size2_lis = [] #Squared beam rms size

    min_pos_moy_lis = []  #Min. if the beam average
    max_pos_moy_lis = []  #Maximum if the beam average

    rms_emit_lis = [] #rms emittances, xx’, yy’, zdp (m.rad)*/
    rms_emit2_lis = [] #Squared rms emittances, xx’, yy’, zdp

    lost_lis = []  #束损
    Milost_lis = [] #最小束损
    Malost_lis = [] #最大束损

    tab_lis = []
    stab_lis = []
    tabp_lis = []
    with open(path, "rb") as f:
        # 获取文件大小
        f.seek(0, 2)  # 移动到文件末尾
        longfichier = f.tell()
        f.seek(0, 0)  # 返回文件开头
        print(9)
        while True:
            # 读取固定大小的数据块
            data_dict = {}
            ver, year, vlong, Nrun, nelp, ib, Zg, Xouv, Youv, dXouv, dYouv, step = struct.unpack("<hhhiiffffffi", f.read(42))

            data_dict["ver"] = ver
            data_dict["year"] = year
            data_dict["vlong"] = vlong
            data_dict["Nrun步数"] = Nrun
            data_dict["nelp 元件"] = nelp
            data_dict["ib"] = ib
            data_dict["Zg 位置"] = Zg
            data_dict["Xouv 横向孔径"] = Xouv
            data_dict["Youv 纵向孔径"] = Youv
            data_dict["dXouv  水平孔径位移"] = dXouv
            data_dict["dYouv 纵向孔径位移"] = dYouv
            data_dict["step 步数"] = step
            data_dict_lis.append(data_dict)
            # print(data_dict)

            moy = struct.unpack("<fffffff", f.read(28))
            # print("平均值")
            # print(moy)
            moy_lis.append(moy)

            moy2 = struct.unpack("<fffffff", f.read(28))
            # print("平方值")
            # print(moy2)
            moy2_lis.append(moy2)

            maxb = struct.unpack("<fffffff", f.read(28))
            # print("最大尺寸")
            # print(maxb)
            maxb_lis.append(maxb)

            minb = struct.unpack("<fffffff", f.read(28))
            # print("最小尺寸")
            # print(minb)
            minb_lis.append(minb)

            if ver >= 11:
                #绝对相位，
                phaseF, phaseG = struct.unpack("<ff", f.read(8))
                # print("绝对参考相位")
                # print(phaseF, phaseG)

            if ver >= 10:
                #最大尺寸或者最小尺寸
                maxR = struct.unpack("<fffffff", f.read(28))
                minR = struct.unpack("<fffffff", f.read(28))
                # print("最大尺寸或者最小尺寸")
                # print(maxR)
                # print(minR)
                maxR_lis.append(maxR)
                minR_lis.append(minR)

            if ver >= 5:
                #rms尺寸
                rms_size = struct.unpack("<fffffff", f.read(28))
                rms_size2 = struct.unpack("<fffffff", f.read(28))
                # print("rms尺寸")
                # print(rms_size)
                # print(rms_size2)
                rms_size_lis.append(rms_size)
                rms_size2_lis.append(rms_size2)

            if ver >= 6:
                print("")
                min_pos_moy = struct.unpack("<fffffff", f.read(28))
                max_pos_moy = struct.unpack("<fffffff", f.read(28))
                # print(min_pos_moy)
                # print(max_pos_moy)
                min_pos_moy_lis.append(min_pos_moy)
                max_pos_moy_lis.append(max_pos_moy)

            if ver >= 7:
                rms_emit = struct.unpack("<fff", f.read(12))
                rms_emit2 = struct.unpack("<fff", f.read(12))
                # print("rms发射度")
                # print(rms_emit)
                # print(rms_emit2)
                rms_emit_lis.append(rms_emit)
                rms_emit2_lis.append(rms_emit2)

            if ver >= 8:
                Eouv, PhPouv, PhMouv = struct.unpack("<fff", f.read(12))
                # print("能量,  正向接收，负向接收")
                # print(Eouv, PhPouv, PhMouv)

            Np = struct.unpack("<q", f.read(8))[0]
            # print("粒子数", Np)
            if Np > 0:
                # 读取粒子损失和束流功率损失数据
                lost = []
                powlost = []
                for i in range(Nrun):
                    lost.append(struct.unpack("<q", f.read(8))[0])
                    powlost.append(struct.unpack("<f", f.read(4))[0])
                # print(lost)
                # print(powlost)
                lost_lis.append(lost)

                #损失的平方
                lost2 = struct.unpack("<q", f.read(8))[0]
                # print(lost2)
                #最小损失

                Milost = struct.unpack("<q", f.read(8))[0]
                # print(Milost)
                Milost_lis.append(Milost)

                #最大损失
                Malost = struct.unpack("<q", f.read(8))[0]
                # print(Malost)
                Malost_lis.append(Malost)

                powlost2 = struct.unpack("<d", f.read(8))[0]

                Mipowlost = struct.unpack("<f", f.read(4))[0]
                Mapowlost = struct.unpack("<f", f.read(4))[0]

                # 读取束流分布数据
                tab = [[] for _ in range(7)]
                stab = [[] for _ in range(7)]

                for j in range(7):
                    if vlong == 1:
                        tab[j] = struct.unpack(f"<{step}Q", f.read(step * 8))
                    else:
                        stab[j] = struct.unpack(f"<{step}I", f.read(step * 4))
                # print(tab[0])
                stab_lis.append(stab)
                if ib > 0:
                    tabp = [[] for _ in range(3)]

                    for j in range(3):
                        tabp[j] = struct.unpack(f"<{step}f", f.read(step * 4))
                tabp_lis.append(tabp)
            # 跳出循环条件
            if f.tell() + 16 >= longfichier:
                break
    res["data_dict_lis"] = data_dict_lis
    res["moy_lis"] = moy_lis
    res["moy2_lis"] = moy2_lis
    res["maxb_lis"] = maxb_lis
    res["minb_lis"] = minb_lis
    res["maxR_lis"] = maxR_lis
    res["minR_lis"] = minR_lis
    res["rms_size_lis"] = rms_size_lis
    res["rms_size2_lis"] = rms_size2_lis
    res["min_pos_moy_lis"] = min_pos_moy_lis
    res["max_pos_moy_lis"] = max_pos_moy_lis
    res["rms_emit_lis"] = rms_emit_lis
    res["rms_emit2_lis"] = rms_emit2_lis
    res["lost_lis"] = lost_lis
    res["Milost_lis"] = Milost_lis
    res["Malost_lis"] = Malost_lis
    res["stab_lis"] = stab_lis
    res["tabp_lis"] = tabp_lis
    return res


if __name__ =="__main__":
    path = r"C:\Users\shliu\Desktop\test_density\result\Density_PAR.dat"
    res = density_file_reading(path)
    zg = [i["Zg 位置"]for i in res['data_dict_lis']]
    print(zg)
    z = [i[5]for i in res['moy_lis']]
    print(z)