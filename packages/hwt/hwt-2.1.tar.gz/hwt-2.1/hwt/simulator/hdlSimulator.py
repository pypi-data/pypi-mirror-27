from simpy.core import BoundClass, Environment
from simpy.events import NORMAL, Timeout

from hwt.hdl.value import Value
from hwt.simulator.hdlSimConfig import HdlSimConfig
from hwt.simulator.simModel import mkUpdater, mkArrayUpdater
from hwt.simulator.simulatorCore import HdlProcess
from hwt.simulator.utils import valueHasChanged
from hwt.synthesizer.uniqList import UniqList


def isEvDependentOn(sig, process):
    if sig is None:
        return False
    return process in sig.simFallingSensProcs\
        or process in sig.simRisingSensProcs


class UpdateSet(set):
    """
    Set of updates for signal

    :ivar destination: signal which are updates for
    """

    def __init__(self, destination):
        self.destination = destination


class IoContainer():
    """
    Container for outputs of process
    """
    __slots__ = ["_all_signals"]

    def __init__(self, dstSignalsTuples):
        """
        :param dstSignalsTuples: tuples (name, signal)
        """
        self._all_signals = []
        for name, s in dstSignalsTuples:
            o = UpdateSet(s)
            setattr(self, name, o)
            self._all_signals.append(o)


