# altes nidaqmx beispiel für ventile

import pprint

import nidaqmx
from nidaqmx.constants import (LineGrouping)

pp = pprint.PrettyPrinter(indent=4)
import time

# State dictionary, um nur notwendige Venitle zu schalten
v_state = [
    {"id": "V1", "state": "NA", "active": "NA"},
    {"id": "V2", "state": "NA", "active": "NA"},
    {"id": "V3", "state": "NA", "active": "NA"},
    {"id": "V4", "state": "NA", "active": "NA"},
    {"id": "V5", "state": "NA", "active": "NA"},
    {"id": "V6", "state": "NA", "active": "NA"},
    {"id": "V7", "state": "NA", "active": "NA"},
]



def Ventiladressen(Ventilname):
    if (Ventilname == "V1"):
        Adress = 'Dev1/port2/line0:1'
        Ventilfunktion = "Pumpe"
    if (Ventilname == "V2"):
        Adress = 'Dev1/port2/line2:3'
        Ventilfunktion = "Vent"
    if (Ventilname == "V3"):
        Adress = 'Dev1/port2/line4:5'
        Ventilfunktion = "Verdampfer"
    if (Ventilname == "V4"):
        Adress = 'Dev1/port1/line0:1'
        Ventilfunktion = "Bypass1"
    if (Ventilname == "V5"):
        Adress = 'Dev1/port1/line2:3'
        Ventilfunktion = "Bypass2"
    if (Ventilname == "V6"):
        Adress = 'Dev1/port1/line4:5'
        Ventilfunktion = "Messzelle"
    if (Ventilname == "V7"):
        Adress = 'Dev1/port1/line6:7'
        Ventilfunktion = "Volumen"
    print(Ventilname, ":\t", Ventilfunktion, "\tAdresse:\t", Adress)
    return (Adress)


def Ventil_schalten(Ventilname, Befehl_in, v_state):
    print("ventilname in Ventil schalten", Ventilname)
    Ventil_auf = [True, False]
    Ventil_zu = [False, True]
    Ventil_aus = [True, True]
    Ventiladresse = Ventiladressen(Ventilname)
    if (Befehl_in == "auf"):
        Befehl = Ventil_auf
    if (Befehl_in == "zu"):
        Befehl = Ventil_zu
    if (Befehl_in == "aus"):
        Befehl = Ventil_aus
    print("Befehl", Befehl)
    with nidaqmx.Task() as VentilTask:
        print(Ventilname, Befehl)
        VentilTask.do_channels.add_do_chan(Ventiladresse, line_grouping=LineGrouping.CHAN_PER_LINE)
        try:
            (VentilTask.write(Befehl))  # beide kanäle an, wird nie gebaucht
            v_state["id" == Ventilname]["active"] = True
            v_state["id" == Ventilname]["state"] = Befehl_in
            print("in Ventil.task", v_state["id" == Ventilname])
        except nidaqmx.DaqError as e:
            print(e)

        time.sleep(0.5)

        try:
            (VentilTask.write(Ventil_aus))  # beide kanäle an, wird nie gebaucht
            v_state["id" == Ventilname]["active"] = False
            v_state["id" == Ventilname]["state"] = "aus"
            print("in Ventil.task", v_state["id" == Ventilname])
        except nidaqmx.DaqError as e:
            print(e)
    print("in ventil schlaten", v_state)
    return (v_state)


def alle_aus():
    Ventil_schalten("V1", "aus")
    Ventil_schalten("V2", "aus")
    Ventil_schalten("V3", "aus")
    Ventil_schalten("V4", "aus")
    Ventil_schalten("V5", "aus")
    Ventil_schalten("V6", "aus")
    Ventil_schalten("V7", "aus")


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
    Ventil_schalten("V1", "auf")
    Ventil_schalten("V4", "auf")
    Ventil_schalten("V7", "auf")
    Ventil_schalten("V2", "zu")
    Ventil_schalten("V3", "zu")
    Ventil_schalten("V5", "zu")
    Ventil_schalten("V6", "zu")


# Volumen_evak_grob()
v_state = alle_auf(v_state)
print(v_state)
