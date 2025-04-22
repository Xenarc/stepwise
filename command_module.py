from module import Module
from models import Command
from command_state_machine import CommandStateMachineModule


class CommandModule(Module):
    def __init__(self):
        super().__init__()
        self.commands = {}  # Dictionary of command signals.
        self.responses = self.signal([])  # Hold responses in a list

    def process_message(self, msg: Command):
        print(f"[CommandModule] Received command: {msg}")

        # Create a new signal for the command or fetch the existing one
        if msg.commandId not in self.commands:
            # Command signal is created here instead of using a dictionary to track state machines.
            self.commands[msg.commandId] = self.signal(msg)

        # Process the state transition in the command signal
        state_machine = self.submodule(CommandStateMachineModule(msg))
        state_machine.process()  # This transitions the state automatically.

        # Generate the response for the command
        response = state_machine.get_response()

        # Add response to the list of responses
        current_responses = self.responses()
        current_responses.append(response)
        self.responses.set(current_responses)

        # Step through the logic for state updates
        self.step()
        self.responses.update()
