import copy
import tqdm
import numpy as np
import matplotlib.pyplot as plt
# from keras.models import Sequential
# from keras.layers import Dense
# from sklearn.model_selection import KFold

def read_input_photo(filename):

    lines = open(filename).readlines()

    ps = [str(L).split(' ') for L in lines[1:]]
    p = []
    for i,_p in enumerate(ps):
        p.append(_p) 
        p[i][-1] = (p[i][-1])[:-1]
        p[i] = list(filter(lambda x: not x.isdigit(), p[i]))
        p[i].append(i)
        p[i] = set(p[i])
    return p

def calculate_score(_a, _b):
    a = set(_a)
    b = set(_b)
    a.remove('V') if 'V' in a else a.remove('H')
    b.remove('V') if 'V' in b else b.remove('H')
    return min(len(a&b), len(a-b), len(b-a))

def merge_slide(slides):
    while (len(slides) > 1):
        slide = slides[0]
        slides.remove(slide)
        best = []
        for j,s in enumerate(slides):
            poss = []
            fb = calculate_score(slide[0], s[-1])
            poss.append(fb)
            bf = calculate_score(slide[-1], s[0])
            poss.append(bf)

            best.append((j, ("fb", fb)) if fb > bf else (j, ("bf", bf)))
        m_best = best.index(max(best, key=lambda x:x[1][1]))
        bst = best[m_best]
        b = slides[bst[0]]
        slides.remove(b)
        if bst[1][0] == "fb":
            for s_i in slide:
                b.append(s_i)
            if len(slides) == 0:
                return b
            slides.append(b)
        else:
            for b_i in b:
                slide.append(b_i)
            if len(slides) == 0:
                return slide
            slides.append(slide)

    return slides

def join_verticals(photos):
    for photo in photos:
        if 'H' in photo:
            photos.remove(photo)

    pairs=[]

    for p1 in photos:
        max_sc = 0
        max_pair = p1
        photos.remove(p1)
        for p2 in photos:
            sc = len(p1.union(p2))
            if sc > max_sc:
                max_sc = sc
                max_pair = p2
        pairs.append((p1, max_pair))
        photos.remove(max_pair)

    return pairs



def greedy_slideshow(photos):
    vertical_pairs = join_verticals(copy.copy(photos))
    photos = list(filter(lambda p: 'H' in p, photos))

    for x,y in vertical_pairs:
        photos.append(x.union(y))


    slideshow = []

    while len(photos) > 0:
        p1 = photos[0]
        slideshow.append(p1)
        max_sc = 0
        max_next = p1
        photos.remove(p1)
        if len(photos) == 0:
            return slideshow

        for p2 in photos:
            sc = calculate_score(p1, p2)
            if sc > max_sc:
                max_sc = sc
                max_next = p2

        slideshow.append(max_next)
        if max_next in photos:
            photos.remove(max_next)

    return slideshow


def slide_to_string(slideshow):
    while (len(slideshow) == 1):
        slideshow = slideshow[0]
    res = ''
    for p in slideshow:
        _p = set(p)
        pic = ''
        if 'V' in p:
            layout = 'V'
        else:
            layout = 'H'
        _p.remove(layout)   

        pic = pic + layout + ' '
        for elem in p:
            if type(elem) == int:
                pic = pic + str(elem) + ' ' 
                _p.remove(elem)

        for elem in _p:
            pic = pic + str(elem) + ' '
        res += pic + '\n'
    return res

def read_parse(fp):
    f = open(fp, 'r')
    res = ''
    with open(fp) as f:
        content = f.readlines()
        content.remove(content[-1])
    res += str(len(content)) + '\n'
    for l in content:
        l = l.split(' ')
        
        if l[0] == 'V':
            res += l[1] + ' ' + l[2] + '\n'
        else:
            res += l[1] + '\n'
    return res


def main():
    a = "../dataset/a_example.txt"
    b = "../dataset/b_lovely_landscapes.txt"
    c = "../dataset/c_memorable_moments.txt"
    d = "../dataset/d_pet_pictures.txt"
    e = "../dataset/e_shiny_selfies.txt"
    files = [a,d,e,c,b]
    for i,f in enumerate(files):
        filepath = f
        photos = read_input_photo(filepath)

        #print(photos)
        slides = []
        step = 1000
        for j in tqdm.tqdm(range(0, len(photos), step)):
            slides.append(greedy_slideshow(photos[j:j+step]))
        slide = merge_slide(slides)

        names={0:'a.txt',1:'d.txt',2:'e.txt',3:'c.txt',4:'b.txt'}

        file = open(names[i], 'w+')
        file.write(slide_to_string(slide))
        file.close()
        correct = read_parse(names[i])
        file = open(names[i], 'w+')
        file.write(correct)


    

    #a = photos[:3]
    #b = photos[3:]
    #print("1 ",a)
    #print("2 ", b, end="\n\n")
    #c = merge_slide([a,b])
    #print("Slideshow:")
    #print(c)

    #print(photos)

if __name__ == "__main__":
    main()