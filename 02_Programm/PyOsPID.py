# coding=utf-8
"""
# Port of the OS-PID Library to Python by Max Baumgartner, baumax@posteo.de
# Original header File:
# /**********************************************************************************************
#  * Arduino PID Library - Version 1.0.1
#  * by Brett Beauregard <br3ttb@gmail.com> brettbeauregard.com
#  *
#  * This Library is licensed under a GPLv3 License
#  **********************************************************************************************/
"""

import time

"""
/*Constructor (...)*********************************************************
* The parameters specified here are those for for which we can't set up
* reliable defaults, so we need to have the user set them.
***************************************************************************/
PID::PID(double* Input, double* Output, double* Setpoint,
        double Kp, double Ki, double Kd, int ControllerDirection)
{
PID::SetOutputLimits(0, 255); //default output limit corresponds to
//the arduino pwm limits

    SampleTime = 100; //default Controller Sample Time is 0.1 seconds

    PID::SetControllerDirection(ControllerDirection);
    PID::SetTunings(Kp, Ki, Kd);

    lastTime = millis()-SampleTime;
    inAuto = false;
    myOutput = Output;
    myInput = Input;
    mySetpoint = Setpoint;

}
"""


class OsPI():
    """
    Eigener differentieller PI Regler
    regelt Ableitung Ouputsignal nach Ableitung von Stellgröße
    Stabiler als PID Regler bei rauschen, Überschwinger sind vermeidbar.

    """
    def __init__(self, startInput, startOutput, Setpoint, Kp, Ti, isRunning=False, isNotReverseAction = True):
        self.isInAutomaticMode = isRunning
        self.setMode(isRunning)
        self.sampletime = 1

        self.setpoint = Setpoint
        self.isNewSetpoint = False
        self.controllerDirection = isNotReverseAction
        self.SetTunings(Kp, Ti)
        self.currentOutput = startOutput
        self.lastOutput = startOutput
        self.lastTime = time.time()

        self.error = 0
        self.lastError = 0

        # set output limits here
        self.minOutput = -100 # -100 - 100 %
        self.maxOutput = 100 # -100 - 100 %

        self.wayUp = True

    def setSetpoint(self, newSetpoint):
        self.setpoint = newSetpoint

    def computePI(self, Input, isNoOverschoot=True):
        """
        :param Input: Current Measuring
        :return: new Output between min an max

         Velocity (Discrete) Controller Form
         delta CO = Kp * (1+T / Ti) * e_i-1

         Where:
        CO = controller output signal (the wire out)
        e(t) = current controller error, defined as SP – PV
        SP = set point
        Kc = proportional gain, a tuning parameter
        Ki = integral gain, a tuning parameter
        ei is the current controller error,
        ei-1 is the controller error at the previous
        sample time, T,
        T = ∆t
        ∆ei = ei – ei-1
        """
        print("PI Setpoint", self.setpoint)

        if self.isInAutomaticMode is False:
            return
        now = time.time()
        deltaT = (now - self.lastTime)
        if deltaT >= self.sampletime:

            # saving values
            self.lastError = self.error
            self.lastOutput = self.currentOutput

            #compute Error
            self.error = self.setpoint - Input
            # PI Algorithm
            #          Velocity (Discrete) Controller Form
            #          delta CO = Kc * (1+T / Ti) * e_i-1

            # deltaCO = self.Kp * (1+deltaT/self.Ti) * self.lastError
            deltaCO = self.Kc * (1 + self.sampletime / self.Ti) * self.lastError

            currentOutputlLocal = self.lastOutput + deltaCO

            # check for max output values
            if currentOutputlLocal > self.maxOutput:
                currentOutputlLocal = self.maxOutput
            if currentOutputlLocal < self.minOutput:
                currentOutputlLocal = self.minOutput



            # new output, ganz am ende:
            self.currentOutput = currentOutputlLocal


            def restetPi(self):
                # setprop(0)
                # state warten , shutoffprop
                pass

            if isNoOverschoot is True:
                if self.wayUp is True:
                    if Input > self.setpoint is True:
                        # restetPi()
                        pass
                if self.wayUp is False:
                    if Input < self.setpoint is True:
                        # resetPI()
                        pass

                pass


            # print("setpoint", self.setpoint, "input", Input)
            # print("error ", self.error)
            return self.currentOutput

    def setMode(self, isRunning=True):
        """
        /* SetMode(...)****************************************************************
        * Allows the controller Mode to be set to manual (0) or Automatic (non-zero)
        * when the transition from manual to auto occurs, the controller is
        * automatically initialized
        ******************************************************************************/
        :param Mode:
        :return:
        """
        if isRunning != self.isInAutomaticMode:
            # { /*we just went from manual to auto*/
            self.isInAutomaticMode = isRunning


    def SetTunings(self, Kc, Ti):
        if Kc < 0 or Ti < 0:
            return
        self.Kc = Kc
        self.Ti = Ti * self.sampletime
        if self.controllerDirection is not True:
            self.Kc = 0 - Kc
            self.Ki = 0 - Ti
        return self.Kc, self.Ti




    # def setSampleTime(self, NewSampleTimeInSec):
    #     """
    #     /* SetSampleTime(...) *********************************************************
    #     * sets the period, in seconds, at which the calculation is performed
    #     ******************************************************************************/
    #     """
    #     if (NewSampleTimeInSec > 0):
    #         ratio = NewSampleTimeInSec / self.sampletime
    #         self.Ki *= ratio
    #         self.sampletime = NewSampleTimeInSec


