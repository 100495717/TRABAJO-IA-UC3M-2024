from Sistema_Banco_Pichin import logica_borrosa
from MFIS_Read_Functions import readFuzzySetsFile, readRulesFile, readApplicationsFile

Rules = readRulesFile()
FuzzySets = readFuzzySetsFile("Files/InputVarSets.txt")
Applications = readApplicationsFile()

inferencia = logica_borrosa(Rules, FuzzySets,  Applications)

print(inferencia)