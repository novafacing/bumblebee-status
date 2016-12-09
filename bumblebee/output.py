# pylint: disable=R0201

"""Output classes"""

import sys
import json

class Widget(object):
    """Represents a single visible block in the status bar"""
    def __init__(self, full_text):
        self._full_text = full_text
        self.module = None

    def link_module(self, module):
        """Set the module that spawned this widget

        This is done outside the constructor to avoid having to
        pass in the module name in every concrete module implementation"""
        self.module = module.name

    def full_text(self):
        """Retrieve the full text to display in the widget"""
        if callable(self._full_text):
            return self._full_text()
        else:
            return self._full_text

class I3BarOutput(object):
    """Manage output according to the i3bar protocol"""
    def __init__(self, theme):
        self._theme = theme
        self._widgets = []

    def start(self):
        """Print start preamble for i3bar protocol"""
        sys.stdout.write(json.dumps({"version": 1, "click_events": True}) + "[\n")

    def stop(self):
        """Finish i3bar protocol"""
        sys.stdout.write("]\n")

    def draw(self, widget, engine=None):
        """Draw a single widget"""
        full_text = widget.full_text()
        prefix = self._theme.prefix(widget)
        suffix = self._theme.suffix(widget)
        if prefix:
            full_text = u"{}{}".format(prefix, full_text)
        if suffix:
            full_text = u"{}{}".format(full_text, suffix)
        separator = self._theme.separator(widget)
        if separator:
            self._widgets.append({
                u"full_text": separator,
                "separator": False,
                "color": self._theme.separator_fg(widget),
                "background": self._theme.separator_bg(widget),
                "separator_block_width": self._theme.separator_block_width(widget),
            })
        self._widgets.append({
            u"full_text": full_text,
            "color": self._theme.fg(widget),
            "background": self._theme.bg(widget),
            "separator_block_width": self._theme.separator_block_width(widget),
            "separator": True if separator is None else False,
        })

    def begin(self):
        """Start one output iteration"""
        self._widgets = []
        self._theme.reset()

    def flush(self):
        """Flushes output"""
        sys.stdout.write(json.dumps(self._widgets))

    def end(self):
        """Finalizes output"""
        sys.stdout.write(",\n")
        sys.stdout.flush()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