class OsPID:
    def __init__(self, startInput, startOutput, Setpoint, Kp, Ki, Kd, ControllerDirection="DIRECT", inAuto=False):


        self.controllerDirection = ControllerDirection
        if ControllerDirection == "DIRECT":
            self.isDirectAndNotReverse = True

        self.isInAutomaticMode = inAuto

        self.sampletime = 0.1  # default Controller Sample Time is 0.1 seconds
        self.now = time.time()
        self.lastTime = time.time() - self.sampletime

        self.myOutput = startOutput
        self.input = startInput
        self.setpoint = Setpoint

        self.ITerm = 0
        self.lastInput = startInput

        self.setOutputLimits(0, 100)  # regelt zwischen 0 und 100 %
        self.SetControllerDirection(ControllerDirection)
        self.SetTunings(Kp, Ki, Kd)

    def setSetpoint(self, newSetpoint):
        self.setpoint = newSetpoint

    def compute(self, Input):
        """
        /* Compute() **********************************************************************
        * This, as they say, is where the magic happens. this function should be called
        * every time "void loop()" executes. the function will decide for itself whether a new
        * pid Output needs to be computed
        **********************************************************************************/
        """
        if self.isInAutomaticMode is False:
            return
        now = time.time()
        timeChange = (now - self.lastTime)
        if timeChange >= self.sampletime:
            error = self.setpoint - Input
            print("setpoint", self.setpoint, "input", Input)
            print("error ", error)

            # Postitional algorithm
            self.ITerm += (self.Ki * error)
            if self.ITerm >= self.outMax:
                self.ITerm = self.outMax
            elif self.ITerm < self.outMin:
                self.ITerm = self.outMin
            self.dInput = (Input - self.lastInput)

            #       /*Compute PID Output*/
            output = self.Kp * error + self.ITerm - self.Kd * self.dInput

            # Alternative velocity PID:
            # output = lastOutput + Kp*(error - lastError) + Ki * error

            # position
            # PID: u(t) = K_p * e(t) + K_i * T_s * [e(0) + e(1) + ... e(t)] + u(0)
            # velocity
            # PID: u(t) = u(t - 1) + K_p * (e(t) - e(t - 1)) + K_i * T_s * e(t)

            if output > self.outMax:
                output = self.outMax
            elif (output < self.outMin):
                output = self.outMin
            self.lastInput = Input
            self.lastTime = now

            self.myOutput = output
            print("Stellgrad: ", output)
            return output

    def SetTunings(self, Kp, Ki, Kd):
        if Kp < 0 or Ki < 0 or Kd < 0:
            return
        self.Kp = Kp
        self.Ki = Ki * self.sampletime
        self.Kd = Kd / self.sampletime
        if self.controllerDirection == "REVERSE":
            self.Kp = 0 - Kp
            self.Ki = 0 - Ki
            self.Kd = 0 - Kd
        return self.Kp, self.Ki, self.Ki

    def setSampleTime(self, NewSampleTime):
        """
        /* SetSampleTime(...) *********************************************************
        * sets the period, in seconds, at which the calculation is performed
        ******************************************************************************/
        """
        if (NewSampleTime > 0):
            ratio = NewSampleTime / self.sampletime
            self.Ki *= ratio
            self.Kd /= ratio
            self.sampletime = NewSampleTime

    def setOutputLimits(self, Min=-100, Max=100):
        """
         /* SetOutputLimits(...)****************************************************
        * This function will be used far more often than SetInputLimits. while
        * the input to the controller will generally be in the 0-1023 range (which is
        * the default already,) the output will be a little different. maybe they'll
        * be doing a time window and will need 0-8000 or something. or maybe they'll
        * want to clamp it from 0-125. who knows. at any rate, that can all be done
        * here.
        **************************************************************************/
        :param outMin:
        :param outMax:
        :return:
        """

        if Min >= Max:
            return
        self.outMin = Min
        self.outMax = Max
        if self.isInAutomaticMode:
            if self.myOutput > self.outMax:
                self.myOutput = self.outMax
            elif self.myOutput < self.outMin:
                self.myOutput = self.outMin

            if self.ITerm > self.outMax:
                self.ITerm = self.outMax
            elif self.ITerm < self.outMin:
                self.ITerm = self.outMin

    def setMode(self, newMode="Automatic"):
        """
        /* SetMode(...)****************************************************************
        * Allows the controller Mode to be set to manual (0) or Automatic (non-zero)
        * when the transition from manual to auto occurs, the controller is
        * automatically initialized
        ******************************************************************************/
        :param Mode:
        :return:
        """
        if newMode == "Automatic":
            isModeAutomatic = True
        else:
            isModeAutomatic = False

        newAuto = (isModeAutomatic is

            True)
        if newAuto != self.isInAutomaticMode:
            # { /*we just went from manual to auto*/
            self.PIDinit()
        self.isInAutomaticMode = newAuto

    def PIDinit(self):
        """
        /* Initialize()****************************************************************
        * does all the things that need to happen to ensure a bumpless transfer
        * from manual to automatic mode.
        ******************************************************************************/
        :return:
        """
        self.ITerm = self.myOutput
        self.lastInput = self.input
        if self.ITerm > self.outMax:
            self.ITerm = self.outMax
        elif self.ITerm < self.outMin:
            self.ITerm = self.outMin

    def SetControllerDirection(self, newDirection="DIRECT"):
        """
        * The PID will either be connected to a DIRECT acting process (+Output leads
        * to +Input) or a REVERSE acting process(+Output leads to -Input.) we need to
        * know which one, because otherwise we may increase the output when we should
        * be decreasing. This is called from the constructor.
        :return:
        """
        if newDirection == "DIRECT":
            newBoolControllerDirection = True
        else:
            newBoolControllerDirection = False
        if self.isInAutomaticMode and newBoolControllerDirection != self.isDirectAndNotReverse:
            self.Kp = 0 - self.Kp
            self.Ki = 0 - self.Ki
            self.Kd = 0 - self.Kd


if __name__ == '__main__':
    df = OsPI(20, 0, 20, 0.4, 300, True)
    time.sleep(1)
    print(df.computePI(12.1))
    time.sleep(1)
    print(df.computePI(12.2))
    time.sleep(1)
    print(df.computePI(12.5))
    time.sleep(1)
    print(df.computePI(12.11))
    time.sleep(1)

    print(df.computePI(12.20))
    time.sleep(1)
    print(df.computePI(12.3))
