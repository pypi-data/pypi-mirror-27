from inspect import signature
from warnings import warn

import numpy as np
import matplotlib.pyplot as plt
import PIL as P

from .codefu import get_parameters
from .color import is_rgb, is_rgba
#from .objects import TileSet


def compute_mask(domain, mask, width, height):
    """
    Compute the mask for a given function on a domain.

    Given the domain of some drawable, its mask function
    and the width and height of the Image, compute the mask
    and return it.

    Parameters
    ----------
    domain: Domain()
        The function to evaluate
    width : int
        The width of the image in pixels
    height : int
        The height of the image in pixels

    Returns
    -------
    mask : ndarry
        Returns a (height, width) shaped numpy array of bools
        indicating which pixels are to be coloured
    """

    # First inspect the function - does it actually depend on
    # anything?
    coordstr = get_parameters(mask)
    coordstr = tuple(s for s in coordstr if s != 'self')

    if coordstr == ():

        # If it doesn't depend on anything - then it must be True
        # everywhere, why else would the user define a drawable?
        return np.full((height, width), True)

    else:

        # Otherwise we have to do the legwork to evaluate this
        coordstr = ''.join(coordstr)
        coords = domain[coordstr, width, height]

        # Vectorise the mask and compute
        vmask_f = np.vectorize(mask)
        mask = vmask_f(*coords)

        # TODO: Perhaps we could get even fancier than what we did
        # above. It *may* be possible to walk the ast of the function
        # in some cases and replace operations with their numpy equivalent.
        # That might lead to further performance improvements?
        return mask


def compute_color(domain, mask, color, width, height):
    """
    Compute the color of the pixels affected by a drawable
    """

    # First, inspect the function - does it depend on anything?
    if color is None:
        color = lambda: (0, 0, 0, 255)
        coordstr = ()
    else:
        coordstr = get_parameters(color)
        coordstr = tuple(s for s in coordstr if s != 'self')

    if coordstr == ():

        # We have to assume that the user wants to use a single
        # color, so let's evaluate the function and see if we can
        # deduce the color they wanted to use
        user_color = color()

        # Try and validate the color
        if is_rgb(user_color):
            pixel_color = tuple([*user_color, 255])

        elif is_rgba(user_color):
            # If its a valid rgba then we don't need to touch it
            pixel_color = user_color
        else:
            # Color is not recognised, default to black
            message = "Color {!s} ".format(user_color)
            message += "is not recognised. Using black as a "
            message += "fallback"
            warn(message)

            pixel_color = (0, 0, 0, 255)

        # Finally construct the pixel array
        pixels = np.full((height, width, 4), pixel_color)
        return pixels[mask]

    else:

        # Otherwise the user's color depends on
        coordstr = ''.join(coordstr)

        coords = domain[coordstr, width, height]

        # Don't forget we don't need to compute the color for pixels
        # not in the drawable!
        coords = tuple(coord[mask] for coord in coords)

        # Vectorise the color function, bear in mind that the signature
        # depends on the number of vars in the colour function
        sig = ','.join('()' for _ in range(len(coords))) + '->(4)'
        vcolor_f = np.vectorize(color, signature=sig)

        pixels = vcolor_f(coords)
        return pixels


