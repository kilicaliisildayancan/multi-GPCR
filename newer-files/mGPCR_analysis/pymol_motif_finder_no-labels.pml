print "Please use GPCRdb numbering and use this script on the processed PDB file! \n"

one_letter ={'VAL':'V', 'ILE':'I', 'LEU':'L', 'GLU':'E', 'GLN':'Q', \
'ASP':'D', 'ASN':'N', 'HIS':'H', 'TRP':'W', 'PHE':'F', 'TYR':'Y',    \
'ARG':'R', 'LYS':'K', 'SER':'S', 'THR':'T', 'MET':'M', 'ALA':'A',    \
'GLY':'G', 'PRO':'P', 'CYS':'C'}

label n. N & (b > 0 and  b <8.1), "%1.2f" %b
color gray, all

select NaPocket, (br. b=2.50 and r. "ASP") or (br. b=3.39 and r. "SER") or (br. b=6.48 and r. "TRP") or (br. b=7.45 and r. "ASN") or (br. b=7.46 and r. "SER") or (br. b=7.49 and r. "ASN")	
color teal, NaPocket
show sticks, NaPocket


select PIF, (br. b=5.50 and r. "PRO") or (br. b=3.40 and r. "ILE") or (br. b=6.44 and r. "PHE")
color tv_green, PIF
show sticks, PIF


select CholesterolMotifs, (br. b=2.41 and (r. "PHE" or r. "TYR")) or (br. b=4.34 and (r. "LYS" or r. "ARG")) or (br. b=4.39 and (r. "LYS" or r. "ARG")) or (br. b=4.46 and (r. "VAL" or r. "ILE" or r. "LEU")) or (br. b=4.50 and (r. "TRP" or r. "TYR"))
color tv_yellow, CholesterolMotifs
show sticks, CholesterolMotifs


select DRY, (br. b=3.49 and r. "ASP") or (br. b=3.50 and r. "ARG") or (br. b=3.51 and r. "TYR")
color tv_red, DRY
show sticks, DRY


select NPxxY, (br. b=7.49 and r. "ASN") or (br. b=7.50 and r. "PRO") or (br. b=7.53 and r. "TYR")
color tv_blue, NPxxY
show sticks, NPxxY


select CWxP, (br. b=6.47 and r. "CYS") or (br. b=6.48 and r. "TRP") or (br. b=6.50 and r. "PRO")
color tv_orange, CWxP
show sticks, CWxP

label n. CA or n. N
