#!/usr/bin/env python3.10
from __future__ import annotations

TransaktionTolerance = 0.01


class Person:

    def __init__(self, name, paid, spend):
        self.name = name
        self.paid = round(float(paid), 2)  # bezahlt, real ausgegeben
        self.spend = round(float(spend), 2)  # vorgeschossene Summe
        self.surplus = (self.spend - self.paid)

    def __str__(self) -> str:
        return "Name: " + str(self.name) + " hat ausgegeben: " + str(self.paid) + " und bezahlte: " + str(self.spend)

    def get_surplus(self) -> float:
        return self.surplus

    def correktSurplus(self, globalSurplus):
        self.surplus -= globalSurplus


class CollactData:

    def __init__(self):
        self.persons = []
        self.count = 0
        self.paidSum = 0
        self.spendSum = 0

    def __str__(self) -> str:
        returnString = str(self.count) + " Personen:" + "\n"
        for each in self.persons:
            returnString += str(each) + "\n"
        returnString += "haben " + str(round(self.paidSum, 2)) + " Euro ausgegeben und " + str(
            round(self.spendSum, 2)) + "Euro bezahlt.\n"
        return returnString

    def addPersion(self, person: Person):
        self.persons.append(person)
        self.count += 1
        self.paidSum += person.paid
        self.spendSum += person.spend

    def calculation(self) -> str:
        returnString = ""

        surplus = round(self.spendSum - self.paidSum, 2)
        eachSurplus = surplus / len(self.persons)

        personSurplusMinus = []
        personSurplusPlus = []

        for each in self.persons:
            each.correktSurplus(eachSurplus)

            if (each.get_surplus() < (TransaktionTolerance * -1)):
                personSurplusMinus.append(each)
                continue
            if (each.get_surplus() > TransaktionTolerance):
                personSurplusPlus.append(each)
                continue

        while (len(personSurplusMinus) != 0 or len(personSurplusPlus) != 0):
            personSurplusPlus.sort(key=Person.get_surplus)
            personSurplusMinus.sort(key=Person.get_surplus)
            eachPlus = personSurplusPlus[0]
            eachMinus = personSurplusMinus[0]

            minTransaktion = min(eachPlus.get_surplus(), - eachMinus.get_surplus())
            eachMinus.correktSurplus(- minTransaktion)
            eachPlus.correktSurplus(minTransaktion)

            returnString += eachMinus.name + " gibt " + eachPlus.name + " " + str(round(minTransaktion, 2)) + " Euro\n"

            if ((TransaktionTolerance * -1) <= eachMinus.get_surplus() <= TransaktionTolerance):
                personSurplusMinus.remove(eachMinus)
            if ((TransaktionTolerance * -1) <= eachPlus.get_surplus() <= TransaktionTolerance):
                personSurplusPlus.remove(eachPlus)

        return returnString


def runCalculation(input) -> str:
    request = input.split()

    if (len(request) % 3 != 0 or len(request) <= 3):
        return "Usage: [[Name] [paid] [spend]]"

    request = [request[i:i + 3] for i in range(0, len(request), 3)]

    coll = CollactData()

    for each in request:
        coll.addPersion(Person(each[0], each[1].replace(',', '.'), each[2].replace(',', '.')))

    return coll.calculation()
