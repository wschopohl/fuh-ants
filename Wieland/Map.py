class Map:
    def __init__(self, image):
        self.image = image
        self.sprite = None
    
    def setSprite(self, sprite):
        self.sprite = sprite