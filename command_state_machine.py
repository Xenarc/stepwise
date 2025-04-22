from module import Module
from models import Command, CommandState, CommandResponse
from signal import Signal


class CommandStateMachineModule(Module):
    def __init__(self, command: Command):
        super().__init__()
        self.command = self.signal(command)
        self.state = self.signal(CommandState.NEW)

        self.always(self.process)

    def process(self):
        if self.command().state == CommandState.NEW:
            self.state.set(CommandState.UPDATED)
        elif self.command().state == CommandState.UPDATED:
            self.state.set(CommandState.DELETED)
        elif self.command().state == CommandState.DELETED:
            self.state.set(CommandState.NEW)
        else:
            raise ValueError(f"Unknown state: {self.command().state}")

    def get_response(self):
        """Generate a CommandResponse based on current state."""
        return CommandResponse(
            commandId=self.command().commandId,
            status=f"Processed {self.command()}",
            data=self.command().data,
        )
