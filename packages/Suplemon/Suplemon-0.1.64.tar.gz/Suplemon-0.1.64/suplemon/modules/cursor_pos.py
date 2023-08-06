# -*- encoding: utf-8

from suplemon.suplemon_module import Module


class CursorPos(Module):
    """Shows cursors vertical position as percentages."""

    def get_status(self):
        total = len(self.app.get_editor().lines)

        cursors = [self.app.get_editor().get_first_cursor().y]
        last = self.app.get_editor().get_last_cursor().y
        if last != cursors[0]:
            cursors.append(last)
        return " - ".join(map(lambda c: str(int(c/total*100)) + "%", cursors))


module = {
    "class": CursorPos,
    "name": "cursor_pos",
    "status": "bottom",
}
