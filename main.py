import random
import time
from top import Top
from models import Command, CommandState


def simulate_incoming_commands():
    command_data = [
        Command(commandId=1, state=CommandState.NEW, data={"action": "create"}),
        Command(commandId=2, state=CommandState.NEW, data={"action": "update"}),
        Command(commandId=3, state=CommandState.NEW, data={"action": "delete"}),
    ]

    while True:
        yield random.choice(command_data)


def main():
    top = Top()
    commands = simulate_incoming_commands()

    for _ in range(5):  # Simulate 5 commands
        command = next(commands)
        try:
            top.command_module.process_message(command)
            top.step()  # Step the simulation to process the message
            time.sleep(0.8)
        except Exception as e:
            print(f"✖ Error: {e}")


if __name__ == "__main__":
    main()
