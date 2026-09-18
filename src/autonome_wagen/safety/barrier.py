"""Barrier and alert handling for the maze car."""


class SoundController:
    """Small sound interface used for driver feedback."""

    def __init__(self) -> None:
        self.last_sound = None

    def play(self, sound_name: str) -> None:
        """Play a sound and store the last sound for inspection."""
        self.last_sound = sound_name


class BarrierController:
    """Handle a barrier or slagboom before continuing along the line."""

    def __init__(self, sound_controller: SoundController) -> None:
        self.sound_controller = sound_controller

    def handle_slagboom(self) -> dict:
        """Stop the vehicle, play a signal, and continue later."""
        self.sound_controller.play("beep")
        return {"state": "stopped", "sound": "beep"}
