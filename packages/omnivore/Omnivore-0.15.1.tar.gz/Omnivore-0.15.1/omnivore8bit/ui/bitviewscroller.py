#-----------------------------------------------------------------------------
# Name:        bitviewscroller.py
# Purpose:     scrolling container for bit patterns
#
# Author:      Rob McMullen
#
# Created:     2014
# RCS-ID:      $Id: $
# Copyright:   (c) 2014 Rob McMullen
# License:     wxWidgets
#-----------------------------------------------------------------------------
"""BitviewScroller -- a container for viewing bit patterns

"""

import os
import time

import numpy as np
import wx
import wx.lib.newevent

from pyface.action.api import Action
from pyface.tasks.action.api import EditorAction

from atrcopy import SegmentData, DefaultSegment, get_style_mask

from omnivore.utils.nputil import intscale
from omnivore8bit.hex_edit.actions import *
from omnivore8bit.arch.disasm import get_style_name

from selection_mixin import SelectionMixin

import logging
log = logging.getLogger(__name__)


class BitviewEvent(wx.PyCommandEvent):
    """Event sent when a LayerControl is changed."""

    def __init__(self, eventType, id, byte, bit):
        wx.PyCommandEvent.__init__(self, eventType, id)
        self.byte = byte
        self.bit = bit


