import skfuzzy

from MFIS_Read_Functions import readFuzzySetsFile, readRulesFile, readApplicationsFile
from MFIS_Classes import FuzzySet, FuzzySetsDict

import numpy as npy
import skfuzzy as fuzz


def logica_borrosa(RuleList, FuzzySetsDict, Application,RisksDict):

    for regla in RuleList:

        antecedentes = regla.antecedent
        consecuente = regla.consequent

        s = 1

        for antecedente in antecedentes:
            print(antecedente)
            fuzzy = FuzzySetsDict[antecedente]
            antecedent_value = next(data[1] for data in Application.data if data[0] == fuzzy.var)
            print(antecedent_value)
            print(fuzzy.x[-1])

            if antecedente == "Age=Young" or antecedente == "Age=Elder" or antecedente == "Age=Adult":
                if fuzzy.x[-1] == antecedent_value -1:
                    grado_pertenencia = fuzz.interp_membership(fuzzy.x,fuzzy.y,antecedent_value-1)
                else:
                    grado_pertenencia = fuzz.interp_membership(fuzzy.x, fuzzy.y, antecedent_value)
            if antecedente == "IncomeLevel=Low" or antecedente == "IncomeLevel=Med" or antecedente == "IncomeLevel=Hig":
                if fuzzy.x[-1] == antecedent_value -1:
                    grado_pertenencia = fuzz.interp_membership(fuzzy.x,fuzzy.y,antecedent_value-1)
                else:
                    grado_pertenencia = fuzz.interp_membership(fuzzy.x, fuzzy.y, antecedent_value)
            if antecedente == "Assets=Scarce" or antecedente == "Assets=Abundant" or antecedente == "Assets=Moderate":
                if fuzzy.x[-1] == antecedent_value -1:
                    grado_pertenencia = fuzz.interp_membership(fuzzy.x,fuzzy.y,antecedent_value-1)
                else:
                    grado_pertenencia = fuzz.interp_membership(fuzzy.x, fuzzy.y, antecedent_value)
            if antecedente == "Amount=Big" or antecedente == "Amount=Small" or antecedente == "Amount=Medium" or antecedente == "Amount=VeryBig":
                if fuzzy.x[-1] == antecedent_value -1:
                    grado_pertenencia = fuzz.interp_membership(fuzzy.x,fuzzy.y,antecedent_value-1)
                else:
                    grado_pertenencia = fuzz.interp_membership(fuzzy.x, fuzzy.y, antecedent_value)
            if antecedente == "Job=Stable" or antecedente == "Job=Unstable":
                if fuzzy.x[-1] == antecedent_value -1:
                    grado_pertenencia = fuzz.interp_membership(fuzzy.x,fuzzy.y,antecedent_value-1)
                else:
                    grado_pertenencia = fuzz.interp_membership(fuzzy.x, fuzzy.y, antecedent_value)
            if antecedente == "History=Poor" or antecedente == "History=Standard" or antecedente == "History=Good":
                if fuzzy.x[-1] == antecedent_value -1:
                    grado_pertenencia = fuzz.interp_membership(fuzzy.x,fuzzy.y,antecedent_value-1)
                else:
                    grado_pertenencia = fuzz.interp_membership(fuzzy.x, fuzzy.y, antecedent_value)




            s = min(s,grado_pertenencia)

        if RisksDict[consecuente] < s:
            RisksDict[consecuente] = s

    return RisksDict










FuzzySetsDict = readFuzzySetsFile('Files/InputVarSets.txt')

RuleList = readRulesFile()

Applications = readApplicationsFile()

Risks = readFuzzySetsFile('Files/Risks.txt')


resultados = open("Resultados.txt", "w")

for application in Applications:
    RisksDict = {"Risk=LowR": 0, "Risk=MediumR": 0, "Risk=HighR": 0}
    resultados.write("Solicitud " + application.appId + "\n")
    #Añadimos al resultado el valor del fuzzy de cada solicitud
    salidas = logica_borrosa(RuleList,FuzzySetsDict, application,RisksDict)
    resultados.write("LowR: " + str(salidas["Risk=LowR"]) + " ")
    resultados.write("MediumR: " + str(salidas["Risk=MediumR"]) + " ")
    resultados.write("HighR: " + str(salidas["Risk=HighR"]) + "\n")

    #Añadimos al resultado el centroide
    #Sacamos los valores clave
    LowR_valor_fuzzy = salidas["Risk=LowR"]
    MediumR_valor_fuzzy = salidas["Risk=MediumR"]
    HighR_valor_fuzzy = salidas["Risk=HighR"]
    for elem in Risks:
        if elem == "Risk=LowR":
            LowR_x = Risks[elem].x
            LowR_MFX = Risks[elem].y
        if elem == "Risk=MediumR":
            MediumR_x = Risks[elem].x
            MediumR_MFX = Risks[elem].y
        if elem == "Risk=HighR":
            HighR_x = Risks[elem].x
            HighR_MFX = Risks[elem].y

    mfxLowR_recortada = npy.minimum(LowR_MFX,LowR_valor_fuzzy)
    mfxMediumR_recortada = npy.minimum(MediumR_MFX,MediumR_valor_fuzzy)
    mfxHighR_recortada = npy.minimum(HighR_MFX,HighR_valor_fuzzy)

    mfx_union = npy.maximum(npy.maximum(mfxLowR_recortada,mfxMediumR_recortada), mfxHighR_recortada)
    centroide = fuzz.centroid(LowR_x,mfx_union)
    resultados.write("Centroide: " + str(centroide) + "\n")




resultados.close()