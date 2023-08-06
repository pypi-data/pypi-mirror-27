#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 16:59:32 2017

@author: songz
"""
from __future__ import print_function
from __future__ import division
def main():
    import argparse
    from FUNGuild import funguilds as gd
    import sys
    
    parser = argparse.ArgumentParser()
    otu_input = parser.add_mutually_exclusive_group()
    otu_input.add_argument('-otu', help='Filename of the OTU table, it can be in the format of either BIOM-JSON or tab-delimited.')
    otu_input.add_argument('-taxa', help='Instead of OTU table, you can use the output of -taxaout.')
    parser.add_argument('-format', choices=['biom', 'biom-json', 'tab', 'tab-delimited'], default='tab', \
                         help='Specify the file format. FUNGuild supports BIOM-JSON or tab-delimited forms. This option only appied to -otu')
    parser.add_argument('-database', choices=['fungi', 'nematode', 'Fungi', 'Nematode'], default='fungi', \
                         help='Specify the database. FUNGuild supported "Fungi" and "Nematode" database, in default \
                         it was set to fungal database')
    parser.add_argument('-taxa_column', default='taxonomy', help='Specify the name of the taxonomic column. By default \
                        it is set to be "taxonomy".')
    parser.add_argument('-taxa_out', help='Specify the filename to save the parsed taxa data. If this option is not used \
                        FUNGuild will not output any taxa data.')
    parser.add_argument('-guild_out', default='guilds.txt', help='Specify the filename to save the functional data. \
                        The output is a tab-delimited file with taxa and functional information.')
    
    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)
    
    args = parser.parse_args()
    
    otu_format = args.format
    db_name = args.database
    taxa_column = args.taxa_column
    taxa_out = args.taxa_out
    guild_out = args.guild_out
    
    # Read in the OTU table and try to parse its taxonomy information
    if args.otu:
        taxa = gd.taxa_parser(args.otu, otu_format = otu_format, taxa_column = taxa_column)
    else:
        taxa = args.taxa
    
    # If the user specify the output name for taxa, write to file
    if taxa_out:
        pass
    else:
        gd.write_taxa(taxa, taxa_out)
    
    # Read in the database
    db = gd.load_database(database_name = db_name)
    
    # Search the database for known functions
    function = gd.guild_parser(taxa, db)
    
    # Write the taxa + function result to file
    gd.write_function(taxa, function, guild_out)

if __name__ == '__main__':
    main()