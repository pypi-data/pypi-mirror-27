# Standard library imports.
import sys
import os

# Major package imports.
import wx
import numpy as np
import json

# Enthought library imports.
from traits.api import Any, Bool, Int, Str, List, Dict, Event, Enum, Instance, File, Unicode, Property, provides, on_trait_change
from pyface.key_pressed_event import KeyPressedEvent

# Local imports.
from omnivore.framework.editor import FrameworkEditor
from omnivore.framework.actions import *
from grid_control import HexEditControl
from omnivore.utils.file_guess import FileMetadata
from omnivore8bit.arch.machine import Machine, Atari800
from omnivore8bit.utils.segmentutil import SegmentData, DefaultSegment, AnticFontSegment
from omnivore8bit.utils.searchutil import known_searchers
from omnivore.utils.processutil import run_detach

from actions import *
from commands import PasteCommand
from disassembly import DisassemblyListSaver

import logging
log = logging.getLogger(__name__)


class HexEditor(FrameworkEditor):
    """ The toolkit specific implementation of a HexEditor.  See the
    IHexEditor interface for the API documentation.
    """

    #### 'IPythonEditor' interface ############################################

    obj = Instance(File)

    #### traits

    grid_range_selected = Bool

    segment_parser = Any

    segment_number = Int(0)

    emulator_label = Unicode("Run Emulator")

    segment_parser_label = Unicode("<parser type>")

    ### View traits

    map_width = Int

    map_zoom = Int

    bitmap_width = Int

    bitmap_zoom = Int

    machine = Any

    segment = Any(None)

    last_cursor_index = Int(0)

    last_anchor_start_index = Int(0)

    last_anchor_end_index = Int(0)

    can_copy_baseline = Bool

    can_trace = Bool(False)

    can_resize_document = Bool(False)

    has_origin = Bool(False)

    segment_view_params = Dict

    # This is a flag to help set the cursor to the center row when the cursor
    # is moved in a different editor. Some editors can't use SetFocus inside an
    # event handler, so the focus could still be set on one editor even though
    # the user clicked on another. This results in the first editor not getting
    # centered unless this flag is checked also.
    pending_focus = Any(None)  # Flag to help

    #### Events ####

    changed = Event

    key_pressed = Event(KeyPressedEvent)

    # Class attributes (not traits)

    searchers = known_searchers

    rect_select = False

    ##### Default traits

    def _machine_default(self):
        return Atari800

    def _segment_default(self):
        rawdata = SegmentData([])
        return DefaultSegment(rawdata)

    def _map_width_default(self):
        prefs = self.task.preferences
        return prefs.map_width

    def _map_zoom_default(self):
        return 2

    def _bitmap_width_default(self):
        prefs = self.task.preferences
        return prefs.bitmap_width

    def _bitmap_zoom_default(self):
        return 5

    # Convenience functions

    @property
    def section_name(self):
        return str(self.segment)

    ###########################################################################
    # 'FrameworkEditor' interface.
    ###########################################################################

    def create(self, parent):
        self.control = self._create_control(parent)
        self.machine.one_time_init(self)
        self.task.machine_menu_changed = self.machine

    def from_metadata_dict(self, e):
        if 'machine mime' in e:
            mime = e['machine mime']
            if not mime.startswith(self.machine.mime_prefix):
                m = self.machine.find_machine_by_mime(mime)
                if m is not None:
                    self.machine = m
        if 'font' in e:
            # FIXME: I don't think 'font' is set anywhere, so this never gets called
            self.machine.set_font(e['font'][0], e['font'][1])
        if 'initial segment' in e:
            self.initial_segment = e['initial segment']
        if 'diff highlight' in e:
            self.diff_highlight = bool(e['diff highlight'])
        if 'map width' in e:
            self.map_width = e['map width']
        if 'map zoom' in e:
            self.map_zoom = e['map zoom']
        if 'bitmap width' in e:
            self.bitmap_width = e['bitmap width']
        if 'bitmap zoom' in e:
            self.bitmap_zoom = e['bitmap zoom']
        if 'segment view params' in e:
            self.segment_view_params = e['segment view params']
        self.machine.restore_extra_from_dict(e)

    def to_metadata_dict(self, mdict, document):
        mdict["diff highlight"] = self.diff_highlight
        mdict["map width"] = self.map_width
        mdict["map zoom"] = self.map_zoom
        mdict["bitmap width"] = self.bitmap_width
        mdict["bitmap zoom"] = self.bitmap_zoom
        if document == self.document:
            # If we're saving the document currently displayed, save the
            # display parameters too.
            mdict["segment view params"] = dict(self.segment_view_params)  # shallow copy, but only need to get rid of Traits dict wrapper
        self.machine.serialize_extra_to_dict(mdict)

    def rebuild_document_properties(self):
        if not self.document.has_baseline:
            self.use_self_as_baseline(self.document)
        FrameworkEditor.rebuild_document_properties(self)
        self.find_segment()
        self.update_emulator()
        self.compare_to_baseline()
        self.can_resize_document = self.document.can_resize
        self.task.machine_menu_changed = self.machine

    def process_preference_change(self, prefs):
        log.debug("%s processing preferences change" % self.task.name)
        self.machine.set_text_font(prefs.text_font)
        self.map_width = prefs.map_width
        self.bitmap_width = prefs.bitmap_width

    def copy_view_properties(self, old_editor):
        try:
            self.machine = old_editor.machine.clone_machine()
        except AttributeError:
            self.machine = self._machine_default()

    @property
    def document_length(self):
        return len(self.segment)

    def process_paste_data_object(self, data_obj, cmd_cls=None):
        bytes, extra = self.get_numpy_from_data_object(data_obj)
        ranges, indexes = self.get_selected_ranges_and_indexes()
        if extra and (extra[0] == "numpy,multiple" or extra[0] == "numpy"):
            source_indexes, style, where_comments, comments = extra[1:5]
        else:
            source_indexes = style = where_comments = comments = None
        if cmd_cls is None:
            cmd_cls = PasteCommand
        cmd = cmd_cls(self.segment, ranges, self.cursor_index, bytes, source_indexes, style, where_comments, comments)
        self.process_command(cmd)

    def get_numpy_from_data_object(self, data_obj):
        # Full list of valid data formats:
        #
        # >>> import wx
        # >>> [x for x in dir(wx) if x.startswith("DF_")]
        # ['DF_BITMAP', 'DF_DIB', 'DF_DIF', 'DF_ENHMETAFILE', 'DF_FILENAME',
        # 'DF_HTML', 'DF_INVALID', 'DF_LOCALE', 'DF_MAX', 'DF_METAFILE',
        # 'DF_OEMTEXT', 'DF_PALETTE', 'DF_PENDATA', 'DF_PRIVATE', 'DF_RIFF',
        # 'DF_SYLK', 'DF_TEXT', 'DF_TIFF', 'DF_UNICODETEXT', 'DF_WAVE']
        extra = None
        if wx.DF_TEXT in data_obj.GetAllFormats():
            value = data_obj.GetText().encode('utf-8')
        elif wx.DF_UNICODETEXT in data_obj.GetAllFormats():  # for windows
            value = data_obj.GetText().encode('utf-8')
        else:
            value = data_obj.GetData().tobytes()
            fmt = data_obj.GetPreferredFormat()
            if fmt.GetId() == "numpy,columns":
                r, c, value = value.split(",", 2)
                extra = fmt.GetId(), int(r), int(c)
            elif fmt.GetId() == "numpy":
                len1, value = value.split(",", 1)
                len1 = int(len1)
                value, j = value[0:len1], value[len1:]
                style, where_comments, comments = self.restore_selected_index_metadata(j)
                extra = fmt.GetId(), None, style, where_comments, comments
            elif fmt.GetId() == "numpy,multiple":
                len1, len2, value = value.split(",", 2)
                len1 = int(len1)
                len2 = int(len2)
                split1 = len1
                split2 = len1 + len2
                value, index_string, j = value[0:split1], value[split1:split2], value[split2:]
                indexes = np.fromstring(index_string, dtype=np.uint32)
                style, where_comments, comments = self.restore_selected_index_metadata(j)
                extra = fmt.GetId(), indexes, style, where_comments, comments
        bytes = np.fromstring(value, dtype=np.uint8)
        return bytes, extra

    supported_clipboard_data_objects = [
        wx.CustomDataObject("numpy,multiple"),
        wx.CustomDataObject("numpy"),
        wx.CustomDataObject("numpy,columns"),
        wx.TextDataObject(),
        ]

    def create_clipboard_data_object(self):
        ranges, indexes = self.get_selected_ranges_and_indexes()
        metadata = self.get_selected_index_metadata(indexes)
        if len(ranges) == 1:
            r = ranges[0]
            data = self.segment[r[0]:r[1]]
            s1 = data.tostring()
            metadata = self.get_selected_index_metadata(indexes)
            data_obj = wx.CustomDataObject("numpy")
            s = "%d,%s%s" % (len(s1), s1, metadata)
            data_obj.SetData(s)
        elif np.alen(indexes) > 0:
            data = self.segment[indexes]
            s1 = data.tostring()
            s2 = indexes.tostring()
            metadata = self.get_selected_index_metadata(indexes)
            data_obj = wx.CustomDataObject("numpy,multiple")
            s = "%d,%d,%s%s%s" % (len(s1), len(s2), s1, s2, metadata)
            data_obj.SetData(s)
        else:
            data_obj = None
        if data_obj is not None:
            text = " ".join(["%02x" % i for i in data])
            text_obj = wx.TextDataObject()
            text_obj.SetText(text)
            c = wx.DataObjectComposite()
            c.Add(data_obj)
            c.Add(text_obj)
            return c
        return None

    def show_data_object_stats(self, data_obj, copy=True):
        try:
            fmt = data_obj.GetFormat()
        except AttributeError:
            fmt = data_obj.GetPreferredFormat()
        if fmt.GetId() == "numpy,columns":
            d = self.get_data_object_by_format(data_obj, fmt)
            value = d.GetData().tobytes()
            r, c, value = value.split(",", 2)
            size = int(r) * int(c)
        elif fmt.GetId() == "numpy":
            d = self.get_data_object_by_format(data_obj, fmt)
            value = d.GetData().tobytes()
            size, _ = value.split(",", 1)
            size = int(size)
        elif fmt.GetId() == "numpy,multiple":
            d = self.get_data_object_by_format(data_obj, fmt)
            value = d.GetData().tobytes()
            size, _, _ = value.split(",", 2)
            size = int(size)
        else:
            FrameworkEditor.show_data_object_stats(self, data_obj)
            return
        self.task.status_bar.message = "%s $%x bytes (%d decimal)" % ("Copied" if copy else "Pasted", size, size)

    def get_selected_index_metadata(self, indexes):
        """Return serializable string containing style information"""
        style = self.segment.get_style_at_indexes(indexes)
        r_orig = self.segment.get_style_ranges(comment=True)
        comments = self.segment.get_comments_at_indexes(indexes)
        log.debug("after get_comments_at_indexes: %s" % str(comments))
        metadata = [style.tolist(), comments[0].tolist(), comments[1]]
        j = json.dumps(metadata)
        return j

    def restore_selected_index_metadata(self, metastr):
        metadata = json.loads(metastr)
        style = np.asarray(metadata[0], dtype=np.uint8)
        where_comments = np.asarray(metadata[1], dtype=np.int32)
        return style, where_comments, metadata[2]

    def rebuild_ui(self):
        self.segment = self.document.segments[self.segment_number]
        self.reconfigure_panes()
        self.update_segments_ui()

    def update_segments_ui(self):
        # Note: via profiling, it turns out that this is a very heavyweight
        # call, producing hundreds of thousands of trait notifier events. This
        # should only be called when the number of segments or document has
        # changed. If only the segment being viewed is changed, just set the
        # task.segment_selected trait
        if self.segment_list is not None:
            self.segment_list.set_segments(self.document.segments, self.segment_number)
        self.sidebar.recalc_active()
        if self.segment_parser is not None:
            self.segment_parser_label = self.segment_parser.menu_name
        else:
            self.segment_parser_label = "No parser"
        self.task.segments_changed = self.document.segments
        self.task.segment_selected = self.segment_number

    def reconfigure_panes(self):
        log.debug("%s: reconfigure_panes" % self.task.name)
        self.hex_edit.recalc_view()
        self.disassembly.recalc_view()
        self.bitmap.recalc_view()
        self.font_map.recalc_view()
        self.has_origin = self.segment.start_addr > 0

    def check_document_change(self):
        if self.last_cursor_index != self.cursor_index or self.last_anchor_start_index != self.anchor_start_index or self.last_anchor_end_index != self.anchor_end_index:
            self.document.change_count += 1
            self.update_cursor_history()

    def get_cursor_state(self):
        return self.segment, self.cursor_index

    def restore_cursor_state(self, state):
        segment, index = state
        number = self.document.find_segment_index(segment)
        if number < 0:
            log.error("tried to restore cursor to a deleted segment? %s" % segment)
        else:
            if number != self.segment_number:
                self.view_segment_number(number)
            self.index_clicked(index, 0, None)
        log.debug(self.cursor_history)

    def refresh_panes(self):
        self.check_document_change()
        self.hex_edit.refresh_view()
        self.disassembly.refresh_view()
        self.bitmap.refresh_view()
        self.font_map.refresh_view()
        self.sidebar.refresh_active()

    def set_bitmap_width(self, width=None):
        if width is None:
            width = self.bitmap_width
        self.bitmap_width = width
        self.bitmap.recalc_view()

    def set_bitmap_zoom(self, zoom=None):
        if zoom is None:
            zoom = self.bitmap_zoom
        self.bitmap_zoom = zoom
        self.bitmap.recalc_view()

    @on_trait_change('machine.bitmap_shape_change_event,machine.bitmap_color_change_event')
    def update_bitmap(self):
        self.bitmap.recalc_view()

    @on_trait_change('machine.font_change_event')
    def update_fonts(self):
        self.font_map.set_font()
        self.font_map.Refresh()
        pane = self.window.get_dock_pane('hex_edit.font_map')
        if pane is not None:
            # subclasses may not have font map pane
            pane.name = self.machine.font_mapping.name
            self.window._aui_manager.Update()

    @on_trait_change('machine.disassembler_change_event')
    def update_disassembler(self):
        self.disassembly.recalc_view()

    @on_trait_change('document.emulator_change_event')
    def update_emulator(self):
        emu = self.document.emulator
        if emu is None:
            emu = self.machine.get_system_default_emulator(self.task)
        if not self.machine.is_known_emulator(emu):
            self.machine.add_emulator(self.task, emu)
        self.emulator_label = "Run using '%s'" % emu['name']

    def run_emulator(self):
        emu = self.document.emulator
        if not emu:
            emu = self.machine.get_system_default_emulator(self.task)
        if self.dirty:
            if not self.save():
                return
        exe = emu['exe']
        args = emu['args']
        fspath = self.document.filesystem_path()
        if fspath is not None:
            try:
                run_detach(exe, args, fspath, "%s")
            except RuntimeError, e:
                self.window.error("Failed launching %s %s\n\nError: %s" % (exe, args, str(e)), "%s Emulator Error" % emu['name'])
        else:
            self.window.error("Can't run emulator on:\n\n%s\n\nDocument is not on local filesystem" % self.document.uri, "%s Emulator Error" % emu['name'])

    def set_map_width(self, width=None):
        if width is None:
            width = self.map_width
        self.map_width = width
        self.font_map.recalc_view()

    def set_map_zoom(self, zoom=None):
        if zoom is None:
            zoom = self.map_zoom
        self.map_zoom = zoom
        self.font_map.recalc_view()

    def get_font_from_selection(self):
        pass

    def set_machine(self, machine):
        self.machine = machine
        self.reconfigure_panes()

    def find_segment_parser(self, parsers, segment_name=None):
        self.document.parse_segments(parsers)
        self.find_segment(segment_name)

    def find_first_valid_segment_index(self):
        return 0

    def find_segment(self, segment_name=None, segment=None, refresh=False):
        if segment_name is not None:
            index = self.document.find_segment_index_by_name(segment_name)
        elif segment is not None:
            index = self.document.find_segment_index(segment)
        else:
            index = self.find_first_valid_segment_index()
        if index < 0:
            index = 0
        self.segment_parser = self.document.segment_parser
        if refresh:
            self.view_segment_number(index)
        else:
            self.segment_number = index
            self.segment_parser = self.document.segment_parser
            self.segment = self.document.segments[index]
            self.view_segment_set_width(self.segment)
            self.select_none(refresh=False)
            self.task.segment_selected = self.segment_number

    def set_segment_parser(self, parser):
        self.find_segment_parser([parser])
        self.rebuild_ui()

    def view_segment_set_width(self, segment):
        pass

    def save_segment_view_params(self, segment):
        d = {
            'cursor_index': self.cursor_index,
            'main_window': self.control.get_view_params(),
        }
        for pane in self.task.iter_panes():
            try:
                d[pane.id] = pane.control.get_view_params()
            except AttributeError:
                pass

        self.segment_view_params[segment.uuid] = d

    def restore_segment_view_params(self, segment):
        try:
            d = self.segment_view_params[segment.uuid]
        except KeyError:
            log.debug("no view params for %s" % segment.uuid)
            return
        log.debug("restoring view params for %s" % segment.uuid)
        self.cursor_index = d['cursor_index']
        if 'main_window' in d:
            self.control.restore_view_params(d['main_window'])
        for pane in self.task.iter_panes():
            try:
                params = d[pane.id]
            except KeyError:
                continue
            try:
                pane.control.restore_view_params(params)
            except AttributeError:
                continue

    def view_segment_number(self, number):
        doc = self.document
        num = number if number < len(doc.segments) else len(doc.segments) - 1
        if num != self.segment_number:
            old_segment = self.segment
            if old_segment is not None:
                self.save_segment_view_params(old_segment)
            self.segment = doc.segments[num]
            self.adjust_selection(old_segment)
            self.segment_number = num
            self.invalidate_search()
            self.view_segment_set_width(self.segment)
            self.reconfigure_panes()
            self.show_trace()
            if self.segment_list is not None:
                self.segment_list.SetSelection(self.segment_number)
            else:
                self.sidebar.refresh_active()
            self.task.status_bar.message = "Switched to segment %s" % str(self.segment)
            self.task.update_window_title()
        self.task.segment_selected = self.segment_number

    def get_extra_segment_savers(self, segment):
        savers = []
        savers.append(self.disassembly)
        savers.append(DisassemblyListSaver)
        return savers

    def save_segment(self, saver, uri):
        try:
            bytes = saver.encode_data(self.segment, self)
            saver = lambda a,b: bytes
            self.document.save_to_uri(uri, self, saver, save_metadata=False)
        except Exception, e:
            log.error("%s: %s" % (uri, str(e)))
            #self.window.error("Error trying to save:\n\n%s\n\n%s" % (uri, str(e)), "File Save Error")
            raise

    def show_trace(self):
        """Highlight the current trace after switching to a new segment

        """
        if self.can_trace:
            self.disassembly.update_trace_in_segment()
            self.document.change_count += 1

    def invalidate_search(self):
        self.task.change_minibuffer_editor(self)

    def compare_to_baseline(self):
        if self.diff_highlight and self.document.has_baseline:
            self.document.update_baseline()

    def adjust_selection(self, old_segment):
        """Adjust the selection of the current segment so that it is limited to the
        bounds of the new segment.
        
        If the current selection is entirely out of bounds of the new segment,
        all the selection indexes will be set to zero.
        """
        # find byte index of view into master array
        g = self.document.container_segment
        s = self.segment
        global_offset = g.get_raw_index(0)
        new_offset = s.get_raw_index(0)
        old_offset = old_segment.get_raw_index(0)

        self.restore_segment_view_params(s)
        self.selected_ranges = s.get_style_ranges(selected=True)
        if self.selected_ranges:
            # Arbitrarily puth the anchor on the last selected range
            last = self.selected_ranges[-1]
            self.anchor_initial_start_index = self.anchor_start_index = last[0]
            self.anchor_initial_end_index = self.anchor_end_index = last[1]
        g.clear_style_bits(selected=True)
        self.document.change_count += 1
        self.highlight_selected_ranges()

    def highlight_selected_ranges(self):
        s = self.segment
        s.clear_style_bits(selected=True)
        s.set_style_ranges(self.selected_ranges, selected=True)
        self.document.change_count += 1
        self.can_copy_baseline = self.can_copy and self.baseline_present

    def convert_ranges(self, from_style, to_style):
        s = self.segment
        ranges = s.get_style_ranges(**from_style)
        s.clear_style_bits(**from_style)
        s.clear_style_bits(**to_style)
        s.set_style_ranges(ranges, **to_style)
        self.selected_ranges = s.get_style_ranges(selected=True)
        self.document.change_count += 1

    def get_label_at_index(self, index):
        return self.hex_edit.table.get_label_at_index(index)

    def get_label_of_ranges(self, ranges):
        labels = []
        for start, end in ranges:
            if start > end:
                start, end = end, start
            labels.append("%s-%s" % (self.get_label_at_index(start), self.get_label_at_index(end - 1)))
        return ", ".join(labels)

    def get_label_of_first_byte(self, ranges):
        labels = []
        for start, end in ranges:
            if start > end:
                start, end = end, start
            labels.append(self.get_label_at_index(start))
        return ", ".join(labels)

    def get_segments_from_selection(self, size=-1):
        s = self.segment
        segments = []

        # Get the selected ranges directly from the segment style data, because
        # the individual range entries in self.selected_ranges can be out of
        # order or overlapping
        ranges = s.get_style_ranges(selected=True)
        if len(ranges) == 1:
            seg_start, seg_end = ranges[0]
            if size < 0:
                size = seg_end - seg_start
            for start in range(seg_start, seg_end, size):
                end = min(seg_end, start + size)
                segment = DefaultSegment(s.rawdata[start:end], s.start_addr + start)
                segments.append(segment)
        elif len(ranges) > 1:
            # If there are multiple selections, use an indexed segment
            indexes = []
            for start, end in ranges:
                indexes.extend(range(start, end))
            if size < 0:
                size = len(indexes)
            for i in range(0, len(indexes), size):
                raw = s.rawdata.get_indexed(indexes[i:i + size])
                segment = DefaultSegment(raw, s.start_addr + indexes[i])
                segments.append(segment)
        return segments

    def get_selected_status_message(self):
        if not self.selected_ranges:
            return ""
        if len(self.selected_ranges) == 1:
            r = self.selected_ranges
            first = r[0][0]
            last = r[0][1]
            num = abs(last - first)
            if num == 1: # python style, 4:5 indicates a single byte
                return "[1 byte selected %s]" % self.get_label_of_ranges(r)
            elif num > 0:
                return "[%d bytes selected %s]" % (num, self.get_label_of_ranges(r))
        else:
            return "[%d ranges selected]" % (len(self.selected_ranges))

    def show_status_message(self, msg):
        s = self.get_selected_status_message()
        if s:
            msg = "%s %s" % (msg, s)
        self.task.status_bar.message = msg

    def add_user_segment(self, segment, update=True):
        self.document.add_user_segment(segment)
        self.added_segment(segment, update)

    def added_segment(self, segment, update=True):
        if update:
            self.update_segments_ui()
            if self.segment_list is not None:
                self.segment_list.ensure_visible(segment)
        self.metadata_dirty = True

    def delete_user_segment(self, segment):
        self.document.delete_user_segment(segment)
        self.view_segment_number(self.segment_number)
        self.update_segments_ui()
        self.metadata_dirty = True

    def find_in_user_segment(self, base_index):
        for s in self.document.user_segments:
            try:
                index = s.get_index_from_base_index(base_index)
                return s, index
            except IndexError:
                continue
        for s in self.document.segment_parser.segments[1:]:
            try:
                index = s.get_index_from_base_index(base_index)
                return s, index
            except IndexError:
                continue
        return None, None

    def ensure_visible(self, start, end):
        self.index_clicked(start, 0, None)

    def update_history(self):
