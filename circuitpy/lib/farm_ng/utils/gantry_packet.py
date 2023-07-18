from struct import pack
from struct import unpack

from canio import Message
from supervisor import ticks_ms

from .general import clip
from .general import ticks_diff
from .packet import Packet

GANTRY_ID = 0x12

    
class GantryControlState:
    """State of the Amiga vehicle control unit (VCU)"""

    STATE_MANUAL_READY = 1
    STATE_MANUAL_ACTIVE = 2
    STATE_AUTO_READY = 3
    STATE_AUTO_ACTIVE = 4
    STATE_ALARM = 5
    STATE_ESTOPPED = 6

#/////////////
class GantryRpdo1(Packet):
    #State, feed, location, and jog (request) sent to the Amiga vehicle control unit (VCU).
    

    cob_id = 0x200

    def __init__(
        self,
        state_req: GantryControlState = GantryControlState.STATE_ESTOPPED,
        cmd_feed: int = 0,
        cmd_x: int = 0,
        cmd_y: int = 0,
        jog: bool = True,
    ):
        self.format = "<e"

        self.state_req = state_req
        self.cmd_feed = cmd_feed
        self.cmd_x = cmd_x
        self.cmd_y = cmd_y
        self.jog = jog

        self.stamp()

    def encode(self):
        """Returns the data contained by the class encoded as CAN message data."""
        return pack(
            self.format,
            self.state_req,
            self.cmd_feed,
            self.cmd_x,
            self.cmd_y,
            self.jog
        )

    def decode(self, data):
        """Decodes CAN message data and populates the values of the class."""

        (self.state_req, self.cmd_feed, self.cmd_x, self.cmd_y, self.jog) = unpack(self.format, data)


    def __str__(self):
        return "Gantry Rpdo1 Request state {} Command feed {:x} Command x {:x} Command y {:x}".format(
            self.state_req, self.cmd_feed, self.cmd_x, self.cmd_y
        ) + " Jog {}".format(self.jog)
#/////////////

#/////////////
class GantryTpdo1(Packet):
    """State, speed, and angular rate of the Amiga vehicle control unit (VCU).

    New in fw v0.1.9 / farm-ng-amiga v0.0.7: Add pto & hbridge control. Message data is now 8 bytes (was 5).
    """

    cob_id = 0x180

    def __init__(
        self,
        state: GantryControlState = GantryControlState.STATE_ESTOPPED,
        meas_feed: int = 0,
        meas_x: int = 0,
        meas_y: int = 0,
        jog: bool = True,
    ):
        self.format = "<e"

        self.state = state
        self.meas_feed = meas_feed
        self.meas_x = meas_x
        self.meas_y = meas_y
        self.jog = jog

        self.stamp()

    def encode(self):
        """Returns the data contained by the class encoded as CAN message data."""
        return pack(
            self.format,
            self.state,
            self.meas_feed,
            self.meas_x,
            self.meas_y,
            self.jog,
        )

    def decode(self, data):
        """Decodes CAN message data and populates the values of the class."""
        (self.state, self.meas_feed, self.meas_x, self.meas_y, self.jog) = unpack(self.format, data)


    def __str__(self):
        return "Gantry Tpdo1 Amiga state {} Measured feed {:x} Measured x {:x} Measured y{:x} @ time {}".format(
            self.state, self.meas_feed, self.meas_x, self.meas_y, self.stamp.stamp
        ) + " Jog {}".format(self.jog)
#/////////////