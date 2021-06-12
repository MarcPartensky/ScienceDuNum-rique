#!/usr/bin/env python
"""Simulation de l'effet compton et de l'effet photoélectrique."""

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

    def compton(self, *args, **kwargs):
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

    def comptonInverse(self):

        print("Energie de l'électron")
        self.Ee = getFloat(0, 10**20, "J")

        print("Energie du photon")
        self.Ep = getFloat(0, 10**20, "J")

        print("Angle du photon incident")
        self.alpha = (getFloat(0, 90, "degré")) * (math.pi/180)
        self.theta1 = math.pi - self.alpha

        print("Angle pris par le photon rétro-diffusé")
        self.theta2 = getFloat(0, 90, "degré") * (math.pi/180)

        beta = 1

        A = self.Ep * (1-beta*math.cos(self.theta1))
        B = (1 - beta * math.cos(self.theta2))
        C = (1-math.cos(self.theta2-self.theta1)) * (self.Ep/self.Ee)

        self.Ex = A/(B+C)

        print("Energie du photon diffusé : {} J".format(self.Ex))


    def photoelectrique(self):

        print("Choisissez une longueur d'onde :")
        self.l = getFloat(100, 1000, "en nm :") * (10 ** (-9))

        print(
            "Choisissez un matériau :"
        )  # to do utiliser curses https://docs.python.org/3/howto/curses.html
        element = {"Cs": 1.19, "K": 2.29, "Na": 2.18, "Li": 2.39, "Zn": 4.3, "Co":3.90, "Al":4.08, "Pb":4.14, "Fe":4.50,
                   "Cu":4.7, "Ag":4.73}
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
    print("Tapez  :\n0 pour l'effet Compton\n1 pour l'effet photoelectrique\n2 pour l'effet compton inverse")
    choix = getInt(0, 2)
    [a.compton, a.photoelectrique, a.comptonInverse][choix]()

input("Tapez sur enter pour quitter")