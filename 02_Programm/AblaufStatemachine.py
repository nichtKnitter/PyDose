# Set up logging; The basic log level will be DEBUG
import logging
import time

import Messkarte
from transitions import Machine

logging.basicConfig(level=logging.DEBUG)
# Set transitions' log level to INFO; DEBUG messages will be omitted
Statemachinelogger = logging.getLogger('transitions').setLevel(logging.INFO)


### Loggin in Console Stoppen




class robotStateMachine(object):
    states = ['start_gereat', 'start_messung', 'start_cycle', 'segmentpruefung', 'messen', 'regelmoduspruefung',
              'regeln_langsam', 'regelnLangsamPropventil', 'warten', 'VentileAusschalten', 'messenCont', 'UserInput']
    # segTime = 0
    # tacktzeit = 0

    MesskarteObj = Messkarte.Messkarte(timeBetweenValveActions=0.001, isDebugDummyMode=True)

    def __init__(self, activeOnStart=False):

        # Taktzeit eines Kompletten Statemachinecycles, warten Cycle dauert so lang an bis das erfüllt ist
        self.startAktTackt = time.time()
        self.gereateTackt = 0.002
        self.messtaktCont = 0.001

        # Schnellmoegliche DAQ Befehl Sequenzen
        self.DAQminimumTakt = 0.001
        self.lastDAQAction = time.time()  # Verfolgt letzte Messkartenaktion, es ist wahrscheinlich eine minimale Pause erforderlich

        ## minimum Aktivzeit für Ventile ~ 0.35 s
        self.minimumValveOnTime = 0.5

        self.userCommandManual = 'NA'
        self.newUserCommand = False

        self.isRunning = activeOnStart

        # aktueller Solldruck
        self.pSollMbar = 35
        # erlaubte regelabweichung
        self.maxDeltaPAllowedMbar = 0.2

        # initialer Stellgrad de Proportionalventils
        self.StellgradProzent = 20
        self.lastStellgrad = self.StellgradProzent  # zum überprüfen og geschaltet werden muss

        # couter für die punkte die beim warten geprintet werden
        self.num = 0
        self.numZeilenumbruch = 0

        # TODO:
        # startzeit des aktuellen Segmentes
        self.segTime = time.time()





        # Alle Kanaele auschalten
        self.MesskarteObj.Ventile_schalten_ges(self.MesskarteObj.vStateSollAlleZu)
        self.valveActivationTracker()

        self.vState = self.MesskarteObj.getVState()  # states vorsorgich mal aktualisieren
        self.aktuellerModus = self.vState['State']['Name']


        # self.lastDAQAction = time.time()  # Verfolgt letzte Messkartenaktion, es ist wahrscheinlich eine minimale Pause erforderlich
        # self.anyValveOn = False  # verfolgt ob gerade ein Ventil an ist, zum uberpruefen ob man sie wieder ausschalten muss
        # time.sleep(
        #     0.1)  # hier noch haendisch, wird spaeter über states geprueft ob letztes Messkartenereigniss lange genug her

        # Alle Ventile beim Starten zu:
        # self.MesskarteObj.Ventile_schalten_ges(self.MesskarteObj.vStateSollAlleZu, shutOffAuto=True)


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
            after=['resetTacktTimer']
        )
        self.machine.add_transition(  # regel 3
            source='segmentpruefung',
            dest='messen',
            trigger='tock',
            after=['messen'],
            conditions=['testLastDAQAction']
        )
        self.machine.add_transition(  # regel 3
            source='messen',
            dest='regelmoduspruefung',
            trigger='tock'
        )
        self.machine.add_transition(  # regel 3
            source='regelmoduspruefung',
            dest='regeln_langsam',
            trigger='tock',
            after=['regeln_langsam'],
            conditions=['testLastDAQAction']
        )
        self.machine.add_transition(  # regel 3
            source='regeln_langsam',
            dest='regelnLangsamPropventil',
            trigger='tock',
            after=['setPropStellgrad'],
            conditions=['testLastDAQAction']
        )
        self.machine.add_transition(  # regel 3
            source='regelnLangsamPropventil',
            dest='warten',
            trigger='tock'
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
        self.machine.add_transition(
            trigger='tock',
            source='warten',
            dest='UserInput',
            conditions=['testUserInput', 'testLastDAQAction'],
            after='doUserInput'
        )
        self.machine.add_transition(
            trigger='tock',
            source='UserInput',
            dest='warten'
        )

        self.machine.add_transition(  # hat hoehere Prio als messen?
            source='warten',
            dest='start_cycle',
            trigger='tock',
            conditions=['testRegelTacktTimer', 'checkIfMachineIsRunning']
        )
        self.machine.add_transition(
            trigger='tock',
            source='warten',
            dest='messenCont',
            conditions=['TestMesstaktOver', 'testLastDAQAction'],
            after='messen'
        )
        self.machine.add_transition(
            trigger='tock',
            source='messenCont',
            dest='warten'
        )

    def getVState(self):
        return self.MesskarteObj.getVState()

    def getIsRunning(self):
        return self.isRunning

    def setIsRunning(self, Befehl=True):
        self.isRunning = Befehl

    def setSolldruck(self, solldruck):
        self.pSollMbar = solldruck

    def resetTacktTimer(self):
        self.startAktTackt = time.time()
        # print ('nextState')
        # self.tock()

    def testRegelTacktTimer(self):
        self.num = self.num + 1

        if self.num == 100:
            print('.', end='', flush=True)
            self.num = 0
            self.numZeilenumbruch += 1
        if self.numZeilenumbruch == 80:
            self.numZeilenumbruch = 0
            print('.', flush=True)
        if (time.time() - self.startAktTackt >= self.gereateTackt):
            result = True
            # print()
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
        # print(self.isRunning)
        return self.isRunning

    def printTransition(self):
        # print("state gewechselt zu:\t", self.state)
        pass

    def testUserInput(self):
        return self.newUserCommand

    def setUserCommand(self, Befehl):
        print('new user command accepted')
        self.userCommandManual = Befehl
        self.newUserCommand = True
        print(self.userCommandManual, self.newUserCommand)

    def doUserInput(self):
        print('doUserInput')
        self.vState = self.MesskarteObj.getVState()  # states vorsorgich mal aktualisieren

        if self.userCommandManual == 'evacSample':
            print('try to evac manually')
            self.MesskarteObj.Ventile_schalten_ges(
                self.MesskarteObj.vStateSollProbeEvakGrob, False)

        if self.userCommandManual == 'alleAuf':
            self.MesskarteObj.Ventile_schalten_ges(
                self.MesskarteObj.vStateSollAlleAuf, False)

        if self.userCommandManual == 'AlleZu':
            self.MesskarteObj.Ventile_schalten_ges(
                self.MesskarteObj.vStateSollAlleZu, False)

        if self.userCommandManual == 'EvakFine':
            self.MesskarteObj.Ventile_schalten_ges(
                self.MesskarteObj.vStateSollEvakFine, False)

        if self.userCommandManual == 'DegassEvaporator':
            self.MesskarteObj.Ventile_schalten_ges(
                self.MesskarteObj.vStateSollDegassEvaporator, False)

        if self.userCommandManual == 'V1':
            print("Toggle V1")
            if self.vState['V1']['state'] == 'zu':
                self.MesskarteObj.Ventil_schalten_einzeln(Ventil_name="V1", Befehl_in="auf", einzeln_deaktivieren=False)
            else:
                self.MesskarteObj.Ventil_schalten_einzeln(Ventil_name="V1", Befehl_in="zu", einzeln_deaktivieren=False)

        if self.userCommandManual == 'V2':
            print("Toggle V2")
            if self.vState['V2']['state'] == 'zu':
                self.MesskarteObj.Ventil_schalten_einzeln(Ventil_name="V2", Befehl_in="auf", einzeln_deaktivieren=False)
            else:
                self.MesskarteObj.Ventil_schalten_einzeln(Ventil_name="V2", Befehl_in="zu", einzeln_deaktivieren=False)

        if self.userCommandManual == 'V3':
            print("Toggle V3")
            if self.vState['V3']['state'] == 'zu':
                self.MesskarteObj.Ventil_schalten_einzeln(Ventil_name="V3", Befehl_in="auf", einzeln_deaktivieren=False)
            else:
                self.MesskarteObj.Ventil_schalten_einzeln(Ventil_name="V3", Befehl_in="zu", einzeln_deaktivieren=False)

        if self.userCommandManual == 'V4':
            print("Toggle V4")
            if self.vState['V4']['state'] == 'zu':
                self.MesskarteObj.Ventil_schalten_einzeln(Ventil_name="V4", Befehl_in="auf", einzeln_deaktivieren=False)
            else:
                self.MesskarteObj.Ventil_schalten_einzeln(Ventil_name="V4", Befehl_in="zu", einzeln_deaktivieren=False)

        if self.userCommandManual == 'V5':
            print("Toggle V5")
            if self.vState['V5']['state'] == 'zu':
                self.MesskarteObj.Ventil_schalten_einzeln(Ventil_name="V5", Befehl_in="auf", einzeln_deaktivieren=False)
            else:
                self.MesskarteObj.Ventil_schalten_einzeln(Ventil_name="V5", Befehl_in="zu", einzeln_deaktivieren=False)

        if self.userCommandManual == 'V6':
            print("Toggle V6")
            if self.vState['V6']['state'] == 'zu':
                self.MesskarteObj.Ventil_schalten_einzeln(Ventil_name="V6", Befehl_in="auf", einzeln_deaktivieren=False)
            else:
                self.MesskarteObj.Ventil_schalten_einzeln(Ventil_name="V6", Befehl_in="zu", einzeln_deaktivieren=False)

        if self.userCommandManual == 'V7':
            print("Toggle V7")
            if self.vState['V7']['state'] == 'zu':
                self.MesskarteObj.Ventil_schalten_einzeln(Ventil_name="V7", Befehl_in="auf", einzeln_deaktivieren=False)
            else:
                self.MesskarteObj.Ventil_schalten_einzeln(Ventil_name="V7", Befehl_in="zu", einzeln_deaktivieren=False)

        if self.userCommandManual == 'VProp':
            print("Toggle VProp")
            if self.vState["V_Prop"]["state"] == 'an':
                self.MesskarteObj.vPropAnAus('aus')
            else:
                self.MesskarteObj.vPropAnAus('an')

        if self.userCommandManual == 'VPropStellgrad':
            print("Toggle VPropStellgrad")
            if self.vState["V_Prop"]["stellgrad"] >= 50:
                self.setPropStellgrad(0)
                # self.MesskarteObj.v_Prop_Stellgrad(0)
            else:
                self.setPropStellgrad(100)
                # self.MesskarteObj.v_Prop_Stellgrad(100)
        #
        # auf jedenfall wieder freigeben, egal was befohlen wurde
        self.newUserCommand = False
        self.valveActivationTracker()

    def valveActivationTracker(self):
        print("try tracking valves")
        self.lastDAQAction = time.time()
        self.lastValveActivation = time.time()
        self.anyValveOn = True
        self.vState = self.MesskarteObj.getVState()
        self.aktuellerModus = self.vState['State']['Name']

    def messen(self):
        self.MesskarteObj.readSensors()
        self.lastDAQAction = time.time()
        self.lastMeasurement = time.time()
        self.p1ManifoldMbar = self.MesskarteObj.getP1ManifoldMbar()
        self.p2ProbeMbar = self.MesskarteObj.getP2ProbeMbar()
        # print('test', self.p1ProbeMbar, self.p2ManifoldMbar)
        # print(self.MesskarteObj.getp2ManifoldArray())
        # print(self.MesskarteObj.getp1ProbeArray())
        # print(self.MesskarteObj.getTimearray())



    def regeln_langsam(self):

        print("Regeln langsam:\tp1=", "{0:0.2f}".format(self.p2ProbeMbar), "\tpsoll=", self.pSollMbar, "\tself.aktuellerModus", self.aktuellerModus)
        print(self.StellgradProzent)
        if self.anyValveOn != True:  # nur schalten wenn gerade kein Ventil an ist
            # print("Kein Ventil a")
            ## wenn kleine als psoll und kommt aus modus alle zu, sonst mach alle zu
            if self.p2ProbeMbar < (self.pSollMbar - self.maxDeltaPAllowedMbar):
                if self.aktuellerModus != "vStateSollDoseFine":
                    print("V_Dose_Fine: nach oben")
                    self.MesskarteObj.Ventile_schalten_ges(self.MesskarteObj.vStateSollDoseFine, False)
                    self.valveActivationTracker()

                    self.StellgradProzent = 25
                    print(self.StellgradProzent)

            elif self.p2ProbeMbar > (self.pSollMbar + self.maxDeltaPAllowedMbar):
                if self.aktuellerModus != "vStateSollEvakFine":
                    print("V evac Fine: nach unten")
                    self.MesskarteObj.Ventile_schalten_ges(self.MesskarteObj.vStateSollEvakFine, False)
                    self.valveActivationTracker()
                    self.StellgradProzent = 35
                    print(self.StellgradProzent)

            else:
                if self.aktuellerModus != "vStateSollAlleZu":  # nur wenn er es nicht eh schon macht
                    print("Hold")
                    self.MesskarteObj.Ventile_schalten_ges(self.MesskarteObj.vStateSollAlleZu, False)
                    self.valveActivationTracker()
                    print(self.StellgradProzent)

    def setPropStellgrad(self):
        if self.lastStellgrad != self.StellgradProzent:
            self.MesskarteObj.v_Prop_Stellgrad(self.StellgradProzent)
            self.lastStellgrad = self.StellgradProzent
            print(self.StellgradProzent)
            self.lastDAQAction = time.time()

    def hasToShutOffValve(self):
        # Überprüft ob ein Ventil an ist und die festgelegt minimumaktivierungszeit vorbei ist
        if self.anyValveOn is True and (time.time() - self.lastValveActivation) > self.minimumValveOnTime:
            result = True
        else:
            result = False
        return result

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
    # blubb.run()