class Image:
    """
    Our base representation of image data, perfectly functional for the
    majority of use cases.

    pixels : ndarry
        The numpy array holding the raw image data
    """

    def __init__(self, width=None, height=None, domain=None,
                 background=(255, 255, 255, 255), xAA=1, pixels=None):
        """
        Image Constructor

        There are two ways to construct an image, the first is to specify the
        width and height in pixels plus a fill color.

        Or you can provide a numpy array with the shape (height, width, 4)
        which you can use as an image.

        It's important to note that if you provide the pixels argument it will
        override all the others.

        width : int, optional
            The width of the image in pixels. Default None
        height : int, optional. Default None
            The height of the image in pixels
        domain : (int, int) -> np.meshgrid-like
            This is a function which given a width and a height returns a grid
            containing the mathematical points associated with each pixel.
            Default: None
        background : 4-tuple, optional
            The fill RGBA colour of the image, each value can be in the range
            0-255 (default is (0, 0, 0, 0) - fully transparent black)
        pixels : numpy array, optional
            If you already have a numpy array you want to use as an image
            simply pass it in here. **Note:** The array must have the shape
            (height, width, 4). Default value None.
        """

        self._domain = domain
        self._xAA = xAA

        if pixels is not None:
            shape = pixels.shape

            if len(shape) != 3 or shape[-1] != 4:
                raise ValueError("Pixels array must have shape:"
                                 " (height, width, 4)")

            self.pixels = pixels
            self._width = shape[1]
            self._height = shape[0]
        else:
            if width is None or height is None:
                raise ValueError("If no pixels array is given you"
                                 " must specify a width and height")

            # If given an RGB lookalike, convert it to RGBA
            if len(background) == 3:
                background = tuple([*background, 255])

            self._height = height
            self._width = width

            self.pixels = np.full((height * xAA, width * xAA, 4), background,
                                  dtype=np.uint8)

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def color(self):
        return self.pixels[:, :, 0:3]

    @color.setter
    def color(self, value):

        try:
            self.pixels[:, :, 0:3] = value
        except ValueError:
            given = np.array(value).shape
            expected = self.pixels[:, :, 0:3].shape

            given_str = 'Color values with shape {} '.format(given)
            expected_str = 'are incompatible with this image {}\n'.format(expected)
            details = 'For more details please see '
            link = 'https://docs.scipy.org/doc/numpy/user/basics.broadcasting.html'
            raise ValueError(given_str + expected_str + details + link)

    @property
    def red(self):
        return self.pixels[:, :, 0]

    @red.setter
    def red(self, value):
        self.pixels[:, :, 0] = value

    @property
    def green(self):
        return self.pixels[:, :, 1]

    @green.setter
    def green(self, value):
        self.pixels[:, :, 1] = value

    @property
    def blue(self):
        return self.pixels[:, :, 2]

    @blue.setter
    def blue(self, value):
        self.pixels[:, :, 2] = value

    @property
    def alpha(self):
        return self.pixels[:, :, 3]

    @alpha.setter
    def alpha(self, value):
        self.pixels[:, :, 3] = value

    @property
    def xAA(self):
        return self._xAA

    @property
    def domain(self):
        return self._domain

    @domain.setter
    def domain(self, value):
        self._domain = value

    @classmethod
    def fromarray(cls, px):
        return cls(pixels=px)

    @classmethod
    def fromfile(cls, filename):
        img = P.Image.open(filename)
        arr = np.array(img.getdata(), dtype=np.uint8)
        arr = arr.reshape(img.size[1], img.size[0], 4)
        return Image(pixels=arr)

    def _flip_index(self, index):
        """
        The underlying representation is in (y,x) 'coordinates' which
        breaks normal mental models of coordinates being (x,y). So in
        an effort to keep this mental model consistent throughout this
        method reorders a given index in that manner.

        If index is just a number, we assume it to be indexing the x
        coordinate so we return (:, x)

        If index is tuple of indices we swap the first two entries
        """

        if isinstance(index, (tuple,)):
            if len(index) == 2:
                return (index[1], index[0])
            else:
                return (index[1], index[0], *index[2:])
        else:
            return (slice(None), index)

    def _get_by_pixels(self, index):
        """
        Once we have decided that the index represents pixels
        this method is responsible for interpreting it and
        returning the appropriate object
        """
        px = self.pixels[index]
        shape = px.shape

        if len(shape) == 3:
            return Image.fromarray(px)
        else:
            return px

    def _is_pixel_addr(self, index):
        """
        This method is for deciding whether or not a given
        index represents a pixel index or mathematical points
        """

        for idx in index:

            # Is this item a simple integer - hence pixel address?
            if isinstance(idx, (int,)):
                continue

            # Is it a float?
            if isinstance(idx, (float,)):
                return False

            # Is it a slice?
            if isinstance(idx, (slice,)):

                if isinstance(idx.start, (float,)) or\
                   isinstance(idx.stop, (float,)):
                    return False

        # If we get this far, then it must be a pixel address
        return True

    def __getitem__(self, index):
        idx = self._flip_index(index)

        if self._is_pixel_addr(idx):
            return self._get_by_pixels(idx)

        # If we get this far, we must be dealing with a 'mathematical
        # address' So we 'simply' have to figure out which pixels are mapped
        # to the mathematial points in question

        # This involves using the built-in domain function - which
        # of course has to exist for this to work
        if self._domain is None:
            raise RuntimeError('In order to index pixels by mathematical '
                               'points the image must be associated with '
                               'a domain!')

        # For the moment we will restrict ourselves to the index being made
        # up of 2 slices. This might change eventually
        if not isinstance(idx[0], (slice,)) or\
           not isinstance(idx[1], (slice,)):
            raise ValueError('Mathematical indexing is currently only '
                             'supported for slices')

        # Step 0: Unpack the slices
        yslice = idx[0]
        ystart = yslice.start
        ystop = yslice.stop

        xslice = idx[1]
        xstart = xslice.start
        xstop = xslice.stop

        # Step 1: Evaluate the domain function to get the points
        (xs, *_), YS = self._domain(self.width * self.xAA,
                                    self.height * self.xAA)
        ys = np.array([it[0] for it in YS])

        # Step 2: See which pixels the values are closest to
        xstart_d = [(None, None)] if xstart is None else\
                   sorted([(abs(x - xstart), i) for i, x in enumerate(xs)])

        xstop_d = [(None, None)] if xstop is None else\
                  sorted([(abs(x - xstop), i) for i, x in enumerate(xs)])

        ystart_d = [(None, None)] if ystart is None else\
                   sorted([(abs(y - ystart), i) for i, y in enumerate(ys)])

        ystop_d = [(None, None)] if ystop is None else\
                  sorted([(abs(y - ystop), i) for i, y in enumerate(ys)])

        # Step 3: Construct new slice objects with the new pixel addresses
        # and pass it off to the _get_by_pixels method
        slice_x = slice(xstart_d[0][1], xstop_d[0][1], None)
        slice_y = slice(ystart_d[0][1], ystop_d[0][1], None)

        return self._get_by_pixels((slice_y, slice_x))

    def __setitem__(self, index, value):

        # If we are given something that looks like RGB
        # convert it to RGBA
        if len(value) == 3:
            value = tuple([*value, 255])

        self.pixels[self._flip_index(index)] = value

    def __repr__(self):
        shape = self.pixels.shape
        return '%ix%i Image' % (shape[1], shape[0])

    def __neg__(self):
        """
        Easily obtain the negative of an image by typing
        (-img)
        """

        # Create the function that will invert the values of
        # the color pixels and vectorize it
        neg = lambda v: abs(v - 255)
        vneg = np.vectorize(neg, otypes=(np.uint8,))

        # Create the new pixel array
        alphas = self.alpha
        alphas.shape = (self.height, self.width, 1)
        colors = vneg(self.color)

        px = np.append(colors, alphas, axis=2)

        return Image(pixels=px)

    def __and__(self, other):
        """
        Implementation of the boolean AND, best when used with black and
        white images
        """

        if not isinstance(other, (Image,)):
            raise TypeError('AND is only supported between instances of '
                            'the Image class')

        if self.pixels.shape != other.pixels.shape:
            raise ValueError('AND can only be used with Images that have '
                             'the same dimensions!')

        height, width, _ = self.pixels.shape
        ax = self.color
        bx = other.alpha

        # Scale the pixels of b
        scaled = bx / 255
        scaled.shape = (height, width, 1)

        # Do the multiplication - it's important to note that the entries
        # of cx are now 'float64'
        cx = ax * scaled

        # Create a new numpy array so that the conversion back to uint8 is
        # correct
        colors = np.array(cx, dtype=np.uint8)
        img = Image(width, height)
        img.color = colors

        return img

    def __add__(self, other):
        """
        Create a new image from two others by adding their pixel values together,
        bounding above and below by 255 and 0 respectively
        """

        if not isinstance(other, (Image,)):
            raise TypeError('ADD id only supported between instances of the '
                            'Image class')

        if self.pixels.shape != other.pixels.shape:
            raise ValueError('ADD can only be used with Images that have '
                             'the same dimensions!')

        height, width, _ = self.pixels.shape
        ax = self.color
        bx = other.color

        # As far as I know, this is the only way to add these two together and
        # capping the result at 255. However it will not be quick
        def bounded_add(a, b):
            v = int(a) + int(b)
            return min(255, v)

        # To make the above work well with arrays we need to vectorize it
        vbounded_add = np.vectorize(bounded_add, otypes=('uint8',))

        cx = vbounded_add(ax, bx)
        img = Image(width, height)
        img.color = cx

        return img

    def __sub__(self, other):
        """
        Create a new image from two others by subtracting their pixel values,
        bounding above and below by 255 and 0 respectively
        """

        if not isinstance(other, (Image,)):
            raise TypeError('SUB is only supported between instances of the '
                            'Image class')

        if self.pixels.shape != other.pixels.shape:
            raise ValueError('SUB can only be used with Images that have '
                             'the same dimensions!')

        height, width, _ = self.pixels.shape
        ax = self.color
        bx = other.color

        # As far as I know, this is the only way to add these two together and
        # capping the result at 255. However it will not be quick
        def bounded_sub(a, b):
            v = int(a) - int(b)
            return max(0, v)

        # To make the above work well with arrays we need to vectorize it
        vbounded_sub = np.vectorize(bounded_sub, otypes=('uint8',))

        cx = vbounded_sub(ax, bx)
        img = Image(512, 512)
        img.color = cx

        return img

    def __call__(self, drawable, overwrite_domain=True, use_host_domain=False):
        """
        Implementing this 'magic' method allows us to use img(drawable)
        to trigger the 'drawing' of an object onto an arbitrary image.

        The default behavior of this function is to take the drawable
        f, extract it's domain function and proceed to compute the mask
        and color of the affected pixels. Once that is done, the extracted
        domain function is stored internally so that users may optionally
        index the pixels by mathematical points, instead of raw pixels.

        However, it is possible to override this behavior with the two
        options:
            - use_host_domain -> False by default
            - overwrite_domain -> True by default

        If use_host_domain is True, instead of using the domain that
        comes with the drawable, the domain already associated with
        the underlying image is used instead.

        If overwrite_domain is False, the image keeps its original
        domain, instead of saving the new one that the drawable
        possesses
        """

        # Of course, the image has to have a domain already if we are
        # to use this one instead
        if use_host_domain and self._domain is None:
            raise RuntimeError('The image does not have an associated '
                               'domain!')

        # Get the domain from the correct place
        if use_host_domain:
            domain = self._domain
        else:
            domain = drawable.domain()

        # Compute the mask
        mask = compute_mask(domain, drawable.mask, self.width * self.xAA,
                            self.height * self.xAA)

        # Compute the colors
        colors = compute_color(domain, mask, drawable.color,
                               self.width * self.xAA,
                               self.height * self.xAA)

        # Color the image
        self.pixels[mask] = colors

        # Only now that all is said and done do we overwrite the domain,
        # that way we don't get something halfway between one or the other
        if overwrite_domain:
            self._domain = domain

    def show(self):
        """
        Show the image using a matplotlib figure - useful for use in
        notebooks
        """
        return plt.imshow(self.pixels)

    def save(self, filename):
        """
        Save the image to the given filename
        """

        image = P.Image.frombuffer('RGBA', (self.width * self.xAA,
                                   self.height * self.xAA), self.pixels,
                                   'raw', 'RGBA', 0, 1)

        # Apply our naive AA by downscaling the image
        if self.xAA > 1:
            image = image.resize((self.width, self.height), resample=P.Image.BICUBIC)

        with open(filename, 'wb') as f:
            image.save(f)


