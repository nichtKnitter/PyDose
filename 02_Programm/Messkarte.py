import logging
import random
import time

import nidaqmx
from nidaqmx.constants import (LineGrouping)


# from transitions.extensions import GraphMachine as Machine

# class Machine

class Messkarte(object):
    # dict zum verfolgen der States der Ventile, damit die nur geschaltet werden wenn es nötig ist.
    v_state = {}

    datenbufferlaenge = 10000  # ~80 mb, 1000 sind 8Mibi
    timeStartMessung = time.time()
    # timearray = np.array()
    timearray = []
    p1ManifoldArray = []  # pProbeMbar
    p2ProbeArray = []  # pManifoldMbar
    setpointarray = []

    def __init__(self, DAQwaitTime=0.005, isDebugDummyMode=False):

        self.isDebugDummyMode = isDebugDummyMode

        self.lastStellgrad = 0  # zum überprüfen og geschaltet werden muss
        self.setpoint = 0  # setpoint in mbar

        # Verfolgt wann die Ventile geschaltet wurden, um sie nach der richtigen Zeit wieder auszuschalten
        self.lastValveActivation = time.time()
        self.anyValveOn = False
        self.DAQwaitTime = DAQwaitTime  ## Wenn zu schnell hintereinander gibt es Komminikationfehler
        self.minimumValveOnTime = 0.4
        self.lastDAQtime = time.time()
        ## muss wohl schneller als messtakt sein....
        self.lastMeasurement = time.time()

        ##############################################################################
        # logging optionen
        self.numberOfCommunicationErrors = 0
        # Create the Logger
        self.Messkartenlogger = logging.getLogger(__name__)
        self.Messkartenlogger.setLevel(logging.INFO)
        # Create the Handler for logging data to a file
        logger_handler = logging.FileHandler('python_logging.log')
        logger_handler.setLevel(logging.INFO)
        # Add the Handler to the Logger
        self.Messkartenlogger.addHandler(logger_handler)
        self.Messkartenlogger.info('Completed configuring logger()!')
        self.Messkartenlogger.disabled = True

        ##############################################################################

        # erstmaliges lesen der sensoren
        self.readSensors()
        time.sleep(self.DAQwaitTime)

        # definition der Relaiszustände für die Ventile pro Kanal
        self.ventil_auf = [True, False]
        self.Ventil_zu = [False, True]
        self.Ventil_aus = [True, True]

        # States initialisiern:
        self.__initVentilStates()  # sollstates initialisieren
        self.v_state = self.vStateInit  # unbekannter ausgangszustand

    def __initVentilStates(self):
        # sollstates initialisieren
        self.vStateInit = {}
        self.vStateInit["State"] = {"Name": "vStateInit"}
        self.vStateInit["V1"] = {"id": 1, "state": "NA", "active": "NA"}
        self.vStateInit["V2"] = {"id": 2, "state": "NA", "active": "NA"}
        self.vStateInit["V3"] = {"id": 3, "state": "NA", "active": "NA"}
        self.vStateInit["V4"] = {"id": 4, "state": "NA", "active": "NA"}
        self.vStateInit["V5"] = {"id": 5, "state": "NA", "active": "NA"}
        self.vStateInit["V6"] = {"id": 6, "state": "NA", "active": "NA"}
        self.vStateInit["V7"] = {"id": 7, "state": "NA", "active": "NA"}
        self.vStateInit["V_Prop"] = {"id": 8, "stellgrad": 100, "state": "NA"}

        self.vStateSollAlleZu = {}
        self.vStateSollAlleZu["State"] = {"Name": "vStateSollAlleZu"}
        self.vStateSollAlleZu["V1"] = {"state": "zu"}
        self.vStateSollAlleZu["V2"] = {"state": "zu"}
        self.vStateSollAlleZu["V3"] = {"state": "zu"}
        self.vStateSollAlleZu["V4"] = {"state": "zu"}
        self.vStateSollAlleZu["V5"] = {"state": "zu"}
        self.vStateSollAlleZu["V6"] = {"state": "zu"}
        self.vStateSollAlleZu["V7"] = {"state": "zu"}
        self.vStateSollAlleZu["V_Prop"] = {"state": "an"}

        self.vStateSollWait = {}
        self.vStateSollWait["State"] = {"Name": "vStateSollWait"}
        self.vStateSollWait["V1"] = {"state": "zu"}
        self.vStateSollWait["V2"] = {"state": "zu"}
        self.vStateSollWait["V3"] = {"state": "zu"}
        self.vStateSollWait["V4"] = {"state": "zu"}
        self.vStateSollWait["V5"] = {"state": "zu"}
        self.vStateSollWait["V6"] = {"state": "auf"}
        self.vStateSollWait["V7"] = {"state": "zu"}
        self.vStateSollWait["V_Prop"] = {"state": "an"}

        self.vStateSollAlleAuf = {}
        self.vStateSollAlleAuf["State"] = {"Name": "vStateSollAlleAuf"}
        self.vStateSollAlleAuf["V1"] = {"state": "auf"}
        self.vStateSollAlleAuf["V2"] = {"state": "auf"}
        self.vStateSollAlleAuf["V3"] = {"state": "auf"}
        self.vStateSollAlleAuf["V4"] = {"state": "auf"}
        self.vStateSollAlleAuf["V5"] = {"state": "auf"}
        self.vStateSollAlleAuf["V6"] = {"state": "auf"}
        self.vStateSollAlleAuf["V7"] = {"state": "auf"}
        self.vStateSollAlleAuf["V_Prop"] = {"state": "an"}

        self.vStateSollVolumenEvakGrob = {}
        self.vStateSollVolumenEvakGrob["State"] = {"Name": "vStateSollVolumenEvakGrob"}
        self.vStateSollVolumenEvakGrob["V1"] = {"state": "auf"}
        self.vStateSollVolumenEvakGrob["V2"] = {"state": "zu"}
        self.vStateSollVolumenEvakGrob["V3"] = {"state": "zu"}
        self.vStateSollVolumenEvakGrob["V4"] = {"state": "auf"}
        self.vStateSollVolumenEvakGrob["V5"] = {"state": "zu"}
        self.vStateSollVolumenEvakGrob["V6"] = {"state": "zu"}
        self.vStateSollVolumenEvakGrob["V7"] = {"state": "auf"}
        self.vStateSollVolumenEvakGrob["V_Prop"] = {"state": "an"}

        self.vStateSollEvakFine = {}
        self.vStateSollEvakFine["State"] = {"Name": "vStateSollEvakFine"}
        self.vStateSollEvakFine["V1"] = {"state": "auf"}
        self.vStateSollEvakFine["V2"] = {"state": "zu"}
        self.vStateSollEvakFine["V3"] = {"state": "zu"}
        self.vStateSollEvakFine["V4"] = {"state": "auf"}
        self.vStateSollEvakFine["V5"] = {"state": "zu"}
        self.vStateSollEvakFine["V6"] = {"state": "auf"}
        self.vStateSollEvakFine["V7"] = {"state": "zu"}
        self.vStateSollEvakFine["V_Prop"] = {"state": "an"}

        self.vStateSollDoseFine = {}
        self.vStateSollDoseFine["State"] = {"Name": "vStateSollDoseFine"}
        self.vStateSollDoseFine["V1"] = {"state": "zu"}
        self.vStateSollDoseFine["V2"] = {"state": "zu"}
        self.vStateSollDoseFine["V3"] = {"state": "auf"}
        self.vStateSollDoseFine["V4"] = {"state": "zu"}
        self.vStateSollDoseFine["V5"] = {"state": "auf"}
        self.vStateSollDoseFine["V6"] = {"state": "auf"}
        self.vStateSollDoseFine["V7"] = {"state": "zu"}
        self.vStateSollDoseFine["V_Prop"] = {"state": "an"}

        self.vStateSollProbeEvakGrob = {}
        self.vStateSollProbeEvakGrob["State"] = {"Name": "vStateSollProbeEvakGrob"}
        self.vStateSollProbeEvakGrob["V1"] = {"state": "auf"}
        self.vStateSollProbeEvakGrob["V2"] = {"state": "zu"}
        self.vStateSollProbeEvakGrob["V3"] = {"state": "zu"}
        self.vStateSollProbeEvakGrob["V4"] = {"state": "auf"}
        self.vStateSollProbeEvakGrob["V5"] = {"state": "auf"}
        self.vStateSollProbeEvakGrob["V6"] = {"state": "auf"}
        self.vStateSollProbeEvakGrob["V7"] = {"state": "zu"}
        self.vStateSollProbeEvakGrob["V_Prop"] = {"state": "an"}

        self.vStateSollDegassEvaporator = {}
        self.vStateSollDegassEvaporator["State"] = {"Name": "vStateSollDegassEvaporator"}
        self.vStateSollDegassEvaporator["V1"] = {"state": "auf"}
        self.vStateSollDegassEvaporator["V2"] = {"state": "zu"}
        self.vStateSollDegassEvaporator["V3"] = {"state": "auf"}
        self.vStateSollDegassEvaporator["V4"] = {"state": "auf"}
        self.vStateSollDegassEvaporator["V5"] = {"state": "auf"}
        self.vStateSollDegassEvaporator["V6"] = {"state": "zu"}
        self.vStateSollDegassEvaporator["V7"] = {"state": "zu"}
        self.vStateSollDegassEvaporator["V_Prop"] = {"state": "an"}

        self.vStateSollEvacFineVol1 = {}
        self.vStateSollEvacFineVol1["State"] = {"Name": "vStateSollEvacFineVol1"}
        self.vStateSollEvacFineVol1["V1"] = {"state": "auf"}
        self.vStateSollEvacFineVol1["V2"] = {"state": "zu"}
        self.vStateSollEvacFineVol1["V3"] = {"state": "zu"}
        self.vStateSollEvacFineVol1["V4"] = {"state": "auf"}
        self.vStateSollEvacFineVol1["V5"] = {"state": "auf"}
        self.vStateSollEvacFineVol1["V6"] = {"state": "zu"}
        self.vStateSollEvacFineVol1["V7"] = {"state": "zu"}
        self.vStateSollEvacFineVol1["V_Prop"] = {"state": "an"}

        self.vStateSollVolSample = {}
        self.vStateSollVolSample["State"] = {"Name": "vStateSollEvacFineVol1"}
        self.vStateSollVolSample["V1"] = {"state": "zu"}
        self.vStateSollVolSample["V2"] = {"state": "zu"}
        self.vStateSollVolSample["V3"] = {"state": "zu"}
        self.vStateSollVolSample["V4"] = {"state": "auf"}
        self.vStateSollVolSample["V5"] = {"state": "auf"}
        self.vStateSollVolSample["V6"] = {"state": "auf"}
        self.vStateSollVolSample["V7"] = {"state": "zu"}
        self.vStateSollVolSample["V_Prop"] = {"state": "an"}

        self.vStateSollDoseFineVol1 = {}
        self.vStateSollDoseFineVol1["State"] = {"Name": "vStateSollEvacFineVol1"}
        self.vStateSollDoseFineVol1["V1"] = {"state": "zu"}
        self.vStateSollDoseFineVol1["V2"] = {"state": "zu"}
        self.vStateSollDoseFineVol1["V3"] = {"state": "auf"}
        self.vStateSollDoseFineVol1["V4"] = {"state": "auf"}
        self.vStateSollDoseFineVol1["V5"] = {"state": "auf"}
        self.vStateSollDoseFineVol1["V6"] = {"state": "zu"}
        self.vStateSollDoseFineVol1["V7"] = {"state": "zu"}
        self.vStateSollDoseFineVol1["V_Prop"] = {"state": "an"}

    def getVState(self):
        return self.v_state

    def getSetpoint(self):
        return self.setpoint

    def setSetpoint(self, newsetpoint):
        self.setpoint = newsetpoint
    def getP1ManifoldMbar(self):
        return self.p1ManifoldMbar

    def getP2ProbeMbar(self):
        return self.p2ProbeMbar

    def getp1ManifoldArray(self):
        return self.p1ManifoldArray

    def getp2ProbeArray(self):
        return self.p2ProbeArray

    def getTimearray(self):
        return self.timearray

    def getIsAnyValveOn(self):
        self.anyValveOn = False
    def setIsAnyValveOn(self, Bool):
        self.anyValveOn = Bool

    def getLastValveActivationTime(self):
        return self.lastValveActivation


    def readSensors(self):
        # sensoren auslesen. bisher nur zwei stück
        if self.isDebugDummyMode is True:
            data = [random.random() * 10, random.random() * 7]
            self.stuffAfterReadingSensors(data)

        if self.isDebugDummyMode is False:
            try:
                with nidaqmx.Task() as LeseTask:
                    LeseTask.ai_channels.add_ai_voltage_chan("Dev1/ai0:4",
                                                             terminal_config=nidaqmx.constants.TerminalConfiguration.RSE,
                                                             max_val=10,
                                                             min_val=0)  # terminal_config=VentilTask.TerminalConfiguration.NRSE

                    data = LeseTask.read()
                    self.lastDAQtime = time.time()
                    self.lastMeasurement = time.time()
                    time.sleep(self.DAQwaitTime)

                    self.stuffAfterReadingSensors(data)

            except nidaqmx.DaqError as e:
                print(e)
                self.numberOfCommunicationErrors += 1
                print("numberOfCommunicationErrors", self.numberOfCommunicationErrors)
                return e

    def stuffAfterReadingSensors(self, data):
        """

        :param data: array auf pressurere values in Volt, e.g [5,1]
        :return:
        """


        # aktuelle Druckwerte als floats speichern
        self.p1ManifoldMbar = data[0] * 10
        self.p2ProbeMbar = data[1] * 10
        self.Messtime = time.time() - self.timeStartMessung

        # In logger anzeigen
        stringp = ("p1ManifoldMbar = " + str(self.p1ManifoldMbar) + ";\tp2ProbeMbar = " + str(
            self.p2ProbeMbar) + "\tSetpoint:" + str(self.setpoint))
        self.Messkartenlogger.info(stringp)

        # daten in arrays abspeichern, mit fester Pufferlaenge
        # müssen ab und zu geflusht werden, oder einfacher: bei jedem takt wenn mehr als x in array?
        self.p1ManifoldArray.append(self.p1ManifoldMbar)
        self.p2ProbeArray.append(self.p2ProbeMbar)
        self.timearray.append(self.Messtime)
        self.setpointarray.append(self.setpoint)
        # buffer auf bestimmter größe halten. gibt anzahl gespeicherter Datenpunkte vor.
        if len(self.p1ManifoldArray) > self.datenbufferlaenge:
            self.p1ManifoldArray.pop(0)
            self.p2ProbeArray.pop(0)
            self.timearray.pop(0)
            self.setpointarray.pop(0)
            self.Messkartenlogger.warning('Werte aus p arrays gepopt/entfernt!')

        # Strings zum loggen erstellen und dann mit Messkartenlogger loggen
        stringp1 = ("aktueller p1 array:\t" + str(self.p1ManifoldArray))
        self.Messkartenlogger.info(stringp1)
        stringp2 = ("aktueller p2 array:\t" + str(self.p2ProbeArray))
        self.Messkartenlogger.info(stringp2)
        return data

    def vPropAnAus(self, Befehl_in="an"):
        Ventil_an = [True]
        Ventil_aus = [False]
        Ventiladresse = self._Ventiladressen("V_PropOnOff")
        if (Befehl_in == "an"):
            Befehl = Ventil_an
        if (Befehl_in == "aus"):
            Befehl = Ventil_aus
        # if (self.v_state["V_Prop"][
        #     "state"] != Befehl_in):  # soll nur schalten wenn Ventil nicht eh schon in Stellung ist

        if self.isDebugDummyMode is True:
            self.v_state["V_Prop"]["state"] = Befehl_in
            print("Ventil:\t", "V_Prop", "\tBefehl_in:\t", Befehl_in, "\tBefehl:\t", Befehl)
            print("in Ventil.task", self.v_state["V_Prop"])
            self.lastDAQtime = time.time()

        if self.isDebugDummyMode is False:
            try:
                with nidaqmx.Task() as VentilTask:
                    VentilTask.do_channels.add_do_chan(Ventiladresse, line_grouping=LineGrouping.CHAN_PER_LINE)
                    VentilTask.write(Befehl)
                    self.v_state["V_Prop"]["state"] = Befehl_in
                    print("Ventil:\t", "V_Prop", "\tBefehl_in:\t", Befehl_in, "\tBefehl:\t", Befehl)
                    print("in Ventil.task", self.v_state["V_Prop"])
                    self.lastDAQtime = time.time()
                    time.sleep(self.DAQwaitTime)


            except nidaqmx.DaqError as e:
                print(e)
                self.numberOfCommunicationErrors += 1
                return e

    def v_Prop_Stellgrad(self, Prozent):
        if self.lastStellgrad != Prozent:
            umax = 5  # V
            umin = 0  # V
            if Prozent > 100:
                Prozent = 100
            if Prozent < 0:
                Prozent = 0
            usoll = ((umax - umin) / 100) * Prozent

            if usoll > umax: usoll = umax
            if usoll < umin: umin = umin

            Ventiladresse = self._Ventiladressen("V_PropStellgrad")
            if self.isDebugDummyMode is True:
                self.v_state["V_Prop"]["stellgrad"] = Prozent
                print("V_prop Stellgrad = \t", self.v_state["V_Prop"]["stellgrad"], "\tProzent", '\t\tUSoll:\t', usoll)
                self.lastDAQtime = time.time()
                self.lastStellgrad = Prozent

            if self.isDebugDummyMode is False:
                with nidaqmx.Task() as VentilTask:
                    # VentilTask = nidaqmx.Task() #nur für debugzwecke
                    # print(Ventil_id, Befehl)
                    try:
                        VentilTask.ao_channels.add_ao_voltage_chan(Ventiladresse, min_val=0,
                                                                   max_val=5)  # task.ao_channels.add_ao_voltage_chan("Dev1/ao0")
                        VentilTask.write(usoll)
                        self.v_state["V_Prop"]["stellgrad"] = Prozent
                        print("V_prop Stellgrad = \t", self.v_state["V_Prop"]["stellgrad"], "\tProzent", '\t\tUSoll:\t',
                              usoll)
                        self.lastDAQtime = time.time()
                        self.lastStellgrad = Prozent
                        time.sleep(self.DAQwaitTime)


                    except nidaqmx.DaqError as e:
                        print(e)
                        self.numberOfCommunicationErrors += 1
                        return e
            return self.v_state

    def _alle_aus(self):
        # todo: umruesten auf iteration von v_state_in
        # [True, True]
