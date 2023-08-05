graphics.py-extra
=================

.. image:: http://img.shields.io/pypi/v/graphics.py-extra.svg
    :target: https://pypi.python.org/pypi/graphics.py-extra

.. image:: https://img.shields.io/github/last-commit/yurihs/graphics_extra.svg
    :target: https://github.com/yurihs/graphics_extra/

Esse pacote fornece mais formas para se desenhar com o pacote
graphics.py_.

Os objetos gráficos incluídos são:

- ``RoundedRectangle`` (um retângulo com os cantos arredondados)
- ``FreeText`` (desenhar texto sem limites sobre a fonte usada)
- ``Triangle`` (triângulo de qualquer tipo: definido pelas medidas dos lados e ângulos)

Exemplos
========

**Exemplo 1:** Desenhar um retângulo com os cantos arredondados.

.. code:: python

    import graphics
    from graphics_extra import RoundedRectangle

    win = graphics.GraphWin('Exemplo do RoundedRectangle', 400, 300)

    rect = RoundedRectangle(
        graphics.Point(50, 50),
        graphics.Point(350, 250),
        radius=100
    )
    rect.setFill('light sky blue')

    rect.draw(win)


**Exemplo 2:** Mostrar texto com uma fonte qualquer.

.. code:: python

    import graphics
    import tkinter.font
    from graphics_extra import FreeText

    win = graphics.GraphWin('Exemplo do FreeText', 400, 300)

    open_sans_font = tkinter.font.Font(family='Open Sans', weight='normal', size=46)
    txt = FreeText(graphics.Point(200, 150), 'Lorem ipsum', open_sans_font)

    # txt.setAlignment('SW')  # esse é o padrão do FreeText
    txt.setAlignment('CENTER')  # esse é o padrão do graphics.Text

    # Mostrar o espaço (largura, altura) que o texto ocupará
    print('Text width:', txt.getWidth(win))
    print('Text height:', txt.getHeight(win))

    txt.draw(win)

**Exemplo 3:** Desenhar um triânglo isósceles agudo.

.. code:: python

    import math
    import graphics
    from graphics_extra import Triangle

    win = graphics.GraphWin('Exemplo do Triangle', 400, 300)

    t = Triangle(
        graphics.Point(125, 200) , # Posição do vértice B
        angle_a=math.radians(55),  # Ângulo do vértice A (converter de graus para radianos)
        angle_b=math.radians(55),  # Ângulo do vértice B (converter de graus para radianos)
        side_c=150  # Comprimento do lado C
    )
    t.draw(win)


.. _graphics.py: https://pypi.python.org/pypi/graphics.py/
