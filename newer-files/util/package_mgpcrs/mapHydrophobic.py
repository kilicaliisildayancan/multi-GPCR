''' This is to map the TM parts of a given protein sequence
 using the Ben-Tal scale in a sliding window manner. 
 As positive control, a known GPCR is used to find 7 TMs.'''

import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
from matplotlib.lines import Line2D
import numpy as np



def hydrophoCalculator(sequence):
    counter = 0
    for aaI in range(len(sequence)):
        counter += BENTALSCALE[sequence[aaI]]
    return counter

def hydroSW(sequence, SWLength):
    """SW: sliding window"""

    hydrophoList = []
    for fIndex in range(len(sequence)-(SWLength-1)):
        slidingWindow = sequence[fIndex:fIndex+SWLength]
        hydrophoList.append(hydrophoCalculator(slidingWindow))
    return hydrophoList



def plotHPhobicity(data, title, out):
    #pdf = matplotlib.backends.backend_pdf.PdfPages(out)
    plt.figure(figsize=(40, 10))
    plt.title(title)
    plt.xticks(np.arange(0, len(data)+1, 10.0), rotation=90)
    plt.axhspan(10, max(data), facecolor='lightgreen', alpha=0.3) 
    plt.axhspan(min(data), 10, facecolor='lightpink', alpha=0.3)
    plt.plot(data)

    plt.show()
    #pdf.savefig()
    #pdf.close()



if __name__ == "__main__":

    from general import BENTALSCALE, HOME
    #P16395
    mGPCRseq = "MHEMEMGAMLSLKIKGPRKMDGNDTFSHNVLPTSHSLFTTNVKGNDEEPTTSYDYDYSEPCRKTSVGQIEAQLLPPLYSLVFIFGFVGNLLVVLILINCKKLKSMTDIYLLNLAISDLLFLLTMPFWAHYAADQWVFGNVMCKFFTGLYHIGYFGGIFFIILLTIDRYLAIVHAVFALKARTVTFGVVTSGVTWVVAVFASLPGIIFIKSLEEHSGYACAPYFPLGWKNFHTIMRSILGLVLPLLVMIVCYSGIIKTLLRCRNEKKKHKAVRLIFVIMIVYFLFWAPYNIVLLLSTFQEFFGLSNCKSSSQLDQAMQVTETLGLTHCCINPIIYAFVGEKFRRYLSTFFRKHIAKHLCKQCPVFYGETGDRVLDLEKDGQHVQLTESSKMDYQTSTPLYDIDYGMSEPCQKLNVRQIAARLLPPLYSLVFIFGFVGNMLVVLILINCKKLKSMTDIYLLNLAISDLLFIITIPFWAHYAADQWVFGNTTCQLFTGFYFIGYFGGIFFIILLTIDRYLAIVHAVFALKARTVTFGAATSVVTWVVAVFASLPGIIFTKSQKEGSRHTCSPHFPSSQYHFWKNFQTLKIVILGLVLPLLVMIVCYSGIIKTLLRCRNEKKKHKAVRLIFVIMIVYFLFWAPYNIVLLLSTFQEFFGLNNCSGSNRLDQAMQVTETLGMTHCCINPIIYAFVGEKFRNYLLRFFRKYFASRFCKGCPVFQGEAPERVSSVYTRSTGEQEISVGL"
        
    H_mGPCR = hydroSW(mGPCRseq, SWLength=15)

    TMindices = [[101,131],[138,167],[173,206],[220,246],[267,296],[713,742],[751,775]]
    plotHPhobicity(H_mGPCR, title="Hydrophobicity plot of A0A6B0S3N8", out=f'{HOME}/plots/P16395hydroph-SW3.pdf')
