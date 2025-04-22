from module import Module
from models import Command, CommandState, CommandResponse


class CommandStateMachineModule(Module):
    def __init__(self, command: Command):
        super().__init__()
        self.command = command
        # Command state is now a signal.
        self.state = self.signal(self.command.state)

    def process(self):
        """Simulate state transitions of the command."""
        if self.state() == CommandState.NEW:
            self.state.set(CommandState.UPDATED)
        elif self.state() == CommandState.UPDATED:
            self.state.set(CommandState.DELETED)
        elif self.state() == CommandState.DELETED:
            self.state.set(CommandState.NEW)
        else:
            raise ValueError(f"Unknown state: {self.state()}")

    def get_response(self):
        """Generate a CommandResponse based on current state."""
        return CommandResponse(
            commandId=self.command.commandId,
            status=f"Processed {self.state()}",
            data=self.command.data,
        )
