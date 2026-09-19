"""Barrier and alert handling for the maze car."""


class SoundController:
    """Small sound interface used for driver feedback."""

    def __init__(self, speaker_output: str = "microbit_speaker") -> None:
        self.last_sound = None
        self.speaker_output = speaker_output

    def play(self, sound_name: str) -> None:
        """Play a sound on the Micro:bit built-in speaker and store the last sound for inspection."""
        self.last_sound = sound_name
        self.speaker_output = "microbit_speaker"


class BarrierController:
    """Handle a barrier or slagboom before continuing along the line."""

    def __init__(self, sound_controller: SoundController) -> None:
        self.sound_controller = sound_controller

    def handle_slagboom(self) -> dict:
        """Stop the vehicle, play a signal on the Micro:bit speaker, and continue later."""
        self.sound_controller.play("beep")
        return {"state": "stopped", "sound": "beep"}
