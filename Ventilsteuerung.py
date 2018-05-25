# altes nidaqmx beispiel für ventile

import pprint

import nidaqmx
from nidaqmx.constants import (LineGrouping)

pp = pprint.PrettyPrinter(indent=4)
import time


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


def Ventil_schalten(Ventilname, Befehl):
    Ventil_auf = [True, False]
    Ventil_zu = [False, True]
    Ventil_aus = [True, True]
    Ventiladresse = Ventiladressen(Ventilname)
    if (Befehl == "auf"):
        Befehl = Ventil_auf
    if (Befehl == "zu"):
        Befehl = Ventil_zu
    if (Befehl == "aus"):
        Befehl = Ventil_aus
    print("Befehl", Befehl)
    with nidaqmx.Task() as VentilTask:
        print(Ventilname, Befehl)
        VentilTask.do_channels.add_do_chan(Ventiladresse,
                                           line_grouping=LineGrouping.CHAN_PER_LINE)
        try:
            print(VentilTask.write(Befehl))  # beide kanäle an, wird nie gebaucht
        except nidaqmx.DaqError as e:
            print(e)
        time.sleep(0.5)
        try:
            print(VentilTask.write(Ventil_aus))  # beide kanäle an, wird nie gebaucht
        except nidaqmx.DaqError as e:
            print(e)


def alle_aus():
    Ventil_schalten("V1", "aus")
    Ventil_schalten("V2", "aus")
    Ventil_schalten("V3", "aus")
    Ventil_schalten("V4", "aus")
    Ventil_schalten("V5", "aus")
    Ventil_schalten("V6", "aus")
    Ventil_schalten("V7", "aus")


def alle_auf():
    Ventil_schalten("V1", "auf")
    Ventil_schalten("V2", "auf")
    Ventil_schalten("V3", "auf")
    Ventil_schalten("V4", "auf")
    Ventil_schalten("V5", "auf")
    Ventil_schalten("V6", "auf")
    Ventil_schalten("V7", "auf")


def Volumen_evak_grob():
    Ventil_schalten("V1", "auf")
    Ventil_schalten("V4", "auf")
    Ventil_schalten("V7", "auf")
    Ventil_schalten("V2", "zu")
    Ventil_schalten("V3", "zu")
    Ventil_schalten("V5", "zu")
    Ventil_schalten("V6", "zu")


# Volumen_evak_grob()
alle_auf()
