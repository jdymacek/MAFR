import PIL
import math
import numpy
from PIL import ImageFilter, Image, ImageOps,ImageChops,ImageMath,ImageDraw
import argparse
import os


class NOFL:
    #old default radius was 0.75
    def __init__(self, size=(256,256),radius=None):
       self.desired_width = size[0]
       self.desired_height = size[1]
       self.blur_radius = radius



    def alternating_fill(self, img):
        #How many AB where B is the mirror of A
        n = 2*math.ceil((self.desired_width//2)/(img.width*2))
        A = numpy.asarray(img)        
        B = numpy.asarray(ImageOps.mirror(img.copy()))

        return Image.fromarray(numpy.hstack([A,B]*n + [A]) ,mode=img.mode)

    def reduce_noise(self, img):
        data = numpy.asarray(img,dtype=numpy.uint32)
        slices = numpy.hsplit(data,img.width//16)
        third = len(slices)//3
        pre = numpy.sum(slices[0:third],axis=0)/third
        post = numpy.sum(slices[-third:0],axis=0)/third
        slices = [x-(pre+post) for x in slices]
        data = numpy.hstack(slices)
        data *= 1.333
        data[data < 0] = 0
        data[data > 255] = 255
        data = data.astype(numpy.uint8)
        return Image.fromarray(data,mode=img.mode)



    def filter(self, org):
        #GREY -- grey scale the image
        img = ImageOps.grayscale(org.copy())

        #CROP Y -- remove excess Y
        if img.height > self.desired_height:
            img = img.crop((0,0,img.width,self.desired_height))

        #FILL X
        if img.width < self.desired_width:
            img = self.alternating_fill(img)    
        
        #CROP X
        if img.width > self.desired_width:
            x = (img.width-self.desired_width) // 2
            img = img.crop((x, 0, x+self.desired_width, img.height))

        #FILL Y -- X should be the correct size
        if img.height < self.desired_height:
            big = Image.new(img.mode,(self.desired_width,self.desired_height))
            big.paste(img,(0,0))
            img = big


        img = self.reduce_noise(img)

        #BLUR -- gaussian blur if wanted
        if self.blur_radius != None:
            img = img.filter(ImageFilter.GaussianBlur(radius=self.blur_radius))


        #CLEAN SIDES -- black out the sides
        if org.width >= self.desired_width:
            return img

        fin = Image.new(img.mode,(self.desired_width,self.desired_height))
        x = (self.desired_width - org.width)//2
        fin.paste(img.crop((x,0,x+org.width,img.height)),(x,0,x+org.width,img.height))
        return fin

"""
parser = argparse.ArgumentParser("Filter")
parser.add_argument("-r", help="Blur radius", default="0.75")
parser.add_argument("-d", help="Source directory")
parser.add_argument("-o", help="Target directory")
parser.add_argument("-g", help="Annotated images", default=False, const=True, action='store_const')
parser.add_argument("-b", help="Blank", default=False, const=True, action='store_const')

args = parser.parse_args()

rad = float(args.r)
tstDirectory = args.d
outDirectory = args.o
if outDirectory[-1] != "/":
	outDirectory += "/"

try:
    os.makedirs(outDirectory)
except FileExistsError:
    pass 

allFiles = [x[0] + "/" +  y  for x in os.walk(tstDirectory) for y in x[2] if y.endswith(".png") and len(os.path.basename(x[0])) == 4]

howWide = 256
howTall = 256

def stripeImage(img,stride):
	stripes = []
	for x in range(0,img.width,stride):
		stripes += [img.crop((x,0,x+stride,img.height))]
	return stripes

def averageImages(pics,weights=None):
	if weights == None:
		weights = [len(pics)] * len(pics)
	
	average = numpy.zeros((pics[0].height,pics[0].width),dtype=numpy.uint32)

	for i in range(len(pics)):
		average = numpy.add(average,numpy.asarray(pics[i],dtype=numpy.uint32) // weights[i])
	average = average.astype(numpy.uint8)
	return Image.fromarray(average,mode=pics[0].mode)



def noiseReductionAverage(img, weights=None):
	rv = img.copy()
	stripes = stripeImage(img,16)
	blocks = len(stripes)//3
	noise = averageImages(stripes[:blocks],weights)

	for i in range(len(stripes)):
		stripes[i] = ImageChops.subtract(stripes[i],noise)

	noise = averageImages(list(reversed(stripes[-blocks:])),weights)
	for i in range(len(stripes)):
		stripes[i] = ImageChops.subtract(stripes[i],noise,scale=0.75)
		rv.paste(stripes[i],(i*16,0))

	return rv

def weightedAverage(pics):
	w = list(reversed([pow(2,x) for x in range(1,len(pics)+1)]))
	print(w)
	return averageImages(pics,w)
	#average = numpy.asarray(pics[0], dtype=numpy.uint32)
	#print(average.shape,average.dtype)
	#for x in pics[1:]:
#		a = numpy.add(average,numpy.asarray(x))
#		average = a // 2
#	average = average.astype(numpy.uint8)
#	return Image.fromarray(average,mode=pics[0].mode)

def spectralGating(img):
    ma = numpy.asarray(img)
    freq_mean = numpy.mean(ma, axis = 1)
    freq_std = numpy.std(ma, axis =1)

    threshhold = freq_mean + freq_std * 1.5
    mask = ma.copy()

    for y in range(len(threshhold)):
        for x in range(len(mask[y])):
            #print(ma[y])
            if mask[y][x] < threshhold[y]:
                mask[y][x] = mask[y][x] * (1-1)
            else:
                mask[y][x] = 255

    kernal = Image.fromarray(mask)
    kernal = kernal.filter(ImageFilter.SMOOTH_MORE)
    mask = numpy.asarray(kernal,dtype=numpy.float32) / 255


    ma = ma * mask
    



    #print(freq_mean)
   # print(ma)
    
    return Image.fromarray(ma.astype(numpy.uint8))
    
'''
    for row in img:
        #get avg
        #get stdev
        thresh = avg + stdev * 
        for col in row:
            if row/col < thresh:
                 row/cow =  -(1-prop_decrease)
'''


def cleanSides(img,org):
	if org.width >= howWide:
		return img
	fin = Image.new(img.mode,(howWide,howTall))
	x = (howWide- org.width)//2
	fin.paste(img.crop((x,0,x+org.width,img.height)),(x,0,x+org.width,img.height))
	return fin

def alternatingImage(img):
	if img.width >= howWide:
		return img

	bigSize = math.ceil((howWide-img.width)/(img.width*2))


	bigImg = Image.new(img.mode,(bigSize*img.width*2+img.width,img.height))

	fli = ImageOps.mirror(img.copy())
	dbl = Image.new(img.mode,(img.width*2,img.height))
    


	if bigSize % 2 ==0:        
		dbl.paste(fli,(0,0,img.width,img.height))
		dbl.paste(img,(img.width,0,img.width*2,img.height))
		bigImg.paste(img,(0,0,img.width,img.height))    
	else:        
		dbl.paste(img,(0,0,img.width,img.height))
		dbl.paste(fli,(img.width,0,img.width*2,img.height))
		bigImg.paste(fli,(0,0,img.width,img.height))
        
	for x in range(img.width,bigImg.width+img.width,dbl.width):
		bigImg.paste(dbl,(x,0,x+dbl.width,img.height))
	x = (bigImg.width//2)-(howWide//2)
	return bigImg.crop((x,0,x+howWide,img.height))


	


for filename in allFiles:
	print(filename)
#LOAD the image
	img = Image.open(filename)
    

#GRAY the image
	img = ImageOps.grayscale(img)
	org = img.copy()

	img = alternatingImage(img)
    
#Spectral Gating
#	img = spectralGating(img)

#CROP the image

	if img.width > howWide:
		x = (img.width-howWide) // 2
		img = img.crop((x, 0, x+howWide, img.height))

	if img.height > howTall:
		img = img.crop((0,0,img.width,howTall))
	
	#TINY sample is smaller than we want
	if img.height < howTall or img.width < howWide:
		big = Image.new(img.mode,(howWide,howTall))
		if not args.b:
			#FILL small image with noise	
			noise = img.crop((0,0,img.width//4,img.height))
			for x in range(0,howWide//2,noise.width):
				big.paste(noise,(x,0))
			noise = img.crop((img.width-img.width//4,0,img.width,img.height))
			for x in range(howWide//2,howWide,noise.width):
				big.paste(noise,(x,0))
		big.paste(img,((howWide-img.width)//2,0))
		img = big

#CLEAN the image    
	#img = noiseReductionWeighted(img)
	img = noiseReductionAverage(img)


#BLUR the image
#	img = img.filter(ImageFilter.GaussianBlur(radius=rad))
    


#SAVE the image

	

	img = cleanSides(img,org)
	
	if args.g:
		cmp = Image.new(img.mode,(img.width+org.width,max(img.height,org.height)))

		cmp.paste(img,(0,0,img.width,img.height))
		cmp.paste(org,(img.width,0,img.width+org.width,org.height))
		draw = ImageDraw.Draw(cmp)
		draw.text((10,10),filename.split("/")[-1],fill=255)
		img = cmp

	img.save(outDirectory + filename.split("/")[-1])
    
   """ 

