# %%
import pytest
from hw05 import *
from hw08 import *


def test_CheckFuelCommand_with_negative():
    fuel = Fuel(volume=-1)
    c = CheckFuelCommand(fuel)
    with pytest.raises(CommandException) as e:
        c.execute()


def test_CheckFuelCommand_with_positive():
    fuel = Fuel(volume=1)
    c = CheckFuelCommand(fuel)
    try:
        c.execute()
    except CommandException:
        assert False


def test_CheckFuelCommand_with_zero():
    fuel = Fuel(volume=0)
    c = CheckFuelCommand(fuel)
    try:
        c.execute()
    except CommandException:
        assert False


def test_BurnFuelCommand():
    fuel_volume = 10
    fuel = Fuel(volume=fuel_volume)
    c = BurnFuelCommand(fuel=fuel)
    c.execute()
    expected_fuel_volume = fuel_volume - 1
    assert expected_fuel_volume == fuel.get_volume()


def test_MoveMacroCommand_check_fuel_volume():
    position = p = Vector([12, 5])
    velocity = v = Vector([1, 1])
    fuel_volume = 3
    fuel = Fuel(volume=fuel_volume)
    check_fuel = CheckFuelCommand(fuel=fuel)
    move = MoveCommand(p, v)
    burn_fuel = BurnFuelCommand(fuel=fuel)
    macro_move = MoveMacroCommand([check_fuel, move, burn_fuel])
    macro_move.execute()
    expected_volume = macro_move.commands[2].fuel.get_volume()
    current_volume = fuel.get_volume()
    assert expected_volume == current_volume


def test_MoveMacroCommand_check_move_position():
    position = p = Vector([12, 5])
    velocity = v = Vector([1, 1])
    fuel_volume = 3
    fuel = Fuel(volume=fuel_volume)
    check_fuel = CheckFuelCommand(fuel=fuel)
    move = MoveCommand(p, v)
    burn_fuel = BurnFuelCommand(fuel=fuel)
    macro_move = MoveMacroCommand([check_fuel, move, burn_fuel])
    macro_move.execute()
    expected_position = Vector([13, 6])
    current_position = macro_move.commands[1].get_position()
    assert expected_position == current_position


def test_ChangeVelocityCommand():
    new_velocity = 25
    c = ChangeVelocityCommand(new_velocity)
    c.execute()
    expected_velocity = new_velocity
    current_velocity = c.get_velocity()
    assert expected_velocity == current_velocity


def test_Fuel():
    fuel_volume = 10
    fuel = Fuel(volume=fuel_volume)
    assert fuel_volume == fuel.get_volume()
