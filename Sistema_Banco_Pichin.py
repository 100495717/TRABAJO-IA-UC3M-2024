from MFIS_Read_Functions import readFuzzySetsFile, readRulesFile, readApplicationsFile
from MFIS_Classes import FuzzySet, FuzzySetsDict


import skfuzzy as fuzz


def logica_borrosa(RuleList, FuzzySetsDict, Application,RisksDict):

    for regla in RuleList:

        antecedentes = regla.antecedent
        consecuente = regla.consequent

        s = 1

        for antecedente in antecedentes:

            fuzzy = FuzzySetsDict[antecedente]
            antecedent_value = next(data[1] for data in Application.data if data[0] == fuzzy.var)

            grado_pertenencia = fuzz.interp_membership(fuzzy.x,fuzzy.y, antecedent_value)


            s = min(s,grado_pertenencia)

        if RisksDict[consecuente] < s:
            RisksDict[consecuente] = s

    return RisksDict

FuzzySetsDict = readFuzzySetsFile('Files/InputVarSets.txt')

RuleList = readRulesFile()

Applications = readApplicationsFile()


resultados = open("Resultados.txt", "w")

for application in Applications:
    RisksDict = {"Risk=LowR": 0, "Risk=MediumR": 0, "Risk=HighR": 0}
    resultados.write("Solicitud " + application.appId + "\n")
    salidas = logica_borrosa(RuleList,FuzzySetsDict, application,RisksDict)
    resultados.write("LowR: " + str(salidas["Risk=LowR"]) + " ")
    resultados.write("MediumR: " + str(salidas["Risk=MediumR"]) + " ")
    resultados.write("HighR: " + str(salidas["Risk=HighR"]) + "\n")

resultados.close()