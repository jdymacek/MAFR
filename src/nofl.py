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



    def filter(self, org, shift=0):
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
        cln = img
        if org.width < self.desired_width:
            cln = Image.new(img.mode,(self.desired_width,self.desired_height))
            x = (self.desired_width - org.width)//2
            cln.paste(img.crop((x,0,x+org.width,img.height)),(x,0,x+org.width,img.height))


        #SHIFT -- shift the image fill with black
        if shift == 0:
            return cln

        fin = Image.new(img.mode,(self.desired_width,self.desired_height))         
        img = cln.crop((max(0,-shift),0,min(self.desired_width-shift,self.desired_width),self.desired_height))
        fin.paste(img,(max(0,shift),0,max(0,shift)+img.width,img.height))

#        draw = ImageDraw.Draw(fin)
#        draw.line([(fin.width//2,0),(fin.width//2,fin.height)],fill=255)

        return fin
	
"""
if args.g:
		cmp = Image.new(img.mode,(img.width+org.width,max(img.height,org.height)))

		cmp.paste(img,(0,0,img.width,img.height))
		cmp.paste(org,(img.width,0,img.width+org.width,org.height))
		draw = ImageDraw.Draw(cmp)
		draw.text((10,10),filename.split("/")[-1],fill=255)
		img = cmp

	img.save(outDirectory + filename.split("/")[-1])
    
   """ 

