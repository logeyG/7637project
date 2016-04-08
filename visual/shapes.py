from PIL import Image
from visual import algorithm

class Shape():
    def __init__(self, name, visualFileName, inner=False):
        self.name = name

        if inner:
            img = {}
            img['visualFilename'] = visualFileName
            self.object = algorithm.get_blobs(algorithm.find_regions(img))[-1]
        else:
            self.object = Image.open(visualFileName)

def load_shapes():

     square = Shape('square', "Problems\\Basic Problems B\\Basic Problem B-01\\2.png")
     circle = Shape('circle', "Problems\\Basic Problems C\\Basic Problem C-07\\E.png")
     pac_man = Shape('pac-man', "Problems\\Basic Problems B\\Basic Problem B-01\\4.png")
     star = Shape('star', "Problems\\Basic Problems B\\Basic Problem B-01\\5.png")
     triangle = Shape('triangle', "Problems\\Basic Problems B\\Basic Problem B-01\\3.png")
     heart = Shape('heart', "Problems\\Basic Problems B\\Basic Problem B-01\\6.png")
     cross = Shape('cross', "Problems\\Basic Problems B\\Basic Problem B-02\\4.png", True)
     x = Shape('x', "Problems\\Basic Problems B\\Basic Problem B-02\\1.png")
     pentagon = Shape('pentagon', "Problems\\Basic Problems B\\Basic Problem B-01\\1.png")

     return [square, pac_man, star, triangle, heart, x, pentagon, circle, cross]