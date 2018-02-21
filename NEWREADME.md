﻿
## SimuLyon (working name) 
##### A new tool to simulate genome evolution accounting for dead lineages

----------

### **Introduction** ###

SimuLyon is a simulator of species tree and genome evolution that accounts for extinct lineages. This feature makes it especially interesting for those studying organisms in which there exists Lateral Gene Transfers, since transfer events can take place between lineages that have left no surviving descendants.
SimuLyon uses a Birth-death model to generate a species tree. Different functions are included to generate species tree with non-constant rates of speciation and extinction. Then it simulates the evolution of gene families along this species tree. Gene families can be already present in the stem branch or appear with a given rate of origination along the different branches of the species tree. Genes can evolve through events of duplication, loss and transfer. SimuLyon also can account for the fact that transfers occur preferentially between closely related lineages. It presents a detailed output of the genome evolution including the total number of families that have gone extinct and the ancestral genomes of the different inner nodes in the species tree.  Finally, the sequence of the different genes is simulated along the different gene families, considering also that substitution rates can change widely over time.
SimuLyon can be of great interest to those who want to test different evolutionary hypothesis under simulations and need to use a fast and easy to use tool to generate species, gene trees and sequences.


Please read the manual before using it. I know you are in a hurry but it only takes around 15 minutes of your time. If you are really in a hurry
then just follow the **Example 1**.

Writen by Adrián A. Davín 

contact to aaredav@gmail.com

----------

Watch out! simuLyon is **unfinished**. Many of the functions explained in this manual
have not tested yet and some others are not even written.

**Everything explained in the Example 1 should be working though** 

========================================================================


### **Usage** ###

You need **python 3.6** installed with **ETE3** and **numpy**

There are **three** modes to run simuLyon. **T** (species Tree) and **G** (Genomes) 
(and we will write a third one for sequences, **S**) 

The order to obtain a complete dataset is 

 1. Species Tree
 2. Genomes
 3. Sequences

This means that if you want to get to the last point you must first compute the 2 first points. So, the very first thing you have to do is running simuLyon to create a species tree using simply

    python simuLyon.py T SpeciesTreeParameters.tsv /Output_folder

The Species Tree will be created in the /Output folder, along some other useful files (this is explained in the Output section of this manual)
Very frequently you will be interested in having a Species Tree that contains only extant species and potentially, only a fraction of all the surviving lineages.

For doing that, we resort to the script **sampLyon.py**. This script is going to prune and sample the different trees generated. For running it you can use:

    python sampLyon.py T /previous_Output_folder Sample_name N
    
T indicates the mode (prune and sample species Tree), then we input the folder we created before, we give a name to this sample and finally we introduce the fraction (N)
of species that will be sampled.

Then, you can simulate the evolution of genomes in that species tree using:

    python simuLyon.py G GenomeParameters.tsv /previous_Output_folder

Make sure that the Output_folder is the same that you were using when you generated the Species Tree! 
simuLyon will simulate the evolution of gene inside the whole species tree and it will print a very detailed
information about the evolution of those genes.

Once you have done that, if you are interested in using the gene trees you *have to* run sampLyon this way: 

    python sampLyon.py G /previous_Output_folder /previous_Sample_name

This will cut the gene trees removing extinct species and other species that were not including in the sampled

Go to Example 1 for more details    
 
    
**Note to anyone who has already used simuLyon before**

_The way I included this sampLyon thing is because I realized that pruning the tree is a big bottleneck when working with really big
datasets. And yes, I have to make that more intuitive... working on that_


Then, the sequences are simulated on the gene trees. *This is not written yet!*


### **Output** ###

##### Mode T


*WholeTree:* The whole species tree including the dead lineages, in newick format

*ParametersLog.tsv*: Parameters used to run the simulation

*SpeciesTreeEvents.tsv*: Events (speciation and extinction) taking place in the species tree

*LineagesInTime.tsv*: Lineages alive in each unit of time (I have to change the format to make it more efficient)

#### Mode G

*Profiles.tsv*: Tsv including the number of copies present of each family for each node of the whole tree

*RawGeneFamilies*: Folder including all the gene trees of evolving inside the species tree. Each gene family has an
events.tsv associated with the detailed list of events taking place in that family

*Transfers.tsv*: A complete list of the transfer events, with donor and recipients

