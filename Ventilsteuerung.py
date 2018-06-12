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

class Ventile(object):
    states = ['evakuieren_grob', 'druck_halten', 'druck_erhoehen', 'druck_veringern', 'aus', 'reset', "Messen",
              "warten"]

    v_state = {}
    next_segment = False

    def __init__(self):
        self.v_state = self.v_state_init()
        self.Takt_s = 1
        self.solldruck = 56
        self.druck = 56

        self.machine = Machine(model=self, states=Ventile.states, initial='reset')

        self.machine.add_transition("Druck_Halten_start", source="warten", dest='druck_halten')
        self.machine.add_transition("druck_halten_ende", source="druck_halten", dest='warten')
        self.machine.add_transition("messen_start", source="warten", dest='messen')
        self.machine.add_transition("messen_stop", source="messen", dest='warten')

    def v_state_init(self):
        v_state = {}
        v_state["V1"] = {"id": 1, "state": "NA", "active": "NA"}
        v_state["V2"] = {"id": 2, "state": "NA", "active": "NA"}
        v_state["V3"] = {"id": 3, "state": "NA", "active": "NA"}
        v_state["V4"] = {"id": 4, "state": "NA", "active": "NA"}
        v_state["V5"] = {"id": 5, "state": "NA", "active": "NA"}
        v_state["V6"] = {"id": 6, "state": "NA", "active": "NA"}
        v_state["V7"] = {"id": 7, "state": "NA", "active": "NA"}
        v_state["V_Prop"] = {"id": 8, "stellgrad": "NA", "state": "NA"}
        return v_state

    def run(self):
        while True:
            time.sleep(self.Takt_s)
            time_s = time.time()
            pp.pprint(time.time())

            self.solldruck = 56  # aus segmentconfig uebernehem
            # Todo: hier in den state messen wechseln
            # Messen(Next_state)
            print("self.druck = readSensors()")
            print(Ventile.states)
            if time_s < (self.druck - 1) or next_segment == True:
                # or max zeit or user event
                break

    def druck_halten(self, solldruck, time_s):
        self.machine.set_state("druck_halten")
        print("Ventile schalten")
        print(solldruck)

        # if abs(solldruck - self.druck)> self.delta_p:

    def readSensors(self):
        self.druck = print("Sensoren lesen")

V = Ventile()
V.druck_halten(50, 30)


def v_state_alle_zu():
    v_state_soll_alle_zu = {}
    v_state_soll_alle_zu["V1"] = {"state": "zu"}
    v_state_soll_alle_zu["V2"] = {"state": "zu"}
    v_state_soll_alle_zu["V3"] = {"state": "zu"}
    v_state_soll_alle_zu["V4"] = {"state": "zu"}
    v_state_soll_alle_zu["V5"] = {"state": "zu"}
    v_state_soll_alle_zu["V6"] = {"state": "zu"}
    v_state_soll_alle_zu["V7"] = {"state": "zu"}
    v_state_soll_alle_zu["V_Prop"] = {"state": "aus"}
    return v_state_soll_alle_zu


def v_state_alle_auf():
    v_state_soll_alle_auf = {}
    v_state_soll_alle_auf["V1"] = {"state": "auf"}
    v_state_soll_alle_auf["V2"] = {"state": "auf"}
    v_state_soll_alle_auf["V3"] = {"state": "auf"}
    v_state_soll_alle_auf["V4"] = {"state": "auf"}
    v_state_soll_alle_auf["V5"] = {"state": "auf"}
    v_state_soll_alle_auf["V6"] = {"state": "auf"}
    v_state_soll_alle_auf["V7"] = {"state": "auf"}
    v_state_soll_alle_auf["V_Prop"] = {"state": "an"}
    return v_state_soll_alle_auf


v_state_soll_Volumen_evak_grob = {}
v_state_soll_Volumen_evak_grob["V1"] = {"state": "auf"}
v_state_soll_Volumen_evak_grob["V2"] = {"state": "zu"}
v_state_soll_Volumen_evak_grob["V3"] = {"state": "zu"}
v_state_soll_Volumen_evak_grob["V4"] = {"state": "zu"}
v_state_soll_Volumen_evak_grob["V5"] = {"state": "auf"}
v_state_soll_Volumen_evak_grob["V6"] = {"state": "zu"}
v_state_soll_Volumen_evak_grob["V7"] = {"state": "zu"}
v_state_soll_Volumen_evak_grob["V_Prop"] = {"state": "aus"}


