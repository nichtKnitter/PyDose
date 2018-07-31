# Set up logging; The basic log level will be DEBUG
import logging
import time

import Messkarte
from transitions import Machine

logging.basicConfig(level=logging.DEBUG)
# Set transitions' log level to INFO; DEBUG messages will be omitted
Statemachinelogger = logging.getLogger('transitions').setLevel(logging.INFO)


### Loggin in Console Stoppen
# Statemachinelogger.disabled =True




class robotStateMachine(object):
    states = ['start_gereat', 'start_messung', 'start_cycle', 'segmentpruefung', 'messen', 'regelmoduspruefung',
              'regeln_langsam', 'regelnLangsamPropventil', 'warten', 'VentileAusschalten', 'messenCont']
    # segTime = 0
    # tacktzeit = 0

    MesskarteObj = Messkarte.Messkarte()

    # test ob karte funktioniert
    # MesskarteObj.Ventile_schalten_ges(MesskarteObj.vStateSollDoseFine)
    # time.sleep(1)
    # print("warten")
    # MesskarteObj.Ventile_schalten_ges(MesskarteObj.vStateSollEvakFine)
    # time.sleep(5)
    # print("warten")
    # MesskarteObj.Ventile_schalten_ges(MesskarteObj.vStateSollAlleZu)
    # MesskarteObj.Ventile_schalten_ges(MesskarteObj.vStateSollDegassEvaporator)
    # aktuellerModus = "vStateSollDegassEvaporator"
    # time.sleep(0.5)

    MesskarteObj.Ventile_schalten_ges(MesskarteObj.vStateSollAlleZu)
    aktuellerModus = "vStateSollAlleZu"

    def __init__(self, activeOnStart=False):

        self.isRunning = activeOnStart

        # aktueller Solldruck
        self.pSollMbar = 17
        # erlaubte regelabweichung
        self.maxDeltaPAllowedMbar = 0.1

        # couter für die punkte die beim warten geprintet werden
        self.num = 0

        # startzeit des aktuellen Segmentes
        self.segTime = time.time()

        # Taktzeit eines Kompletten Statemachinecycles, warten Cycle dauert so lang an bis das erfüllt ist
        self.startAktTackt = time.time()
        self.gereateTackt = 0.5
        self.messtaktCont = 0.1

        # Schnellmoegliche DAQ Befehl Sequenzen
        self.DAQminimumTakt = 0.01
        self.lastDAQAction = time.time()  # Verfolgt letzte Messkartenaktion, es ist wahrscheinlich eine minimale Pause erforderlich

        ## minimum Aktivzeit für Ventile ~ 0.35 s
        self.minimumValveOnTime = 0.5

        # Alle Kanaele auschalten
        self.MesskarteObj._alle_aus()

        self.lastDAQAction = time.time()  # Verfolgt letzte Messkartenaktion, es ist wahrscheinlich eine minimale Pause erforderlich
        self.anyValveOn = False  # verfolgt ob gerade ein Ventil an ist, zum uberpruefen ob man sie wieder ausschalten muss
        time.sleep(
            0.1)  # hier noch haendisch, wird spaeter über states geprueft ob letztes Messkartenereigniss lange genug her

        # Alle Ventile beim Starten zu:
        self.MesskarteObj.Ventile_schalten_ges(self.MesskarteObj.vStateSollAlleZu, shutOffAuto=True)
        self.aktuellerModus = "vStateSollAlleZu"
        self.lastDAQAction = time.time()
        self.anyValveOn = False

        # Initialize the state machine
        self.machine = Machine(model=self, states=robotStateMachine.states, initial='start_gereat', queued=True)
        self._initTransitions()

        self.messen()

    def _initTransitions(self):
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
            after=['printTransition', 'messen'],
            conditions=['testLastDAQAction']
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
            dest='regelnLangsamPropventil',
            trigger='tock',
            after=['printTransition', 'setPropStellgrad'],
            conditions=['testLastDAQAction']
        )
        self.machine.add_transition(  # regel 3
            source='regelnLangsamPropventil',
            dest='warten',
            trigger='tock',
            after=['printTransition']
        )
        ### aus Warten in Ventile Ausschalten und zurück
        self.machine.add_transition(  # muss vor transition zu start cycle gemacht werden, damit das höhere Pr
            source='warten',
            dest='VentileAusschalten',
            trigger='tock',
            after=['shutOffValves'],
            conditions=['hasToShutOffValve']
        )
        self.machine.add_transition(  # regel 3
            source='VentileAusschalten',
            dest='warten',
            trigger='tock'
        )

        self.machine.add_transition(  # hat hoehere Prio als messen?
            source='warten',
            dest='start_cycle',
            trigger='tock',
            conditions=['testTacktTimer', 'checkIfMachineIsRunning']
        )
        self.machine.add_transition(
            trigger='tock',
            source='warten',
            dest='messenCont',
            conditions=['TestMesstaktOver'],
            after='messen'
        )
        self.machine.add_transition(
            trigger='tock',
            source='messenCont',
            dest='warten'
        )

    def setSolldruck(self, solldruck):
        self.pSollMbar = solldruck

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

    def testLastDAQAction(self):
        if time.time() - self.lastDAQAction > self.DAQminimumTakt:
            result = True
        else:
            result = False
        return result

    def TestMesstaktOver(self):
        if time.time() - self.lastMeasurement > self.messtaktCont:
            ergebnis = True
        else:
            ergebnis = False
        return (ergebnis)

    def checkIfMachineIsRunning(self):
        return self.isRunning

    def printTransition(self):
        # print("state gewechselt zu:\t", self.state)
        pass


    def messen(self):
        self.MesskarteObj.readSensors()
        self.lastDAQAction = time.time()
        self.lastMeasurement = time.time()
        self.p1ProbeMbar = self.MesskarteObj.getP1ProbeMbar()
        self.p2ManifoldMbar = self.MesskarteObj.getP2ManifoldMbar()
        print(self.p1ProbeMbar, self.p2ManifoldMbar)
        print(self.MesskarteObj.getp2ManifoldArray())
        print(self.MesskarteObj.getp1ProbeArray())
        print(self.MesskarteObj.getTimearray())



    def regeln_langsam(self):
        print("Regeln langsam:\tp1=", "{0:0.2f}".format(self.p1ProbeMbar), "\tpsoll=", self.pSollMbar)
        if self.anyValveOn != True:  # nur schalten wenn gerade kein Ventil an ist
            if self.p1ProbeMbar < (self.pSollMbar - self.maxDeltaPAllowedMbar):
                print("V_Dose_Fine: nach oben")
                if self.aktuellerModus != "vStateSollDoseFine":  # nur wenn er es nicht eh schon macht
                    self.MesskarteObj.Ventile_schalten_ges(self.MesskarteObj.vStateSollDoseFine, False)
                    self.lastDAQAction = time.time()
                    self.aktuellerModus = "vStateSollDoseFine"
                    # Verfolgt wann die Ventile geschaltet wurden, um sie nach der richtigen Zeit wieder auszuschalten
                    self.lastValveActivation = time.time()
                    self.anyValveOn = True

            elif self.p1ProbeMbar > (self.pSollMbar + self.maxDeltaPAllowedMbar):
                print("V evac Fine: nach unten")
                if self.aktuellerModus != "vStateSollProbeEvakGrob":  # nur wenn er es nicht eh schon macht
                    self.MesskarteObj.Ventile_schalten_ges(self.MesskarteObj.vStateSollProbeEvakGrob, False)
                    self.lastDAQAction = time.time()
                    self.aktuellerModus = "vStateSollProbeEvakGrob"
                    # Verfolgt wann die Ventile geschaltet wurden, um sie nach der richtigen Zeit wieder auszuschalten
                    self.lastValveActivation = time.time()
                    self.anyValveOn = True
            else:
                if self.aktuellerModus != "vStateSollAlleZu":  # nur wenn er es nicht eh schon macht
                    self.MesskarteObj.Ventile_schalten_ges(self.MesskarteObj.vStateSollAlleZu, False)
                    print("Hold")
                    self.aktuellerModus = "vStateSollAlleZu"
                    # Verfolgt wann die Ventile geschaltet wurden, um sie nach der richtigen Zeit wieder auszuschalten
                    self.lastValveActivation = time.time()
                    self.anyValveOn = True

    def setPropStellgrad(self):
        self.MesskarteObj.v_Prop_Stellgrad(0)
        self.lastDAQAction = time.time()

    def hasToShutOffValve(self):
        # print(self.anyValveOn)
        # print(time.time()-self.lastDAQAction, self.DAQminimumTakt)
        # print (time.time()-self.lastValveActivation)
        # print(self.lastValveActivation)
        # print(time.time() - self.lastValveActivation)
        # print(self.minimumValveOnTime)
        if self.anyValveOn is True and (time.time() - self.lastValveActivation) > self.minimumValveOnTime:
            # time.time()-self.lastDAQAction > self.DAQminimumTakt and \
            result = True
        else:
            result = False
        return (result)

    def shutOffValves(self):
        self.MesskarteObj._alle_aus()
        self.lastDAQAction = time.time()
        self.anyValveOn = False


class globalRobot():
    # Initialisiert ein Statemachine Object von robotStateMachine,
    # und sendet dann in hoher Geschwindigkeit dieses
    localRobotStMachObj = robotStateMachine(activeOnStart=True)  # achtung! hier wird batman gleich wieder zerstört

    def run(self):
        time_total = time.time()
        while True:
            time.sleep(0.00001)
            self.localRobotStMachObj.tock()
            # if (time.time() - time_total > 150):
            #     break


if __name__ == '__main__':
    blubb = globalRobot()
    blubb.run()
