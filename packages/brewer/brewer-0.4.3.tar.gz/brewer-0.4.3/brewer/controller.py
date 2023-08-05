from os import getenv
import time

from . import str116
from . import settings
from .slack import BrewerBot
import serial
from .omega import Omega
from terminaltables import AsciiTable
from .fake_controller import FakeController
from .color import *


class Controller:
    """
    This is class that interfaces with the hardware of the brew rig and you.
    """
    def __new__(cls):
        """
        Looks for hardware. If it doesn't find any, return a `FakeController`

        Can be overridden by environment variables `force_fake_controller` and `force_real_controller` set to '1'
        """
        if getenv("force_fake_controller") == '1':
            green("force_fake_controller enabled")
            green("Using FakeController()")
            return FakeController()
        elif getenv("force_real_controller") == '1':
            green("force_real_controller enabled")
            green("Using Controller()")
            return super(Controller, cls).__new__(cls)

        try:
            # This is what throws the error if there's no hardware. Might seem a bit out of place.
            omega = Omega(
                settings.port,
                settings.rimsAddress,
                settings.baudRate,
                settings.timeout
            )
        except serial.serialutil.SerialException as exc:
            yellow("No hardware detected!")
            green("Using FakeConroller()")
            return FakeController()
        green("Hardware found")
        green("Using Controller()")
        return super(Controller, cls).__new__(cls)

    def __init__(self):
        self.omega = Omega(
            settings.port,
            settings.rimsAddress,
            settings.baudRate,
            settings.timeout
        )

        self.settings = settings

        self.slack = BrewerBot()

    @staticmethod
    def simulator():
        return FakeController()

    def relay_status(relay_num: int):
        """
        Returns the relay status of a specified relay
        """
        return str116.get_relay(relay_num)

    def set_relay(self, relay_num: int, state: int):
        """
        Sets relay state to on or off.
        """
        str116.set_relay(relay_num, state)

    def pid_running(self):
        """
        Returns True if pid is running, False otherwise.
        """
        return self.omega.is_running()

    def pid_status(self):
        """
        Returns an a dictionary of pid status, pv, and sv
        """
        return {
            "pid_running": bool(self.pid_running()),
            "sv": self.sv(),
            "pv": self.pv()
        }

    def pid(self, state: int):
        """
        Set the pid on or off.

        Note: the pid should *never* be on if the pump is off. Liquid needs to circulate, or the heater will burn itself out.
        """
        self._safegaurd_state(state)
        if state == 1:
            self.pump(1)
            self.omega.run()
        else:
            self.omega.stop()
        return True

    def hlt(self, state: int):
        """
        Opens or closes the hlt valve
        """
        self._safegaurd_state(state)
        self.set_relay(self.settings.relays["hlt"], state)
        return True

    def hlt_to(self, location: str):
        """
        Sets location of hlt divert valve to 'mash' or 'boil' tuns.
        """
        if location == "mash":
            self.set_relay(self.settings.relays["hltToMash"], 1)
            return True
        elif location  == "boil":
            self.set_relay(self.settings.relays["hltToMash"], 0)
            return True
        else:
            raise ValueError("Location unknown: valid locations are 'mash' and 'boil'")


    def rims_to(self, location: str):
        """
        Sets location of rims divert valve to 'mash' or 'boil' tuns.
        """
        if location == "mash":
            self.set_relay(self.settings.relays["rimsToMash"], 1)
            return True
        elif location == "boil":
            self.set_relay(self.settings.relays["rimsToMash"], 0)
            return True
        else:
            raise ValueError("Location unknown: valid locations are 'mash' and 'boil'")

    def pump_status(self):
        return self.relay_status(self.settings.relays["pump"])

    def pump(self, state: int):
        """
        Turns the pump on or off
        """
        self._safegaurd_state(state)
        if state == 0:
            self.pid(0)
        self.set_relay(self.settings.relays['pump'], state)
        return True

    def _safegaurd_state(self, state):
        """
        Ensures the argument is an int 0 or 1
        """
        if not isinstance(state, int):
            raise ValueError("Relay State needs to be an integer, " + str(type(state)) + " given.")
        if state < 0 or state > 1:
            raise ValueError("State needs to be integer 0 or 1, " + str(state) + " given.")
        return True

    def sv(self):
        """
        Returns the Setpoint value (SV)
        """
        return float(self.omega.sv())

    def set_sv(self, temp: float):
        """
        Sets the setpoint value. Should be float, int is acceptable
        """
        self.omega.safeguard(temp, [int, float])
        self.omega.set_sv(temp)
        return self.omega.sv()

    def pv(self):
        """
        Returns the Proccess Value (PV)
        """
        return float(self.omega.pv())

    def watch(self):
        """
        Watches temperatures, and returns true when PV is >= SV.
        """
        while self.pv() <= self.sv():
            time.sleep(2) # :nocov:

        self.slack.send("PV is now at " + str(self.pv()) + " f")
        return True

    def status_table(self):
        """
        Returns an `AsciiTable` class of pid and pump status.
        """
        status = AsciiTable([
            ["Setting", "Value"],
            ["PID on?", str(self.pid_status()['pid_running'])],
            ["Pump on?", str(self.pump_status())],
            ["pv", str(self.pv())],
            ["sv", str(self.sv())]
        ])
        return status
