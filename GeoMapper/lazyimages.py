class LazyImageManager(object):
    def __init__(self, maxInFlight=3):
        self.maxInFlight = maxInFlight
    
        self._allImages = []
    
    def addLazyImage(self, *args, **kwds):
        self.add(LazyImage(*args, **kwds))
    
    def add(self, lazyImage):
        self._allImages.append(lazyImage)

    def request(self):
        """Continue the loading process."""

        if self.numInFlight < self.maxInFlight and self.numInQueue > 0:
            self._requestNextImage()
        
        for lazyImage in self.allImages:
            lazyImage.check()

    @property
    def allLazyImagesLoaded(self):
        return self.numTotal > 0 and self.numTotal == self.numLoaded
    
    @property
    def allImages(self):
        return self._allImages
    @property
    def numTotal(self):
        return len(self.allImages)
    
    @property
    def lazyImageQueue(self):
        return filter(lambda img: img.pending, self.allImages)
    @property
    def numInQueue(self):
        return len(self.lazyImageQueue)
    
    @property
    def imagesInFlight(self):
        return filter(lambda img: img.requesting, self.allImages)
    @property
    def numInFlight(self):
        return len(self.imagesInFlight)
    
    @property
    def imagesLoaded(self):
        return filter(lambda img: img.loaded, self.allImages)
    @property
    def numLoaded(self):
        return len(self.imagesLoaded)
    
    def _requestNextImage(self):
        if self.numInQueue == 0:
            return
        nextImage = self.lazyImageQueue[0]
        nextImage.request()


class LazyImage(object):
    """Class to load images lazily using the dumb Processing.py requestImage() function.
    
    The problem is that Processing.py doesn't yet support Pythonic patterns, like providing
    callback functions to complete aynchronous operations.
    """
    
    def __init__(self, url, callback, meta={}):
        self.url = url
        self.callback = callback  # What to do when the image is loaded.
        self.meta = meta
        
        self.img = None  # PImage
        self._done = False
    
    def request(self):
        if self.img is not None:
            return
        self.img = requestImage(self.url)
    
    def check(self):
        if self._done:
            return True
        
        if self.pending:
            return False
        elif self.requesting:
            return False
        elif self.error:
            # Error
            return True  # We're still done though.
        elif not self._done:
            # Success!
            self._done = True
            self.callback(self.img, self.meta)
            return True
    
    @property
    def loaded(self):
        if self.img is None:
            return False
        return self.img.width != 0
    @property
    def requesting(self):
        if self.img is None:
            return False
        return self.img.width == 0
    @property
    def error(self):
        if self.img is None:
            return False
        return self.img.width == -1
    @property
    def pending(self):
        return self.img is None
