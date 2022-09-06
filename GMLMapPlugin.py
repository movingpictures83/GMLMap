# Not used in the analysis


import pandas as pd

def get_mapping_dict(metadata):
    metadata_path = metadata

    name_col = 1 #started from 0
    metabolite_col=-1

    map_dict = {}

    with open(metadata_path, 'r') as f:
        f.readline()
        for line in f.readlines():
            line = line.strip("\n")
            row = line.split("\t")
            id = row[metabolite_col]
            if id!="":
                map_dict[id] = id + "__" + row[name_col].replace(",","").replace(" ","_")
    return map_dict


def rename_gml(in_gml, out_gml, metadata):
    hmdb_map = get_mapping_dict(metadata)
    with open(in_gml, 'r') as f:
        with open(out_gml, 'w') as out:
            for line in f.readlines():
                if "HMDB" in line:
                    id = line.strip("\n").split(" ")[1].strip('"')
                    new_line = 'label "{}"\n'.format(hmdb_map[id])
                    out.write(new_line)
                else:
                    out.write(line)

# Step 1 - rename abundance file:

import PyPluMA
class GMLMapPlugin:
    def input(self, infile):
        inputfile = open(infile, 'r')
        self.parameters = dict()
        for line in inputfile:
            contents = line.strip().split('\t')
            self.parameters[contents[0]] = contents[1]

    def run(self):
        pass

    def output(self, outputfile):
        rename_gml(PyPluMA.prefix()+"/"+self.parameters["gmlfile"], outputfile, PyPluMA.prefix()+"/"+self.parameters["metadata"])


