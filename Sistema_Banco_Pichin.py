from MFIS_Read_Functions import readFuzzySetsFile, readRulesFile, readApplicationsFile
from MFIS_Classes import FuzzySet, FuzzySetsDict

import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt


def logica_borrosa(RuleList, FuzzySetsDict, Application,RisksDict):
    reglita = 0

    s_antigua = 0

    for regla in RuleList:



        print("Regla:", reglita, "\n")
        antecedentes = regla.antecedent
        consecuente = regla.consequent
        print(antecedentes)
        print(consecuente)

        s = 1

        for antecedente in antecedentes:

            fuzzy = FuzzySetsDict[antecedente]
            antecedent_value = next(data[1] for data in Application.data if data[0] == fuzzy.var)
            print(antecedent_value)
            grado_pertenencia = fuzz.interp_membership(fuzzy.x,fuzzy.y, antecedent_value)
            print(grado_pertenencia)

            s = min(s,grado_pertenencia)
            print("S:", s)

        RisksDict[consecuente] = max(s,s_antigua)
        s_antigua = s







    return RisksDict

FuzzySetsDict = readFuzzySetsFile('Files/InputVarSets.txt')

RuleList = readRulesFile()

Applications = readApplicationsFile()
RisksDict = readFuzzySetsFile("Files/Risks.txt")

resultados = open("Resultados.txt", "w")

for application in Applications:
    resultados.write("Solicitud número" + application.appId + "\n")
    salidas = logica_borrosa(RuleList,FuzzySetsDict, application,RisksDict)
    resultados.write("LowR: " + str(salidas["Risk=LowR"]))
    resultados.write("MediumR: " + str(salidas["Risk=MediumR"]))
    resultados.write("HighR: " + str(salidas["Risk=HighR"]) + "\n")

resultados.close()