#### Mode S 

### Examples 

#### Example 1 - Simulating a standard dataset with duplications, transfers and losses ####

First thing we do is we are going to change the parameters of the Species Tree.
 For that we create a new file using:
 
     cp SpeciesTreeParameters.tsv   example1_SpeciesTreeParameters.tsv
        
We are going to change also the speciation rate to a fixed number of 10 and the extinction rate to 3.
 For that we make SPECIATION_P0 = 10 and EXTINCTION_P0 = 3. Once we have changed that, we can run the command
        
     python simuLyon.py T example1_SpeciesTreeParameters.tsv EXAMPLE_1
   
 Then we can go to the folder /EXAMPLE_1 and inspect the files that have been created there.
 
 The resulting tree has 793 extant lineages and it can be found in the file /EXAMPLE_1/WholeTree
 
 Once we have done that, let us prune the tree to one containing 20% of the surviving lineages.
 For that we run:
 
      python sampLyon.py T EXAMPLE_1 /SAMPLE20 0.2       
 
 This will sample randomly 20% of the living species and will write the pruned tree
 on the folder SAMPLE20, inside the folder EXAMPLE_1
  
 Then we want to simulate the evolution of genes inside the species tree.
 
 We will change the default parameters. We will use as rates 0.1 for duplications, 0.2 for transfers and 0.3 for losses.
 For that we do:
 
     cp GenomeParameters.tsv   example1_GenomeParameters.tsv
    
 And then modify DUPLICATION_P0 = 0.1, TRANSFER_P0 = 0.2, LOSS_P0 = 0.3
 
 We will simulate 10 families already present in the root and 500 more families. For that we change STEM_FAMILIES = 10 and 
 N_FAMILIES = 500
 
 Finally, we launch simuLyon using the command
  
     python simuLyon.py G example1_GenomeParameters.tsv EXAMPLE_1
     
 This will produce the raw gene families in the folder EXAMPLE_1/RawGeneFamilies
 
 To obtain the genes presented in the species we sampled before, we resort again to sampLyon
 
     python sampLyon.py G  EXAMPLE_1 SAMPLE20
     
 This will prune the species tree of the gene families. The end result can be found
 in the folder SAMPLE20 
       
  

#### Example 2 - Simulating a dataset with a massive extinction event NOT FINISHED YET####

In this example we will simulate a dataset in which a massive extinction event takes between
time 0.6 and time 0.7.

 First thing we do is we are going to change the parameters of the Species Tree.
 For that we create a new file using:
 
     cp SpeciesTreeParameters.tsv   example2_SpeciesTreeParameters.tsv
     
 Then we are going to open example1_SpeciesTreeParameters.tsv in any text editor and modify
 SPECIES_EVOLUTION_MODE to 4 (user defined rates).
 
 We are going to change also the speciation rate to a fixed number of 10 and the extinction rate to 3.
 For that we make SPECIATION_P0 = 10 and EXTINCTION_P0 = 3  
 
 Then we are going to use the file massive_extinction.tsv included in the folder SimuLYON/Example/1
 
 If we open it we see a single line, that includes in this order:
 
 The beginning of the rate change, the end of the rate change, the number by which the speciation rate is multiplied
 during that period and the number by which the extinction rate is multiplied during that period.
 
 In plain words, the file says that during the time 0.6 and until time 0.7, the speciation rate is maintained the same (multiplied by 1)
 and the extinction rate is multiplied by 15.
 
 We need to modify then the example1_SpeciesTreeParameters.tsv to include also USER_DEFINE_RATES = path_to_massive_extinction.tsv
 
 Once we have done that, we can run simuLyon by using:
 
 
     python simuLyon.py T example1_SpeciesTreeParameters.tsv EXAMPLE_2 
     
 

### Parameters ###

You can change the parameters directly in the tsv files. Watch out, it is a tabular separated values file, so you do not want mess spaces and tabs. In the case you do not understand what a parameter does, you do not want to touch it.
 

#### Global parameters ####

This parameters are found in the python script and you are strongly encouraged not to change them

**TOTAL_TIME**
The total distance from the root of the species tree and the present time and the present. It is 1 by default. 

**TIME_INCREASE**

The size of the discretized time units. It is 0.0001 by default and recommended. A smaller number will produce more fine-grained scenarios at a larger computational cost. Think carefully before changing this.

