from tkinter import Frame
from .tkmixins import ScheduleMixin, DestroyMixin, FocusMixin, DisplayMixin, ReprMixin
from . import utilities as utils

class Box(ScheduleMixin, DestroyMixin, FocusMixin, DisplayMixin, ReprMixin):

    def __init__(self, master, layout="auto", grid=None, align=None):

    	# Description of this object (for friendly error messages)
        self.description = "[Box] object (may also contain other objects)"

        self.tk = Frame(master.tk)

        # Store this object's layout manager
        self._layout_manager = layout

        # Pack or grid depending on parent
        utils.auto_pack(self, master, grid, align)