class LayeredImage:
    """
    This is a container for a number of images, with a number of conveniences
    for blending/merging them together - just as you would in GIMP/Photoshop
    etc.
    """

    def __init__(self, width=None, height=None, num_layers=4, imgs=None):

        if imgs is not None:

            # TODO: Do a check to make sure given images make sense
            self._layers = imgs
            self._width = imgs[0].width
            self._height = imgs[0].height

        else:
            self._layers = [Image(width, height, background=(0, 0, 0, 0))
                            for _ in range(num_layers)]

            self._width = width
            self._height = height

    def __repr__(self):
        return "%ix%i Layered Image with %i layers"\
                % (self.width, self.height, self.nlayers)

    def __getitem__(self, key):

        if isinstance(key, (int,)):
            return self._layers[key]

        else:
            return 'Other methods coming soon'

    @classmethod
    def fromlist(cls, imgs):
        return cls(imgs=imgs)

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def nlayers(self):
        return len(self._layers)


# class TiledImage(Image):
#     """
#     This builds on the base image class, to allow easy creation of
#     images from tilesets. Useful for constructing backgrounds based
#     on a grid - e.g level designs etc.
#     """

#     def __init__(self, width, height, xmax=10, ymax=10,
#                  xmin=0, ymin=0, *args, **kwargs):