class BitviewScroller(wx.ScrolledWindow, SelectionMixin):
    dbg_call_seq = 0
    short_name = "_bitview base class"

    def __init__(self, parent, task, **kwargs):
        wx.ScrolledWindow.__init__(self, parent, -1, **kwargs)
        SelectionMixin.__init__(self)

        # Settings
        self.task = task
        self.editor = None
        self.segment = None
        self.max_zoom = 16
        self.min_zoom = 1
        self.bytes_per_row = 1
        self.pixels_per_byte = 8
        self.bitplanes = 1

        # internal storage
        self.start_addr = 0
        self.start_byte = None
        self.end_byte = None
        self.img = None
        self.scaled_bmp = None
        self.grid_width = 0
        self.grid_height = 0
        self.zoom = 5
        self.start_row = 0
        self.start_col = 0
        self.fully_visible_rows = 1
        self.fully_visible_cols = 1
        self.visible_rows = 1
        self.visible_cols = 1

        self.rect_select = False
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE, self.on_resize)
        self.Bind(wx.EVT_MOUSEWHEEL, self.on_mouse_wheel)
        self.Bind(wx.EVT_LEFT_UP, self.on_left_up)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)
        self.Bind(wx.EVT_LEFT_DCLICK, self.on_left_dclick)
        self.Bind(wx.EVT_MOTION, self.on_motion)
        self.Bind(wx.EVT_RIGHT_DOWN, self.on_popup)
        self.Bind(wx.EVT_SET_FOCUS, self.on_focus)
        self.Bind(wx.EVT_KILL_FOCUS, self.on_focus_lost)
        self.Bind(wx.EVT_ENTER_WINDOW, self.on_mouse_enter)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.on_mouse_leave)
        self.Bind(wx.EVT_CHAR, self.on_char)
        self.Bind(wx.EVT_CHAR_HOOK, self.on_char_hook)

    def __repr__(self):
        return "<%s at 0x%x>" % (self.__class__.__name__, id(self))

    @property
    def command_help(self):
        return ""

    def get_view_params(self):
        s = self.GetViewStart()
        return [s[0], s[1]]  # might be a wx.Point, so ensure it's a list for json serialization

    def restore_view_params(self, data):
        self.Scroll(*data)

    def find_center(self, pos, visible, total):
        last = total - 1
        pos = max(0, pos - (visible / 2))
        if pos + visible > last:
            pos = max(0, last - visible + 1)
        return pos

    def find_upper_left_for_center_index(self, index):
        r, c = self.index_to_row_col(index)
        log.debug("find_upper_left_for_center_index: r=%d c=%d, vis: r=%d c=%d" % (r, c, self.fully_visible_rows, self.fully_visible_cols))
        r = self.find_center(r, self.fully_visible_rows, self.total_rows)
        c = self.find_center(c, self.fully_visible_cols, self.bytes_per_row)
        return r, c

    def center_on_index(self):
        ul = self.find_upper_left_for_center_index(self.editor.cursor_index)
        self.set_upper_left(ul)

    def set_upper_left(self, ul):
        log.debug("center_on_index: new upper left=%s" % str(ul))
        self.start_row, self.start_col = ul
        self.Scroll(ul[1], ul[0])
        self.Refresh()

    def is_ready_to_render(self):
        return self.editor is not None

    def set_task(self, task):
        self.task = task

    def recalc_view(self):
        editor = self.task.active_editor
        if editor is not None:
            self.editor = editor
            self.segment = self.get_segment(editor)
            self.rect_select = editor.rect_select
            self.start_addr = editor.segment.start_addr
            self.update_bytes_per_row()
            self.set_colors()
            self.set_font()
            self.update_zoom()
            self.set_scale()

    def get_segment(self, editor):
        """Get segment from editor; provided for subclasses that use
        a computed segment to represent the segment data (like Jumpman)
        """
        return editor.segment

    def refresh_view(self):
        editor = self.task.active_editor
        if editor is not None:
            if self.editor != editor:
                self.recalc_view()
            else:
                if self.FindFocus() != self and editor.pending_focus != self:
                    self.center_on_index()
                else:
                    self.Refresh()

    def sync_settings(self):
        e = self.editor
        if e is not None:
            self.sync_to_editor(e)

    def sync_to_editor(self, e):
        pass

    def set_colors(self):
        pass

    def set_font(self):
        pass

    def zoom_in(self, zoom=1):
        self.set_zoom(self.zoom + zoom)
        self.set_scale()

    def zoom_out(self, zoom=1):
        self.set_zoom(self.zoom - zoom)
        self.set_scale()

    def set_zoom(self, zoom):
        if zoom > self.max_zoom:
            zoom = self.max_zoom
        elif zoom < self.min_zoom:
            zoom = self.min_zoom
        self.zoom = zoom
        self.sync_settings()

    def get_zoom_factors(self):
        return self.zoom, self.zoom

    def get_highlight_indexes(self):
        e = self.editor
        anchor_start, anchor_end = e.anchor_start_index, e.anchor_end_index
        r1 = c1 = r2 = c2 = -1
        if self.rect_select:
            anchor_start, anchor_end, (r1, c1), (r2, c2) = self.segment.get_rect_indexes(anchor_start, anchor_end, self.bytes_per_row)
        elif anchor_start > anchor_end:
            anchor_start, anchor_end = anchor_end, anchor_start
        elif anchor_start == anchor_end:
            anchor_start = e.cursor_index
            anchor_end = anchor_start + 1
        return anchor_start, anchor_end, (r1, c1), (r2, c2)

    def get_image(self, segment=None):
        raise NotImplementedError

    def copy_to_clipboard(self):
        """Copies current image to clipboard.

        Copies the current image, including scaling, zooming, etc. to
        the clipboard.
        """
        bmpdo = wx.BitmapDataObject(self.scaled_bmp)
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(bmpdo)
            wx.TheClipboard.Close()

    def prepare_image(self):
        """Creates new image at specified zoom factor.

        Creates a new image that is to be used as the background of
        the scrolled bitmap.  Currently, actually creates the entire
        image, which could lead to memory problems if the image is
        really huge and the zoom factor is large.
        """
        if self.is_ready_to_render():
            self.calc_image_size()

            w, h = self.GetClientSize().Get()
            dc = wx.MemoryDC()
            self.scaled_bmp = wx.Bitmap(w, h)

            dc.SelectObject(self.scaled_bmp)
            dc.SetBackground(wx.Brush(self.editor.machine.empty_color))
            dc.Clear()

            array = self.get_image()
            width = array.shape[1]
            height = array.shape[0]
            if width > 0 and height > 0:
                zw, zh = self.get_zoom_factors()
                array = intscale(array, zh, zw)
                self.draw_overlay(array, width, height, zw, zh)
                image = wx.Image(array.shape[1], array.shape[0])
                image.SetData(array.tostring())
                bmp = wx.Bitmap(image)
                dc.DrawBitmap(bmp, 0, 0)

    def draw_overlay(self, array, w, h, zw, zh):
        """ Hook to draw overlay image on top of finished scaled image
        """
        pass

    def calc_image_size(self):
        x, y = self.GetViewStart()
        w, h = self.GetClientSize().Get()
        self.start_row = y
        self.start_col = x

        # For proper buffered paiting, the visible_rows must include the
        # (possibly) partially obscured last row.  fully_visible_rows
        # indicates the number of rows without that last partially obscured
        # row (if it exists).
        self.fully_visible_rows = h / self.zoom
        self.fully_visible_cols = w / self.zoom
        self.visible_rows = ((h + self.zoom - 1) / self.zoom)
        self.visible_cols = ((w + self.zoom - 1) / self.zoom)
        log.debug("x, y, w, h, rows start, num, cols start, num:%s" % str([x, y, w, h, self.start_row, self.visible_rows, self.fully_visible_rows, self.start_col, self.visible_cols, self.fully_visible_cols]))

    def update_bytes_per_row(self):
        self.pixels_per_byte = self.editor.machine.bitmap_renderer.pixels_per_byte
        self.bitplanes = self.editor.machine.bitmap_renderer.bitplanes

    def update_zoom(self):
        pass

    def set_scale(self):
        """Creates new image at specified zoom factor.

        Creates a new image that is to be used as the background of
        the scrolled bitmap.  Currently, actually creates the entire
        image, which could lead to memory problems if the image is
        really huge and the zoom factor is large.
        """
        if self.segment is not None:
            self.calc_scale_from_bytes()
        else:
            self.grid_width = 10
            self.grid_height = 10
        log.debug("set_scale: %s" % str([self.grid_width, self.grid_height]))
        self.calc_scroll_params()
        self.Refresh()

    def calc_scale_from_bytes(self):
        self.total_rows = (len(self.segment) + self.bytes_per_row - 1) / self.bytes_per_row
        self.grid_width = int(self.pixels_per_byte * self.bytes_per_row)
        self.grid_height = int(self.total_rows)

    def calc_scroll_params(self):
        self.SetVirtualSize((self.grid_width * self.zoom, self.grid_height * self.zoom))
        rate = int(self.zoom)
        if rate < 1:
            rate = 1
        self.SetScrollRate(rate, rate)

    def event_coords_to_byte(self, evt):
        """Convert event coordinates to world coordinates.

        Convert the event coordinates to world coordinates by locating
        the offset of the scrolled window's viewport and adjusting the
        event coordinates.
        """
        raise NotImplementedError

    def get_index_range(self, row, col):
        """Get the byte offset from start of file given row, col
        position.
        """
        index = row * self.bytes_per_row + col
        return index, index + 1

    def index_to_row_col(self, index):
        return divmod(index, self.bytes_per_row)

    def select_index(self, from_control, rel_pos, first_row=None):
        r, c = self.index_to_row_col(rel_pos)