#        history = document.undo_stack.serialize()
#        self.window.application.save_log(str(history), "command_log", ".log")
        if self.undo_history is not None:
            self.undo_history.update_history()
        self.sidebar.refresh_active()

    def mark_index_range_changed(self, index_range):
        self.disassembly.restart_disassembly(index_range[0])

    def get_goto_action_in_segment(self, addr_dest):
        if addr_dest >= 0:
            segment_start = self.segment.start_addr
            segment_num = -1
            addr_index = addr_dest - segment_start
            segments = self.document.find_segments_in_range(addr_dest)
            if addr_dest < segment_start or addr_dest > segment_start + len(self.segment):
                # segment_num, segment_dest, addr_index = self.editor.document.find_segment_in_range(addr_dest)
                if not segments:
                    msg = "Address $%04x not in any segment" % addr_dest
                    addr_dest = -1
                else:
                    # Don't chose a default segment, just show the sub menu
                    msg = None
            else:
                msg = "Go to $%04x" % addr_dest
            if msg:
                action = GotoIndexAction(name=msg, enabled=True, segment_num=segment_num, addr_index=addr_index, task=self.task, active_editor=self)
            else:
                action = None
        else:
            msg = "No address to jump to"
            action = GotoIndexAction(name=msg, enabled=False, task=self.task)
        return action

    def get_goto_actions_other_segments(self, addr_dest):
        """Add sub-menu to popup list for segments that have the same address
        """
        goto_actions = []
        segments = self.document.find_segments_in_range(addr_dest)
        if len(segments) > 0:
            other_segment_actions = ["Go to $%04x in Other Segment..." % addr_dest]
            for segment_num, segment_dest, addr_index in segments:
                if segment_dest == self.segment:
                    continue
                msg = str(segment_dest)
                action = GotoIndexAction(name=msg, enabled=True, segment_num=segment_num, addr_index=addr_index, task=self.task, active_editor=self)
                other_segment_actions.append(action)
            if len(other_segment_actions) > 1:
                # found another segment other than itself
                goto_actions.append(other_segment_actions)
        return goto_actions

    def get_goto_actions_same_byte(self, index):
        """Add sub-menu to popup list for for segments that have the same raw
        index (index into the base array) as the index into the current segment
        """
        goto_actions = []
        raw_index = self.segment.get_raw_index(index)
        segments = self.document.find_segments_with_raw_index(raw_index)
        if len(segments) > 0:
            other_segment_actions = ["Go to Same Byte in Other Segment..."]
            for segment_num, segment_dest, addr_index in segments:
                if segment_dest == self.segment:
                    continue
                msg = str(segment_dest)
                action = GotoIndexAction(name=msg, enabled=True, segment_num=segment_num, addr_index=addr_index, task=self.task, active_editor=self)
                other_segment_actions.append(action)
            if len(other_segment_actions) > 1:
                # found another segment other than itself
                goto_actions.append(other_segment_actions)
        return goto_actions

    def common_popup_actions(self):
        return [CutAction, CopyAction, ["Copy Special", CopyDisassemblyAction, CopyCommentsAction, CopyAsReprAction, CopyAsCBytesAction], PasteAction, ["Paste Special", PasteAndRepeatAction, PasteCommentsAction], None, SelectAllAction, SelectNoneAction, ["Mark Selection As", MarkSelectionAsCodeAction, MarkSelectionAsDataAction, MarkSelectionAsUninitializedDataAction, MarkSelectionAsDisplayListAction, MarkSelectionAsJumpmanLevelAction, MarkSelectionAsJumpmanHarvestAction], None, GetSegmentFromSelectionAction, RevertToBaselineAction, None, AddCommentPopupAction, RemoveCommentPopupAction, AddLabelPopupAction, RemoveLabelPopupAction]

    def change_bytes(self, start, end, bytes, pretty=None):
        """Convenience function to perform a ChangeBytesCommand
        """
        self.document.change_count += 1
        cmd = CoalescingChangeByteCommand(self.segment, start, end, bytes)
        if pretty:
            cmd.pretty_name = pretty
        self.process_command(cmd)

    def popup_visible(self):
        log.debug("checking sidebar: popup visible? %s" % self.sidebar.control.has_popup())
        return self.sidebar.control.has_popup()

    def clear_popup(self):
        log.debug("clearing popup")
        self.sidebar.control.clear_popup()

    ###########################################################################
    # Trait handlers.
    ###########################################################################

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _create_control(self, parent):
        """ Creates the toolkit-specific control for the widget. """

        # Base-class constructor.
        self.hex_edit = HexEditControl(parent, self.task)

        ##########################################
        # Events.
        ##########################################

        # Get related controls
        self.disassembly = self.window.get_dock_pane('hex_edit.disassembly').control
        self.bitmap = self.window.get_dock_pane('hex_edit.bitmap').control
        self.font_map = self.window.get_dock_pane('hex_edit.font_map').control
        try:
            self.segment_list = self.window.get_dock_pane('hex_edit.segments').control
        except AttributeError:
            self.segment_list = None
        try:
            self.undo_history = self.window.get_dock_pane('hex_edit.undo').control
        except AttributeError:
            self.undo_history = None
        self.sidebar = self.window.get_dock_pane('hex_edit.sidebar')

        # Load the editor's contents.
        self.load()

        return self.hex_edit

    #### wx event handlers ####################################################

    def index_clicked(self, index, bit, from_control, refresh_from=True):
        self.cursor_index = index
        self.check_document_change()
        skip_control = None if refresh_from else from_control
        if skip_control != self.hex_edit:
            self.hex_edit.select_index(from_control, index)
        if skip_control != self.disassembly:
            self.disassembly.select_index(from_control, index, bit)
        if skip_control != self.bitmap:
            self.bitmap.select_index(from_control, index)
        if skip_control != self.font_map:
            self.font_map.select_index(from_control, index)
        self.sidebar.refresh_active()
        self.can_copy = len(self.selected_ranges) > 1 or (bool(self.selected_ranges) and (self.selected_ranges[0][0] != self.selected_ranges[0][1]))
        self.can_copy_baseline = self.can_copy and self.baseline_present
