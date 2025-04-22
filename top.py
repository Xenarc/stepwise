from module import Module
from command_module import CommandModule


class Top(Module):
    def __init__(self):
        super().__init__()
        self.command_module = self.submodule(CommandModule())
        self.always(self.run)

    def run(self):
        for command_machine in self.command_module.command_machines.values():
            response = command_machine.get_response()
            print(f"Response for Command {response.commandId}: {response.status}")
