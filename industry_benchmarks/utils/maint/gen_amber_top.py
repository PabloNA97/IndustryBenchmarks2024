#!/usr/bin/env python3

# Script to generate AMBER-compatible topology from an already fixed PDB file
from biobb_amber.leap.leap_gen_top import leap_gen_top
from biobb_amber.pdb4amber.pdb4amber_run import pdb4amber_run
from pathlib import Path
import argparse
import os

def main(input_pdb, force_field, output_folder):
    
    # Check input pdb exists
    if not os.path.exists(input_pdb):
        raise Exception("Input PDB file not found")
    
    # Make output folder if it does not exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    output_pdb_path = os.path.join(output_folder, f"{Path(input_pdb).stem}_pdb4amber.pdb")
    
    prop = {
        'remove_hydrogens': False,
        'remove_waters': False
    }
        
    pdb4amber_run(input_pdb_path=input_pdb,
              output_pdb_path=output_pdb_path,
              properties=prop)
    
    
    prop = {
        'forcefield': [force_field]
    }
    
    input_pdb = output_pdb_path
    output_pdb_path = os.path.join(output_folder, f"{Path(input_pdb).stem}_leap.pdb")
    output_top_path = os.path.join(output_folder, f"{Path(input_pdb).stem}.parmtop")
    output_crd_path = os.path.join(output_folder, f"{Path(input_pdb).stem}.crd")
    
    # Generate AMBER topology file
    leap_gen_top(input_pdb_path=input_pdb, output_pdb_path=output_pdb_path, output_top_path=output_top_path, 
                 output_crd_path=output_crd_path, properties=prop)
    
    return

if __name__ == "__main__":

    parser = argparse.ArgumentParser("AMBER top generation")
    
    parser.add_argument("-pdb", type=str, help="Path to the PDB file")
    parser.add_argument("-ff", type=str, help="Force field to use. Default: protein.ff14SB", default="protein.ff14SB")
    parser.add_argument("-o", type=str, help="Path to the output folder with AMBER topology files.")
    
    args = parser.parse_args()
    
    main(input_pdb = args.pdb, force_field = args.ff, output_folder = args.o)