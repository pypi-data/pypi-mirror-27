import graphics
from tkinter.font import Font as TkFont
from typing import Optional, Tuple


class FreeText(graphics.Text):
    """
    Draws text, without font restrictions.
    The default graphics object restricts, for some reason,
    the font families, styles, and sizes that can be used.

    Adds arguments to change the font at initialization.
    Adds methods to set the alignment and aligns to the left by default.

    Parameters:
        corner: reference point for the positioning of the text
        text: the characters to be displayed
        font: the font to be used
    """
    def __init__(self, corner: graphics.Point, text: str, font: Optional[TkFont] = None):
        super().__init__(corner, text)
        self.setAlignment('SW')

        if font is not None:
            font_conf = font.config()
            if font_conf.get('family') is not None:
                self.setFace(font_conf['family'])
            if font_conf.get('size') is not None:
                self.setSize(font_conf['size'])
            if font_conf.get('weight') is not None:
                self.setStyle(font_conf['weight'])

    def __repr__(self):
        return "FreeText({}, '{}')".format(self.anchor, self.getText())

    def setFace(self, new_face: str):
        face, size, style = self.config['font']
        self._reconfig("font", (new_face, size, style))

    def setSize(self, new_size: int):
        face, size, style = self.config['font']
        self._reconfig("font", (face, new_size, style))

    def setStyle(self, new_style: str):
        face, size, style = self.config['font']
        self._reconfig("font", (face, size, new_style))

    def setAlignment(self, new_alignment: str):
        """
        Changes the text's aligment (internally called the anchor)

        Arguments:
            new_alignment: aceita siglas dos pontos cardinais, ou 'CENTER'
                           accepts compass points, or 'CENTER'
                              N = north = top, middle
                              NW = northwest = top, left
                              uppercase or lowercase characters.
        """
        valid_alignments = [
            'NW', 'N',      'NE',
            'W',  'CENTER', 'E',
            'SW', 'S',      'SE'
        ]
        if new_alignment.upper() in valid_alignments:
            # Internally, only lowercase values are allowed
            self.config['anchor'] = new_alignment.lower()
        else:
            raise ValueError('Invalid alignment.')

    def getBounds(self, window: graphics.GraphWin) -> Tuple[int, int, int, int]:
        """
        Calculates the corners of a bounding box that surrounds the text.

        Arguments:
            window: needed to temporarily draw the text

        Returns:
            tuple containg the coordinates of the
            (1) top left and (2) bottom right corners
            (x1, y1, x2, y2)
        """
        if self.id is not None:
            # The text is already drawn.
            # All we need to do is to create a bounding box around it.
            bounds = window.bbox(self.id)
        else:
            # The text isn't drawn as of yet.
            # We need to draw it temporarily, so that we can create a 'bbox'

            previous_tag = self.config.get('tag', None)
            self.config['tag'] = 'getting_width'
            self.draw(window)
            bounds = window.bbox(self.config['tag'])
            self.undraw()
            self.config['tag'] = previous_tag

        return bounds

    def getWidth(self, window: graphics.GraphWin) -> int:
        """
        Calculates the width taken up by the text.

        Arguments:
            window: needed to temporarily draw the text

        Returns:
            width
        """
        bounds = self.getBounds(window)
        return bounds[2] - bounds[0]

    def getHeight(self, window: graphics.GraphWin) -> int:
        """
        Calculates the height taken up by the text.

        Arguments:
            window: needed to temporarily draw the text

        Returns:
            height
        """
        bounds = self.getBounds(window)
        return bounds[3] - bounds[1]

    def clone(self):
        other = FreeText(self.anchor, self.config['text'])
        other.config = self.config.copy()
        return other
