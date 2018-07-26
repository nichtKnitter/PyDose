# Set up logging; The basic log level will be DEBUG
import logging
import time

import Messkarte
from transitions import Machine

logging.basicConfig(level=logging.DEBUG)
# Set transitions' log level to INFO; DEBUG messages will be omitted
Statemachinelogger = logging.getLogger('transitions').setLevel(logging.CRITICAL)


### Loggin in Console Stoppen
# Statemachinelogger.disabled =True

# # Create the Handler for logging data to a file
# logger_handler = logging.FileHandler('python_logging.log')
# logger_handler.setLevel(logging.INFO)
# # Add the Handler to the Logger
# self.Messkartenlogger.addHandler(logger_handler)

class VDummyKlasse(object):
    def schalten1(self):
        print("Geschaltet 1")

    def schalten2(self):
        print("Geschaltet 2")

    def say_hello(self): print("hello, new state!")

    def say_goodbye(self): print("goodbye, old state!")


class robotStateMachine(object):
    states = ['start_gereat', 'start_messung', 'start_cycle', 'segmentpruefung', 'messen', 'regelmoduspruefung',
              'regeln_langsam', 'warten']
    # segTime = 0
    # tacktzeit = 0
    MesskarteOld = VDummyKlasse()

    MesskarteObj = Messkarte.Messkarte()

    # test ob karte funktioniert
    # MesskarteObj.Ventile_schalten_ges(MesskarteObj.vStateSollDoseFine)
    # time.sleep(1)
    # print("warten")
    # MesskarteObj.Ventile_schalten_ges(MesskarteObj.vStateSollEvakFine)
    # time.sleep(5)
    # print("warten")
    # MesskarteObj.Ventile_schalten_ges(MesskarteObj.vStateSollAlleZu)
    MesskarteObj.Ventile_schalten_ges(MesskarteObj.vStateSollDegassEvaporator)
    aktuellerModus = "vStateSollDegassEvaporator"
    time.sleep(5)
    MesskarteObj.Ventile_schalten_ges(MesskarteObj.vStateSollAlleZu)
    aktuellerModus = "vStateSollAlleZu"

    def __init__(self, startparameter1):

        self.name = startparameter1

        # aktueller Solldruck
        self.pSollMbar = 30

        # couter für die punkte die beim warten geprintet werden
        self.num = 0

        # startzeit des aktuellen Segmentes
        self.segTime = time.time()

        # Taktzeit
        self.gereateTackt = 0.1
        self.startAktTackt = time.time()

        # Alle Ventile beim Starten zu:
        self.MesskarteObj.Ventile_schalten_ges(self.MesskarteObj.vStateSollAlleZu)
        self.aktuellerModus = "vStateSollAlleZu"

        # Initialize the state machine
        self.machine = Machine(model=self, states=robotStateMachine.states, initial='start_gereat', queued=True)

        self.machine.add_transition(  # regel 1
            source='start_gereat',
            dest='start_messung',
            trigger='tock',
            after=['printTransition']
        )
        self.machine.add_transition(  # regel 2
            source='start_messung',
            dest='start_cycle',
            trigger='tock',
            after=['printTransition']
            # ,            conditions=[self.testTimeisUp]
        )
        self.machine.add_transition(  # regel 2
            source='start_cycle',
            dest='segmentpruefung',
            trigger='tock',
            after=['printTransition', 'resetTacktTimer']
        )
        self.machine.add_transition(  # regel 3
            source='segmentpruefung',
            dest='messen',
            trigger='tock',
            after=['printTransition', 'messen']
        )
        self.machine.add_transition(  # regel 3
            source='messen',
            dest='regelmoduspruefung',
            trigger='tock',
            after=['printTransition']
            # ,            conditions=[self.testTimeisUp]
        )
        self.machine.add_transition(  # regel 3
            source='regelmoduspruefung',
            dest='regeln_langsam',
            trigger='tock',
            after=['printTransition', 'regeln_langsam']
        )
        self.machine.add_transition(  # regel 3
            source='regeln_langsam',
            dest='warten',
            trigger='tock',
            after=['printTransition']
        )
        self.machine.add_transition(  # regel 3
            source='warten',
            dest='start_cycle',
            trigger='tock',
            after=['printTransition'],
            conditions=[self.testTacktTimer]
        )

    def resetTacktTimer(self):
        self.startAktTackt = time.time()
        # print ('nextState')
        # self.tock()
    def testTacktTimer(self):
        self.num = self.num + 1
        if self.num == 10:
            print('.', end='', flush=True)
            self.num = 0
        # result = True if  else False
        if (time.time() - self.startAktTackt >= self.gereateTackt):
            result = True
            print()
        else:
            result = False

        return result



    def printTransition(self):
        # print("state gewechselt zu:\t", self.state)
        pass

    def VentileSchalten(self):
        self.MesskarteOld.schalten1()

    def messen(self):
        print('messen')
        data = self.MesskarteObj.readSensors()
        # self.p1ProbeMbar = data[0]
        # self.p2ManifoldMbar = data[1]
        self.p1ProbeMbar = self.MesskarteObj.getP1ProbeMbar()
        self.p2ManifoldMbar = self.MesskarteObj.getP2ManifoldMbar()


    def regeln_langsam(self):
        print("Regeln langsam:\tp1=", self.p1ProbeMbar, "\tpsoll=", self.pSollMbar)

        if self.p1ProbeMbar < self.pSollMbar:
            if self.aktuellerModus != "vStateSollDoseFine":
                self.MesskarteObj.v_Prop_Stellgrad(1)
                self.MesskarteObj.Ventile_schalten_ges(self.MesskarteObj.vStateSollDoseFine)
                print("V_Dose_Fine")
                self.aktuellerModus = "vStateSollDoseFine"
        elif self.p1ProbeMbar > self.pSollMbar:
            # if self.aktuellerModus != "vStateSollEvakFine":
            #     self.MesskarteObj.Ventile_schalten_ges(self.MesskarteObj.vStateSollEvakFine)
            #     print("V evac Fine")
            #     self.aktuellerModus = "vStateSollEvakFine"

            if self.aktuellerModus != "vStateSollProbeEvakGrob":
                self.MesskarteObj.v_Prop_Stellgrad(1)
                self.MesskarteObj.Ventile_schalten_ges(self.MesskarteObj.vStateSollProbeEvakGrob)
                print("V evac Fine")
                self.aktuellerModus = "vStateSollProbeEvakGrob"
        else:
            if self.aktuellerModus != "vStateSollAlleZu":
                self.MesskarteObj.Ventile_schalten_ges(self.MesskarteObj.vStateSollAlleZu)
                print("Hold")
                self.aktuellerModus = "vStateSollAlleZu"






class globalRobot():
    # Initialisiert ein Statemachine Object von robotStateMachine,
    # und sendet dann in hoher Geschwindigkeit dieses
    localRobotStMachObj = robotStateMachine("Batman")  # achtung! hier wird batman gleich wieder zerstört

    def run(self):
        time_total = time.time()
        while True:
            time.sleep(0.00001)
            self.localRobotStMachObj.tock()
            # if (time.time() - time_total > 150):
            #     break


blubb = globalRobot()
blubb.run()
