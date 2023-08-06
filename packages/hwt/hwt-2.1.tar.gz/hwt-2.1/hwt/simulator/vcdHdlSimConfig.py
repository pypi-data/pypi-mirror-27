from datetime import datetime
import sys

from hwt.hdl.types.bits import Bits
from hwt.hdl.types.bool import HBool
from hwt.hdl.types.enum import HEnum
from hwt.simulator.hdlSimConfig import HdlSimConfig
from hwt.simulator.vcdWritter import VcdWritter


class VcdHdlSimConfig(HdlSimConfig):
    supported_type_classes = (HBool, Bits, HEnum)

    def __init__(self, dumpFile=sys.stdout):
        self.vcdWritter = VcdWritter(dumpFile)
        self.logPropagation = False
        self.logApplyingValues = False

    def vcdRegisterUnit(self, unit):
        with self.vcdWritter.module(unit._name) as m:
            for se in unit._cntx.signals:
                if isinstance(se._dtype, self.supported_type_classes):
                    m.var(se)

            for u in unit._units:
                self.vcdRegisterUnit(u)

    def beforeSim(self, simulator, synthesisedUnit):
        """
        This method is called before first step of simulation.
        """
        self.vcdWritter.date(datetime.now())
        self.vcdWritter.timescale(1)

        self.vcdRegisterUnit(synthesisedUnit)
        self.vcdWritter.enddefinitions()

    def logChange(self, nowTime, sig, nextVal):
        """
        This method is called for every value change of any signal.
        """
        try:
            self.vcdWritter.change(nowTime, sig, nextVal)
        except KeyError:
            # not every signal has to be registered
            pass