#        print "r, c, start, vis", r, c, self.start_row, self.fully_visible_rows
        last_scroll_row = self.total_rows - self.fully_visible_rows
        if first_row is not None:
            first_row = min(max(0, first_row), last_scroll_row)
        if self.FindFocus() != self and self.editor.pending_focus != self:
            first_row = self.find_upper_left_for_center_index(self.editor.cursor_index)[0]
        last_row = self.start_row + self.fully_visible_rows - 1
        last_col = self.start_col + self.fully_visible_cols - 1

        update = False
        if first_row:
            if first_row != self.start_row:
                update = True
                r = first_row
        else:
            if r < self.start_row:
                # above current view
                update = True
            elif r >= last_row:
                # below last row
                if r >= last_scroll_row:
                    r = last_scroll_row
                    update = True
                elif r >= self.fully_visible_rows:
                    r = r - self.fully_visible_rows + 1
                    update = True
            else:
                # row is already visible so don't change row position
                r = self.start_row

        if c < self.start_col:
            # left of start column, so set start view to that column
            update = True
        elif c >= last_col:
            c = c - self.fully_visible_cols + 1
            update = True
        else:
            c = self.start_col

        if update:
            self.Scroll(c, r)
        self.Refresh()

    def select_addr(self, addr):
        rel_pos = addr - self.start_addr
        self.select_index(self, rel_pos)

    def on_mouse_wheel(self, evt):
        """Driver to process mouse events.

        This is the main driver to process all mouse events that
        happen on the BitmapScroller.  Once a selector is triggered by
        its event combination, it becomes the active selector and
        further mouse events are directed to its handler.
        """
        if self.end_byte is None:  # end_byte is a proxy for the image being loaded
            return

        w = evt.GetWheelRotation()
        if evt.ControlDown():
            if w < 0:
                self.zoom_out()
            elif w > 0:
                self.zoom_in()

        evt.Skip()

    def on_left_up(self, evt):
        self.handle_select_end(self.editor, evt)

    def set_cursor_pos_from_event(self, evt):
        e = self.editor
        byte, bit, inside = self.event_coords_to_byte(evt)
        if inside:
            self.select_extend_mode = evt.ShiftDown()
            if self.select_extend_mode:
                if byte < e.anchor_start_index:
                    e.anchor_start_index = byte
                elif byte + 1 > e.anchor_start_index:
                    e.anchor_end_index = byte + 1
                e.anchor_initial_start_index, e.anchor_initial_end_index = e.anchor_start_index, e.anchor_end_index
                e.cursor_index = byte
            else:
                e.set_cursor(byte, False)
            wx.CallAfter(e.index_clicked, byte, bit, self, True)

    def get_location_from_event(self, evt):
        byte, bit, inside = self.event_coords_to_byte(evt)
        index1 = byte
        index2 = byte + 1
        return byte // self.bytes_per_row, bit, index1, index2, inside

    def get_start_end_index_of_row(self, row):
        index1, _ = self.get_index_range(row, 0)
        _, index2 = self.get_index_range(row, self.bytes_per_row - 1)
        return index1, index2

    def on_left_down(self, evt):
        self.handle_select_start(self.editor, evt)
        wx.CallAfter(self.SetFocus)

    def on_left_dclick(self, evt):
        self.on_left_down(evt)

    def on_motion(self, evt):
        self.on_motion_update_status(evt)
        if self.editor is not None and evt.LeftIsDown():
            self.handle_select_motion(self.editor, evt)
        evt.Skip()

    def on_motion_update_status(self, evt):
        byte, bit, inside = self.event_coords_to_byte(evt)
        if inside:
            self.show_status_at_index(byte, bit)
            self.task.status_bar.command_help = self.command_help
        else:
            self.task.status_bar.command_help = ""

    def show_status_at_index(self, index, bit=None):
        label = self.get_label_at_index(index)
        message = self.get_status_message_at_index(index, bit)
        self.editor.show_status_message("%s: %s %s" % (self.short_name, label, message))

    def get_label_at_index(self, index):
        try:
            label = self.editor.control.table.get_label_at_index(index)
        except AttributeError:
            label = "%x" % index
        return label

    def get_status_message_at_index(self, index, bit):
        msg = get_style_name(self.segment, index)
        comments = self.segment.get_comment(index)
        bittext = "bit=%d " % bit if bit is not None else ""
        return "%s%s  %s" % (bittext, msg, comments)

    def on_paint(self, evt):
        self.dbg_call_seq += 1
        log.debug("In on_paint %d" % self.dbg_call_seq)
        self.prepare_image()
        if self.scaled_bmp is not None:
            dc = wx.BufferedPaintDC(self, self.scaled_bmp, wx.BUFFER_CLIENT_AREA)
        evt.Skip()

    def on_resize(self, evt):
        if self.is_ready_to_render():
            self.calc_image_size()

    def on_popup(self, evt):
        byte, bit, inside = self.event_coords_to_byte(evt)
        actions = self.get_popup_actions()
        style = self.segment.style[byte] if inside else 0
        popup_data = {'index': byte, 'in_selection': style&0x80}
        if actions:
            self.editor.popup_context_menu_from_actions(self, actions, popup_data)

    def get_popup_actions(self):
        return self.editor.common_popup_actions()

    def on_focus(self, evt):
        log.debug("on_focus!")

    def on_focus_lost(self, evt):
        log.debug("on_focus_lost!")

    def on_mouse_enter(self, evt):
        evt.Skip()

    def on_mouse_leave(self, evt):
        evt.Skip()

    def on_char(self, evt):
        log.debug("on_char!")
        evt.Skip()

    def process_movement_keys(self, char):
        delta_index = None
        first_row = None
        if char == wx.WXK_UP:
            delta_index = -self.bytes_per_row
        elif char == wx.WXK_DOWN:
            delta_index = self.bytes_per_row
        elif char == wx.WXK_LEFT:
            delta_index = -1
        elif char == wx.WXK_RIGHT:
            delta_index = 1
        elif char == wx.WXK_PAGEUP:
            delta_index = -(self.fully_visible_rows * self.bytes_per_row)
            first_row = self.start_row - self.fully_visible_rows
        elif char == wx.WXK_PAGEDOWN:
            delta_index = self.fully_visible_rows * self.bytes_per_row
            first_row = self.start_row + self.fully_visible_rows
        elif char == wx.WXK_HOME:
            delta_index = -len(self.segment)
        elif char == wx.WXK_END:
            delta_index = len(self.segment)
        if delta_index is None:
            return None
        return (delta_index, first_row)

    def process_delta_index(self, delta_index):
        e = self.editor
        delta_index, first_row = delta_index  # Now a tuple, was an int
        index = e.set_cursor(e.cursor_index + delta_index, False)
        self.select_index(self, index, first_row)
        e.index_clicked(index, 0, self, False)

    def on_char_hook(self, evt):
        log.debug("on_char_hook! char=%s, key=%s, modifiers=%s" % (evt.GetUnicodeKey(), evt.GetKeyCode(), bin(evt.GetModifiers())))
        mods = evt.GetModifiers()
        char = evt.GetUnicodeKey()
        if char == 0:
            char = evt.GetKeyCode()
        delta_index = self.process_movement_keys(char)
        if delta_index is not None:
            wx.CallAfter(self.process_delta_index, delta_index)
        else:
            evt.Skip()


