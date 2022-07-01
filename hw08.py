# %%
import abc
from hw05 import Vector, MoveCommand, RotateCommand


# %%
class CommandException(Exception):
    pass


# %%
class CommandInterface(abc.ABC):
    @abc.abstractmethod
    def execute(self):
        pass


class CheckFuelCommand(CommandInterface):
    def __init__(self, fuel):
        self.fuel = fuel

    def execute(self):
        if self.fuel.get_volume() < 0:
            raise CommandException('Fuel is empty')


class BurnFuelCommand(CommandInterface):
    def __init__(self, fuel: int):
        self.fuel = fuel

    def execute(self):
        v = self.fuel.get_volume()
        self.fuel.set_volume(v-1)


class MoveMacroCommand(CommandInterface):
    def __init__(self, commands=[]):
        self.commands = commands

    def execute(self):
        try:
            for c in self.commands:
                c.execute()
        except:
            raise CommandException("Can't move macro move")


class ChangeVelocityCommand(CommandInterface):
    def __init__(self, new_velocity):
        self.velocity = None
        self.new_velocity = new_velocity

    def set_velocity(self, new_velocity):
        self.velocity = new_velocity

    def get_velocity(self):
        return self.velocity

    def execute(self):
        self.set_velocity(self.new_velocity)


# %%
class FuelInterface(abc.ABC):
    @abc.abstractmethod
    def set_volume(self):
        pass

    @abc.abstractmethod
    def get_volume(self):
        pass


class Fuel():
    def __init__(self, volume: int):
        self.volume = volume

    def set_volume(self, volume: int):
        self.volume = volume

    def get_volume(self):
        return self.volume


# %%
if __name__ == "__main__":
    position = p = Vector([12, 5])
    # velocity = v = Vector([-7, 3])
    velocity = v = Vector([1, 1])

    fuel = Fuel(volume=3)
    check_fuel = CheckFuelCommand(fuel=fuel)
    move = MoveCommand(p, v)
    burn_fuel = BurnFuelCommand(fuel=fuel)
    macro_move = MoveMacroCommand([check_fuel, move, burn_fuel])
    for i in range(10):
        macro_move.execute()
        print(macro_move.commands[-1].fuel.get_volume())
        print(macro_move.commands[1].get_position())
