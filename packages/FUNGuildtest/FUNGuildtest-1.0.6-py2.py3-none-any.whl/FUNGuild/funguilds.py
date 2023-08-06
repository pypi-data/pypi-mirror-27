#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 16:59:32 2017

These are the functions used by FUNGuild.

@author: songz
"""
from __future__ import print_function
from __future__ import division
import requests
import json
import pandas as pd
#%%
# Load the Mongo database into memory
# Default is fungal database, another option is "nematode"
# The data is saved as Python dictionary, with the taxon as keywords.
def load_database(database_name = 'fungi'):
    if database_name == 'fungi':
        url = 'http://www.stbates.org/funguild_db.php'
        print('Connecting with FUNGuild database ...')
    elif database_name == 'nematode':
        url = 'http://www.stbates.org/nemaguild_db.php'
        print('Connecting with Nematode database ...')
    
    print('This may take a minute ...')
    db_url = requests.get(url)
    db_url = db_url.content.decode('utf-8').split('\n')[6].strip('[').strip(']</body>').replace('} , {', '} \n {').split('\n')
    db = []
    for record in db_url:
        current_record = json.loads(record)
        if current_record['taxonomicLevel'] == 20: # If species level
            current_record['taxon'] = current_record['taxon'].replace(' ', '_')
        db.append(current_record)

    print('Current database has {0} records.'.format(len(db)))
    # Build the search dictinary using taxon as keywords
    search_dict = {}
    for item in db:
        search_dict[item['taxon']] = item
    return search_dict
#%%
# Read in user's OTU table and identify all taxonomy data
# The table can be in BIOM-JSON format (due to the compatibility to Windows, only JSON version is supported),
# or in tab-delimited form.
# Due to the wide variability of the form of OTU data, instead of trying to parse every posibilities,
# we leave this duty of format control to users by supoprting the two most common formats.
# Again, it is impossible for us to provide a solution for parsing all taxonomic formats.
# Instead, we use this as a check point for the users.
# We support here the format used by QIIME and UNITE (and most of other program), in which taxonomy is written as:
#k__XXX;p__XXX;c__XXX;o_XXX;f__XXX;g__XXX;s__XXX
# For species, we anticipate that it is Genus_Species (so genus name and species name connect with a underscore)
def taxa_parser(otu_file, otu_format = 'biom-json', taxa_column = 'taxonomy'):
    if otu_format == 'tab-delimited' or otu_format == 'tab':
        otu = pd.read_csv(otu_file, sep='\t', header=0, index_col=0, comment='#')
        otu_id = list(otu.index)
        taxa = list(otu[taxa_column]) # Save the taxa information
        taxa = pd.DataFrame(taxa, index=otu_id, columns=['taxonomy'])

    elif otu_format == 'biom-json' or otu_format == 'biom':
        otu = json.loads(open(otu_file).read())
        taxa = []
        otu_id = []
        for line in otu['rows']:
            taxa.append(line['metadata'][taxa_column])
            otu_id.append(line['id'])
        taxa = pd.DataFrame(taxa, index=otu_id, columns=['taxonomy'])
    else:
        print('Please enter the right OTU table format.')
        taxa = pd.DataFrame()

    # Parse the taxonomy column into separated taxa levels
    taxa_level = []
    taxa_otu = []
    taxa_dict = []
    level = ['k', 'p', 'c', 'o', 'f', 'g', 's']
    for record in taxa.iterrows():
        current_otu = record[0] # This is the name of the current OTU
        taxa_string = record[1][taxa_column].split('|') # This is the taxonomy

        if len(taxa_string) == 6: # The string has the UNITE label beofore the run of taxonomy
            taxa_string = taxa_string[5].split(';')
        elif len(taxa_string) == 1: # The string only have taxonomy
            taxa_string = taxa_string[0].split(';')

        taxa_string = [i[3:] for i in taxa_string] # Remove the k__, f__, g__ prefix
        taxa_otu.append(current_otu)
        taxa_level.append(taxa_string)
        
        # Build a list for taxa, taxonomy is saved in a dictionary. The order of OTUs are kept in this way.
        # [OTU name, {}]        
        d = {}
        for l, v in zip(level, taxa_string):
            d[l] = v
        taxa_dict.append([record[0], d])
    print('Found {0} OTUs in the provided table.'.format(len(taxa_dict)))
    return taxa_dict


#%% Write the taxa data to file
def write_taxa(taxa, output_file):
    level = ['k', 'p', 'c', 'o', 'f', 'g', 's']
    output = [['OTU_ID'] + ['Kingdom', 'Phylum', 'Class', 'Order', 'Family', 'Genus', 'Species']]
    for item in taxa:
        current_line = [item[0]]
        for l in level:
            current_line.append(item[1][l])
        output.append(current_line)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for line in output:
            f.write('%s\n' % '\t'.join(line))
    print('Parsed taxa wrote to {0}.'.format(output_file))
    return None    


#%% Load the taxa file as the input of guild_parser()
# The file must be the output of write_taxa()
def load_taxa(input_file):
    level = ['k', 'p', 'o', 'c', 'f', 'g', 's']    
    taxa = []
    with open(input_file, 'r') as f:
        for line in f:
            taxa.append(line.strip('\n').split('\t'))
        taxa = taxa[1:] # Read in all data except the header
    
    taxa_dict = []
    for item in taxa:
        d = {}
        for t, l in zip(item[1:], level):
            d[l] = t
        taxa_dict.append(item[0], d)
    return taxa_dict

    
#%%
# Use the output of taxa_parser() as input, output the FUNGuild stype results.
# This result will have the same order (in terms of OTU) as the original OTU table,
# so users can attach the additional column to the orginal table,
# or use it separately.
# For the given OTU's taxonomy, search for database keywords
# The search will start from species to phylum (although most of the records are below the level of Family)
def guild_parser(taxa, database):
    level = ['s', 'g', 'f', 'o', 'c', 'p', 'k']
    output_columns = ['taxon', 'taxonomicLevel', 'trophicMode', 'guild', 'trait',\
                      'growthForm', 'confidenceRanking', 'notes', 'citationSource']
    
    taxa_function = []
    count = 0
    for record in taxa:
        current_record = [record[0]]
        checker = 0
        for l in level: # Start search from the lowest (species) level
            if checker == 1:
                break
            else:
                try:
                    current_function = database[record[1][l]] # If current level is in the database
                    for item in output_columns:
                        current_record.append(current_function[item])
                    checker = 1 # Stop at the lowest matching level
                    count += 1
                except KeyError:
                    pass
        if len(current_record) == 1: # if no matching record
            for item in output_columns:
                current_record.append('na')
        else:
            pass
        taxa_function.append(current_record) 
    print('Found matching record for {0} OTUs.'.format(count))
    return taxa_function


#%% Write the FUNGuild result to file
def write_function(taxa, function, output_file):
    level = ['s', 'g', 'f', 'o', 'c', 'p', 'k']
    output_columns = ['taxon', 'taxonomicLevel', 'trophicMode', 'guild', 'trait',\
                      'growthForm', 'confidenceRanking', 'notes', 'citationSource']
    header = ['OTU', 'Kingdom', 'Phylum', 'Order', 'Class', 'Family', 'Genus', 'Species'] + output_columns
    output = [header]
    for taxonomy, function in zip(taxa, function):
        current_taxa = [taxonomy[0]]
        for l in level[::-1]:
            current_taxa.append(taxonomy[1][l])
        current_line = current_taxa + function[1:]
        output.append(current_line)
    
    #% Output the results
    with open(output_file, 'w') as f:
        for line in output:
            f.write('%s\n' % '\t'.join([str(i) for i in line]))
    print('FUNGuild results wrote to {0}.'.format(output_file))
    return None


#%% Generate an example OTU table file
def example():
    otu = ['OTU ID\tsample1\tsample2\tsample3\tsample4\tsample5\ttaxonomy\n',\
 'OTU_100\t0\t1\t0\t0\t0\t93.6%|Laetisaria_fuciformis|EU118639|SH012042.06FU|reps_singleton|k__Fungi;p__Basidiomycota;c__Agaricomycetes;o__Corticiales;f__Corticiaceae;g__Laetisaria;s__Laetisaria_fuciformis\n',\
 'OTU_1002\t95\t127\t183\t10\t121\t100%|Leptodontidium_sp|FJ552955|SH209316.06FU|refs|k__Fungi;p__Ascomycota;c__Leotiomycetes;o__Helotiales;f__Incertae_sedis;g__Leptodontidium;s__Leptodontidium_sp\n',\
 'OTU_1003\t1\t0\t1\t0\t0\t79.31%|uncultured_fungus|KC966088|SH441311.06FU|reps_singleton|k__Fungi;p__unidentified;c__unidentified;o__unidentified;f__unidentified;g__unidentified;s__uncultured_fungus\n',\
 'OTU_1008\t9\t3\t0\t0\t1\t97.09%|Helotiaceae_sp|FJ475546|SH195739.06FU|reps|k__Fungi;p__Ascomycota;c__Leotiomycetes;o__Helotiales;f__Helotiaceae;g__unidentified;s__Helotiaceae_sp\n',\
 'OTU_1011\t2\t12\t18\t0\t12\t81.96%|Entrophospora_sp_JJ38|AY035644|SH431532.06FU|reps_singleton|k__Fungi;p__Glomeromycota;c__Glomeromycetes;o__Diversisporales;f__Acaulosporaceae;g__Entrophospora;s__Entrophospora_sp_JJ38\n',\
 'OTU_1015\t29\t9\t0\t0\t8\t100%|uncultured_fungus|KC965399|SH451013.06FU|reps_singleton|k__Fungi;p__unidentified;c__unidentified;o__unidentified;f__unidentified;g__unidentified;s__uncultured_fungus\n',\
 'OTU_1018\t0\t0\t2\t0\t0\t96.97%|uncultured_Ascomycota|FN562038|SH449221.06FU|reps_singleton|k__Fungi;p__Ascomycota;c__unidentified;o__unidentified;f__unidentified;g__unidentified;s__uncultured_Ascomycota\n',\
 'OTU_1021\t1\t0\t28\t289\t267\t100%|Massarina_sp_JP_2013|JX981477|SH018317.06FU|reps_singleton|k__Fungi;p__Ascomycota;c__Dothideomycetes;o__Pleosporales;f__Massarinaceae;g__Massarina;s__Massarina_sp_JP_2013\n',\
 'OTU_1023\t0\t0\t3\t0\t0\t100%|Scleroderma_areolatum|EU784408|SH434269.06FU|reps_singleton|k__Fungi;p__Basidiomycota;c__Agaricomycetes;o__Boletales;f__Sclerodermataceae;g__Scleroderma;s__Scleroderma_areolatum\n',\
 'OTU_1024\t1\t1\t0\t0\t0\t100%|Derxomyces_sp_LTD_2009a|AB508840|SH457761.06FU|reps_singleton|k__Fungi;p__Basidiomycota;c__Tremellomycetes;o__Tremellales;f__Incertae_sedis;g__Derxomyces;s__Derxomyces_sp_LTD_2009a\n']
    with open('otu.txt', 'w') as f:
        for line in otu:
            f.write('%s' % line)
    print('An example OTU table was written to otu.txt.')