class HdlSimulator(Environment):
    """
    Circuit simulator with support for external agents

    .. note:: *Signals without driver, constant driver, initial value*
        Every signal is initialized at start with its default value

    .. note:: *Communication between processes*
        Every interprocess signal is marked by synthesizer.
        For each output for every process there is an IO object
        which is container container of updates to signals.
        Every process has (generated) sensitivity-list.
        Process is reevaluated when there is a new value on any signal
        from sensitivity list.

    .. note: *Delta steps*
        Delta step is minimum quantum of changes in simulation, on the begining
        of delta step all read are performed and on the end all writes
        are performed. Writes are causing revalution of HWprocesses
        which are planet into next delta step.
        Delta steps does not update time.
        When there is no process to reevaluate that means thereis nothing to do
        in delta step this delta step is considered
        as last in this time and time is shifted on begining of next event
        by simulator.

    .. note:: *Simulation inputs*
        HWprocess can not contain any blocking statement
        Simulation processes are written in python and can contain anything.
        (Using hdl as main simulator driver is not efficient.
         That is why it is not supported.)

    .. note::
        HWprocesses have lower priority than simulation processes
        this allows simplify logic of all agents.
        When simulation process is executed, HW part did not anything
        in this time, Simulation process can prepare anything for HW part
        (= can write) if simulation process need to read, it has to yield
        simulator.updateComplete event first, process then will be wakened
        after reaction of HW in this time:
        agents are greatly simplified, they just need to yield
        simulator.updateComplete before first read
        and then can not write in this time

    :ivar now: actual simulation time
    :ivar updateComplete: this event is triggered
        when there are not any values to apply in this time
    :ivar valuesToApply: is container of values
        which should be applied in single delta step
    :ivar env: simply environment
    :ivar applyValuesPlaned: flag if there is planed applyValues
        for current values quantum
    :ivar seqProcsToRun: list of event dependent processes
        which should be evaluated after applyValEv
    """
    # updating of combinational signals (wire updates)
    PRIORITY_APPLY_COMB = NORMAL + 1
    # simulation agents waiting for updateComplete event
    PRIORITY_AGENTS_UPDATE_DONE = PRIORITY_APPLY_COMB + 1
    # updateing of event dependent signals (writing in gegisters,rams etc)
    PRIORITY_APPLY_SEQ = PRIORITY_AGENTS_UPDATE_DONE + 1

    process = BoundClass(HdlProcess)
    wait = BoundClass(Timeout)

    def __init__(self, config=None):
        super(HdlSimulator, self).__init__()
        if config is None:
            # default config
            config = HdlSimConfig()

        self.config = config
        self.combUpdateDoneEv = None
        self.applyValEv = None
        self.runSeqProcessesEv = None

        # (signal, value) tuples which should be applied before
        # new round of processes
        #  will be executed
        self.valuesToApply = []
        self.seqProcsToRun = UniqList()
        self.combProcsToRun = UniqList()
        # container of outputs for every process
        self.outputContainers = {}

    def waitOnCombUpdate(self):
        """
        Sim processes can wait on combUpdateDoneEv by:
        yield sim.waitOnCombUpdate()

        Sim process is then woken up when all combinational updates
        are done in this delta step
        """
        cud = self.combUpdateDoneEv
        if cud is None:
            return self.scheduleCombUpdateDoneEv()
        return cud

    def addHwProcToRun(self, trigger, proc):
        # first process in time has to plan executing of apply values on the
        # end of this time
        if self.applyValEv is None:
            # (apply on end of this time to minimalize process reevaluation)
            self.scheduleApplyValues()

        if isEvDependentOn(trigger, proc):
            if self._now == 0:
                return  # pass event dependent on startup
            self.seqProcsToRun.append(proc)
        else:
            self.combProcsToRun.append(proc)

    def _initUnitSignals(self, unit):
        """
        * Inject default values to simulation

        * Instantiate IOs for every process
        """
        for s in unit._cntx.signals:
            v = s.defaultVal.clone()

            # force update all signals to deafut values and propagate it
            s.simUpdateVal(self, mkUpdater(v, False))

        for u in unit._units:
            self._initUnitSignals(u)

        for p in unit._processes:
            self.addHwProcToRun(None, p)

        for p, outputs in unit._outputs.items():
            # name has to be explicit because it may be possible that signal
            # with has this name was replaced by signal from parent/child
            containerNames = list(map(lambda x: x[0], outputs))

            class SpecificIoContainer(IoContainer):
                __slots__ = containerNames

            self.outputContainers[p] = SpecificIoContainer(outputs)

    def __deleteCombUpdateDoneEv(self, ev):
        """
        Callback called on combUpdateDoneEv finished
        """
        self.combUpdateDoneEv = None

    def scheduleCombUpdateDoneEv(self):
        """
        Scheduele combUpdateDoneEv event to let agents know that current
        delta step is ending and values from combinational logic are stable
        """
        assert self.combUpdateDoneEv is None
        cud = self.combUpdateDoneEv = self.event()
        cud.callbacks.append(self.__deleteCombUpdateDoneEv)
        cud._ok = True
        cud._value = None
        self.schedule(cud,
                      priority=self.PRIORITY_AGENTS_UPDATE_DONE)
        return cud

    def scheduleApplyValues(self):
        """
        Apply stashed values to signals
        """
        assert self.applyValEv is None, self.now
        applyVal = self.applyValEv = self.event()
        applyVal._ok = True
        applyVal._value = None
        applyVal.callbacks.append(self.applyValues)

        self.schedule(applyVal,
                      priority=self.PRIORITY_APPLY_COMB)

        if self.runSeqProcessesEv is not None:
            # if runSeqProcessesEv is already scheduled
            return

        assert not self.seqProcsToRun, self.now
        runSeq = self.runSeqProcessesEv = self.event()
        runSeq._ok = True
        runSeq._value = None
        runSeq.callbacks.append(self.runSeqProcesses)

        self.schedule(runSeq, priority=self.PRIORITY_APPLY_SEQ)

    def conflictResolveStrategy(self, actionSet):
        """
        This functions resolves write conflicts for signal

        :param actionSet: set of actions made by process
        """
        invalidate = False
        asLen = len(actionSet)
        # resolve if there is write collision
        if asLen == 0:
            return
        elif asLen == 1:
            res = actionSet.pop()
        else:
            # we are driving signal with two or more different values
            # we have to invalidate result
            res = actionSet.pop()
            invalidate = True

        resLen = len(res)
        if resLen == 3:
            # update for item in array
            val, indexes, isEvDependent = res
            return (mkArrayUpdater(val, indexes, invalidate), isEvDependent)
        else:
            # update for simple signal
            val, isEvDependent = res
            return (mkUpdater(val, invalidate), isEvDependent)

    def runCombProcesses(self):
        """
        Delta step for combinational processes
        """
        for proc in self.combProcsToRun:
            outContainer = self.outputContainers[proc]
            proc(self, outContainer)
            for actionSet in outContainer._all_signals:
                if actionSet:
                    res = self.conflictResolveStrategy(actionSet)
                    # prepare update
                    updater, isEvDependent = res
                    self.valuesToApply.append(
                        (actionSet.destination, updater, isEvDependent, proc))
                    actionSet.clear()
                # else value is latched

        self.combProcsToRun = UniqList()

    def runSeqProcesses(self, ev):
        """
        Delta step for event dependent processes
        """
        updates = []
        for proc in self.seqProcsToRun:
            try:
                outContainer = self.outputContainers[proc]
            except KeyError:
                # processes does not have to have outputs
                outContainer = None

            proc(self, outContainer)

            if outContainer is not None:
                updates.append(outContainer)

        self.seqProcsToRun = UniqList()
        self.runSeqProcessesEv = None

        for cont in updates:
            for actionSet in cont._all_signals:
                if actionSet:
                    v = self.conflictResolveStrategy(actionSet)
                    updater, _ = v
                    actionSet.destination.simUpdateVal(self, updater)
                    actionSet.clear()

    def applyValues(self, ev):
        """
        Perform delta step by writing stacked values to signals
        """
        va = self.valuesToApply
        self.applyValEv = None

        # log if there are items to log
        lav = self.config.logApplyingValues
        if va and lav:
            lav(self, va)
        self.valuesToApply = []

        # apply values to signals, values can overwrite each other
        # but each signal should be driven by only one process and
        # it should resolve value collision
        addSp = self.seqProcsToRun.append
        for s, vUpdater, isEventDependent, comesFrom in va:
            if isEventDependent:
                # now=0 and this was process initialization or async reg
                addSp(comesFrom)
            else:
                # regular combinational process
                s.simUpdateVal(self, vUpdater)

        self.runCombProcesses()

        # processes triggered from simUpdateVal can add new values
        if self.valuesToApply and self.applyValEv is None:
            self.scheduleApplyValues()

    def read(self, sig):
        """
        Read value from signal or interface
        """
        try:
            v = sig._val
        except AttributeError:
            v = sig._sigInside._val

        return v.clone()

    def write(self, val, sig):
        """
        Write value to signal or interface.
        """
        # get target RtlSignal
        try:
            simSensProcs = sig.simSensProcs
        except AttributeError:
            sig = sig._sigInside
            simSensProcs = sig.simSensProcs

        # type cast of input value
        t = sig._dtype

        if isinstance(val, Value):
            v = val.clone()
            v = v._auto_cast(t)
        else:
            v = t.fromPy(val)

        # can not update value in signal directly due singnal proxies
        sig.simUpdateVal(self, lambda curentV: (
            valueHasChanged(curentV, v), v))

        if self.applyValEv is None:
            if not (simSensProcs or
                    sig.simRisingSensProcs or
                    sig.simFallingSensProcs):
                # signal value was changed but there are no sensitive processes
                # to it because of this applyValues is never planed
                # and should be
                self.scheduleApplyValues()
            elif (sig._writeCallbacks or
                  sig._writeCallbacksToEn):
                # signal write did not caused any change on any other signal
                # but there are still simulation agets waiting on
                # updateComplete event
                self.scheduleApplyValues()

    def simUnit(self, synthesisedUnit, time, extraProcesses=[]):
        """
        Run simulation
        """
        beforeSim = self.config.beforeSim
        if beforeSim is not None:
            beforeSim(self, synthesisedUnit)

        for p in extraProcesses:
            self.process(p(self))

        self._initUnitSignals(synthesisedUnit)
        self.run(until=time)
