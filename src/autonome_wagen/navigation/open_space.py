"""Open-space navigation when no line is present."""


class OpenSpaceNavigator:
    """Choose a path based on surrounding free space in an open area."""

    def choose_direction(self, *, front_clear: bool, left_clear: bool, right_clear: bool) -> str:
        """Return the preferred movement direction for a free-space route."""
        if front_clear:
            return "forward"
        if left_clear:
            return "left"
        if right_clear:
            return "right"
        return "stop"
