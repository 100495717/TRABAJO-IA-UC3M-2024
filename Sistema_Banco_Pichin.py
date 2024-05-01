from MFIS_Read_Functions import readFuzzySetsFile, readRulesFile, readApplicationsFile
from MFIS_Classes import FuzzySetsDict, RuleList, Application
import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt


def logica_borrosa(RuleList, FuzzySetsDict, Application):
    for regla in RuleList:
        antecedentes = regla.antecedent
        consecuente = regla.consequent

        s = 1

        for antecedente in antecedentes:

            fuzzy = FuzzySetsDict[antecedente]

            grado_pertenencia = fuzz.interp_membership(fuzzy.x,fuzzy.y, Application.data)

            s = min(s,grado_pertenencia)

        consecuente_borroso = FuzzySetsDict[consecuente]
        consecuente_borroso.memDegree = max(consecuente_borroso.memDegree, s)
    return FuzzySetsDict

FuzzySetsDict = readFuzzySetsFile("InputVarSets.txt")

RuleList = readRulesFile("Rules.txt")

Applications = readApplicationsFile("Application.txt")

resultados = open("Resultados.txt", "w")

for application in Applications:

    inferencia = logica_borrosa(RuleList,FuzzySetsDict, application)

    resultados.write("Solicitud" + application.appId + "\n")
    for id, fuzzy in resultados.items():
        if fuzzy.memDegree < 0.5:
            resultados.write("Solicitud de préstamo" + str(id) + ": Denegada\n")
        elif fuzzy.memDegree >= 0.5:
            resultados.write("Solicitud de préstamo" + str(id) + ": Aceptada\n")

resultados.close()