#!/usr/local/bin/python3

import math

# open data file for writing
datafile = open("data.json",'w')

# generates all partitions of a positive integer n
def accel_asc(n):
    a = [0 for i in range(L + 1)]
    k = 1
    y = L - 1
    while k != 0:
        x = a[k - 1] + 1
        k -= 1
        while 2 * x <= y:
            a[k] = x
            y -= x
            k += 1
        l = k + 1
        while x <= y:
            a[k] = x
            a[l] = y
            yield a[:k + 2]
            x += 1
            y -= 1
        a[k] = x + y
        y = x + y - 1
        yield a[:k + 1]

# targtal number of monomer units in system
L = 5

# container for configurations
# 1st index = number of unbound monomers
# 2nd index = number of separate units (i.e. a single monomer counts as a unit and a segment of arbirtary length also counts as a unit
tbl = []
for i in range(L+1):
    tbl.append([])
    for j in range(L):
        tbl[-1].append([])

for i in accel_asc(L):
    idx1 = i.count(1)
    idx2 = len(i) - 1
    tbl[idx1][idx2].append(i)

datafile.write( "{\n" )
datafile.write( "\t\"nodes\": [\n" )

## write node information

# counter for nodes
nodeCt = 0;
for i_idx, i_val in enumerate(tbl):
    for j_idx, j_val in enumerate(i_val):
        
        n_ustates = len(j_val)
        if n_ustates == 0: continue

        nodeCt += 1
        if nodeCt > 1: datafile.write( ",\n" )
        datafile.write( "\t\t{\n" )
        datafile.write( "\t\t\t\"id\": \"n{}\",\n".format(nodeCt) )
        datafile.write( "\t\t\t\"label\": \"{}\",\n".format(n_ustates) )
        datafile.write( "\t\t\t\"x\": {},\n".format(i_idx*0.1) )
        datafile.write( "\t\t\t\"y\": {},\n".format(j_idx*0.1) )
        datafile.write( "\t\t\t\"size\": {}\n".format(n_ustates) )
        datafile.write( "\t\t}" )
        
datafile.write( "\n\t],\n" )
datafile.write( "\t\"edges\": [\n" )


## write edge information

# counter for edges
edge_ct = 0

# counter for nodes
node_ct_src = 0 # source
# iterate over source nodes
for i_idx_src, i_val_src in enumerate(tbl):
    for j_idx_src, j_val_src in enumerate(i_val_src):
        
        # number of microstates lumped together at given node
        n_ustates = len(j_val_src)
        if n_ustates == 0: continue
        node_ct_src += 1

        target_driven = []
        target_nondriven = []
        for k_partition in j_val_src:
            prev_elem = math.nan
            for l_idx, l_elem in enumerate(k_partition):

                if l_elem == prev_elem: continue
                else: prev_elem = l_elem

                for m_idx in range(len(k_partition) - 1):
                    
                    chg_partition = k_partition[:]
                    del chg_partition[l_idx]
                    
                    chg_partition[m_idx] += l_elem
                    chg_partition.sort()

                    if l_elem == 1:
                        if target_driven.count(chg_partition) == 0:
                            target_driven.append(chg_partition)
                    else:
                        if target_driven.count(chg_partition) == 0:
                            target_nondriven.append(chg_partition)

        node_ct_targ = 0 # target
        # iterate over target nodes
        for i_idx_targ, i_val_targ in enumerate(tbl):
            for j_idx_targ, j_val_targ in enumerate(i_val_targ):
                
                # number of microstates lumped together at given node
                n_ustates = len(j_val_targ)
                if n_ustates == 0: continue
                node_ct_targ += 1

                if node_ct_targ >= node_ct_src: continue

                color = "nocolor"
                
                # total number of target partition matches with partitions in current node
                matches_curr_targ = 0
                for k_partition in j_val_targ:
                    match = target_nondriven.count(k_partition)
                    matches_curr_targ += match
                    if match > 0:
                        color = "#00f"
                        break
                for k_partition in j_val_targ:
                    match = target_driven.count(k_partition)
                    matches_curr_targ += match
                    if match > 0:
                        color = "#f00"
                        break

                if matches_curr_targ == 0: continue

                edge_ct += 1
                if edge_ct > 1: datafile.write( ",\n" )
                datafile.write( "\t\t{\n" )
                datafile.write( "\t\t\t\"id\": \"e{}\",\n".format(edge_ct) )
                datafile.write( "\t\t\t\"source\": \"n{}\",\n".format(node_ct_src) )
                datafile.write( "\t\t\t\"target\": \"n{}\",\n".format(node_ct_targ) )
                datafile.write( "\t\t\t\"color\": \"{}\"\n".format(color) )
                # datafile.write( "\t\t\t\"type\": \"curvedArrow\"\n" )
                datafile.write( "\t\t}" )

datafile.write( "\n\t]\n" )
datafile.write( "}\n" )
