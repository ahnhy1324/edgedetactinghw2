########################################################################################################################
#                                                   2017253019 안희영                                                   #
########################################################################################################################
import numpy as np
import math
import matplotlib.pyplot as plt
header_size = 54
cmp_size = 1024
image_height = 512
image_width = 512
end_in_min = 42
end_in_max = 210
file_name = "lena_bmp_512x512_new.bmp"
stochastic_mask = np.array([[0.267, 0.364, 0, -0.364, -0.267],
                            [0.373, 0.562, 0, -0.562, -0.373],
                            [-0.463, 1.0, 0, -1.0, -0.463],
                            [0.267, 0.364, 0, -0.364, -0.267],
                            [0.373, 0.562, 0, -0.562, -0.373]])
robert_mask = np.array([[1, 0],
                        [0, -1]])
prewit_mask = np.array([[-1, 0, 1],
                        [-1, 0, 1],
                        [-1, 0, 1]])


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
            out_data[i][e] = int(np.sum(data[i:i+len(mask), e:e+len(mask)]*mask))
    return out_data


def padding(data,mask):
    out_data = np.pad(data, pad_width = int(len(mask)/2), mode='edge')
    return out_data


def threshold(data):
    out_data = np.zeros((image_height, image_width), dtype='u1')
    for i in range(len(data)):
        for e in range(len(data)):
            if 0 < data[i][e]:
                out_data[i][e] = 255
            else:
                out_data[i][e] = 0
    return out_data


bmp_header, bmp_cmp, bmp_data = image_read(file_name) #파일 입력


bmp_padded = padding(bmp_data, stochastic_mask)
masked_data = (masking(bmp_padded, stochastic_mask) + masking(bmp_padded, stochastic_mask.T))
bmp_data = threshold(masked_data)


image_write('test.bmp', bmp_header, bmp_cmp, bmp_data)
exit()