import os
import sys
import re

print('Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv))

host_ticks_per_cycle=1000
#dir = str(sys.argv[1])
dma_cycle_sum=0
dma_start_cycle=0
dma_end_cycle=0
fout = open("/dma_extracted.txt", "w")
if os.path.isfile("stdout"):
    f = open("stdout")
    for line in f:
        if "DMA Accesses" in line:
            words = line.split()
            # print(words[2])
            dma_start_cycle = int(re.sub(":","",words[0]))
            # kernel_invokes+=1
            fout.write(line)
        if "dmaCompleteCallback" in line:
            words = line.split()
            # print(words[2])
            dma_end_cycle = int(re.sub(":","",words[0]))
            dma_cycle_sum+=(dma_end_cycle-dma_start_cycle)
            fout.write(line)
    # print("kernel invokes:" + str(kernel_invokes))
    dma_cycle_sum/=host_ticks_per_cycle
    print("total dma cycles: "+str(dma_cycle_sum))

fout.close()