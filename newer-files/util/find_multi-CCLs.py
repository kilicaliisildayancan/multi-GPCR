from package_mgpcrs import hmmout_parsing

import os

#define directories here

home_main = "/home/kilicali/multi-domain_gpcr/chemokines/"
hmmouts_dir = home_main + "hmmouts"
prefilt_dir = home_main + "prefiltered"
lengthfilt_dir = home_main + "length_filtered"

for hfile in os.listdir(hmmouts_dir):
    
    full_hmmout = os.path.join(hmmouts_dir, hfile)
    
    prefilt_out_dir = os.path.join(prefilt_dir, hfile)


    hmmout_parsing.prefilter_hmmout(full_hmmout, prefilt_out_dir, length_constraint=70)


    lengthf_out_dir = os.path.join(lengthfilt_dir, hfile)


    hmmout_parsing.lengthfilter_hmmout(prefilt_out_dir, lengthf_out_dir, length_constraint=140)
    print(f"done with {hfile}!\n")