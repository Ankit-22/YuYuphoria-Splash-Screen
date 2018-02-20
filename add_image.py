from PIL import Image
import numpy as np
import struct

def encode_rle(pixels):
	rle = []
	i = 0
	while(i < 720*1280):
		count = 1
		j = i + 1
		while(j < 720*1280 and pixels[i % 720, i // 720] == pixels[j % 720, j // 720]):
			count = count + 1
			j = j + 1
			i = i + 1
		loop = count // 255
		count = count % 255
		for _ in range(loop):
			rle.append(np.uint8(pixels[i % 720, i // 720][2]))
			rle.append(np.uint8(pixels[i % 720, i // 720][1]))
			rle.append(np.uint8(pixels[i % 720, i // 720][0]))
			rle.append(np.uint8(255))
		rle.append(np.uint8(pixels[i % 720, i // 720][2]))
		rle.append(np.uint8(pixels[i % 720, i // 720][1]))
		rle.append(np.uint8(pixels[i % 720, i // 720][0]))
		rle.append(np.uint8(count))
		i = i + 1
	return rle

def writeHeader(data):
	for _ in range(512):
		data.append(b'\x00')
	header = b'\x43\x4D\x2D\x53\x50\x4C\x41\x53\x48\x21\x21\x00\x76\x31\x00by\x00ankit_22'
	for i, byte in enumerate(header):
		data[i] = bytes([byte])
	return data

def makeBytes(data, npArrayRle, byteCount, offset, widthAdd, heightAdd, offsetAdd, dataAdd):
	padding = byteCount % 512
	for _ in range(padding):
		np.append(npArrayRle, [b'\x00'], axis = 0)
	for index, byte in enumerate(struct.pack("<I", 720)):
		data[widthAdd + index] = bytes([byte])
	for index, byte in enumerate(struct.pack("<I", 1280)):
		data[heightAdd + index] = bytes([byte])
	for index, byte in enumerate(struct.pack("<I", byteCount)):
		data[offsetAdd + index] = bytes([byte])
	for index, byte in enumerate(struct.pack("<I", offset)):
		data[dataAdd + index] = bytes([byte])

	for byte in npArrayRle:
		data.append(bytes([byte]))

	return data

data = writeHeader([])

im = Image.open("logo.png")
pix = im.load()

rle = encode_rle(pix)
npArrayRle = np.array(rle, dtype = np.uint8)

byteCount = npArrayRle.shape[0]

data = makeBytes(data, npArrayRle, byteCount, len(data), 0x20, 0x24, 0x30, 0x3c)

im = Image.open("images/splash2.png")
pix = im.load()

rle = encode_rle(pix)
npArrayRle = np.array(rle, dtype = np.uint8)

byteCount = npArrayRle.shape[0]

data = makeBytes(data, npArrayRle, byteCount, len(data), 0x40, 0x44, 0x50, 0x5c)

im = Image.open("images/splash3.png")
pix = im.load()

rle = encode_rle(pix)
npArrayRle = np.array(rle, dtype = np.uint8)

byteCount = npArrayRle.shape[0]

data = makeBytes(data, npArrayRle, byteCount, len(data), 0x60, 0x64, 0x70, 0x7c)

with open('newSplash.img', 'wb') as newSplash:
	newSplash.write(b''.join(data))
	newSplash.close()