**SEED**

The seed used, to make reproducible the results. 

#### Species evolution ####

**SPECIES_EVOLUTION_MODE**

 - 0: Global rates of speciation and extinction 
 - 1: Lineage-specific rates (time and lineage autocorrelated)
 - 2: Lineage-specific rates (lineage autocorrelated)
 - 3: Lineage-specific rates (uncorrelated)
 - 4: User defined rates

**STOPPING_RULE**

 - 0: Time stops arriving at TOTAL_TIME
 - 1: Tree evolves until a total of species = N_LINEAGES (extinct and alive) have been generated
 - 2: Tree evolves until a total of species = N_LINEAGES (extinct) have been generated
 - 3: Tree evolves until a total of species = N_LINEAGES (alive) have been generated
 
**REESCALE**

- 0: No reescale is performed in the whole tree
- 1: A reescale to 1 is performed in the whole tree. Used in combination with the stopping rules 1,2 and 3

**SPECIES_NUMBER**

To use in combination with the stopping rules 1,2 or 3

**SPECIATION_RATE**
 Speciation rate, measured in mean number of speciation per unit of time  

**EXTINCTION_RATE**
 Extinction rate, measured in mean number of speciation per unit of time   

**USER_DEFINED_RATES**
File containing the multipliers on the speciation and the extinction rate per unit of time, to be used when the species tree is simulated in mode 4
The format is (separated by tabs)
time_start	time_end	spec_mult	ext_mult	
See example 1 for more information

#### Genome evolution ####

**GENOME_EVOLUTION_MODE**

- 0: Families are simulated independently of each other
- 1: Families evolve simultaneously

**STOPPING_RULE**

Both stopping rules only apply to GENOME_EVOLUTION_MODE = 0
For GENOME_EVOLUTION_MODE = 1 you have to input an origination rate and an initial number of families

 - 0: A fixed number of gene families will be simulated == N_FAMILIES. Notice that gene families introduced by STEM_FAMILIES are not accounted for in the above computation
 - 1: Families will be simulated until the mean size of genomes >=  MEAN_SIZE_GENOME. 
 
**GENE_EVOLUTION_MODE**

 - 0: Global rates 
 - 1: Family-wise rates
 - 2: Lineage-specific rates (time and lineage autocorrelated)
 - 3: Lineage-specific rates (lineage autocorrelated)
 - 4: Lineage-specific rates (uncorrelated)
 - 5: User defined rates

**DUPLICATION_D, TRANSFER_D, LOSS_D, REPLACEMENT_D**

Distribution probability for each type of event

 - **fixed**: In this case, the value of the corresponding parameter 0 will be use as the rate. For example, if you are planning to use a constant rate of 0.5 for duplications you must use: duplication_d = fixed ; duplication_p0 = 0.5
 - **uniform**: The value will be sampled from an uniform distribution between the corresponding values of p0 and p1. For example, if you want the duplication rate is randomly sampled from an uniform distribution U(3,5) you should use duplication_d = uniform; duplication_p0 = 3; duplication_p1 = 5.
 - **normal**: The value will be sampled from a normal distribution between the corresponding values of p0 and p1. For example, if you want the duplication rate is randomly sampled from an normal distribution N(3,5) you should use duplication_d = normal; duplication_p0 = 3; duplication_p1 = 5.

**STEM_FAMILIES**
Number of gene families already in the stem clade

**STEM_LENGTH**
If different from 0, a stem of length STEM_LENGTH is added to the root. In this stem the origination of new gene families occur with a probability proportional to its length. NOT WRITTEN YET!!

**TRANSFER_CLOSE_SPECIES**  

If True (1), transfers take place preferentially between closely related species. When a transfer event occurs, the recipient is chosen randomly among all coexisting lineages with a probability inversely proportional to the logarithm of the evolutionary distance between the two clades.  NOT WRITTEN YET!!

#### Sequence evolution ####

**SEQUENCE_EVOLUTION_MODE**

 - 0: No heterogeneity
 - 1: Lineage-specific heterogeneity (time and lineage autocorrelated)
 - 2: Lineage-specific heterogeneity (lineage autocorrelated)
 - 3: Lineage-specific heterogeneity (uncorrelated)
 - 4: User defined heterogeneity