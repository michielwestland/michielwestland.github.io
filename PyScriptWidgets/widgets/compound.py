"""
Copyright (c) 2025 Michiel Westland
This software is distributed under the terms of the MIT license. See LICENSE.txt

PyScriptWidgets - A client side GUI class (widget) library for building web applications with PyScript.
"""


from widgets.base import PBaseWidget


class PCompoundWidget(PBaseWidget):
    """Abstract compound widget base class, that can have children"""

    # TODO Also implement padding property, move both properties to widget class.

    def __init__(self, tag):
        """Constructor, define tag and class attributes"""
        super().__init__(tag)
        # Children
        self._children = []
        # Properties
        self._margin = 0
        self._render_margin()
        self._gap = 0
        self._render_gap()

    def find_id(self, widget_id):
        """Find a reference to the widget with this id, also search in children"""
        if self._widget_id == widget_id:
            return self
        for c in self._children:
            f = c.findId(widget_id)
            if f is not None:
                return f
        return None

    # Children
    def get_children(self):
        """Get the list of children"""
        return self._children

    def remove_child(self, child):
        """Remove a single child"""
        child._parent = None  # pylint: disable=protected-access
        self._elem.removeChild(child._elem)  # pylint: disable=protected-access
        self._children.remove(child)
        return self

    def remove_all_children(self):
        """Remove all children"""
        self._elem.replaceChildren()
        for c in self._children:
            c._parent = None  # pylint: disable=protected-access
        self._children.clear()
        return self

    def add_child(self, child):
        """Add a single child"""
        child._parent = self  # pylint: disable=protected-access
        child.set_dark_mode(
            child.get_parent().is_dark_mode()
        )  # Inherit dark mode property from parent
        self._elem.appendChild(child._elem)  # pylint: disable=protected-access
        self._children.append(child)
        return self

    def add_children(self, children):
        """Add a list of children"""
        for c in children:
            self.add_child(c)
        return self

    def backup_state(self):
        """Override this method to backup runtime DOM state to widget instance fields before pickling to session storage"""
        super().backup_state()
        for c in self._children:
            c.backup_state()

    def restore_state(self):
        """Override this method to restore runtime DOM state from widget instance fields after unpickling from session storage"""
        super().restore_state()
        for c in self._children:
            c.restore_state()
            c._parent = self  # pylint: disable=protected-access
            self._elem.appendChild(c._elem)  # pylint: disable=protected-access
        # Properties
        self._render_gap()
        self._render_margin()

    def after_page_load(self):
        """Override this method tot execute code after the page DOM has loaded"""
        super().after_page_load()
        for c in self._children:
            c.after_page_load()

    # Property: dark_mode (overridden)
    def set_dark_mode(self, dark_mode):
        """Mutator"""
        super().set_dark_mode(dark_mode)
        for c in self._children:
            c.set_dark_mode(dark_mode)

    # Property: margin
    def _render_margin(self):
        """Renderer"""
        self._elem.style.margin = str(self._margin) + "px"

    def get_margin(self):
        """Accessor"""
        return self._margin

    def set_margin(self, margin):
        """Mutator"""
        if self._margin != margin:
            self._margin = margin
            self._render_margin()
        return self

    # Property: gap
    def _render_gap(self):
        """Renderer"""
        self._elem.style.gap = str(self._gap) + "px"

    def get_gap(self):
        """Accessor"""
        return self._gap

    def set_gap(self, gap):
        """Mutator"""
        if self._gap != gap:
            self._gap = gap
            self._render_gap()
        return self
