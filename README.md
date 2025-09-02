# EEE-Sparkle

## Aim of the lab

This lab activity is an introduction to some principles and techniques in Electronic Engineering. You will build an illuminated artwork that can be controlled with touch sensors and an internet connection. Along the way, you will see how the behaviour of an electronic circuit can be analysed mathmatically, you will assemble some hardware by soldering components to a circuit board, and you will develop a hardware-software interface by writing code for an embedded computer.

### System overview

Electronic systems are often conceptualised as a block diagram, which shows how energy or information flows between various building blocks. A block diagram for the system in this lab activity looks like this:


The main user input is a set of three _touch sensors_, which measure the capacitance of the user's finger and converts it into an electrical signal using an _oscillator_. The frequency of the signal is converted to a voltage with a _charge pump_, and this voltage is measured by a _microcontroller_. The microcontroller detects touches and sets the colour and brightness of two LEDs, which illuminate the artwork.


![Water pump](sensor-cct.png)

## The Oscillator

We will begin by building and testing the oscillator. The oscillator repeatedly charges and discharges a capacitor to find out how much electrical charge it can store when a voltage is applied. This quantity, charge per unit voltage, is the _capacitance_, measured in _Farads_. The capacitance in this case is a combination of an electronic component and the capacitance of the user's finger ($C$). The capacitance of a finger is very small and it is best measured in _picofarads_ - trillionths of a Farad. The circuit diagram for the oscillator looks like this:

![Circuit Diagram for the oscillator](osc-cct.png)

The active component in the oscillator is an inverter, which measures the input voltage as above or below a certain threshold and sets the output to the logical opposite. If the voltage is below the threshold, the output is set to a high value (3.3V in this case), and if the input exceeds the threshold the output voltage is low: 0V. The output of the inverter is the output of the oscillator ($V_1$).

$V_1$ is also connected to a capacitor $C$ and resistor $R$ in series such as $V_1 = V_\text{C} + V_\text{R}$, where $V_\text{C}$ and $V_\text{R}$ are the voltages between the terminals of the capacitor and resistor respectively. The capacitor consists of two elements: a 47pF chip capacitor and the capacitance of the user's finger touching the pads. 

$V_\text{C}$ is connected to the inverter input, so if $V_\text{C}$ is low $V_1$ will be high and a current flows into the capacitor charging it. When $V_\text{C}$ rises above the threshold of the inverter, $V_1$ will be low and the capacitor will discharge again. Of course, once the voltage drops below the threshold the inverter will switch again and so the process will continue indefinitely, with the capacitor voltage wavering around the threshold voltage and the inverter output toggling between high and low. This is the purpose of an oscillator, to produce a signal that varies, repetitively, over time.

![Current flowing around the circuit, charging the capacitor]()

$V_\text{C}$ can be expressed in terms of the charge $Q$ stored in the capacitor: $V_\text{C} = \frac{Q}{C}$. $V_\text{R}$ is related to the current $I$ flowing through the resistor: $V_\text{R} = IR$. Furthermore, since the same current flows through the resistor and capacitor, $I$ can be expressed as the rate of change of capacitor charge, giving $V_\text{R} = R\frac{dQ}{dt}$. Combining everything gives the differential equation $V_1 = R\frac{dQ}{dt} + \frac{Q}{C}$

Solving the differential equation gives $Q = Ae^{-\frac{1}{RC}t}+CV_1$, and applying $Q = CV_\text{C}$ gives 

$V_\text{C} = Be^{-\frac{1}{RC}t}+V_1$

### Building the Oscillator

Start by building the oscillator just for touch sensor 0. Solder the capactior C4 and resistor R2 to the circuit. The inverter, plus an additional capacitor C5 to stabilise the power input to the circuit, are already fitted for you.

Power up the circuit by connecting a USB cable to the socket on the Raspberry Pi Pico module. The Pico isn't doing anything yet except passing the USB power into the rest of the circuit.

Connect an oscilloscope probe to the proble point for oscillator output 0 on the PCB and attach the ground clip to the bigger loop marked GND. The oscilloscope is already set up to show you the output of the oscillator. If it works, you will see a square wave - the oscillator output alternating between high and low over time. The oscilloscope measures the frequency of oscillation for you and displays the result on the screen - it's the number of times per second that the voltage switches from low to high and back. Touch the sensor pad for channel 0 - you should see the frequency reduce as the increase in capacitance means it takes more charge and more time for the capacitor voltage to rise above and fall below the threshold.

