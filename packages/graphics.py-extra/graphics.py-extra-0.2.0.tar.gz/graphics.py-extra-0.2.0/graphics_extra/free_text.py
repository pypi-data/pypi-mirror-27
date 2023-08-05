import graphics
from tkinter.font import Font as TkFont
from typing import Optional, Tuple


class FreeText(graphics.Text):
    """
    Desenha texto, sem restrição de fontes.
    O objeto do graphics padrão restringe, por algum motivo,
    as famílias, estilos, e tamanhos de fontes que podem ser usadas.

    Adiciona argumentos para mudar a fonte na inicialização.
    Adiciona métodos para mudar o alinhamento do texto,
    e a linha à esquerda por padrão.

    Parâmetros:
        corner: ponto de referência para o posicionamento do texto
        text: os caracteres a serem mostrados
        font: a fonte a ser usada
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
        Muda o alinhamento do texto (internamente chamado de modo de âncora/anchor).

        Argumentos:
            new_alignment: aceita siglas dos pontos cardinais, ou 'CENTER'
                              N = norte = acima, meio
                              NW = noroeste = acima, esquerda
                              aceita caracteres maiúsculos e minúsculos.
        """
        valid_alignments = [
            'NW', 'N',      'NE',
            'W',  'CENTER', 'E',
            'SW', 'S',      'SE'
        ]
        if new_alignment.upper() in valid_alignments:
            # Internamente, somente valores minúsculos são aceitos.
            self.config['anchor'] = new_alignment.lower()
        else:
            raise ValueError('Invalid alignment.')

    def getBounds(self, window: graphics.GraphWin) -> Tuple[int, int, int, int]:
        """
        Calcula os cantos de uma bounding box ao redor do texto.

        Argumentos:
            window: necessária para desenhar o texto temporariamente

        Retorna:
            tupla contento as coordenadas dos cantos
            (1) acima, esquerdo e (2) abaixo, direito
            (x1, y1, x2, y2)
        """
        if self.id is not None:
            # O texto já está desenhado.
            # Só precisamos criar a bouding box ao redor dele.
            bounds = window.bbox(self.id)
        else:
            # O texto ainda não está desenhado.
            # Nós precisamos desenhá-lo temporariamente, para criar a bounding box.

            previous_tag = self.config.get('tag', None)
            self.config['tag'] = 'getting_width'
            self.draw(window)
            bounds = window.bbox(self.config['tag'])
            self.undraw()
            self.config['tag'] = previous_tag

        return bounds

    def getWidth(self, window: graphics.GraphWin) -> int:
        """
        Calcula a largura ocupada pelo texto.

        Argumentos:
            window: necessária para desenhar o texto temporariamente

        Retorna:
            largura
        """
        bounds = self.getBounds(window)
        return bounds[2] - bounds[0]

    def getHeight(self, window: graphics.GraphWin) -> int:
        """
        Calcula a altura ocupada pelo texto.

        Argumentos:
            window: necessária para desenhar o texto temporariamente

        Retorna:
            altura
        """
        bounds = self.getBounds(window)
        return bounds[3] - bounds[1]

    def clone(self):
        other = FreeText(self.anchor, self.config['text'])
        other.config = self.config.copy()
        return other
