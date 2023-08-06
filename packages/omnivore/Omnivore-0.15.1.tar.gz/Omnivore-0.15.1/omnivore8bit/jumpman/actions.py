""" Action definitions for Jumpman Task

"""
import os
import sys

import wx

# Enthought library imports.
from pyface.action.api import Action, ActionItem
from pyface.tasks.action.api import EditorAction

from omnivore.utils.wx.dialogs import prompt_for_hex, prompt_for_string, ChooseOnePlusCustomDialog
from omnivore.utils.textutil import text_to_int
from omnivore.framework.actions import SelectAllAction, SelectNoneAction, SelectInvertAction, TaskDynamicSubmenuGroup
from omnivore8bit.utils.jumpman import DrawObjectBounds, is_valid_level_segment
from omnivore8bit.hex_edit.actions import UseSegmentAction

from commands import *

import logging
log = logging.getLogger(__name__)


def trigger_dialog(event, e, obj):
    possible_labels = e.get_triggers()
    label = e.get_trigger_label(obj.trigger_function)
    if label is None and obj.trigger_function:
        custom_value = "%04x" % obj.trigger_function
    else:
        custom_value = ""
    dlg = ChooseOnePlusCustomDialog(event.task.window.control, possible_labels.keys(), label, custom_value, "Choose Trigger Function", "Select one trigger function or enter custom address", "Trigger Addr (hex)")
    if dlg.ShowModal() == wx.ID_OK:
        label, addr = dlg.get_selected()
        if label is not None:
            addr = possible_labels[label]
        else:
            try:
                addr = text_to_int(addr, "hex")
            except ValueError:
                event.task.window.error("Invalid address %s" % addr)
                addr = None
    else:
        addr = None
    dlg.Destroy()
    return addr


class ClearTriggerAction(EditorAction):
    """Remove any trigger function from the selected peanut(s).
    
    """
    name = "Clear Trigger Function"
    enabled_name = 'can_copy'
    command = ClearTriggerCommand

    picked = None

    def get_objects(self):
        if self.picked is not None:
            return self.picked
        return self.active_editor.bitmap.mouse_mode.objects

    def get_addr(self, event, objects):
        return None

    def permute_object(self, obj, addr):
        obj.trigger_function = addr

    def perform(self, event):
        e = self.active_editor
        objects = self.get_objects()
        try:
            addr = self.get_addr(event, objects)
            for o in objects:
                self.permute_object(o, addr)
            e.bitmap.save_changes(self.command)
            e.bitmap.mouse_mode.resync_objects()
        except ValueError:
            pass


class SetTriggerAction(ClearTriggerAction):
    """Set a trigger function for the selected peanut(s).

    If you have used the custom code option, have compiled your code using the
    built-in assembler, *and* your code has labels that start with ``trigger``,
    these will show up in the list that appears when you invoke this action.

    Otherwise, you can specify the hex address of a subroutine.
    """
    name = "Set Trigger Function..."
    command = SetTriggerCommand

    def get_addr(self, event, objects):
        e = self.active_editor
        addr = trigger_dialog(event, e, objects[0])
        if addr is not None:
            return addr
        raise ValueError("Cancelled!")


class SelectAllJumpmanAction(EditorAction):
    """Select all drawing elements in the main level

    """
    name = 'Select All'
    accelerator = 'Ctrl+A'
    tooltip = 'Select the entire document'
    enabled_name = 'can_select_objects'

    def perform(self, event):
        event.task.active_editor.select_all()


class SelectNoneJumpmanAction(EditorAction):
    """Clear all selections

    """
    name = 'Select None'
    accelerator = 'Shift+Ctrl+A'
    tooltip = 'Clear selection'
    enabled_name = 'can_select_objects'

    def perform(self, event):
        event.task.active_editor.select_none()


