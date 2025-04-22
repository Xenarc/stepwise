from typing import Dict
from module import Module
from models import Command
from signal import Signal
from command_state_machine import CommandStateMachineModule
from message_module import MessageModule


class CommandModule(Module):
    def __init__(self):
        super().__init__()
        self.message_handler: MessageModule = self.submodule(MessageModule())
        self.command_machines: Dict[str, CommandStateMachineModule] = {}

        self.always(self.run)

    def run(self):
        msg = self.message_handler.msg()
        print(f"[CommandModule] Received command: {msg}")

        if msg.commandId not in self.command_machines:
            self.command_machines[msg.commandId] = self.submodule(
                CommandStateMachineModule(msg)
            )

        self.command_machines[msg.commandId].command.set(msg)
