from SpeciesTreeSimulator import SpeciesTreeGenerator
from GenomeSimulator import GenomeSimulator
from SequenceSimulator import SequenceSimulator
import AuxiliarFunctions as af
import argparse
import os
import sys

class simuLyon():

    def __init__(self):

        self.tree_parameters = dict()
        self.genome_parameters = dict()
        self.sequence_parameters = dict()


    def T(self, parameters_file, experiment_folder, advanced_mode):

        tree_folder = os.path.join(experiment_folder, "T")

        if advanced_mode == "i":

            # In this case the input is a tree file
            tree_file = parameters_file
            print("Generate events for input file %s" % tree_file)

            stg = SpeciesTreeGenerator({})
            stg.start()
            stg.events = af.generate_events(tree_file)

            whole_tree_file = os.path.join(tree_folder, "WholeTree.nwk")
            #extant_tree_file = os.path.join(tree_folder, "ExtantTree.nwk")
            events_file = os.path.join(tree_folder, "Events.tsv")

            stg.generate_whole_tree()
            #stg.generate_extant_tree()

            #stg.write_whole_tree(whole_tree_file)
            #stg.write_extant_tree(extant_tree_file)
            stg.write_events_file(events_file)

            return 0

        else:

            parameters = af.prepare_species_tree_parameters(af.read_parameters(parameters_file))
            stg = SpeciesTreeGenerator(parameters)

        run_counter = 0
        success = False

        while success == False and run_counter <= 50:
            run_counter+=1
            print("Computing Species Tree. Trial number %s" % str(run_counter))
            if advanced_mode == "0":
                success = stg.run()
            if advanced_mode == "a":
                success = stg.run_a()
            if advanced_mode == "b":
                success = stg.run_b()
            if advanced_mode == "p":
                success = stg.run_p()

        if run_counter >= 50:
            print("Aborting computation of the Species Tree. Please use other speciation and extinction rates!")
            return 0

        whole_tree_file = os.path.join(tree_folder, "WholeTree.nwk")
        extant_tree_file = os.path.join(tree_folder, "ExtantTree.nwk")
        events_file = os.path.join(tree_folder, "Events.tsv")
        stg.generate_whole_tree()
        stg.generate_extant_tree()
        stg.write_whole_tree(whole_tree_file)
        stg.write_extant_tree(extant_tree_file)
        stg.write_events_file(events_file)

        if advanced_mode == "b" or advanced_mode == "a":
            rates_file = os.path.join(tree_folder, "Rates.tsv")
            stg.write_rates(rates_file)


    def G(self,parameters_file, experiment_folder, advanced_mode):

        parameters = af.prepare_genome_parameters(af.read_parameters(parameters_file))
        events_file = os.path.join(experiment_folder, "T/Events.tsv")
        genome_folder = os.path.join(experiment_folder, "G")

        genomes_folder = os.path.join(genome_folder, "Genomes")
        gene_families_folder = os.path.join(genome_folder, "Gene_families")
        gene_trees_folder = os.path.join(genome_folder, "Gene_trees")
        events_per_branch_folder = os.path.join(genome_folder, "Events_per_branch")
        profiles_folder = os.path.join(genome_folder, "Profiles")

        gss = GenomeSimulator(parameters, events_file)

        if advanced_mode == "0":
            gss.run()
        elif advanced_mode == "a":
            gss.run_a()
        elif advanced_mode == "b":
            gss.run_b()
        elif advanced_mode == "s":
            gss.run_s()
        elif advanced_mode == "u":
            gss.run_u()

        print("Writing Genomes")
        gss.write_genomes(genomes_folder)
        print("Writing Profiles")
        gss.write_profiles(profiles_folder)
        print("Writing Gene Families")
        gss.write_gene_family_events(gene_families_folder)
        print("Writing Events Per Branch")
        gss.write_events_per_branch(events_per_branch_folder)
        print("Writing Gene Trees")
        gss.write_gene_trees(gene_trees_folder)


    def S(self, parameters_file, experiment_folder, advanced_mode):


        gene_trees_folder = os.path.join(experiment_folder, "G/Gene_trees")
        sequences_folder = os.path.join(experiment_folder, "S/Sequences")

        if not os.path.isdir(sequences_folder):
            os.mkdir(sequences_folder)

        parameters = af.prepare_sequence_parameters(af.read_parameters(parameters_file))

        print("Preparing simulator of sequences")

        ss = SequenceSimulator(parameters)

        whole_trees = [x.replace("_pruned","_whole") for x in os.listdir(gene_trees_folder) if "pruned" in x]

        for tree_file in whole_trees:

            tree_path = os.path.join(gene_trees_folder, tree_file)

            print("Simulating sequence for gene family %s" % tree_file.split("_")[0])

            ss.run(tree_path, sequence_folder)



if __name__ == "__main__":


    parser = argparse.ArgumentParser()
    parser.add_argument("mode", type=str, choices=["T","Ti","Ta","Tb","Tp","S","G"], help="Mode")
    parser.add_argument("params",  type=str, help="Parameters file")
    parser.add_argument("output", type=str, help="Name of the experiment folder")

    args = parser.parse_args()

    mode, parameters_file, experiment_folder =  args.mode, args.params, args.output

    if len(mode) == 1:
        main_mode = mode[0]
        advanced_mode = "0"

    elif len(mode) == 2:
        main_mode = mode[0]
        advanced_mode = mode[1]

    else:
        print ("Incorrect value for mode")

    SL = simuLyon()

    if main_mode == "T":

        if not os.path.isdir(experiment_folder):
            os.mkdir(experiment_folder)

        if not os.path.isdir(os.path.join(experiment_folder,"T")):
            os.mkdir(os.path.join(experiment_folder, "T"))

        SL.T(parameters_file, experiment_folder, advanced_mode)

    elif main_mode == "G":

        genome_folder = os.path.join(experiment_folder, "G")

        if not os.path.isdir(genome_folder):
            os.mkdir(genome_folder)

        SL.G(parameters_file, experiment_folder, advanced_mode)

    elif main_mode == "S":

        sequence_folder = os.path.join(experiment_folder, "S")

        if not os.path.isdir(sequence_folder):
            os.mkdir(sequence_folder)

        SL.S(parameters_file, experiment_folder, advanced_mode)


    else:
        print("Incorrect usage. Please select a mode: T, G or S")

