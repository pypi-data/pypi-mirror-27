graphics.py-extra
=================

This package provides greater possibilities for drawing shapes with the
graphics.py_ package.

The included graphics objects are:

- ``RoundedRectangle`` (a rectangle with rounded corners)
- ``FreeText`` (write text without font limitations)

------------

*(Portuguese)*

Esse pacote fornece mais formas para se desenhar com o pacote
graphics.py_.

Os objetos gráficos incluídos são:

- ``RoundedRectangle`` (um retângulo com os cantos arredondados)
- ``FreeText`` (desenhar texto sem limites sobre a fonte usada)


Examples/Exemplos
=================

.. code:: python

    import graphics
    from graphics_extra import RoundedRectangle

    win = graphics.GraphWin('Example for RoundedRectangle', 400, 300)

    rect = RoundedRectangle(
        graphics.Point(50, 50),
        graphics.Point(350, 250),
        radius=100
    )
    rect.setFill('light sky blue')

    rect.draw(win)

.. code:: python

    import graphics
    import tkinter.font
    from graphics_extra import FreeText

    win = graphics.GraphWin('Example for FreeText', 400, 300)

    open_sans_font = tkinter.font.Font(family='Open Sans', weight='normal', size=46)
    txt = FreeText(graphics.Point(200, 150), 'Lorem ipsum', open_sans_font)

    # txt.setAlignment('SW')  # (the default in FreeText)
    txt.setAlignment('CENTER')  # (the default in graphics.Text)

    # Show the space that the text will take up
    print('Text width:', txt.getWidth(win))
    print('Text height:', txt.getHeight(win))

    txt.draw(win)

.. _graphics.py: https://pypi.python.org/pypi/graphics.py/