class BitmapScroller(BitviewScroller):
    short_name = "bitmap"

    def update_bytes_per_row(self):
        BitviewScroller.update_bytes_per_row(self)
        self.bytes_per_row = self.editor.machine.bitmap_renderer.validate_bytes_per_row(self.editor.bitmap_width)

    def update_zoom(self):
        self.set_zoom(self.editor.bitmap_zoom)

    def sync_to_editor(self, e):
        e.bitmap_zoom = self.zoom
        e.bitmap_width = self.bytes_per_row

    def event_coords_to_byte(self, evt):
        if self.end_byte is None:  # end_byte is a proxy for the image being loaded
            return 0, 0, False

        inside = True

        x, y = self.GetViewStart()
        x = (evt.GetX() // self.zoom) + x
        y = (evt.GetY() // self.zoom) + y
        if x < 0 or x >= self.grid_width or y < 0 or y > (self.start_row + self.visible_rows):
            inside = False
        if x < 0:
            x = 0
        elif x >= self.pixels_per_byte * self.bytes_per_row / self.bitplanes:
            x = self.pixels_per_byte * self.bytes_per_row / self.bitplanes - 1
        xbyte = (x // self.pixels_per_byte) * self.bitplanes
        byte = (self.bytes_per_row * y) + xbyte
        if byte >= self.end_byte:
            inside = False
        bitmask = self.pixels_per_byte - 1
        bit = bitmask - (x & bitmask)
        return byte, bit, inside

    def get_image(self, segment=None):
        if segment is None:
            segment = self.segment
        viewport_byte_start, viewport_col_offset = divmod(self.start_col, self.pixels_per_byte)
        log.debug("get_image: bit image: rows=%d:%d, cols=%d:%d, viewport_byte,col=%d,%d" % (self.start_row, self.start_row + self.visible_rows - 1, self.start_col, self.start_col + self.visible_cols - 1, viewport_byte_start, viewport_col_offset))
        sr = self.start_row
        nr = self.visible_rows
        self.start_byte = sr * self.bytes_per_row
        self.end_byte = self.start_byte + (nr * self.bytes_per_row)
        if self.end_byte > len(segment):
            self.end_byte = len(segment)
            count = self.end_byte - self.start_byte
            bytes = np.zeros((nr * self.bytes_per_row), dtype=np.uint8)
            bytes[0:count] = segment[self.start_byte:self.end_byte]
            style = np.zeros((nr * self.bytes_per_row), dtype=np.uint8)
            style[0:count] = segment.style[self.start_byte:self.end_byte]
        else:
            count = self.end_byte - self.start_byte
            bytes = segment[self.start_byte:self.end_byte]
            style = segment.style[self.start_byte:self.end_byte]
        m = self.editor.machine
        array = m.bitmap_renderer.get_image(m, self.bytes_per_row, nr, count, bytes, style)
        sc = self.start_col
        nc = self.visible_cols
        clipped = array[:,sc:sc + nc,:]
        return clipped

    def get_popup_actions(self):
        actions = BitviewScroller.get_popup_actions(self)
        actions.extend([None, BitmapWidthAction, BitmapZoomAction])
        return actions


class FontMapScroller(BitviewScroller):
    short_name = "charmap"

    def __init__(self, parent, task, bytes_per_row=8, command=None, **kwargs):
        BitviewScroller.__init__(self, parent, task, **kwargs)
        self.zoom = 2
        self.bytes_per_row = bytes_per_row
        self.pixels_per_row = 8
        self.font = None
        self.command_cls = command
        self.inverse = 0
        self.editing = False
        self.blink_index = 0
        self.blink_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update, self.blink_timer)

    @property
    def command_help(self):
        if not self.editing:
            message = "Double click or press F2 to begin editing text"
        else:
            if self.inverse:
                message = "Editing text (INVERSE MODE): Press F1 for normal characters"
            else:
                message = "Editing text: Press F1 for inverse"
            message += " (press F2 to stop editing or click outside the character map window)"
        return message

    def update(self, event):
        self.blink_index = (self.blink_index + 1) % 2
        self.Refresh()

    def is_ready_to_render(self):
        return self.font is not None

    def update_bytes_per_row(self):
        BitviewScroller.update_bytes_per_row(self)
        self.bytes_per_row = self.editor.map_width

    def update_zoom(self):
        self.set_zoom(self.editor.map_zoom)

    def sync_to_editor(self, e):
        e.map_zoom = self.zoom
        e.map_width = self.bytes_per_row

    def calc_scale_from_bytes(self):
        self.total_rows = (len(self.segment) + self.bytes_per_row - 1) / self.bytes_per_row
        self.grid_width = int(self.pixels_per_byte * self.bytes_per_row)
        self.grid_height = int(self.pixels_per_row * self.total_rows)

    def get_zoom_factors(self):
        zw = self.font.scale_w
        zh = self.font.scale_h
        return zw * self.zoom, zh * self.zoom

    def calc_scroll_params(self):
        zw, zh = self.get_zoom_factors()
        self.SetVirtualSize((self.grid_width * zw, self.grid_height * zh))
        self.SetScrollRate(self.pixels_per_byte * zw, self.pixels_per_row * zh)

    def calc_image_size(self):
        x, y = self.GetViewStart()
        w, h = self.GetClientSize().Get()
        self.start_row = y
        self.start_col = y

        # For proper buffered paiting, the visible_rows must include the
        # (possibly) partially obscured last row.  fully_visible_rows
        # indicates the number of rows without that last partially obscured
        # row (if it exists).
        zw, zh = self.get_zoom_factors()
        zoom_factor = self.pixels_per_row * zh
        self.fully_visible_rows = h / zoom_factor
        self.visible_rows = (h + zoom_factor - 1) / zoom_factor
        zoom_factor = self.pixels_per_byte * zw
        self.fully_visible_cols = w / zoom_factor
        self.start_col, self.visible_cols = x, (w + zoom_factor - 1) / zoom_factor
        log.debug("fontmap: : x, y, w, h, row start, num: %s" % str([x, y, w, h, self.start_row, self.visible_rows, self.fully_visible_rows, "col start, num:", self.start_col, self.visible_cols, self.fully_visible_cols]))

    def set_font(self):
        self.font = self.editor.machine.antic_font
        self.pixels_per_byte = self.editor.machine.font_renderer.char_bit_width
        self.pixels_per_row = self.editor.machine.font_renderer.char_bit_height
        self.calc_scroll_params()
        if self.font.use_blinking:
            self.blink_timer.Start(267)  # on/off cycle in 1.87 Hz
        else:
            self.blink_timer.Stop()

    def get_image(self, segment=None):
        if segment is None:
            segment = self.segment
        log.debug("get_image: fontmap: start=%d, num=%d" % (self.start_row, self.visible_rows))
        sr = self.start_row
        nr = self.visible_rows
        self.start_byte = sr * self.bytes_per_row
        self.end_byte = self.start_byte + (nr * self.bytes_per_row)
        if self.end_byte > len(segment):
            self.end_byte = len(segment)
            bytes = np.zeros((nr * self.bytes_per_row), dtype=np.uint8)
            bytes[0:self.end_byte - self.start_byte] = segment[sr * self.bytes_per_row:self.end_byte]
            style = np.zeros((nr * self.bytes_per_row), dtype=np.uint8)
            style[0:self.end_byte - self.start_byte] = segment.style[sr * self.bytes_per_row:self.end_byte]
        else:
            bytes = segment[self.start_byte:self.end_byte]
            style = segment.style[self.start_byte:self.end_byte]
        bytes = bytes.reshape((nr, -1))
        style = style.reshape((nr, -1))
        #log.debug("get_image: bytes", bytes)

        m = self.editor.machine
        font = m.get_blinking_font(self.blink_index)
        array = m.font_renderer.get_image(m, font, bytes, style, self.start_byte, self.end_byte, self.bytes_per_row, nr, self.start_col, self.visible_cols)
        return array

    def get_full_image(self, segment=None):
        if segment is None:
            segment = self.segment
        log.debug("get_full_image: fontmap: start=%d, num=%d" % (self.start_row, self.visible_rows))
        sr = 0
        nr = self.total_rows
        start_byte = 0
        end_byte = self.total_rows * self.bytes_per_row
        if end_byte > len(segment):
            end_byte = len(segment)
            bytes = np.zeros((nr * self.bytes_per_row), dtype=np.uint8)
            bytes[0:end_byte - start_byte] = segment[sr * self.bytes_per_row:end_byte]
            style = np.zeros((nr * self.bytes_per_row), dtype=np.uint8)
            style[0:end_byte - start_byte] = segment.style[sr * self.bytes_per_row:self.end_byte]
        else:
            bytes = segment[start_byte:end_byte].copy()
            style = segment.style[start_byte:end_byte].copy()
        # turn off any selections
        style &= get_style_mask(selected=True)

        bytes = bytes.reshape((nr, -1))
        style = style.reshape((nr, -1))
        #log.debug("get_image: bytes", bytes)

        m = self.editor.machine
        font = m.get_blinking_font(0)
        array = m.font_renderer.get_image(m, font, bytes, style, start_byte, end_byte, self.bytes_per_row, nr, 0, self.bytes_per_row)
        if self.font.scale_h > 1 or self.font.scale_w > 1:
            array = intscale(array, self.font.scale_h, self.font.scale_w)
        if self.zoom > 1:
            array = intscale(array, self.zoom)
        return array

    def draw_overlay(self, array, w, h, zw, zh):
        # Draw highlight border around rectangular selection (if any)
        anchor_start, anchor_end, rc1, rc2 = self.get_highlight_indexes()
        self.show_highlight(array, rc1, rc2, zw, zh)

        # Draw cursor position
        r, c = self.index_to_row_col(self.editor.cursor_index)
        if self.FindFocus() == self:
            color = (0, 0, 0)
        else:
            color = (128, 128, 128)
        log.debug("Draw cursor: %04x (%d, %d) start_row=%d vis=%d color=%s" % (self.editor.cursor_index + self.start_addr, r, c, self.start_row, self.fully_visible_rows, color))
        self.show_highlight(array, (r, c), (r + 1, c + 1), zw, zh, color)

    def show_highlight(self, array, rc1, rc2, zw, zh, color=None):
        if rc1 is None:
            return
        r1, c1 = rc1
        r2, c2 = rc2
        sr = r1 - self.start_row
        er = r2 - self.start_row
        sc = c1 - self.start_col
        ec = c2 - self.start_col
        x1 = sc * self.pixels_per_byte * zw
        x2 = ec * self.pixels_per_byte * zw - 1
        y1 = sr * self.pixels_per_row * zh
        y2 = er * self.pixels_per_row * zh - 1
        xmax = array.shape[1]
        ymax = array.shape[0]
        c1 = max(x1, 0)
        c2 = min(x2, xmax)
        m = self.editor.machine
        if color is None:
            color = m.empty_color

        # top
        if y1 >= 0 and y1 < ymax and c2 > c1:
            array[y1, c1:c2 + 1] = color

        # bottom
        if y2 >= 0 and y2 < ymax and c2 > c1:
            array[y2, c1:c2 + 1] = color

        c1 = max(y1, 0)
        c2 = min(y2, ymax)

        # left
        if x1 >= 0 and x1 < xmax and c2 > c1:
            array[c1:c2 + 1, x1] = color

        # right
        if x2 >= 0 and x2 < xmax and c2 > c1:
            array[c1:c2 + 1, x2] = color

    def event_coords_to_byte(self, evt):
        """Convert event coordinates to world coordinates.

        Convert the event coordinates to world coordinates by locating
        the offset of the scrolled window's viewport and adjusting the
        event coordinates.
        """
        inside = True

        zw, zh = self.get_zoom_factors()
        x, y = self.GetViewStart()
        x = (evt.GetX() // zw // self.pixels_per_byte) + x
        y = (evt.GetY() // zh // self.pixels_per_row) + y
        if x < 0 or x >= self.bytes_per_row or y < 0 or y > (self.start_row + self.visible_rows):
            inside = False
        byte = (self.bytes_per_row * y) + x
        if byte >= self.end_byte:
            inside = False
        return byte, x, inside

    def get_popup_actions(self):
        actions = BitviewScroller.get_popup_actions(self)
        actions.extend([None, FontMappingWidthAction, FontMappingZoomAction, None])
        actions.extend(self.task.get_font_mapping_actions(self.task))
        return actions

    def get_status_message_at_index(self, index, bit):
        msg = get_style_name(self.segment, index)
        comments = self.segment.get_comment(index)
        return "%s  %s" % (msg, comments)

    def set_status_message(self):
        e = self.editor
        if e is None:
            return
        e.task.status_bar.command_help = self.command_help

    def on_focus(self, evt):
        log.debug("on_focus!")
        self.inverse = 0
        self.pending_esc = False
        self.set_status_message()
        self.editing = False

    def on_focus_lost(self, evt):
        log.debug("on_focus_lost!")
        e = self.editor
        if e is not None:
            e.task.status_bar.command_help = ""
        self.editing = False

    def on_left_dclick(self, evt):
        e = self.editor
        byte, bit, inside = self.event_coords_to_byte(evt)
        if inside:
            e.set_cursor(byte, False)
            wx.CallAfter(e.index_clicked, byte, bit, self, True)
            wx.CallAfter(self.SetFocus)
            self.editing = True
            self.set_status_message()
        evt.Skip()

    def on_char(self, evt):
        log.debug("on_char! char=%s, key=%s, shift=%s, ctrl=%s, cmd=%s" % (evt.GetUnicodeKey(), evt.GetRawKeyCode(), evt.ShiftDown(), evt.ControlDown(), evt.CmdDown()))
        if not self.editing:
            evt.Skip()
            return
        char = evt.GetUnicodeKey()
        if char > 0:
            self.editor.select_none_if_selection()
            char = self.editor.machine.font_mapping.convert_byte_mapping(char)
            self.change_byte(char | self.inverse)

    def change_byte(self, value):
        e = self.editor
        if e is None:
            return
        cmd_cls = self.command_cls
        if cmd_cls is None:
            return
        if e.can_copy:
            index = e.anchor_start_index
        else:
            index = e.cursor_index
        cmd = cmd_cls(e.segment, index, index+1, value, True)
        e.process_command(cmd)

    def on_char_hook(self, evt):
        log.debug("on_char_hook! char=%s, key=%s, modifiers=%s" % (evt.GetUnicodeKey(), evt.GetKeyCode(), bin(evt.GetModifiers())))
        mods = evt.GetModifiers()
        char = evt.GetUnicodeKey()
        if char == 0:
            char = evt.GetKeyCode()
        byte = None
        delta_index = None
        if not self.editing:
            if char == wx.WXK_F2:
                self.editing = True
                self.set_status_message()
            else:
                delta_index = self.process_movement_keys(char)
        else:
            byte = self.editor.machine.font_mapping.wx_char_to_byte(char, mods, self)
            if byte is None:
                if char == wx.WXK_F1:
                    self.inverse = (self.inverse + 0x80) & 0x80
                    self.set_status_message()
                elif char == wx.WXK_F2:
                    self.editing = False
                    self.set_status_message()

                else:
                    delta_index = self.process_movement_keys(char)

        if byte is not None:
            byte = self.editor.machine.font_mapping.convert_byte_mapping(byte)
            self.change_byte(byte)
            self.pending_esc = False
        elif delta_index is not None:
            wx.CallAfter(self.process_delta_index, delta_index)
        else:
            evt.Skip()


class CharacterSetViewer(FontMapScroller):
    def __init__(self, parent, task, bytes_per_row=16, command=None, **kwargs):
        FontMapScroller.__init__(self, parent, task, bytes_per_row, command, **kwargs)
        self.segment = DefaultSegment(SegmentData(np.arange(256, dtype=np.uint8), np.zeros(256, dtype=np.uint8)), 0)
        self.start_addr = 0
        self.selected_char = -1

    def set_selected_char(self, index):
        self.selected_char = index
        e = self.editor
        if e is not None:
            e.set_current_draw_pattern(self.selected_char, self)

    def center_on_index(self):
        ul = self.find_upper_left_for_center_index(self.selected_char)
        self.set_upper_left(ul)

    def show_pattern(self, pattern):
        log.debug("charset showing pattern: %s" % str(pattern))
        index = pattern[0]
        self.selected_char = index
        self.refresh_view()

    def clear_tile_selection(self):
        self.selected_char = -1
        self.Refresh()

    def recalc_view(self):
        editor = self.task.active_editor
        if editor is not None:
            self.editor = editor
            self.set_colors()
            self.set_font()
            self.set_scale()

    def on_left_down(self, evt):
        e = self.editor
        byte, bit, inside = self.event_coords_to_byte(evt)
        if inside:
            wx.CallAfter(e.set_current_draw_pattern, byte)
        evt.Skip()

    def on_left_dclick(self, evt):
        e = self.editor
        byte, bit, inside = self.event_coords_to_byte(evt)
        if inside:
            wx.CallAfter(e.set_current_draw_pattern, byte)
        evt.Skip()

    def on_motion(self, evt):
        self.on_motion_update_status(evt)
        e = self.editor
        if e is not None and evt.LeftIsDown():
            byte, bit, inside = self.event_coords_to_byte(evt)
            if inside:
                pass
        evt.Skip()

    def set_status_message(self):
        return

    def get_popup_actions(self):
        return []

    def get_highlight_indexes(self):
        if self.selected_char < 0:
            return 0, 0, None, None
        return self.selected_char, self.selected_char + 1, None, None

    def draw_overlay(self, array, w, h, zw, zh):
        # Draw selected char position
        r, c = self.index_to_row_col(self.selected_char)
        if self.FindFocus() == self:
            color = (0, 0, 0)
        else:
            color = (128, 128, 128)
        log.debug("Draw index: %04x (%d, %d) start_row=%d vis=%d color=%s" % (self.selected_char, r, c, self.start_row, self.fully_visible_rows, color))
        self.show_highlight(array, (r, c), (r + 1, c + 1), zw, zh, color)

    def process_delta_index(self, delta_index):
        delta_index, first_row = delta_index
        _, byte = divmod(self.selected_char + delta_index, 256)
        wx.CallAfter(self.editor.set_current_draw_pattern, byte)

    def on_char_hook(self, evt):
        log.debug("on_char_hook! char=%s, key=%s, modifiers=%s" % (evt.GetUnicodeKey(), evt.GetKeyCode(), bin(evt.GetModifiers())))
        mods = evt.GetModifiers()
        char = evt.GetUnicodeKey()
        if char == 0:
            char = evt.GetKeyCode()
        delta_index = self.process_movement_keys(char)
        if delta_index is not None:
            wx.CallAfter(self.process_delta_index, delta_index)
        else:
            evt.Skip()


class MemoryMapScroller(BitviewScroller):
    def __init__(self, parent, task, **kwargs):
        BitviewScroller.__init__(self, parent, task, **kwargs)
        self.bytes_per_row = 256
        self.zoom = 2

    def update_bytes_per_row(self):
        BitviewScroller.update_bytes_per_row(self)
        self.bytes_per_row = self.editor.map_width

    def DoGetBestSize(self):
        """ Base class virtual method for sizer use to get the best size
        """
        width = self.bytes_per_row * self.zoom
        height = -1

        vw, vh = self.GetVirtualSize().Get()
        ww, wh = self.GetClientSize().Get()
        if wh < vh:
            # Scrollbar is present!
            width += wx.SystemSettings.GetMetric(wx.SYS_VSCROLL_X) + 1
        best = wx.Size(width, height)

        # Cache the best size so it doesn't need to be calculated again,
        # at least until some properties of the window change
        self.CacheBestSize(best)

        return best

    def calc_scale_from_bytes(self):
        self.total_rows = (len(self.segment) + self.bytes_per_row - 1) / self.bytes_per_row
        self.grid_width = int(self.bytes_per_row)
        self.grid_height = int(self.total_rows)

    def calc_scroll_params(self):
        z = self.zoom
        self.SetVirtualSize((self.grid_width * z, self.grid_height * z))
        self.SetScrollRate(z, z)

    def calc_image_size(self):
        x, y = self.GetViewStart()
        w, h = self.GetClientSize().Get()
        self.start_row = y
        self.start_col = x

        # For proper buffered paiting, the visible_rows must include the
        # (possibly) partially obscured last row.  fully_visible_rows
        # indicates the number of rows without that last partially obscured
        # row (if it exists).
        z = self.zoom
        self.fully_visible_rows = h / z
        self.fully_visible_cols = w / z
        self.visible_rows = (h + z - 1) / z
        self.start_col, self.visible_cols = x, (w + z - 1) / z
        log.debug("memory map: x, y, w, h, row start, num: %s" % str([x, y, w, h, self.start_row, self.visible_rows, self.fully_visible_rows, "col start, num:", self.start_col, self.visible_cols, self.fully_visible_cols]))

    def get_image(self, segment=None):
        if segment is None:
            segment = self.segment
        log.debug("get_image: memory map: start=%d, num=%d" % (self.start_row, self.visible_rows))
        t0 = time.clock()
        sr = self.start_row
        nr = self.visible_rows
        self.start_byte = sr * self.bytes_per_row
        self.end_byte = self.start_byte + (nr * self.bytes_per_row)
        if self.end_byte > len(segment):
            self.end_byte = len(segment)
            bytes = np.zeros((nr * self.bytes_per_row), dtype=np.uint8)
            bytes[0:self.end_byte - self.start_byte] = segment[sr * self.bytes_per_row:self.end_byte]
            style = np.zeros((nr * self.bytes_per_row), dtype=np.uint8)
            style[0:self.end_byte - self.start_byte] = segment.style[sr * self.bytes_per_row:self.end_byte]
        else:
            bytes = segment[self.start_byte:self.end_byte]
            style = segment.style[self.start_byte:self.end_byte]
        bytes = bytes.reshape((nr, -1))
        style = style.reshape((nr, -1))
        #log.debug("get_image: bytes", bytes)

        m = self.editor.machine
        array = m.page_renderer.get_image(m, bytes, style, self.start_byte, self.end_byte, self.bytes_per_row, nr, self.start_col, self.visible_cols)
        log.debug(array.shape)
        t = time.clock()
        log.debug("get_image: time %f" % (t - t0))
        return array

    def event_coords_to_byte(self, evt):
        """Convert event coordinates to world coordinates.

        Convert the event coordinates to world coordinates by locating
        the offset of the scrolled window's viewport and adjusting the
        event coordinates.
        """
        inside = True

        z = self.zoom
        x, y = self.GetViewStart()
        x = (evt.GetX() // z) + x
        y = (evt.GetY() // z) + y
        if x < 0 or x >= self.bytes_per_row or y < 0 or y > (self.start_row + self.visible_rows):
            inside = False
        byte = (self.bytes_per_row * y) + x
        if byte >= self.end_byte:
            inside = False
        return byte, 0, inside


if __name__ == '__main__':
    app   = wx.PySimpleApp()
    frame = wx.Frame(None, -1, title='Test', size=(500,500))
    frame.CreateStatusBar()

    panel = BitviewScroller(frame)
    bytes = np.arange(256, dtype=np.uint8)
    panel.set_data(bytes)

    sizer = wx.BoxSizer(wx.VERTICAL)
    sizer.Add(panel,  1, wx.EXPAND | wx.ALL, 5)

    def buttonHandler(evt):
        id = evt.GetId()
        if id == 100:
            panel.zoom_in()
        elif id == 101:
            panel.zoom_out()
        elif id == 200:
            wildcard="*"
            dlg = wx.FileDialog(
                frame, message="Open File",
                defaultFile="", wildcard=wildcard, style=wx.FD_OPEN)

            # Show the dialog and retrieve the user response. If it is the
            # OK response, process the data.
            if dlg.ShowModal() == wx.ID_OK:
                # This returns a Python list of files that were selected.
                paths = dlg.GetPaths()

                for path in paths:
                    dprint("open file %s:" % path)
                    fh = open(path, 'rb')
                    img = wx.Image()
                    if img.LoadStream(fh):
                        panel.setImage(img)
                    else:
                        dprint("Invalid image: %s" % path)
            # Destroy the dialog. Don't do this until you are done with it!
            # BAD things can happen otherwise!
            dlg.Destroy()
        elif id == 201:
            pass
        elif id == 202:
            panel.copy_to_clipboard()
    buttonsizer = wx.BoxSizer(wx.HORIZONTAL)
    sizer.Add(buttonsizer, 0, wx.EXPAND | wx.ALL, 5)
    button = wx.Button(frame, 100, 'Zoom In')
    frame.Bind(wx.EVT_BUTTON, buttonHandler, button)
    buttonsizer.Add(button, 0, wx.EXPAND, 0)
    button = wx.Button(frame, 101, 'Zoom Out')
    frame.Bind(wx.EVT_BUTTON, buttonHandler, button)
    buttonsizer.Add(button, 0, wx.EXPAND, 0)
    button = wx.Button(frame, 200, 'Load')
    frame.Bind(wx.EVT_BUTTON, buttonHandler, button)
    buttonsizer.Add(button, 0, wx.EXPAND, 0)
    button = wx.Button(frame, 202, 'Copy to Clipboard')
    frame.Bind(wx.EVT_BUTTON, buttonHandler, button)
    buttonsizer.Add(button, 0, wx.EXPAND, 0)

    frame.SetAutoLayout(1)
    frame.SetSizer(sizer)
    frame.Show(1)
    app.MainLoop()