#         # First call the parent to set things up
#         super().__init__(width, height, *args, **kwargs)

#         # Now we will set up the domain for the image
#         self._xmin = xmin
#         self._xmax = xmax

#         self._ymin = ymin
#         self._ymax = ymax

#         self.domain = mk_domain(xmin, xmax, ymin, ymax)

#     def __call__(self, tileset, overwrite_domain=False):
#         """
#         This allows for the possibility of easy application
#         of a tileset to the Image, but bog standard drawables
#         are still ok.
#         """

#         # Are we dealing with a drawable?
#         if isinstance(tileset, (Drawable,)):

#             # If so do the "normal" thing
#             super().__call__(tileset, overwrite_domain)
#             return

#         if isinstance(tileset, (TileSet,)):

#             # Here we assume that the tileset is not time dependent
#             # so just call the layout method with some, argument
#             layout = tileset.layout(0, 0)
#             tiles = tileset._tiles

#         elif isinstance(tileset, (tuple,)):

#             # Here we assume that we have been given a time dependent
#             # tileset
#             tiles, layout = tileset

#         else:
#             raise TypeError('TiledImages only support Drawables and '
#                             'TileSets!!')

#         # With that out of the way let's get down to it. First let's check
#         # that the given tileset makes sense

#         # Numpy freaks out if we try to .unique() an array containing None's
#         # So just turn them into zeros, as a tileset will always have a
#         # zeroth tile
#         tozero = lambda v: v if v is not None else 0
#         vtoz = np.vectorize(tozero)
#         test_layout = vtoz(layout)

