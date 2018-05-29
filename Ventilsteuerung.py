# altes nidaqmx beispiel für ventile

import pprint

import nidaqmx
from nidaqmx.constants import (LineGrouping)

pp = pprint.PrettyPrinter(indent=4)
import time

# State dictionary, um nur notwendige Venitle zu schalten
# v_state = [
#     {"id": 1, "state": "NA", "active": "NA"},
#     {"id": 2, "state": "NA", "active": "NA"},
#     {"id": 3, "state": "NA", "active": "NA"},
#     {"id": 4, "state": "NA", "active": "NA"},
#     {"id": 5, "state": "NA", "active": "NA"},
#     {"id": 6, "state": "NA", "active": "NA"},
#     {"id": 7, "state": "NA", "active": "NA"},
# ]


v_state = {}
v_state["V1"] = {"id": 1, "state": "NA", "active": "NA"}
v_state["V2"] = {"id": 2, "state": "NA", "active": "NA"}
v_state["V3"] = {"id": 3, "state": "NA", "active": "NA"}
v_state["V4"] = {"id": 4, "state": "NA", "active": "NA"}
v_state["V5"] = {"id": 5, "state": "NA", "active": "NA"}
v_state["V6"] = {"id": 6, "state": "NA", "active": "NA"}
v_state["V7"] = {"id": 7, "state": "NA", "active": "NA"}


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
    print(Ventil_name, ":\t", Ventilfunktion, "\tAdresse:\t", Adress)
    return (Adress)


def Ventil_schalten(Ventil_name, Befehl_in, v_state):
    print("ventilid in Ventil schalten", Ventil_name)
    time.sleep(0.5)
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
    print("Befehl_in:\t", Befehl_in, "\tBefehl:\t", Befehl)
    with nidaqmx.Task() as VentilTask:
        # VentilTask = nidaqmx.Task() #nur für debugzwecke
        # print(Ventil_id, Befehl)
        VentilTask.do_channels.add_do_chan(Ventiladresse, line_grouping=LineGrouping.CHAN_PER_LINE)
        try:
            (VentilTask.write(Befehl))
            v_state[Ventil_name]["active"] = True
            v_state[Ventil_name]["state"] = Befehl_in
            print("in Ventil.task", v_state[Ventil_name])
        except nidaqmx.DaqError as e:
            print(e)

        time.sleep(0.5)

        try:
            (VentilTask.write(Ventil_aus))  # beide kanäle an, wird nie gebaucht
            v_state[Ventil_name]["active"] = False
            v_state[Ventil_name]["state"] = "aus"
            print("in Ventil.task", v_state[Ventil_name])
        except nidaqmx.DaqError as e:
            print(e)
    print("in ventil schalten", v_state)
    return (v_state)


def alle_aus():
    Ventil_schalten(1, "aus")
    Ventil_schalten(2, "aus")
    Ventil_schalten(3, "aus")
    Ventil_schalten(4, "aus")
    Ventil_schalten(5, "aus")
    Ventil_schalten(6, "aus")
    Ventil_schalten(7, "aus")


def alle_auf(v_state):
    v_state = Ventil_schalten("V1", "auf", v_state)
    print("in alle_auf", v_state)
    v_state = Ventil_schalten("V2", "auf", v_state)
    print("in alle_auf", v_state)
    v_state = Ventil_schalten("V3", "auf", v_state)
    print("in alle_auf", v_state)
    v_state = Ventil_schalten("V4", "auf", v_state)
    print("in alle_auf", v_state)
    v_state = Ventil_schalten("V5", "auf", v_state)
    print("in alle_auf", v_state)
    v_state = Ventil_schalten("V6", "auf", v_state)
    print("in alle_auf", v_state)
    v_state = Ventil_schalten("V7", "auf", v_state)
    print("in alle_auf", v_state)
    return (v_state)


def Volumen_evak_grob():
    Ventil_schalten(1, "auf")
    Ventil_schalten(4, "auf")
    Ventil_schalten(7, "auf")
    Ventil_schalten(2, "zu")
    Ventil_schalten(3, "zu")
    Ventil_schalten(5, "zu")
    Ventil_schalten(6, "zu")


# Volumen_evak_grob()
Ventil_schalten(Ventil_name="V3", Befehl_in="auf", v_state=v_state)
v_state = alle_auf(v_state)
print(v_state)
