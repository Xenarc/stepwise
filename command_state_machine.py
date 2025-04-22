from module import Module
from models import Command, CommandState, ProcessingState, CommandResponse
from signal import Signal


class CommandStateMachineModule(Module):
    def __init__(self, command: Command):
        super().__init__()
        self.command: Signal[Command] = self.signal(command)
        self.processing_state: Signal[ProcessingState] = self.signal(
            ProcessingState.NONE
        )

        self.always_on(self.process_on_command, [self.command])

    def process_on_command(self):
        if self.command().state == CommandState.NEW:
            if self.processing_state() == ProcessingState.COMPLETED:
                # Cannot restart an fulfilled command
                pass
            else:
                self.processing_state.set(ProcessingState.RUNNING)
        elif self.command().state == CommandState.UPDATED:
            if self.processing_state() == ProcessingState.COMPLETED:
                # Cannot update a fulfilled command
                pass
            elif self.processing_state() == ProcessingState.RUNNING:
                # Command already running
                pass
            elif self.processing_state() == ProcessingState.NONE:
                # Command hasn't been run yet.
                pass

        elif self.command().state == CommandState.DELETED:
            if self.processing_state() == ProcessingState.COMPLETED:
                # Cannot delete a fulfilled command
                pass
            elif self.processing_state() == ProcessingState.RUNNING:
                self.processing_state.set(ProcessingState.COMPLETED)
            elif self.processing_state() == ProcessingState.NONE:
                self.processing_state.set(ProcessingState.COMPLETED)
        else:
            raise ValueError(f"Unknown state: {self.command().state}")

    def get_response(self):
        """Generate a CommandResponse based on current state."""
        return CommandResponse(
            commandId=self.command().commandId,
            status=self.processing_state(),
            data=self.command().data,
        )