#         if len(tiles) < len(np.unique(test_layout)):
#             raise ValueError('The layout defined references more tiles '
#                              'than are defined!')

#         # Transpose the layout array so that it makes sense to the user
#         layout = layout.transpose()

#         # Next we need to decide on the size of each of the grid squares
#         nx, ny = layout.shape
#         xsize = (self.xmax - self.xmin) / nx
#         ysize = (self.ymax - self.ymin) / ny

#         # Now we go through each tile in the layout and apply it to the
#         # image
#         for j in range(ny):

#             ystart = self.ymin + j*ysize
#             yend = ystart + ysize

#             for i in range(nx):
#                 xstart = self.xmin + i*xsize
#                 xend = xstart + xsize

#                 tileidx = layout[i, j]

#                 if tileidx is not None:
#                     tile = tiles[tileidx]
#                     self[xstart:xend, ystart:yend](tile)

#     @property
#     def xmin(self):
#         return self._xmin

#     @xmin.setter
#     def xmin(self, value):

#         if not isinstance(value, (int, float)):
#             raise TypeError('xmin must be a number!')

#         if value >= self.xmax:
#             raise ValueError('xmin cannot be larger than xmax!')

#         self._xmin = value
#         self.domain = mk_domain(value, self.xmax, self.ymin, self.ymax)

#     @property
#     def xmax(self):
#         return self._xmax

#     @xmax.setter
#     def xmax(self, value):

#         if not isinstance(value, (int, float)):
#             raise TypeError('xmax must be a number!')

#         if value <= self.xmin:
#             raise ValueError('xmax cannot be less than xmin!')

#         self._xmin = value
#         self.domain = mk_domain(self.xmin, value, self.ymin, self.ymax)

#     @property
#     def ymin(self):
#         return self._ymin

#     @ymin.setter
#     def ymin(self, value):

#         if not isinstance(value, (int, float)):
#             raise TypeError('ymax must be a number!')

#         if value >= self.ymax:
#             raise ValueError('ymin cannot be larger than ymax!')

#         self._ymin = value
#         self.domain = mk_domain(self.xmin, self.xmax, value, self.ymax)

#     @property
#     def ymax(self):
#         return self._ymax

#     @ymax.setter
#     def ymax(self, value):

#         if not isinstance(value, (int, float)):
#             raise TypeError('ymax must be a number!')

#         if value <= self.ymin:
#             raise ValueError('ymax cannot be less than ymin!')

#         self._ymax = value
#         self.domain = mk_domain(self.xmin, self.xmax, self.ymin, value)
