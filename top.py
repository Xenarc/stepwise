from module import Module
from command_module import CommandModule


class Top(Module):
    def __init__(self):
        super().__init__()
        self.command_module = self.submodule(CommandModule())
        self.always(self.run)

    def run(self):
        # Print the responses each time a message is processed
        responses = self.command_module.responses()
        if responses:
            for response in responses:
                print(f"Response for Command {response.commandId}: {response.status}")
