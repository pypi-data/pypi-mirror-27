import trianglesolver
import math
import graphics
from collections import namedtuple
from typing import Optional, Tuple

Measurements = namedtuple(
    'Measurements',
    'side_a side_b side_c angle_a angle_b angle_c'
)

class Triangle(graphics.GraphicsObject):
    """
    Desenha um triangulo, conforme os dados fornecidos.

    É NECESSÁRIO FORNECER AO MENOS 3 das seguintes medidas para definir um
    triângulo válido.
    SIDE (a, b, c): Comprimento dos lados
    ANGLE (a, b, c): Ângulos internos (EM RADIANOS)

    O posicionamento do triângulo é definido pela posição do vértice (vertex) B.

            C
            |\
            | \
            |  \
            |   \
     side_a |    \ side_b
            |     \
            |      \
            |_______\
           B  side_c  A

    Parametros:
        vertex_b: Vértice b. Define a posição do triângulo na tela.
                  Os outros vértice serão calculados automaticamente,
                  e só podem ser mudados indiretamente, ao alterar as outras
                  medidas do triângulo.
        data: AO MENOS 3 das medidas necessárias para definir um triângulo
              (comprimento dos lados ou angulos internos EM RADIANOS).
              Qualquer desses: lado_a, lado_b, lado_c,
                               angulo_a, angulo_b, angulo_c


    """
    def __init__(self, vertex_b: graphics.Point, **data):
        super().__init__(options=["outline", "width", "fill"])
        self.vertex_b = vertex_b
        # Dados serão processados depois, para completar as medidas do triângulo
        self._data = dict(data)

    def __repr__(self) -> str:
        description = []
        for k, v in self.measurements._asdict().items():
            if v is not None:
                if k.startswith('angle_'):
                    # Mostrar os ângulos em graus
                    description.append('{}={:.2f}°'.format(k, math.degrees(v)))
                else:
                    description.append('{}={:.2f}'.format(k, v))

        return 'Triangle({})'.format(', '.join(description))

    def _move(self, dx: Optional[int] = None, dy: Optional[int] = None):
        # O triângulo é movido com relação ao vértice B.
        self.vertex_b._move(dx, dy)

    def _draw(self, canvas: graphics.GraphWin, options) -> int:
        # Converter as posições dos vértices em posições reais na tela (pixels)
        vertices = [(canvas.toScreen(p.getX(), p.getY())) for p in self.vertices]
        # Desenhar como um polígono
        return canvas.create_polygon(*vertices, options)

    @property
    def measurements(self) -> Measurements:
        """
        Calcular as medidas absolutas do triângulo,
        a partir dos dados incompletos fornecidos.
        """
        a, b, c, aA, aB, aC = trianglesolver.solve(
            a=self._data.get('side_a'),
            b=self._data.get('side_b'),
            c=self._data.get('side_c'),
            A=self._data.get('angle_a'),
            B=self._data.get('angle_b'),
            C=self._data.get('angle_c')
        )
        return Measurements(
            side_a=a, side_b=b, side_c=c, angle_a=aA, angle_b=aB, angle_c=aC
        )

    @property
    def vertex_a(self) -> graphics.Point:
        """
        Calcular a posiçao do vértice A, partindo do vértice B (linha reta).
        """
        return graphics.Point(
            self.vertex_b.getX() + self.measurements.side_c,
            self.vertex_b.getY()
        )

    @property
    def vertex_c(self) -> graphics.Point:
        """
        Calcular a posição do vértice C, partindo do vértice B.
        Fórmula de: https://stackoverflow.com/a/1571322
        """
        return graphics.Point(
            self.vertex_b.getX() + self.measurements.side_a * math.cos(self.measurements.angle_b),
            self.vertex_b.getY() - self.measurements.side_a * math.sin(self.measurements.angle_b)
        )

    @property
    def vertices(self) -> Tuple[graphics.Point, graphics.Point, graphics.Point]:
        """
        Retorna os três vértices do triângulo, que o definem absolutamente.
        """
        return (self.vertex_a, self.vertex_b, self.vertex_c)