### Oscillator Frequency

Earlier we derived an equation for expressing the capacitor voltage as a function of time and we can use this to find how long the capacitor will take to charge and discharge. First, we need to consider another element: hysteresis. We have established that the capacitor voltage varies slightly above and below the inverter threshold voltage, but by how much? If all the components behaved perfectly and the inverter could detect an infinitesimal difference between input and threshold, the oscillator would switch at an unlimited frequency.

In fact, the inverter has a special type of input called a _schmitt trigger_, and it's designed for this scenario where you want to deliberately desensitise the input a little. It works by introducing a dependency between the threshold voltage and the output voltage. If the output is high, the threshold voltage is reduced slightly and if it's low, the threshold is increased.

So there are two threshold voltages $V_{\text{t}-}$ and $V_{\text{t}+}$, and the capacitor voltage will oscillate between them. The difference between them is called the hysteresis and the larger the hysteresis, the lower the frequency of oscillation. For the inverter in our circuit, the lower threshold $V_\text{t-}$ is around 1.5V and the upper threshold $V_\text{t+}$ is around 2.15V.

Consider the capacitor charging from $V_{\text{t}-}$ to $V_{\text{t}+}$. At time $t=0$, $V_\text{C} = V_{\text{t}-} = 1.5\text{V}$ and $V_1 = 3.3\text{V}$. Using these initial conditions in the earlier equation gives $V_\text{C} = -1.8e^{-\frac{1}{RC}t}+3.3$. The capacitor charges until $V_\text{C} = 2.15V$, and rearranging gives $t_\text{charge}=0.45RC$. $V_{\text{t}-}$ and $V_{\text{t}+}$ are not quite symmetrically spaced within the range of $V_1$, so analysing separately for the discharging time gives $t_\text{discharge}=0.36RC$.

Adding them together gives a total period of $0.81RC$ and an oscillator frequency of $f=\frac{1}{0.81RC}$. Using values from the circuit and ignoring the touch pad capacitance we have $R=270\text{k}\Omega$, $C=47\text{pF}$ and $f=97.3\text{kHz}$. The capacitance of a finger on the touch pad is quite variable, but if we assume an additional 30pF then the frequency drops to around 60kHz

## The Charge Pump

The charge pump makes it easy for the Raspberry Pi to detect touch inputs by converting the oscillator frequency into a steady voltage. If the frequency changes, the voltage will change.

![Water pump](pump-cct.png)

A water pump serves as a useful analogy for the charge pump:

![Water pump](water-pump.svg)

When the pump handle (input voltage) is low, water (charge) flows into the pump to equalise at the ground level. When the handle is raised, the water level inside the pump also increases, and when it exceeds the level of the output reservoir, the water in the pump flows into the reservoir. A non-return valve (diode) prevent the reservoir from discharging back into the pump when the level is lowered. Another valve stops the pump discharging to the ground when the level is high. The output reservoir leaks away through a small hole (resistor).

In a similar way, the charge pump uses a capacitor $C$ to transfer an amount of charge from to the output on every oscillator cycle. The higher the frequency $f$, the more charge is transferred. The pumped charge is held in a reservoir capacitor, where it slowly leaks away through a resistor $R$. The leakage current depends on the voltage of the reservoir and therefore the charge in the reservoir, so the pumped charge and leakage current will, on average, balance and the reservoir voltage $V_\text{out}$ will reach an equilibrium, depending on the frequency.

### Building the Charge Pump

The two diodes for channel 0 are already fitted for you - they are combined into a single device D1 with three pins.

### Analysing the Charge Pump

The charge transferred on each cycle is $Q = (3.3V - V_\text{out})C$, since the high input raises the pump capacitor to 3.3V and it discharges until the pump capacitor and the reservoir capacitor have the same voltage ($V_\text{out}$).

The pump operates once per oscillator cycle with frequency $f$, so the average current transferred is $i = f(3.3V - V_\text{out})C_\text{pump}$

The reservoir leakage current balances the input current, and it depends on the voltage and the resistor: $i = V_\text{out}/R$

Solving for $V_\text{out}$ gives

$V_\text{out} = \frac{3.3}{(1/RfC + 1)}$

That means for low frequencies, $V_\text{out}$ is approximately proportional to $f$. But once $RfC$ grows much over 1, $V_\text{out}$ converges towards 3.3V.

In practice, $V_\text{out}$ will be lower due to effects we haven't considered here, such as energy lost in the diodes.



## The LED Controller