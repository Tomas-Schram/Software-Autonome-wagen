"""Maze navigation logic for turn decisions."""


class MazeNavigator:
    """Simple maze strategy based on line sensor readings."""

    def decide_turn(self, *, left: bool, center: bool, right: bool) -> str:
        """Return the preferred direction based on sensor input."""
        if left:
            return "left"
        if center:
            return "forward"
        if right:
            return "right"
        return "stop"
