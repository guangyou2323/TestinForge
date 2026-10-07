#For this repo, we are mainly testing out new functionality and features. This repo is used to test out new code before it is added to the main project.
#Whenever required, please see the certain requirements stated in code file in formats like:
'''
Library requirements:
pandas
pytorch
biopython
'''
#If required, please do !pip install <library_name> to install the required libraries.
#We do not conduct code/ environment segregation for this repo, please check the conflicts before running the code.
#An example is stated below:
#The library used here is biopython, which is used to analyze protein sequences. If you do not have it installed, please run !pip install biopython in your environment.
import Bio.SeqUtils.ProtParam as ProtParam  

sequence = "MAEGEITTFTALTEKFNLPPGNYKKPKLLYCSNGGHFLRILPDGTVDGTRDRSDQHIQLQLSAESVGEVYIKSTETGQYLAMDTSGLLYGSQTPSEECLFLERLEENHYNTYTSKKHAEKNWFVGLKKNGSCKRGPRTHYGQKAILFLPLPV"

analysed_seq = ProtParam.ProteinAnalysis(sequence)

molecular_weight = analysed_seq.molecular_weight()
isoelectric_point = analysed_seq.isoelectric_point()
aromaticity = analysed_seq.aromaticity()
instability_index = analysed_seq.instability_index()
gravy = analysed_seq.gravy()
aa_count = analysed_seq.count_amino_acids()

print(f"Molecular Weight: {molecular_weight:.2f} Da")
print(f"Isoelectric Point (pI): {isoelectric_point:.2f}")
print(f"Aromaticity: {aromaticity:.3f}")
print(f"Instability Index: {instability_index:.2f} ({'Instable' if instability_index > 40 else 'Stable'})")
print(f"GRAVY (Hydropathicity): {gravy:.3f}")
print(f"Alanine Count: {aa_count['A']}")