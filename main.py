########################################################################################################################
#                                                   2017253019 안희영                                                   #
########################################################################################################################
import numpy as np
import matplotlib.pyplot as plt
header_size = 54
cmp_size = 1024
image_height = 512
image_width = 512
end_in_min = 42
end_in_max = 210
file_name = "lena_bmp_512x512_new.bmp"
test_mask = np.array([[0, -1, 0], [-1, 4, -1], [0, -1, 0]])


def image_read(file):
    with open(file, "rb") as f:
        rectype = np.dtype(np.uint8)
        image_data = np.fromfile(f, dtype=rectype)
    header = image_data[0:header_size]
    cmp = image_data[header_size:cmp_size + header_size]
    data = image_data[len(image_data):cmp_size + header_size - 1:-1].reshape((image_height, image_width))
    data = np.flip(data, axis=1)
    return header, cmp, data


def lut_to_data(lut, origin_data):
    out_data = np.zeros((image_height, image_width), dtype='u1')
    for index in range(image_height):
        for E in range(image_width):
            out_data[E][index] = lut[origin_data[E][index]]
    return out_data


def image_write(name, header, cmp, image):
    with open(name, "wb") as f:
        f.write(bytes(header))
        f.write(bytes(cmp))
        f.write(bytes( np.flipud(image)))


def clamping(origin_data):
    out_data = np.zeros((image_height, image_width), dtype='u1')
    for index in range(image_height):
        for E in range(image_width):
            if origin_data[E][index] > 0xff:
                out_data[E][index] = 0xff
            elif origin_data[E][index] < 0x0:
                out_data[E][index] = origin_data[E][index]
            else:
                out_data[E][index] = 0x0
    return out_data


def masking(data, mask):
    out_data = np.zeros((image_height, image_width))
    for i in range(image_width):
        for e in range(image_height):
            out_data[i][e] = np.sum(data[i:i+3, e:e+3]*mask)
    return out_data


def padding(data):
    out_data = np.zeros((image_height+2, image_width+2))
    for i in range(len(out_data)):
        for e in range(len(out_data)):
            if (i == 0 or i == len(out_data)-1) and (e == 0 or e == len(out_data)-1):
                pass
            elif i == 0:

            elif i == len(out_data)-1):
            elif e == 0:
            elif e == len(out_data)-1:
            else:
                out_data[i][e] = data[i-1][e-1]


    out_data[0][0]=data[0][0]
    out_data[0][len(out_data)-1]
    return out_data


bmp_header, bmp_cmp, bmp_data = image_read(file_name)#파일 입력


bmp_padded = padding(bmp_data)
masked_data = masking(bmp_padded, test_mask)

# 파일로 출력
bmp_data = clamping(masked_data)
image_write('test.bmo', bmp_header, bmp_cmp, masked_data)
exit()