def v_Prop_an_aus(v_state, Befehl_in):
    Ventil_an = [True]
    Ventil_aus = [False]
    Ventiladresse = Ventiladressen("V_PropOnOff")
    if (Befehl_in == "an"):
        Befehl = Ventil_an
    if (Befehl_in == "aus"):
        Befehl = Ventil_aus
    if (v_state["V_Prop"]["state"] != Befehl_in):  # soll nur schalten wenn Ventil nicht eh schon in Stellung ist
        with nidaqmx.Task() as VentilTask:
            VentilTask.do_channels.add_do_chan(Ventiladresse, line_grouping=LineGrouping.CHAN_PER_LINE)
            try:
                (VentilTask.write(Befehl))
                v_state["V_Prop"]["state"] = Befehl_in
                pp.pprint("Ventil:\t", "V_Prop", "\tBefehl_in:\t", Befehl_in, "\tBefehl:\t", Befehl)
                pp.pprint("in Ventil.task", v_state["V_Prop"])
            except nidaqmx.DaqError as e:
                pp.pprint(e)
    return v_state


def v_Prop_Stellgrad(v_state, Prozent):

    umax = 5  # V
    umin = 0  # V
    usoll = ((umax - umin) / 100) * Prozent
    Ventiladresse = Ventiladressen("V_PropStellgrad")

    with nidaqmx.Task() as VentilTask:
        # VentilTask = nidaqmx.Task() #nur für debugzwecke
        # print(Ventil_id, Befehl)
        VentilTask.ao_channels.add_ao_voltage_chan("Dev1/ao0", min_val=0,
                                                   max_val=5)  # task.ao_channels.add_ao_voltage_chan("Dev1/ao0")

        try:
            VentilTask.write(usoll)
            v_state["V_Prop"]["stellgrad"] = Prozent
            pp.pprint("V_prop Stellgrad = \t", v_state["V_Prop"]["stellgrad"], "\tProzent")
        except nidaqmx.DaqError as e:
            pp.pprint(e)
    return v_state


def alle_aus(v_state_in):
    # todo: umruesten auf iteration von v_state_in
    # for blabla in v_state:
    #     print(blabla)
    #     print(v_state[blabla])
    v_state_in = Ventil_schalten_einzeln("V1", "aus", v_state_in, False)
    v_state_in = Ventil_schalten_einzeln("V2", "aus", v_state_in, False)
    v_state_in = Ventil_schalten_einzeln("V3", "aus", v_state_in, False)
    v_state_in = Ventil_schalten_einzeln("V4", "aus", v_state_in, False)
    v_state_in = Ventil_schalten_einzeln("V5", "aus", v_state_in, False)
    v_state_in = Ventil_schalten_einzeln("V6", "aus", v_state_in, False)
    v_state_in = Ventil_schalten_einzeln("V7", "aus", v_state_in, False)
    pp.pprint("in alle_aus", v_state_in)
    return (v_state_in)


def Ventile_schalten_ges(v_state_soll, v_state_in):
    # todo: umruesten auf iteration von v_state_in
    # for blabla in v_state:
    #     print(blabla)
    #     print(v_state[blabla])
    v_state_in = Ventil_schalten_einzeln("V1", v_state_soll["V1"]["state"], v_state_in, False)
    v_state_in = Ventil_schalten_einzeln("V2", v_state_soll["V2"]["state"], v_state_in, False)
    v_state_in = Ventil_schalten_einzeln("V3", v_state_soll["V3"]["state"], v_state_in, False)
    v_state_in = Ventil_schalten_einzeln("V4", v_state_soll["V4"]["state"], v_state_in, False)
    v_state_in = Ventil_schalten_einzeln("V5", v_state_soll["V5"]["state"], v_state_in, False)
    v_state_in = Ventil_schalten_einzeln("V6", v_state_soll["V6"]["state"], v_state_in, False)
    v_state_in = Ventil_schalten_einzeln("V7", v_state_soll["V7"]["state"], v_state_in, False)
    v_state_in = v_Prop_an_aus(v_state_in, v_state_soll["V_Prop"]["state"])
    time.sleep(0.5)
    v_state_in = alle_aus(v_state_in)
    return v_state_in


def Ventiladressen(Ventil_name):  # Todo: durch dict ersetzen
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
        Adress = 'Dev1/ao0/'  # vprop on/off = P0 line 7 "Dev1/ai0"   # vprop = ao0 (0 - max 5 V)
    # print(Ventil_name, ":\t", Ventilfunktion, "\tAdresse:\t", Adress)
    return (Adress)


