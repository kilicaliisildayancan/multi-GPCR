import requests
import json

class KI_proteins():

    def __init__(self):

        self.prot1_attributes = {
            "gene_name": "",
            "uniprot_acc": "",
            "alt_splicing": False,
            "cell_component": [],
            "ligand": [],
            "bio_process": [],
            "interaction":[],
            "subc_loc": []
        }

        self.prot2_attributes = {
            "gene_name": "",
            "uniprot_acc": "",
            "alt_splicing": False,
            "cell_component": [],
            "ligand": [],
            "bio_process": [],
            "interaction":[],
            "subc_loc": []
        }

        
        
    def from_online(self, prot1, prot2):
        self.prot1_attributes['gene_name'] = prot1
        self.prot2_attributes['gene_name'] = prot2

        self.prot1_attributes.update(self._analyze_prot(prot1))
        self.prot2_attributes.update(self._analyze_prot(prot2))


    def from_tsv(self, tsv_dir):

        with open(tsv_dir, 'r') as infile:
            header = infile.readline()
            for line in infile:
                line = line.strip().lower().split('\t')
                attr_name = line[0]

                if attr_name == "alt_splicing":
                    prot1_attr = True if line[1] == "True" else False
                    prot2_attr = True if line[2] == "True" else False

                #way to process TSV list string into python lists
                elif ('['  in ''.join(line)) or (']' in ''.join(line)):
                    prot1_attr = [x for x in line[1].split("'") if any(char.isalpha() for char in x)]
                    prot2_attr = [x for x in line[2].split("'") if any(char.isalpha() for char in x)]


    def _analyze_prot(self, prot_name):
        _data = self._search_uniprot(prot_name)
        if _data != 0:
            attributes = self._parse_uniprot_response(_data)
            return attributes
        else:
            return {}



    def _search_uniprot(self, gene: str):

        query = f"gene:{gene}+AND+reviewed:true+AND+organism_id:9606" #this can be generalized if wanted

        URL = f"https://rest.uniprot.org/uniprotkb/search?query={query}"

        response = requests.get(URL).text
        response_all=json.loads(response)['results']

        if len(response_all) == 1:
            return response_all[0]
        elif len(response_all) == 0:
            print(f"No entries for {gene}")
            return 0
        else:
            print(f"Multiple entries for {gene}")
            return response_all[0]


    def _parse_uniprot_response(self, json_response):
        #keywords: category: ["Coding sequence diversity", "Cellular component", "Ligand", "Biological process"]
        #comments: commentType: ["INTERACTION", "SUBCELLULAR LOCATION"]

        try:
            kws = json_response["keywords"]
            comments = json_response["comments"]
        except:
            return {}

        attributes = {"uniprot_acc": json_response["primaryAccession"]}

        new_kw_attrs = self._parse_kw(kws)
        new_comment_attrs = self._parse_comment(comments)

        attributes.update(new_kw_attrs)
        attributes.update(new_comment_attrs)

        return attributes


    def _parse_comment(self, comments):
        select_comments = ["INTERACTION", "SUBCELLULAR LOCATION"]
        new_attrs = {"interaction":[],
                     "subc_loc": []}

        for comment in comments:
            if "commentType" in comment:
                if comment["commentType"] in select_comments:

                    cond = comment["commentType"]

                    if cond == "INTERACTION":
                        try:
                            new_attrs["interaction"] = new_attrs["interaction"] + [x['interactantTwo']['geneName'] for x in comment["interactions"]]
                        except:
                            pass
                    elif cond == "SUBCELLULAR LOCATION":
                        try:
                            new_attrs["subc_loc"] = new_attrs["subc_loc"] + [x["location"]["value"] for x in comment["subcellularLocations"]]
                        except:
                            pass
        return new_attrs


    
    def _parse_kw(self, kws):
        select_kws = ["Coding sequence diversity", "Cellular component", "Ligand", "Biological process"]
        new_attrs = {"alt_splicing": False,
                     "cell_component": [],
                     "ligand": [],
                     "bio_process": []}
        for kw in kws:
            if "category" in kw.keys():
                if kw["category"] in select_kws:


                    if kw["category"] == "Coding sequence diversity":
                        new_attrs["alt_splicing"] = True
                    elif kw["category"] == "Cellular component":
                        new_attrs["cell_component"].append(kw["name"])
                    elif kw["category"] == "Ligand":
                        new_attrs["ligand"].append(kw["name"])
                    elif kw["category"] == "Biological process":
                        new_attrs["bio_process"].append(kw["name"])
                    else:
                        raise KeyError


        return new_attrs
    
    def check_similar_attributes(self):

        similarity_counter = 0

        interaction1 = self.prot1_attributes["interaction"]
        interaction2 = self.prot2_attributes["interaction"]

        if (self.prot2_attributes["gene_name"] in interaction1) or (self.prot1_attributes["gene_name"] in interaction2):
            print(f"Interacts with each other! {self.prot1_attributes['gene_name']} and {self.prot2_attributes['gene_name']}")
            similarity_counter += 1

        cell_comp1 = set(self.prot1_attributes["cell_component"])
        cell_comp2 = set(self.prot2_attributes["cell_component"])

        both_cell_comps = cell_comp1.intersection(cell_comp2)

        if len(both_cell_comps) != 0:
            similarity_counter += 1

        ligand1 = set(self.prot1_attributes["ligand"])
        ligand2 = set(self.prot2_attributes["ligand"])

        both_ligand = ligand1.intersection(ligand2)

        if len(both_ligand) != 0:
            similarity_counter += 1

        bio_process1 = set(self.prot1_attributes["bio_process"])
        bio_process2 = set(self.prot2_attributes["bio_process"])
        
        both_bio_process = bio_process1.intersection(bio_process2)

        if len(both_bio_process) != 0:
            similarity_counter += 1

        subc_loc1 = set(self.prot1_attributes["subc_loc"])
        subc_loc2 = set(self.prot2_attributes["subc_loc"])

        both_subc_loc = subc_loc1.intersection(subc_loc2)

        if len(both_subc_loc) != 0:
            similarity_counter += 1

        if similarity_counter >= 3:
            return True
        else:
            return False




        #interaction with each other


        # "cell_component": [],
        #     "ligand": [],
        #     "bio_process": [],
        #     "interaction":[],
        #     "subc_loc": []
        
    
    def tsv_out(self, out_dir):
        
        with open(out_dir, 'w+') as out:
            out.write("ATTRIBUTE\tGENE1\tGENE2\n")

            for key in self.prot1_attributes.keys():
                out.write(f"{key.upper()}\t{self.prot1_attributes[key]}\t{self.prot2_attributes[key]}\n")

