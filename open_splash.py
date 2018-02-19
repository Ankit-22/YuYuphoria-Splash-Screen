import struct
from PIL import Image
import numpy as np

def addImage(rows, offset, byteCount, width, height):
	with open("splash.img", "rb") as splashFile:
		splashFile.seek(offset - 1)
		count = splashFile.read(1)
		d = 0
		byt = 0
		cols = []
		while count:
			byt = byt + 4
			colorblue = splashFile.read(1)
			colorgreen = splashFile.read(1)
			colorred = splashFile.read(1)
			count = splashFile.read(1)
			for _ in range(struct.unpack('B', count)[0]):
				cols.append([struct.unpack('B', colorred)[0], struct.unpack('B', colorgreen)[0], struct.unpack('B', colorblue)[0]])
				if(len(cols) == width):
					rows.append(cols)
					cols = []
				d = d + 1
			if(d == width*height or byt == byteCount):
				print("Done")
				break
		if(len(cols) != 0):
			for _ in range(width - len(cols)):
				cols.append([0, 0, 0])
		return rows

def getImage():
	with open("splash.img", "rb") as splashFile:
		splashFile.seek(0x30)
		byteCount = int.from_bytes(splashFile.read(4), byteorder='little')
		splashFile.seek(0x3c)
		offset = int.from_bytes(splashFile.read(4), byteorder='little')
		rows = addImage([], offset, byteCount, 720, 1280)
		splashFile.seek(0x50)
		byteCount = int.from_bytes(splashFile.read(4), byteorder='little')
		splashFile.seek(0x5c)
		offset = int.from_bytes(splashFile.read(4), byteorder='little')
		rows = addImage(rows, offset, byteCount, 720, 1280)
		splashFile.seek(0x70)
		byteCount = int.from_bytes(splashFile.read(4), byteorder='little')
		splashFile.seek(0x7c)
		offset = int.from_bytes(splashFile.read(4), byteorder='little')
		rows = addImage(rows, offset, byteCount, 720, 1280)
		data = np.array(rows, dtype=np.uint8);
		print(data.shape)
		img = Image.fromarray(data, 'RGB')
		img.save('mySplash.png')
		print(len(rows))
		print(len(rows[1279]))

getImage()
