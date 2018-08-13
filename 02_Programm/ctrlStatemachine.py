import transitions
# Set up logging; The basic log level will be DEBUG
import logging
import time

import Messkarte
from transitions import Machine

logging.basicConfig(level=logging.DEBUG)
# Set transitions' log level to INFO; DEBUG messages will be omitted
Statemachinelogger = logging.getLogger('transitions').setLevel(logging.INFO)


# states = ['start_gereat', 'start_messung', 'start_cycle', 'segmentpruefung', 'messen', 'regelmoduspruefung',
#           'regeln_langsam', 'regelnLangsamPropventil', 'warten', 'VentileAusschalten', 'messenCont', 'UserInput']

class ctrlStatemachine(object):
    MesskarteObj = Messkarte.Messkarte(timeBetweenValveActions=0.001, isDebugDummyMode=False)

    states = [
              # wenn nicht an:
              'wait',

                    'messenCont',
                    'UserInput',



                  # wenn messung läuft
                  'start_cycle'
                  
                  # pro zyklus messen
                  'messen',

                  # wenn segment noch nicht vorbei, sonst seg += 1 und zurück zu wait
                  'segmentpruefung',



                  # wenn neuer regelmudus
                  'regelmoduspruefung',
                      # wenn modus = cont
                      'cmpPID',
                      'setProp',
                        ## def ventile schalten
                              # wenn cont + zu hoch + istState = wait:
                              'evac_1propOff',  'evac_StartProp',
                              # wenn cont + zu hoch + istState = evac
                               'ControlWait', 'ControlWaitShutOffRelais',

                              # wenn cont + zu niedrig + istState = wait
                              'dose_1propOff',  'dose_3StartProp',
                            # wenn cont + zu niedrig + istState = dose
                            'ControlWait', 'ControlWaitShutOffRelais',

                            # wenn cont + psoll = pist + iststate != halten
                            'ControlWait', 'ControlWaitShutOffRelais',

    ]

    def __init__(self):

        self.anyValveOn = self.MesskarteObj.getIsAnyValveOn()
        self.minimumValveOnTime = self.MesskarteObj.minimumValveOnTime
        self.lastValveActivation = self.MesskarteObj.lastValveActivation

        # self.machine = Machine(model=self, states=robotStateMachine.states, initial='start_gereat', queued=True)
        self.machine = Machine(model=self, states=ctrlStatemachine.states, initial='wait', queued=True)

        ### transitionen aus wait heraus, geordnet nach prio:
        # 1. wenn ein ventil schon lange genug an
        self.machine.add_transition('tick', source='wait', dest='wait',
                                    conditions='hasToShutOffValve', after='shutOffValves')
        # 2. user input geht vor messung
        self.machine.add_transition('tick', source='wait', dest='wait',
                                    conditions='testUserInput', after='doUserInput')
        # 3. wenn automatikmode = an
        self.machine.add_transition('tick', source='wait', dest='start_cycle',
                                    conditions=['checkControlClock', 'checkIfMachineIsRunning'])
        # 4. wenn nichts zu tun messen
        self.machine.add_transition('tick', source='wait', dest='wait',
                                    conditions='checkMeasuringClock', after='messen')

        ## ablauf Messcycle
        # messen
        self.machine.add_transition('tick', source='start_cycle', dest='messen')
        self.machine.add_transition('tick', source='messen', dest='segmentpruefung', after='messen')

        self.machine.add_transition('tick', source='segmentpruefung', dest='wait',
                                    conditions='isSegmentOver', after='setNewSegment')
        self.machine.add_transition('tick', source='segmentpruefung', dest='regelmoduspruefung',
                                    unless='isSegmentOver')
        self.machine.add_transition('tick', source='regelmoduspruefung', dest='cmpPID', conditions='isCtrContinuous')
        self.machine.add_transition('tick', source='cmpPID', dest='setProp', after='ComPID')

        self.machine.add_transition('tick', source='setProp', dest='VentileSchalten', after='setPropSetpoint')

        self.machine.add_transition('tick', source='VentileSchalten', dest='evac_1propOff')
        self.machine.add_transition('tick', source='VentileSchalten', dest='ControlWait')
        self.machine.add_transition('tick', source='VentileSchalten', dest='dose_1propOff')

    def hasToShutOffValve(self):
        # Überprüft ob ein Ventil an ist und die festgelegt minimumaktivierungszeit vorbei ist
        self.anyValveOn = self.MesskarteObj.getIsAnyValveOn()
        self.lastValveActivation = self.MesskarteObj.lastValveActivation

        if self.anyValveOn is True and (time.time() - self.lastValveActivation) > self.minimumValveOnTime:
            result = True
        else:
            result = False
        return result