class SelectInvertJumpmanAction(EditorAction):
    """Invert the selection; that is: select everything that is currently
    unselected and unselect those that were selected.

    """
    name = 'Invert Selection'
    tooltip = 'Invert selection'
    enabled_name = 'can_select_objects'

    def perform(self, event):
        event.task.active_editor.select_invert()


class FlipVerticalAction(EditorAction):
    """Flips the selected items top to bottom.

    This calculates the bounding box of just the selected items and uses that
    to find the centerline about which to flip.
    """
    name = "Flip Selection Vertically"
    enabled_name = 'can_copy'
    picked = None
    command = FlipVerticalCommand

    def permute_object(self, obj, bounds):
        obj.flip_vertical(bounds)

    def perform(self, event):
        e = self.active_editor
        objects = e.bitmap.mouse_mode.objects
        bounds = DrawObjectBounds.get_bounds(objects)
        for o in e.bitmap.mouse_mode.objects:
            self.permute_object(o, bounds)
        e.bitmap.save_changes(self.command)
        e.bitmap.mouse_mode.resync_objects()


class FlipHorizontalAction(FlipVerticalAction):
    """Flips the selected items left to right.

    This calculates the bounding box of just the selected items and uses that
    to find the centerline about which to flip.
    """
    name = "Flip Selection Horizontally"
    command = FlipHorizontalCommand

    def permute_object(self, obj, bounds):
        obj.flip_horizontal(bounds)


class AssemblySourceAction(EditorAction):
    """Add an assembly source file to this level (and compile it)

    This is used to provide custom actions or even game loops, beyond what is
    already built-in with trigger painting. There are special labels that are
    recognized by the assembler and used in the appropriate places:

        * vbi1
        * vbi2
        * vbi3
        * vbi4
        * dead_begin
        * dead_at_bottom
        * dead_falling
        * gameloop
        * out_of_lives
        * level_complete
        * collect_callback

    See our `reverse engineering notes
    <http://playermissile.com/jumpman/notes.html#h.s0ullubzr0vv>`_ for more
    details.
    """
    name = 'Custom Code...'

    def perform(self, event):
        e = self.active_editor
        filename = prompt_for_string(e.window.control, "Enter MAC/65 assembly source filename for custom code", "Source File For Custom Code", e.assembly_source)
        if filename is not None:
            e.set_assembly_source(filename)


class RecompileAction(EditorAction):
    """Recompile the assembly source code.

    This is a manual action, currently the program doesn't know when the file
    has changed. Making this process more automatic is a planned future
    enhancement.
    """
    name = 'Recompile Code'

    def perform(self, event):
        e = self.active_editor
        e.compile_assembly_source(True)


class UseLevelAction(UseSegmentAction):
    """This submenu contains a list of all Jumpman levels in the disk image.
    Selecting one of these items will change the display to edit that level.

    Note that no changes are lost when switching levels; they remain in memory
    and your edits will be restored when switching back to a previously editing
    level. However, no changes for any level are saved on disk until using the
    `Save`_ or `Save As`_ commands.
    """
    doc_hint = "parent"


class LevelListGroup(TaskDynamicSubmenuGroup):
    """Dynamic menu group to display the available levels
    """
    #### 'DynamicSubmenuGroup' interface #####################################

    event_name = 'segments_changed'

    ##########################################################################
    # Private interface.
    ##########################################################################

    def _get_items(self, event_data=None):
        items = []
        if event_data is not None:
            for i, segment in enumerate(event_data):
                if is_valid_level_segment(segment):
                    action = UseLevelAction(segment=segment, segment_number=i, task=self.task, checked=False)
                    log.debug("LevelListGroup: created %s for %s, num=%d" % (action, str(segment), i))
                    items.append(ActionItem(action=action, parent=self))

        if not items:
            action = UseLevelAction(segment="<no valid levels>", segment_number=0, task=self.task, checked=False, enabled=False)
            log.debug("LevelListGroup: created empty menu")
            items.append(ActionItem(action=action, parent=self))

        return items
