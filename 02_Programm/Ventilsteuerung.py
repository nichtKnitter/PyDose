# altes nidaqmx beispiel für ventile

import pprint

import nidaqmx
from nidaqmx.constants import (LineGrouping)

pp = pprint.PrettyPrinter(indent=4)
import time

from transitions import Machine

# Set up logging; The basic log level will be DEBUG
import logging

logging.basicConfig(level=logging.DEBUG)
# Set transitions' log level to INFO; DEBUG messages will be omitted
logging.getLogger('transitions').setLevel(logging.INFO)


# from transitions.extensions import GraphMachine as Machine

# class Machine

class Ventile(object):
    statesAblauf = ['evakuieren_grob', 'druck_halten', 'druck_erhoehen', 'druck_veringern', 'aus', 'reset', "Messen",
              "warten"]
    statesAblauf_aktuell = "NA"

    statesAktionen = ['Messen', 'Schalten', 'Speichern', 'warten']

    next_segment = False
    v_state = {}

    machine_test = Machine()


    def __init__(self):
        self.v_state = self.vSstateInit()
        self.Takt_s = 1
        self.solldruck = 5600
        self.druck = 56

        self.ventil_auf = [True, False]
        self.Ventil_zu = [False, True]
        self.Ventil_aus = [True, True]

        self.machine = Machine(model=self, states=Ventile.statesAblauf, initial='reset')

        self.machine.add_transition("Druck_Halten_start", source="warten", dest='druck_halten')
        self.machine.add_transition("druck_halten_ende", source="druck_halten", dest='warten')
        self.machine.add_transition("messen_start", source="warten", dest='messen')
        self.machine.add_transition("messen_stop", source="messen", dest='warten')

        # States:
        # nur zum initialisieren, macht nichts wenn ich methoden überschreibe
        self.v_soll_alle_zu = self.vStateAlleZu()
        self.v_soll_alle_auf = self.vStateAlleAuf()
        self.vSollAlleAus = self.alle_aus()
        self.v_state_soll_Volumen_evak_grob = self.vStateSollVolumenEvakGrob()
        # self.vStateSollAlleAuf = self.vStateAlleAuf()



    def run(self):
        timeStart = time.time()
        while True:
            time.sleep(self.Takt_s)
            time_s = time.time()
            pp.pprint(time.time())

            # -> Messen ->
            # -> run (Entscheiden)
            #   if bedingung = True
            #       <-> Schalten
            #       <-> Speichern
            #       <-> Anzeigen
            # -> Warten

            self.solldruck = 56  # aus segmentconfig uebernehem
            # Todo: hier in den state messen wechseln
            # Messen(Next_state)
            print("self.druck = readSensors()")
            print(Ventile.statesAblauf)
            if (time_s - timeStart > 3): break
            # if time_s < (self.druck - 1) or next_segment == True:
            #     # or max zeit or user event
            #     break

    def druck_halten(self, solldruck, time_s):
        self.machine.set_state("druck_halten")
        print("Ventile schalten")
        print(solldruck)

        # if abs(solldruck - self.druck)> self.delta_p:

    def readSensors(self):
        self.druck = print("Sensoren lesen")

    def v_Prop_Stellgrad(self, Prozent):

        umax = 5  # V
        umin = 0  # V
        usoll = ((umax - umin) / 100) * Prozent
        Ventiladresse = self.Ventiladressen("V_PropStellgrad")
        print('test4\t',Ventiladresse)

        with nidaqmx.Task() as VentilTask:
            # VentilTask = nidaqmx.Task() #nur für debugzwecke
            # print(Ventil_id, Befehl)
            VentilTask.ao_channels.add_ao_voltage_chan(Ventiladresse, min_val=0,
                                                       max_val=5)  # task.ao_channels.add_ao_voltage_chan("Dev1/ao0")

            try:
                VentilTask.write(usoll)
                self.v_state["V_Prop"]["stellgrad"] = Prozent
                print("V_prop Stellgrad = \t", self.v_state["V_Prop"]["stellgrad"], "\tProzent")
            except nidaqmx.DaqError as e:
                print(e)
        return self.v_state

    # Ab hier Statedefinitionen

    def vPropAnAus(self, Befehl_in="an"):
        Ventil_an = [True]
        Ventil_aus = [False]
        Ventiladresse = self.Ventiladressen("V_PropOnOff")
        if (Befehl_in == "an"):
            Befehl = Ventil_an
        if (Befehl_in == "aus"):
            Befehl = Ventil_aus
        if (self.v_state["V_Prop"][
            "state"] != Befehl_in):  # soll nur schalten wenn Ventil nicht eh schon in Stellung ist
            with nidaqmx.Task() as VentilTask:
                VentilTask.do_channels.add_do_chan(Ventiladresse, line_grouping=LineGrouping.CHAN_PER_LINE)
                try:
                    (VentilTask.write(Befehl))
                    self.v_state["V_Prop"]["state"] = Befehl_in
                    print("Ventil:\t", "V_Prop", "\tBefehl_in:\t", Befehl_in, "\tBefehl:\t", Befehl)
                    print("in Ventil.task", self.v_state["V_Prop"])
                except nidaqmx.DaqError as e:
                    print(e)

    def vStateAlleZu(self):
        self.vStateSollAlleZu = {}
        self.vStateSollAlleZu["V1"] = {"state": "zu"}
        self.vStateSollAlleZu["V2"] = {"state": "zu"}
        self.vStateSollAlleZu["V3"] = {"state": "zu"}
        self.vStateSollAlleZu["V4"] = {"state": "zu"}
        self.vStateSollAlleZu["V5"] = {"state": "zu"}
        self.vStateSollAlleZu["V6"] = {"state": "zu"}
        self.vStateSollAlleZu["V7"] = {"state": "zu"}
        self.vStateSollAlleZu["V_Prop"] = {"state": "aus"}
        return self.vStateSollAlleZu

    def vSstateInit(self):
        self.v_state = {}
        self.v_state["V1"] = {"id": 1, "state": "NA", "active": "NA"}
        self.v_state["V2"] = {"id": 2, "state": "NA", "active": "NA"}
        self.v_state["V3"] = {"id": 3, "state": "NA", "active": "NA"}
        self.v_state["V4"] = {"id": 4, "state": "NA", "active": "NA"}
        self.v_state["V5"] = {"id": 5, "state": "NA", "active": "NA"}
        self.v_state["V6"] = {"id": 6, "state": "NA", "active": "NA"}
        self.v_state["V7"] = {"id": 7, "state": "NA", "active": "NA"}
        self.v_state["V_Prop"] = {"id": 8, "stellgrad": "NA", "state": "NA"}
        return self.v_state

    def vStateAlleAuf(self):
        self.vStateSollAlleAuf = {}
        self.vStateSollAlleAuf["V1"] = {"state": "auf"}
        self.vStateSollAlleAuf["V2"] = {"state": "auf"}
        self.vStateSollAlleAuf["V3"] = {"state": "auf"}
        self.vStateSollAlleAuf["V4"] = {"state": "auf"}
        self.vStateSollAlleAuf["V5"] = {"state": "auf"}
        self.vStateSollAlleAuf["V6"] = {"state": "auf"}
        self.vStateSollAlleAuf["V7"] = {"state": "auf"}
        self.vStateSollAlleAuf["V_Prop"] = {"state": "an"}

    def vStateSollVolumenEvakGrob(self):
        self.vStateSollVolumenEvakGrob = {}
        self.vStateSollVolumenEvakGrob["V1"] = {"state": "auf"}
        self.vStateSollVolumenEvakGrob["V2"] = {"state": "zu"}
        self.vStateSollVolumenEvakGrob["V3"] = {"state": "zu"}
        self.vStateSollVolumenEvakGrob["V4"] = {"state": "zu"}
        self.vStateSollVolumenEvakGrob["V5"] = {"state": "auf"}
        self.vStateSollVolumenEvakGrob["V6"] = {"state": "zu"}
        self.vStateSollVolumenEvakGrob["V7"] = {"state": "zu"}
        self.vStateSollVolumenEvakGrob["V_Prop"] = {"state": "aus"}
        return self.vStateSollVolumenEvakGrob

    def alle_aus(self):
        # todo: umruesten auf iteration von v_state_in
        self.Ventil_schalten_einzeln("V1", "aus", False)
        self.Ventil_schalten_einzeln("V2", "aus", False)
        self.Ventil_schalten_einzeln("V3", "aus", False)
        self.Ventil_schalten_einzeln("V4", "aus", False)
        self.Ventil_schalten_einzeln("V5", "aus", False)
        self.Ventil_schalten_einzeln("V6", "aus", False)
        self.Ventil_schalten_einzeln("V7", "aus", False)

    def Ventil_schalten_einzeln(self, Ventil_name, Befehl_in, einzeln_deaktivieren=True):
        # time.sleep(0.005)    #minimale Sicherheitspause, hilft vielleicht gegen Kommunikationsprobleme?

        Ventiladresse = self.Ventiladressen(Ventil_name)
        if (Befehl_in == "auf"):
            Befehl = self.ventil_auf
        if (Befehl_in == "zu"):
            Befehl = self.Ventil_zu
        if (Befehl_in == "aus"):
            Befehl = self.Ventil_aus

        if (Befehl_in == "auf" or Befehl_in == "zu"):
            if (self.v_state[Ventil_name][
                "state"] != Befehl_in):  # soll nur schalten wenn Ventil nicht eh schon in Stellung ist
                with nidaqmx.Task() as VentilTask:
                    # VentilTask = nidaqmx.Task() #nur für debugzwecke
                    # print(Ventil_id, Befehl)
                    VentilTask.do_channels.add_do_chan(Ventiladresse, line_grouping=LineGrouping.CHAN_PER_LINE)
                    try:
                        (VentilTask.write(Befehl))
                        self.v_state[Ventil_name]["active"] = True
                        self.v_state[Ventil_name]["state"] = Befehl_in
                        print("Ventil:\t", Ventil_name, "\tBefehl_in:\t", Befehl_in, "\tBefehl:\t", Befehl)
                        print("in Ventil.task", self.v_state[Ventil_name])
                    except nidaqmx.DaqError as e:
                        print(e)
        if (Befehl_in == "aus"):
            print(self.v_state)
            print(Ventil_name)
            print(self.v_state[Ventil_name])
            print("test ,", self.v_state[Ventil_name]["active"])
            print("test2\t", self.v_state[Ventil_name]["active"] != False)  # ist True
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

    def Ventiladressen(self, Ventil_name):  # Todo: durch dict ersetzen
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


    def Ventile_schalten_ges(self,v_state_soll):
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
        print('test3/t', v_state_soll["V_Prop"]["state"])
        self.vPropAnAus( v_state_soll["V_Prop"]["state"])
        time.sleep(0.5)
        self.alle_aus()



    def Ablauf_Test1(self):
        print("\n\n\n Vierter Durchlauf")
        self.Ventile_schalten_ges(self.v_state_soll_Volumen_evak_grob)
        print("\n\n\n Vierter Durchlauf")
        time.sleep(2)
        self.Ventile_schalten_ges(self.v_soll_alle_zu)
        print("\n\n\n Vierter Durchlauf")
        time.sleep(2)
        self.Ventile_schalten_ges(self.v_state_soll_Volumen_evak_grob)
        time.sleep(2)
        self.v_Prop_Stellgrad(Prozent=1)
        time.sleep(2)
        self.v_Prop_Stellgrad(Prozent=50)
        time.sleep(2)
        self.v_Prop_Stellgrad(Prozent=70)






if __name__ == '__main__':
    # folgende Zeilen müssen in self.init kommen

    # v_state = v_state_init()  # state initialisieren, oder zurücksetzen...

    # v_state = Ventile_schalten_ges(v_state_soll_alle_zu, v_state)
    # Ablauf_Test1(v_state)
    V = Ventile()
    V.to_Messen()
    print(V.state)
    V.to_warten()
    print(V.state)
    V.run()
    V.druck_halten(50, 30)
    V = Ventile()
    V = Ventile()
