import string
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import numpy as np

fobidden_chars = {'■','●','︱', '｜','▉' ,'▼','▊','█', '▇','▇'}.union(set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'))
def char_to_pixels(text, path='font.ttf', fontsize=80):
    """
    Based on https://stackoverflow.com/a/27753869/190597 (jsheperd)
    """
    font = ImageFont.truetype(path, fontsize) 
    #getsize lead to w, h change for diffrent chars 
    #w, h = font.getsize(text)  
    w, h = fontsize+5, fontsize+5 
    #print(w,h)
    h *= 2
    image = Image.new('L', (w, h), 1)  
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), text, font=font) 
    arr = np.asarray(image)
    arr = np.where(arr, 0, 1)
    #arr = arr[(arr != 0).any(axis=1)]
    return arr
    
def display(arr):
    result = np.where(arr, '1', '0')
    print('\n'.join([''.join(row) for row in result]))

def get_distance(vecs,me):
    #calculate the cos distance of me with other vecs
    dst = (np.dot(vecs, me) / np.linalg.norm(vecs, axis=1) / np.linalg.norm(me))
    return dst
    
    
def get_closest_chars (li_arrs, vec,li_gbk_chars, number=6):
    dst = get_distance(li_arrs, vec)
    gbk_char_ids = np.argsort(-dst)
    return [li_gbk_chars[ind] for ind in gbk_char_ids[:number] ]
if __name__ == '__main__':
	li_gbk_chars = []
	li_arrs = []
	#GBK 33088-65278
	for ind in range(33088,65278+1):
		try:
		  gbk_char =  bytes.fromhex(str(hex(ind))[2:]).decode("GBK")
		  if gbk_char in fobidden_chars: continue
		  arr = char_to_pixels(gbk_char,'./FZLanTingHei-R-GBK.TTF')
		  #print(gbk_char)
		  #display(arr)
		  li_gbk_chars.append(gbk_char) 
		  #print(gbk_char, arr)
		  li_arrs.append(arr.reshape(-1)) 	
		  #print(arr.reshape(-1).shape)	  	
		except:
			pass
	
	
	
	li_arrs = np.vstack(li_arrs)
	f = open('top5_similar_gbk_chars.txt','w')
	for i, gbk_char in enumerate(li_gbk_chars):
		top_similar_gbk_chars = get_closest_chars(li_arrs, li_arrs[i], li_gbk_chars)
		print(gbk_char, [e for e in top_similar_gbk_chars if e!= gbk_char])
		f.write(gbk_char)
		f.write(',')
		for e in top_similar_gbk_chars:
			if e!= gbk_char:
				f.write(e)
				f.write(',')
		f.write('\r\n')
	f.close()

  
  
    
	