import graphics


class RoundedRectangle(graphics._BBox):
    """
    Desenha um retângulo com cantos arredondados.
    Baseado em ttps://wiki.tcl.tk/1416

    Usando os cantos e o raio dados,
    calcula os vértices de um polígono equivalente à um retângulo arredondado,
    e então usa uma função Tk/Tcl (?) para desenhá-lo suavemente.

    Parâmetros:
        p1: canto superior esquerdo do retângulo
        p2: canto inferior direito do retângulo
        radius: tamanho dos cantos (máximo: 3/8 do comprimento do menor lado do retângulo)
    """
    def __init__(self, p1: graphics.Point, p2: graphics.Point, radius: int):
        super().__init__(p1, p2)
        self.radius = radius

    def __repr__(self):
        return "RoundedRectangle({}, {}, r={})".format(self.p1, self.p2, self.radius)

    def _draw(self, canvas: graphics.GraphWin, options: dict):
        print(type(canvas), type(options))
        # Converte as coordenadas dos cantos para medidas reais de pixels na tela
        x1, y1 = canvas.toScreen(self.p1.x, self.p1.y)
        x2, y2 = canvas.toScreen(self.p2.x, self.p2.y)

        # Argumentos passados ao tkinter.Canvas.
        # Começando com o canvas em que está sendo operado.
        args = [canvas]

        diameter = 2 * self.radius

        # O raio pode ter no máximo 3/8 do tamanho do menor lado do retângulo,
        # devido a uma limitação do Tk/Tcl.
        # 2 * (3/8) = 6/8 = 3/4 = 0.75
        # (Eu não entendi essa parte muito bem)
        maxr = 0.75
        if diameter > (maxr * (x2 - x1)):
            diameter = maxr * (x2 - x1)
        if diameter > (maxr * (y2 - y1)):
            diameter = maxr * (y2 - y1)

        # Calcula os 12 pontos que contornam o retângulo,
        # com base nos dois cantos dados.
        #
        # A---c--------c---B \
        # |                |  } diâmetro
        # c                c /
        # |                |
        # |                |
        # |                |
        # c                c \
        # |                |  } diâmetro
        # B---c--------c---A /
        # Legenda:
        # A - os dois cantos dados
        # B - os outros dois cantos do retângulo
        # c - pontos de guia para o processo de suavização do Tk/Tcl
        #
        # Um exemplo de como um canto será desenhado:
        #
        #               |                         |
        #               |                         |
        #               c                         c
        #               |                        _`
        #               |     =>                /
        #               |                   __``
        # ----c---------A           ----c```      A
        #
        a1 = x1 + diameter
        a2 = x2 - diameter
        b1 = y1 + diameter
        b2 = y2 - diameter
        args.extend([
            x1, y1,  # A1
            a1, y1,  # c1
            a2, y1,  # c2
            x2, y1,  # B1
            x2, b1,  # c3
            x2, b2,  # c4
            x2, y2,  # A2
            a2, y2,  # c5
            a1, y2,  # c6
            x1, y2,  # B2
            x1, b2,  # c7
            x1, b1,  # c8
            '-smooth', '1'
        ])
        # O comando '-smooth 1' ativa o modo de suavização,
        # que é essencial para o funcionamento dos cantos arredondados.

        # Outras opções herdadas do graphics ou do tkinter.Canvas
        args.append(options)

        return graphics.GraphWin.create_polygon(*args)

    def clone(self):
        other = RoundedRectangle(self.p1, self.p2, self.radius)
        other.config = self.config.copy()
        return other
