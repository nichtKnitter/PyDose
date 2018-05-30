# altes nidaqmx beispiel für ventile

import pprint

import nidaqmx
from nidaqmx.constants import (LineGrouping)

pp = pprint.PrettyPrinter(indent=4)
import time


def v_state_init():
    v_state = {}
    v_state["V1"] = {"id": 1, "state": "NA", "active": "NA"}
    v_state["V2"] = {"id": 2, "state": "NA", "active": "NA"}
    v_state["V3"] = {"id": 3, "state": "NA", "active": "NA"}
    v_state["V4"] = {"id": 4, "state": "NA", "active": "NA"}
    v_state["V5"] = {"id": 5, "state": "NA", "active": "NA"}
    v_state["V6"] = {"id": 6, "state": "NA", "active": "NA"}
    v_state["V7"] = {"id": 7, "state": "NA", "active": "NA"}
    return v_state


def v_state_alle_zu():
    v_state_soll_alle_zu = {}
    v_state_soll_alle_zu["V1"] = {"state": "zu"}
    v_state_soll_alle_zu["V2"] = {"state": "zu"}
    v_state_soll_alle_zu["V3"] = {"state": "zu"}
    v_state_soll_alle_zu["V4"] = {"state": "zu"}
    v_state_soll_alle_zu["V5"] = {"state": "zu"}
    v_state_soll_alle_zu["V6"] = {"state": "zu"}
    v_state_soll_alle_zu["V7"] = {"state": "zu"}
    return v_state_soll_alle_zu

v_state_soll_alle_auf = {}
v_state_soll_alle_auf["V1"] = {"state": "auf"}
v_state_soll_alle_auf["V2"] = {"state": "auf"}
v_state_soll_alle_auf["V3"] = {"state": "auf"}
v_state_soll_alle_auf["V4"] = {"state": "auf"}
v_state_soll_alle_auf["V5"] = {"state": "auf"}
v_state_soll_alle_auf["V6"] = {"state": "auf"}
v_state_soll_alle_auf["V7"] = {"state": "auf"}

v_state_soll_Volumen_evak_grob = {}
v_state_soll_Volumen_evak_grob["V1"] = {"state": "auf"}
v_state_soll_Volumen_evak_grob["V2"] = {"state": "zu"}
v_state_soll_Volumen_evak_grob["V3"] = {"state": "zu"}
v_state_soll_Volumen_evak_grob["V4"] = {"state": "zu"}
v_state_soll_Volumen_evak_grob["V5"] = {"state": "auf"}
v_state_soll_Volumen_evak_grob["V6"] = {"state": "zu"}
v_state_soll_Volumen_evak_grob["V7"] = {"state": "zu"}



def alle_aus(v_state_in):
    v_state_in = Ventil_schalten_einzeln("V1", "aus", v_state_in)
    v_state_in = Ventil_schalten_einzeln("V2", "aus", v_state_in)
    v_state_in = Ventil_schalten_einzeln("V3", "aus", v_state_in)
    v_state_in = Ventil_schalten_einzeln("V4", "aus", v_state_in)
    v_state_in = Ventil_schalten_einzeln("V5", "aus", v_state_in)
    v_state_in = Ventil_schalten_einzeln("V6", "aus", v_state_in)
    v_state_in = Ventil_schalten_einzeln("V7", "aus", v_state_in)
    print("in alle_aus", v_state_in)
    return (v_state_in)


def Ventile_schalten_ges(v_state_soll, v_state_in):
    v_state_in = Ventil_schalten_einzeln("V1", v_state_soll["V1"]["state"], v_state_in)
    v_state_in = Ventil_schalten_einzeln("V2", v_state_soll["V2"]["state"], v_state_in)
    v_state_in = Ventil_schalten_einzeln("V3", v_state_soll["V3"]["state"], v_state_in)
    v_state_in = Ventil_schalten_einzeln("V4", v_state_soll["V4"]["state"], v_state_in)
    v_state_in = Ventil_schalten_einzeln("V5", v_state_soll["V5"]["state"], v_state_in)
    v_state_in = Ventil_schalten_einzeln("V6", v_state_soll["V6"]["state"], v_state_in)
    v_state_in = Ventil_schalten_einzeln("V7", v_state_soll["V7"]["state"], v_state_in)
    time.sleep(0.5)
    v_state_in = alle_aus(v_state_in)
    return v_state_in

def Ventiladressen(Ventil_name):
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
    # print(Ventil_name, ":\t", Ventilfunktion, "\tAdresse:\t", Adress)
    return (Adress)


def Ventil_schalten_einzeln(Ventil_name, Befehl_in, v_state, einzeln_deaktivieren=True):

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
    if (einzeln_deaktivieren == True):
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


v_state_soll_alle_zu = v_state_alle_zu()
v_state = v_state_init()
# print(v_state)
v_state = Ventile_schalten_ges(v_state_soll_alle_zu, v_state)
time.sleep(2)
print("\n\n\n Vierter Durchlauf")
v_state = Ventile_schalten_ges(v_state_soll_Volumen_evak_grob, v_state)
# print("\n\n\n Zweiter Durchlauf")
# v_state = Ventile_schalten_ges(v_state_soll_alle_auf, v_state)
# time.sleep(2)
# print("\n\n\n Dritter Durchlauf")
# v_state = Ventile_schalten_ges(v_state_soll_alle_zu, v_state)
# time.sleep(2)

print("\n\n\n Vierter Durchlauf")
v_state = Ventile_schalten_ges(v_state_soll_alle_zu, v_state)
print("\n\n\n Vierter Durchlauf")
v_state = Ventile_schalten_ges(v_state_soll_Volumen_evak_grob, v_state)
