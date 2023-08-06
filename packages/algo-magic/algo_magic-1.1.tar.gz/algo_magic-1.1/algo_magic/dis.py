from IPython.core.magic import (Magics, magics_class, line_cell_magic)
import dis

@magics_class
class DisMagics(Magics):
    @line_cell_magic
    def dis(self, line, cell = None):
        """
        Disassembling CPython code magic extension.
        This is a thin wrapper around dis.dis().
        Cf. https://docs.python.org/3/library/dis.html

        Magic methods:
            %dis statements

            %%dis
            statements
        """
        print(dis.dis(line if line else cell))