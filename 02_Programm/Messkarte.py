import logging
import time

import nidaqmx
from nidaqmx.constants import (LineGrouping)


# from transitions.extensions import GraphMachine as Machine

# class Machine

class Messkarte(object):
    # dict zum verfolgen der States der Ventile, damit die nur geschaltet werden wenn es nötig ist.
    v_state = {}

    datenbufferlaenge = 100
    timeStartMessung = time.time()
    timearray = []
    p1ProbeArray = []  # pProbeMbar
    p2ManifoldArray = []  # pManifoldMbar

    def __init__(self):

        ##############################################################################
        # logging optionen
        self.debugOn = True
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

        # definition der Relaiszustände für die Ventile pro Kanal
        self.ventil_auf = [True, False]
        self.Ventil_zu = [False, True]
        self.Ventil_aus = [True, True]

        # States initialisiern:
        self.__initVentilStates()  # sollstates initialisieren
        self.v_state = self.vStateInit  # unbekannter ausgangszustand

        # Verfolgt wann die Ventile geschaltet wurden, um sie nach der richtigen Zeit wieder auszuschalten
        self.lastValveActivation = time.time()

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
        self.vStateInit["V_Prop"] = {"id": 8, "stellgrad": "NA", "state": "NA"}

        self.vStateSollAlleZu = {}
        self.vStateSollAlleZu["State"] = {"Name": "vStateSollAlleZu"}
        self.vStateSollAlleZu["V1"] = {"state": "zu"}
        self.vStateSollAlleZu["V2"] = {"state": "zu"}
        self.vStateSollAlleZu["V3"] = {"state": "zu"}
        self.vStateSollAlleZu["V4"] = {"state": "zu"}
        self.vStateSollAlleZu["V5"] = {"state": "zu"}
        self.vStateSollAlleZu["V6"] = {"state": "zu"}
        self.vStateSollAlleZu["V7"] = {"state": "zu"}
        self.vStateSollAlleZu["V_Prop"] = {"state": "aus"}

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
        self.vStateSollVolumenEvakGrob["V_Prop"] = {"state": "aus"}

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
        self.vStateSollDoseFine["V1"] = {"state": "auf"}
        self.vStateSollDoseFine["V2"] = {"state": "zu"}
        self.vStateSollDoseFine["V3"] = {"state": "zu"}
        self.vStateSollDoseFine["V4"] = {"state": "auf"}
        self.vStateSollDoseFine["V5"] = {"state": "zu"}
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
        self.vStateSollDegassEvaporator["V_Prop"] = {"state": "aus"}

        self.vStateSollEvacFineVol1 = {}
        self.vStateSollEvacFineVol1["State"] = {"Name": "vStateSollEvacFineVol1"}
        self.vStateSollEvacFineVol1["V1"] = {"state": "auf"}
        self.vStateSollEvacFineVol1["V2"] = {"state": "zu"}
        self.vStateSollEvacFineVol1["V3"] = {"state": "zu"}
        self.vStateSollEvacFineVol1["V4"] = {"state": "auf"}
        self.vStateSollEvacFineVol1["V5"] = {"state": "auf"}
        self.vStateSollEvacFineVol1["V6"] = {"state": "zu"}
        self.vStateSollEvacFineVol1["V7"] = {"state": "zu"}
        self.vStateSollEvacFineVol1["V_Prop"] = {"state": "aus"}

        self.vStateSollVolSample = {}
        self.vStateSollVolSample["State"] = {"Name": "vStateSollEvacFineVol1"}
        self.vStateSollVolSample["V1"] = {"state": "zu"}
        self.vStateSollVolSample["V2"] = {"state": "zu"}
        self.vStateSollVolSample["V3"] = {"state": "zu"}
        self.vStateSollVolSample["V4"] = {"state": "auf"}
        self.vStateSollVolSample["V5"] = {"state": "auf"}
        self.vStateSollVolSample["V6"] = {"state": "auf"}
        self.vStateSollVolSample["V7"] = {"state": "zu"}
        self.vStateSollVolSample["V_Prop"] = {"state": "aus"}

        self.vStateSollDoseFineVol1 = {}
        self.vStateSollDoseFineVol1["State"] = {"Name": "vStateSollEvacFineVol1"}
        self.vStateSollDoseFineVol1["V1"] = {"state": "zu"}
        self.vStateSollDoseFineVol1["V2"] = {"state": "zu"}
        self.vStateSollDoseFineVol1["V3"] = {"state": "auf"}
        self.vStateSollDoseFineVol1["V4"] = {"state": "auf"}
        self.vStateSollDoseFineVol1["V5"] = {"state": "auf"}
        self.vStateSollDoseFineVol1["V6"] = {"state": "zu"}
        self.vStateSollDoseFineVol1["V7"] = {"state": "zu"}
        self.vStateSollDoseFineVol1["V_Prop"] = {"state": "aus"}

    def getP1ProbeMbar(self):
        return self.p1ProbeMbar

    def getP2ManifoldMbar(self):
        return self.p2ManifoldMbar

    def getp1ProbeArray(self):
        return self.p1ProbeArray

    def getp2ManifoldArray(self):
        return self.p2ManifoldArray

    def getTimearray(self):
        return self.timearray


    def readSensors(self):
        # sensoren auslesen. bisher nur zwei stück
        try:
            with nidaqmx.Task() as LeseTask:
                LeseTask.ai_channels.add_ai_voltage_chan("Dev1/ai0:4",
                                                         terminal_config=nidaqmx.constants.TerminalConfiguration.NRSE,
                                                         max_val=10,
                                                         min_val=0)  # terminal_config=VentilTask.TerminalConfiguration.NRSE

                data = LeseTask.read()
                # aktuelle Druckwerte als floats speichern
                self.p1ProbeMbar = data[0] * 10
                self.p2ManifoldMbar = data[1] * 10
                self.Messtime = time.time() - self.timeStartMessung


                # In logger anzeigen
                stringp = ("p1ProbeMbar = " + str(self.p1ProbeMbar) + ";\tp2ManifoldMbar = " + str(self.p2ManifoldMbar))
                self.Messkartenlogger.info(stringp)

                # daten in arrays abspeichern, mit fester Pufferlaenge
                # müssen ab und zu geflusht werden, oder einfacher: bei jedem takt wenn mehr als x in array?
                self.p1ProbeArray.append(self.p1ProbeMbar)
                self.p2ManifoldArray.append(self.p2ManifoldMbar)
                self.timearray.append(self.Messtime)
                # buffer auf bestimmter größe halten. gibt anzahl gespeicherter Datenpunkte vor.
                if len(self.p1ProbeArray) > self.datenbufferlaenge:
                    self.p1ProbeArray.pop(0)
                    self.p2ManifoldArray.pop(0)
                    self.timearray.pop(0)
                    self.Messkartenlogger.warning('Werte aus p arrays gepopt/entfernt!')

                # Strings zum loggen erstellen und dann mit Messkartenlogger loggen
                stringp1 = ("aktueller p1 array:\t" + str(self.p1ProbeArray))
                self.Messkartenlogger.info(stringp1)
                stringp2 = ("aktueller p2 array:\t" + str(self.p2ManifoldArray))
                self.Messkartenlogger.info(stringp2)
                return data
        except nidaqmx.DaqError as e:
            print(e)



    def vPropAnAus(self, Befehl_in="an"):
        Ventil_an = [True]
        Ventil_aus = [False]
        Ventiladresse = self._Ventiladressen("V_PropOnOff")
        if (Befehl_in == "an"):
            Befehl = Ventil_an
        if (Befehl_in == "aus"):
            Befehl = Ventil_aus
        if (self.v_state["V_Prop"][
            "state"] != Befehl_in):  # soll nur schalten wenn Ventil nicht eh schon in Stellung ist
            with nidaqmx.Task() as VentilTask:
                try:
                    VentilTask.do_channels.add_do_chan(Ventiladresse, line_grouping=LineGrouping.CHAN_PER_LINE)
                    (VentilTask.write(Befehl))
                    self.v_state["V_Prop"]["state"] = Befehl_in
                    print("Ventil:\t", "V_Prop", "\tBefehl_in:\t", Befehl_in, "\tBefehl:\t", Befehl)
                    print("in Ventil.task", self.v_state["V_Prop"])
                except nidaqmx.DaqError as e:
                    print(e)

    def v_Prop_Stellgrad(self, Prozent):

        umax = 5  # V
        umin = 0  # V
        usoll = ((umax - umin) / 100) * Prozent
        Ventiladresse = self._Ventiladressen("V_PropStellgrad")

        with nidaqmx.Task() as VentilTask:
            # VentilTask = nidaqmx.Task() #nur für debugzwecke
            # print(Ventil_id, Befehl)
            try:
                VentilTask.ao_channels.add_ao_voltage_chan(Ventiladresse, min_val=0,
                                                       max_val=5)  # task.ao_channels.add_ao_voltage_chan("Dev1/ao0")
                VentilTask.write(usoll)
                self.v_state["V_Prop"]["stellgrad"] = Prozent
                print("V_prop Stellgrad = \t", self.v_state["V_Prop"]["stellgrad"], "\tProzent", '\t\tUSoll:\t', usoll)
            except nidaqmx.DaqError as e:
                print(e)
        return self.v_state

    def _alle_aus(self):
        # todo: umruesten auf iteration von v_state_in
        self.Ventil_schalten_einzeln("V1", "aus", False)
        self.Ventil_schalten_einzeln("V2", "aus", False)
        self.Ventil_schalten_einzeln("V3", "aus", False)
        self.Ventil_schalten_einzeln("V4", "aus", False)
        self.Ventil_schalten_einzeln("V5", "aus", False)
        self.Ventil_schalten_einzeln("V6", "aus", False)
        self.Ventil_schalten_einzeln("V7", "aus", False)

    def Ventil_schalten_einzeln(self, Ventil_name="V1", Befehl_in="zu", einzeln_deaktivieren=True):
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
                with nidaqmx.Task() as VentilTask:
                    # VentilTask = nidaqmx.Task() #nur für debugzwecke
                    # print(Ventil_id, Befehl)
                    VentilTask.do_channels.add_do_chan(Ventiladresse, line_grouping=LineGrouping.CHAN_PER_LINE)
                    try:
                        (VentilTask.write(Befehl))
                        self.v_state[Ventil_name]["active"] = True
                        self.v_state[Ventil_name]["state"] = Befehl_in
                        self.Messkartenlogger.info(
                            "Ventil:\t" + str(Ventil_name) + "\tBefehl_in:\t" + str(Befehl_in) + "\tBefehl:\t" + str(
                                Befehl))
                        self.Messkartenlogger.info("in Ventil.task" + str(self.v_state[Ventil_name]))
                        # Verfolgt wann die Ventile geschaltet wurden, um sie nach der richtigen Zeit wieder auszuschalten
                        self.lastValveActivation = time.time()
                        time.sleep(0.01)

                    except nidaqmx.DaqError as e:
                        print(e)
        if (Befehl_in == "aus"):
            self.Messkartenlogger.info(self.v_state)
            self.Messkartenlogger.info(Ventil_name)
            self.Messkartenlogger.info(self.v_state[Ventil_name])
            # self.Messkartenlogger.info("test ,", self.v_state[Ventil_name]["active"])
            # self.Messkartenlogger.info("test2\t", self.v_state[Ventil_name]["active"] != False)  # ist True
            if (self.v_state[Ventil_name]["active"] != False):
                with nidaqmx.Task() as VentilTask:
                    # VentilTask = nidaqmx.Task() #nur für debugzwecke
                    # print(Ventil_id, Befehl)
                    VentilTask.do_channels.add_do_chan(Ventiladresse, line_grouping=LineGrouping.CHAN_PER_LINE)
                    try:
                        (VentilTask.write(self.Ventil_aus))  # beide kanäle an, wird nie gebaucht
                        self.v_state[Ventil_name]["active"] = False
                        # v_state[Ventil_name]["state"] = "aus"
                        print("Ventil:\t", Ventil_name, "\tBefehl_in:\t", Befehl_in, "\tBefehl:\t", Befehl)
                        print("in Ventil.task", self.v_state[Ventil_name])
                    except nidaqmx.DaqError as e:
                        print(e)
        if (einzeln_deaktivieren == True and Befehl_in != "aus"):
            time.sleep(0.5)
            with nidaqmx.Task() as VentilTask:
                # VentilTask = nidaqmx.Task() #nur für debugzwecke
                # print(Ventil_id, Befehl)
                VentilTask.do_channels.add_do_chan(Ventiladresse, line_grouping=LineGrouping.CHAN_PER_LINE)
                try:
                    (VentilTask.write(self.Ventil_aus))  # beide kanäle an, wird nie gebaucht
                    self.v_state[Ventil_name]["active"] = False
                    print("Ventil:\t", Ventil_name, "\tBefehl_in:\t", Befehl_in, "\tBefehl:\t", Befehl)
                    print("in Ventil.task", self.v_state[Ventil_name])
                except nidaqmx.DaqError as e:
                    print(e)

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
        # todo: umruesten auf iteration von self.v_state
        # for blabla in v_state:
        #     print(blabla)
        #     print(v_state[blabla])
        self.Ventil_schalten_einzeln("V1", v_state_soll["V1"]["state"], False)
        self.Ventil_schalten_einzeln("V2", v_state_soll["V2"]["state"], False)
        self.Ventil_schalten_einzeln("V3", v_state_soll["V3"]["state"], False)
        self.Ventil_schalten_einzeln("V4", v_state_soll["V4"]["state"], False)
        self.Ventil_schalten_einzeln("V5", v_state_soll["V5"]["state"], False)
        self.Ventil_schalten_einzeln("V6", v_state_soll["V6"]["state"], False)
        self.Ventil_schalten_einzeln("V7", v_state_soll["V7"]["state"], False)
        self.vPropAnAus( v_state_soll["V_Prop"]["state"])
        if shutOffAuto == True:
            ## TODO: hier nur warten, wenn eines der Magnetvetile geschaltet hat
            time.sleep(0.5)
            self._alle_aus()

if __name__ == '__main__':
    V = Messkarte()
    # V.Ventile_schalten_ges(V.vStateSollVolumenEvakGrob)
    V.Ventile_schalten_ges(V.vStateSollProbeEvakGrob)
