#!/usr/bin/env python
"""Simulation of the compton effect."""

import math
from scipy import constants


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def isint(value):
    try:
        int(value)
        return True
    except Exception:
        return False


def getFloat(min_, max_, txt=""):
    result = ""
    while True:
        result = input(txt)
        if isfloat(result):
            result = float(result)
            if min_ <= result <= max_:
                return result
        print("{} n'est pas un nombre entre {} et {}".format(result, min_, max_))


def getInt(min_, max_, txt=""):
    result = ""
    while True:
        result = input(txt)
        if isint(result):
            result = int(result)
            if min_ <= result <= max_:
                return result
        print("{} n'est pas un nombre entier entre {} et {}".format(result, min_, max_))


class Main:
    def __init__(self):
        pass

    def __call__(self, *args, **kwargs):
        # LC Compton wavelength
        self.LC = constants.physical_constants["Compton wavelength"][0]

        print("Choisissez l'angle du photon diffusé en degré")
        self.phi = getFloat(1, 175) * math.pi / 180
        print("Choisissez la longueur d'onde du photon incident :")
        self.L0 = getFloat(1, 10 ** 3, "facteur: 10e-12 :") * 10 ** (-12)
        self.Ee = constants.electron_mass * (constants.c ** 2)

        self.L1 = self.L0 + self.LC * (1 - math.cos(self.phi))
        self.E0 = (constants.h * constants.c) / self.L0
        self.E1 = constants.h * constants.c / self.L1

        self.psi = - math.atan(1 / ((1 + self.E0 / self.Ee) * math.tan(self.phi / 2)))
        self.K = (self.Ee / (self.Ee + self.E0 - self.E1)) ** 2
        self.V = constants.c * math.sqrt(1 - self.K)

        E0_Kev = math.floor(
            self.E0 / (constants.physical_constants["electron volt"][0] * 1000)
        )

        txt = "Énergie du photon incident {E0} keV\nLongueur d'onde du photon diffusé \u03bb' = {L1} m\nAngle de l'électron  \u03B8 = {psi}°\nVitesse de l'électron Ve = {V} m/s".format(
            **{
                "E0": E0_Kev,
                "L1": self.L1,
                "psi": self.psi * (180 / math.pi),
                "V": self.V,
            }
        )
        print(txt)

    def ics(self):
        self.Ee = constants.electron_mass * (constants.c ** 2)
        # self.lorentz=
        self.E0_E = self.lorentz * self.E0(
            1 - (self.v / constants.c) * math.cos(self.theta0)
        )
        self.E1_L = self.E0_E / (
            1 + (self.E0_E / self.Ee) * (1 - math.cos(self.theta_E))
        )

        self.E1 = self.lorentz * self.E1_L(
            1 + (self.v / constants.c) * math.cos(self.theta1_E)
        )

    def photoelectrique(self):

        # http://mdevmd.accesmad.org/mediatek/pluginfile.php/5037/mod_resource/content/2/Corrections%20des%20exercices%20sur%20leffet%20photo%C3%A9lectriqueTA%20-%20accesmad.htm

        print("Choisissez une longueur d'onde :")
        self.l = getFloat(300, 800, "en nm :") * (10 ** (-9))

        # print("Choisissez une intensitée (%) :")
        # self.i = getFloat(0, 100, "%")

        print(
            "Choisissez un matériau :"
        )  # to do utiliser curses https://docs.python.org/3/howto/curses.html
        element = {"Cs": 1.19, "K": 2.29, "Na": 2.18, "Li": 2.39, "Zn": 4.3}
        # txt = "\n".join(["{} : {}".format(elem[0], list(t.items()).index(elem)) for elem in element.items()])
        # print(txt)
        print(",".join([e for e, _ in element.items()]))
        while True:
            result = input()
            if result in element:
                break
            print(
                "{} n'est pas dans la liste : ".format(result)
                + ",".join(element.keys())
            )
        self.W0 = element[result]  # en eV

        self.W0 = self.W0 * constants.physical_constants["electron volt"][0]  # en J
        self.W = constants.h * constants.c / self.l  # en J

        if self.W <= self.W0:
            print("Il n'y a pas d'émission d'électrons")
        else:
            print("Il y a émissison d'électrons")
            self.Ec = self.W - self.W0
            self.v = math.sqrt(2 * self.Ec / constants.electron_mass)
            print("Vitesse des éléctrons émis : {} m/s".format(self.v))
            self.U0 = -self.Ec / abs(constants.elementary_charge)
            print(
                "Tension à appliquer entre le métal émissif et l’anode pour annuler le courant photoélectrique :"
            )
            print("{} V".format(self.U0))


a = Main()
while True:
    print("Tapez 0 pour l'effet Compton et 1 pour l'effet photoelectrique")
    choix = getInt(0, 1)
    if choix == 0:
        a()
    else:
        a.photoelectrique()

input("Tapez sur enter pour quitter")