def Ventil_schalten_einzeln(Ventil_name, Befehl_in, v_state, einzeln_deaktivieren=True):
    # time.sleep(0.005)    #minimale Sicherheitspause, hilft vielleicht gegen Kommunikationsprobleme?
    Ventil_auf = [True, False]
    Ventil_zu = [False, True]
    Ventil_aus = [True, True]
    Ventiladresse = Ventiladressen(Ventil_name)
    if (Befehl_in == "auf"):
        Befehl = Ventil_auf
    if (Befehl_in == "zu"):
        Befehl = Ventil_zu
    if (Befehl_in == "aus"):
        Befehl = Ventil_aus

    if (Befehl_in == "auf" or Befehl_in == "zu"):
        if (v_state[Ventil_name]["state"] != Befehl_in):  # soll nur schalten wenn Ventil nicht eh schon in Stellung ist
            with nidaqmx.Task() as VentilTask:
                # VentilTask = nidaqmx.Task() #nur für debugzwecke
                # print(Ventil_id, Befehl)
                VentilTask.do_channels.add_do_chan(Ventiladresse, line_grouping=LineGrouping.CHAN_PER_LINE)
                try:
                    (VentilTask.write(Befehl))
                    v_state[Ventil_name]["active"] = True
                    v_state[Ventil_name]["state"] = Befehl_in
                    print("Ventil:\t", Ventil_name, "\tBefehl_in:\t", Befehl_in, "\tBefehl:\t", Befehl)
                    print("in Ventil.task", v_state[Ventil_name])
                except nidaqmx.DaqError as e:
                    print(e)
    if (Befehl_in == "aus"):
        if (v_state[Ventil_name]["active"] != False):
            with nidaqmx.Task() as VentilTask:
                # VentilTask = nidaqmx.Task() #nur für debugzwecke
                # print(Ventil_id, Befehl)
                VentilTask.do_channels.add_do_chan(Ventiladresse, line_grouping=LineGrouping.CHAN_PER_LINE)
                try:
                    (VentilTask.write(Ventil_aus))  # beide kanäle an, wird nie gebaucht
                    v_state[Ventil_name]["active"] = False
                    # v_state[Ventil_name]["state"] = "aus"
                    print("Ventil:\t", Ventil_name, "\tBefehl_in:\t", Befehl_in, "\tBefehl:\t", Befehl)
                    print("in Ventil.task", v_state[Ventil_name])
                except nidaqmx.DaqError as e:
                    print(e)
    if (einzeln_deaktivieren == True and Befehl_in != "aus"):
        time.sleep(0.5)
        with nidaqmx.Task() as VentilTask:
            # VentilTask = nidaqmx.Task() #nur für debugzwecke
            # print(Ventil_id, Befehl)
            VentilTask.do_channels.add_do_chan(Ventiladresse, line_grouping=LineGrouping.CHAN_PER_LINE)
            try:
                (VentilTask.write(Ventil_aus))  # beide kanäle an, wird nie gebaucht
                v_state[Ventil_name]["active"] = False
                print("Ventil:\t", Ventil_name, "\tBefehl_in:\t", Befehl_in, "\tBefehl:\t", Befehl)
                print("in Ventil.task", v_state[Ventil_name])
            except nidaqmx.DaqError as e:
                print(e)
    return (v_state)


def Ablauf_Test1(v_state):
    print("\n\n\n Vierter Durchlauf")
    v_state = Ventile_schalten_ges(v_state_soll_Volumen_evak_grob, v_state)
    print("\n\n\n Vierter Durchlauf")
    time.sleep(2)
    v_state = Ventile_schalten_ges(v_state_soll_alle_zu, v_state)
    print("\n\n\n Vierter Durchlauf")
    time.sleep(2)
    v_state = Ventile_schalten_ges(v_state_soll_Volumen_evak_grob, v_state)
    time.sleep(2)
    v_state = v_Prop_Stellgrad(v_state=v_state, Prozent=1)
    time.sleep(2)
    v_state = v_Prop_Stellgrad(v_state=v_state, Prozent=50)
    time.sleep(2)
    v_state = v_Prop_Stellgrad(v_state=v_state, Prozent=70)
    return v_state


if __name__ == '__main__':
    # folgende Zeilen müssen in self.init kommen
    v_state_soll_alle_zu = v_state_alle_zu()
    v_state_soll_alle_auf = v_state_alle_auf()
    # v_state = v_state_init()  # state initialisieren, oder zurücksetzen...

    # v_state = Ventile_schalten_ges(v_state_soll_alle_zu, v_state)
    # Ablauf_Test1(v_state)
    V.to_Messen()
    print(V.state)
    V.to_warten()
    print(V.state)