# 'Dev1/port2/line0:1'\
# 'Dev1/port2/line2:3'\
# 'Dev1/port2/line4:5'' \
# ''Dev1/port1/line0:1'' \
# ''Dev1/port1/line2:3'' \
# ''Dev1/port1/line4:5'\
# 'Dev1/port1/line6:7'
        befehl = [True, True, True, True,True, True, True, True,True, True, True, True,True, True]
        try:
            with nidaqmx.Task() as VentilTask:
                Ventiladresse = 'Dev1/port1/line0:7'
                VentilTask.do_channels.add_do_chan(Ventiladresse, line_grouping=LineGrouping.CHAN_PER_LINE)
                # VentilTask.write(befehl)
                Ventiladresse = 'Dev1/port2/line0:5'
                VentilTask.do_channels.add_do_chan(Ventiladresse, line_grouping=LineGrouping.CHAN_PER_LINE)
                VentilTask.write(befehl)
                time.sleep(self.DAQwaitTime)
                self.lastDAQtime = time.time()

                self.v_state["V1"]["active"] = False
                self.v_state["V2"]["active"] = False
                self.v_state["V3"]["active"] = False
                self.v_state["V4"]["active"] = False
                self.v_state["V5"]["active"] = False
                self.v_state["V6"]["active"] = False
                self.v_state["V7"]["active"] = False

                self.anyValveOn = self.isAnyValveOn()

        except nidaqmx.DaqError as e:
            print(e)
            self.numberOfCommunicationErrors += 1
            return e

    def isAnyValveOn(self):
        if self.v_state["V1"]["active"] is False and self.v_state["V2"]["active"] is False and self.v_state["V3"][
            "active"] is False and self.v_state["V4"]["active"] is False and self.v_state["V5"]["active"] == False and \
                self.v_state["V6"]["active"] is False and self.v_state["V6"]["active"] is False:
            return False


    def Ventil_schalten_einzeln(self, Ventil_name="V1", Befehl_in="zu", einzeln_deaktivieren=True):
        # Todo: wenn fehler, state auf V-State ini setzen
        Ventiladresse = self._Ventiladressen(Ventil_name)
        if (Befehl_in == "auf"):
            Befehl = self.ventil_auf
        if (Befehl_in == "zu"):
            Befehl = self.Ventil_zu
        if (Befehl_in == "aus"):
            Befehl = self.Ventil_aus

        if (Befehl_in == "auf" or Befehl_in == "zu"):
            # Debug und Infoausgaben
            self.Messkartenlogger.debug("Ventil_schalten_einzeln:\t" + Ventil_name + Befehl_in)
            self.Messkartenlogger.debug(self.v_state)
            # soll nur schalten wenn Ventil nicht eh schon in Stellung ist
            if (self.v_state[Ventil_name]["state"] != Befehl_in):
                def stuffAfterAction():
                    self.lastValveActivation = time.time()
                    self.lastDAQtime = time.time()
                    time.sleep(self.DAQwaitTime)
                    self.anyValveOn = True

                    self.v_state[Ventil_name]["active"] = True
                    self.v_state[Ventil_name]["state"] = Befehl_in

                    self.Messkartenlogger.info(
                        "Ventil:\t" + str(Ventil_name) + "\tBefehl_in:\t" + str(Befehl_in) + "\tBefehl:\t" + str(
                            Befehl))
                    self.Messkartenlogger.info("in Ventil.task" + str(self.v_state[Ventil_name]))
                    # Verfolgt wann die Ventile geschaltet wurden, um sie nach der richtigen Zeit wieder auszuschalten

                if self.isDebugDummyMode is True:
                    stuffAfterAction()


                if self.isDebugDummyMode is False:
                    try:
                        with nidaqmx.Task() as VentilTask:
                            # VentilTask = nidaqmx.Task() #nur für debugzwecke
                            # print(Ventil_id, Befehl)
                            VentilTask.do_channels.add_do_chan(Ventiladresse, line_grouping=LineGrouping.CHAN_PER_LINE)
                            VentilTask.write(Befehl)
                            stuffAfterAction()

                    except nidaqmx.DaqError as e:
                        print(e)
                        self.numberOfCommunicationErrors += 1
                        return e
        if (Befehl_in == "aus"):
            self.Messkartenlogger.info(self.v_state)
            self.Messkartenlogger.info(Ventil_name)
            self.Messkartenlogger.info(self.v_state[Ventil_name])
            # self.Messkartenlogger.info("test ,", self.v_state[Ventil_name]["active"])
            # self.Messkartenlogger.info("test2\t", self.v_state[Ventil_name]["active"] != False)  # ist True
            if (self.v_state[Ventil_name]["active"] != False):
                def stuffAfterAction():
                    self.v_state[Ventil_name]["active"] = False
                    # v_state[Ventil_name]["state"] = "aus"
                    print("Ventil:\t", Ventil_name, "\tBefehl_in:\t", Befehl_in, "\tBefehl:\t", Befehl)
                    print("in Ventil.task", self.v_state[Ventil_name])
                    time.sleep(self.DAQwaitTime)
                    self.lastDAQtime = time.time()
                    self.anyValveOn = self.isAnyValveOn()


                if self.isDebugDummyMode is True:
                    stuffAfterAction()
                if self.isDebugDummyMode is False:
                    try:
                        with nidaqmx.Task() as VentilTask:
                            # VentilTask = nidaqmx.Task() #nur für debugzwecke
                            # print(Ventil_id, Befehl)
                            VentilTask.do_channels.add_do_chan(Ventiladresse, line_grouping=LineGrouping.CHAN_PER_LINE)
                            VentilTask.write(self.Ventil_aus)  #
                            stuffAfterAction()

                    except nidaqmx.DaqError as e:
                        print(e)
                        self.numberOfCommunicationErrors += 1
                        return e
        if (einzeln_deaktivieren == True and Befehl_in != "aus"):
            time.sleep(0.5)

            def stuffAfterAction():
                self.v_state[Ventil_name]["active"] = False
                print("Ventil:\t", Ventil_name, "\tBefehl_in:\t", Befehl_in, "\tBefehl:\t", Befehl)
                print("in Ventil.task", self.v_state[Ventil_name])
                self.lastDAQtime = time.time()
                time.sleep(self.DAQwaitTime)

            if self.isDebugDummyMode is True:
                stuffAfterAction()
            if self.isDebugDummyMode is False:
                try:
                    with nidaqmx.Task() as VentilTask:
                        # VentilTask = nidaqmx.Task() #nur für debugzwecke
                        # print(Ventil_id, Befehl)
                        VentilTask.do_channels.add_do_chan(Ventiladresse, line_grouping=LineGrouping.CHAN_PER_LINE)
                        VentilTask.write(self.Ventil_aus)
                        stuffAfterAction()
                except nidaqmx.DaqError as e:
                    print(e)
                    self.numberOfCommunicationErrors += 1
                    return e
        return Befehl

    def _Ventiladressen(self, Ventil_name):  # Todo: durch dict ersetzen
        if (Ventil_name == "V1"):
            Adress = 'Dev1/port2/line0:1'
            Ventilfunktion = "Pumpe"
        if (Ventil_name == "V2"):
            Adress = 'Dev1/port2/line2:3'
            Ventilfunktion = "Vent"
        if (Ventil_name == "V3"):
            Adress = 'Dev1/port2/line4:5'
            Ventilfunktion = "Verdampfer"
        if (Ventil_name == "V4"):
            Adress = 'Dev1/port1/line0:1'
            Ventilfunktion = "Bypass1"
        if (Ventil_name == "V5"):
            Adress = 'Dev1/port1/line2:3'
            Ventilfunktion = "Bypass2"
        if (Ventil_name == "V6"):
            Adress = 'Dev1/port1/line4:5'
            Ventilfunktion = "Messzelle"
        if (Ventil_name == "V7"):
            Adress = 'Dev1/port1/line6:7'
            Ventilfunktion = "Volumen"
        if (Ventil_name == "V_PropOnOff"):
            Adress = 'Dev1/port0/line7'  # vprop on/off = P0 line 7
            Ventilfunktion = "PropOnOff"
        if (Ventil_name == "V_PropStellgrad"):
            Adress = 'Dev1/ao0'  # vprop on/off = P0 line 7 "Dev1/ai0"   # vprop = ao0 (0 - max 5 V)
        # print(Ventil_name, ":\t", Ventilfunktion, "\tAdresse:\t", Adress)
        return (Adress)

    def Ventile_schalten_ges(self, v_state_soll, shutOffAuto=True):

        # def befehluebersetzung(Befehl_in):
        #     if (Befehl_in == "auf"):
        #         Befehl = self.ventil_auf
        #     if (Befehl_in == "zu"):
        #         Befehl = self.Ventil_zu
        #     if (Befehl_in == "aus"):
        #         Befehl = self.Ventil_aus
        #     return Befehl
        #
        # with nidaqmx.Task() as VentilTask:
        #     "V4"  'Dev1/port1/line0:1'
        #     "V5"  'Dev1/port1/line2:3'
        #     "V6"  'Dev1/port1/line4:5'
        #     "V7"  'Dev1/port1/line6:7'
        #     "V1"  'Dev1/port2/line0:1'
        #     "V2"  'Dev1/port2/line2:3'
        #     "V3"  'Dev1/port2/line4:5'

            # adresse = list(self._Ventiladressen("V1"))
            # VentilTask.do_channels.add_do_chan(adresse, line_grouping=LineGrouping.CHAN_PER_LINE)
            # befehl = befehluebersetzung(v_state_soll["V1"]["state"])
            # print (befehl)
            #
            # adresse.append(self._Ventiladressen("V2"))
            # print(adresse)
            # VentilTask.do_channels.add_do_chan(adresse, line_grouping=LineGrouping.CHAN_PER_LINE)
            # befehl += befehluebersetzung(v_state_soll["V2"]["state"])
            # print (befehl)
            #
            #
            # VentilTask.write(befehl)  #

        if self.anyValveOn is False:  # nur schalten wenn nichts aktiv
            self.vPropAnAus(v_state_soll["V_Prop"]["state"])
            self.Ventil_schalten_einzeln("V1", v_state_soll["V1"]["state"], False)
            self.Ventil_schalten_einzeln("V6", v_state_soll["V6"]["state"], False)
            self.Ventil_schalten_einzeln("V4", v_state_soll["V4"]["state"], False)
            self.Ventil_schalten_einzeln("V5", v_state_soll["V5"]["state"], False)
            self.Ventil_schalten_einzeln("V3", v_state_soll["V3"]["state"], False)
            self.Ventil_schalten_einzeln("V2", v_state_soll["V2"]["state"], False)
            self.Ventil_schalten_einzeln("V7", v_state_soll["V7"]["state"], False)
            if self.v_state["V1"]["state"] == v_state_soll["V1"]["state"] and self.v_state["V2"]["state"] == \
                    v_state_soll["V2"]["state"] and self.v_state["V3"]["state"] == v_state_soll["V3"]["state"] and \
                    self.v_state["V4"]["state"] == v_state_soll["V4"]["state"] and self.v_state["V5"]["state"] == \
                    v_state_soll["V5"]["state"] and self.v_state["V6"]["state"] == v_state_soll["V6"]["state"] and \
                    self.v_state["V7"]["state"] == v_state_soll["V7"]["state"] and v_state_soll["V_Prop"]["state"] == \
                    self.v_state["V_Prop"]["state"]:
                self.v_state["State"]["Name"] = v_state_soll["State"]["Name"]
                print("state gewechselt zu:", self.v_state["State"]["Name"])
            else:
                print("konnte state nicht von ", self.v_state["State"]["Name"], "\tzu\t", v_state_soll["State"]["Name"],
                      "\twechseln")
            if shutOffAuto == True:
                ## TODO: hier nur warten, wenn eines der Magnetvetile geschaltet hat
                time.sleep(0.5)
                self._alle_aus()

if __name__ == '__main__':
    V = Messkarte()
    # V.Ventile_schalten_ges(V.vStateSollVolumenEvakGrob)
    # V.Ventile_schalten_ges(V.vStateSollProbeEvakGrob)
