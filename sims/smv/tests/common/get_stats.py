import os
import sys

print('Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv))

dir = str(sys.argv[1])
accelerator_cycle_sum=0
kernel_invokes=0
if os.path.isfile(dir+"/nnet_fwd_summary"):
    f = open(dir+"/nnet_fwd_summary")
    for line in f:
        if line.startswith("Cycle"):
            words = line.split()
            # print(words[2])
            accelerator_cycle_sum += int(words[2])
            kernel_invokes+=1
    print("kernel invokes:" + str(kernel_invokes))
    print("total kernel cycles: "+str(accelerator_cycle_sum))
else:
    i=0
    while os.path.isfile(dir+"/nnet_fwd_"+str(i)+"_summary"):
        kernel_invokes=0
        accelerator_cycle_sum=0
        f = open(dir+"/nnet_fwd_"+str(i)+"_summary")
        for line in f:
            if line.startswith("Cycle"):
                words = line.split()
                # print(words[2])
                accelerator_cycle_sum += int(words[2])
                kernel_invokes+=1
        print("acc"+str(i)+" kernel invokes:" + str(kernel_invokes))
        print("acc"+str(i)+" total kernel cycles: "+str(accelerator_cycle_sum))
        i+=1

f = open(dir+"/stats_extracted.txt", "w")
host_ticks_per_cycle=1000
host_cycle_sum=0
for line in open(dir+"/stats.txt"):
    if line.startswith("# Stats desc") or line.startswith("final_tick") or line.startswith("sim_ticks")\
        or line.startswith("system.ruby.l1_cntrl0.L1Dcache.demand_accesses") \
        or line.startswith("system.ruby.l1_cntrl0.L1Dcache.demand_hits")\
        or line.startswith("system.ruby.l1_cntrl0.L1Dcache.demand_misses")\
        or line.startswith("system.switch_cpus.iq.fu_busy_cnt")\
        or line.startswith("system.switch_cpus.iq.fu_busy_rate")\
        or line.startswith("system.switch_cpus.commit.op_class_0::MemRead")\
        or line.startswith("system.switch_cpus.commit.op_class_0::MemWrite")\
        or line.startswith("system.switch_cpus.commit.op_class_0::FloatMemRead")\
        or line.startswith("system.switch_cpus.commit.op_class_0::FloatMemWrite")\
        or line.startswith("system.switch_cpus.commit.fp_insts")\
        or line.startswith("system.switch_cpus.commit.int_insts"):
        f.write(line)
    if line.startswith("sim_ticks"):
        words = line.split()
        host_cycle_sum+=int(words[1])
    if line.endswith("end"):
        words = next()
host_cycle_sum/=1000
print("total host cycles: "+str(host_cycle_sum))
f.write("total host cycles: "+str(host_cycle_sum))
f.close()

data_prep_cycle_sum=0
data_final_cycle_sum=0
data_reorder_cycle_sum=0
with open(dir+"/stats.txt") as f:
    lines = f.readlines()
    for i in range(len(lines)):
        if lines[i].startswith("# Stats desc: Tensor preparation end"):
            for j in range(i,len(lines)):
                if lines[j].startswith("sim_ticks"):
                    words = lines[j].split()
                    data_prep_cycle_sum+=int(words[1])
                    break
        if lines[i].startswith("# Stats desc: Tensor finalization end"):
            for j in range(i,len(lines)):
                if lines[j].startswith("sim_ticks"):
                    words = lines[j].split()
                    data_final_cycle_sum+=int(words[1])
                    break
        if lines[i].startswith("# Stats desc: Reordering end"):
            for j in range(i,len(lines)):
                if lines[j].startswith("sim_ticks"):
                    words = lines[j].split()
                    data_reorder_cycle_sum+=int(words[1])
                    break
data_prep_cycle_sum/=1000
data_final_cycle_sum/=1000
data_reorder_cycle_sum/=1000
print("data preparation cycles:"+str(data_prep_cycle_sum))
print("data finalization cycles:"+str(data_final_cycle_sum))
print("data reordering cycles:"+str(data_reorder_cycle_sum))