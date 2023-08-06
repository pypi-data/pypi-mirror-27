import wx


class SelectionMixin(object):
    def __init__(self):
        self.multi_select_mode = False
        self.select_extend_mode = False
        self.mouse_drag_started = False
        self.pending_select_awaiting_drag = None

    def handle_select_start(self, editor, evt, selecting_rows=False, col=0):
        editor.pending_focus = self
        self.mouse_drag_started = True
        r, c, index1, index2, inside = self.get_location_from_event(evt)
        if c < 0 or selecting_rows or not inside:
            c = 0
            selecting_rows = True
        else:
            selecting_rows = False
        if evt.ControlDown():
            self.multi_select_mode = True
            self.select_extend_mode = False
        elif evt.ShiftDown():
            self.multi_select_mode = False
            self.select_extend_mode = True
        if self.select_extend_mode:
            if index1 < editor.anchor_start_index:
                editor.anchor_start_index = index1
                editor.cursor_index = index1
            elif index2 > editor.anchor_start_index:
                editor.anchor_end_index = index2
                editor.cursor_index = index2 - 1
            editor.anchor_initial_start_index, editor.anchor_initial_end_index = editor.anchor_start_index, editor.anchor_end_index
            editor.select_range(editor.anchor_start_index, editor.anchor_end_index, add=self.multi_select_mode)
        else:
            self.ClearSelection()
            if selecting_rows:
                index1, index2 = self.get_start_end_index_of_row(r)
            editor.anchor_initial_start_index, editor.anchor_initial_end_index = index1, index2
            editor.cursor_index = index1
            if selecting_rows:
                editor.select_range(index1, index2, add=self.multi_select_mode)
            else:
                # initial click when not selecting rows should move the cursor,
                # not select the grid square
                self.pending_select_awaiting_drag = (index1, index2)
                if not self.multi_select_mode:
                    editor.select_none()
                    # status line doesn't get automatically updated to show
                    # nothing is selected, so force the update
                    wx.CallAfter(self.show_status_at_index, index1)
        wx.CallAfter(editor.index_clicked, editor.cursor_index, c, self, True)

    def handle_select_motion(self, editor, evt, selecting_rows=False):
        if not self.mouse_drag_started:
            # On windows, it's possible to get a motion event before a mouse
            # down event, so need this flag to check
            return
        update = False
        r, c, index1, index2, inside = self.get_location_from_event(evt)
        if c < 0 or selecting_rows or not inside:
            selecting_rows = True
            c = 0
        else:
            selecting_rows = False
            if self.pending_select_awaiting_drag is not None:
                # We have an actual drag so we can begin the selection
                editor.anchor_initial_start_index, editor.anchor_initial_end_index = self.pending_select_awaiting_drag
                self.pending_select_awaiting_drag = None
                editor.select_range(editor.anchor_initial_start_index, editor.anchor_initial_end_index, add=self.multi_select_mode)
                update = True
        if self.select_extend_mode:
            if index1 < editor.anchor_initial_start_index:
                editor.select_range(index1, editor.anchor_initial_end_index, extend=True)
                update = True
            else:
                editor.select_range(editor.anchor_initial_start_index, index2, extend=True)
                update = True
        else:
            if index2 >= editor.anchor_initial_end_index:
                if selecting_rows:
                    index1, index2 = self.get_start_end_index_of_row(r)
                if index2 != editor.anchor_end_index:
                    editor.select_range(editor.anchor_initial_start_index, index2, extend=self.multi_select_mode)
                    update = True
            elif index1 <= editor.anchor_initial_start_index:
                if selecting_rows:
                    index1, index2 = self.get_start_end_index_of_row(r)
                if index1 != editor.anchor_start_index:
                    editor.select_range(index1, editor.anchor_initial_end_index, extend=self.multi_select_mode)
                    update = True
        if update:
            editor.cursor_index = index1
            wx.CallAfter(editor.index_clicked, editor.cursor_index, c, self, True)

    def handle_select_end(self, editor, evt):
        self.mouse_drag_started = False
        self.select_extend_mode = False
        self.multi_select_mode = False
        editor.pending_focus = None

    def ClearSelection(self):
        # Stub function for those controls that don't have it. Tables use this
        # but nothing else so far.
        pass

    def get_location_from_event(self, evt):
        raise NotImplementedError

    def get_start_end_index_of_row(self, row):
        raise NotImplementedError
