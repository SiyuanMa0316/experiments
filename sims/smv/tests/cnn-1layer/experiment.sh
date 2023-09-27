#!/usr/bin/env bash
TESTS="/workspace/smaug/experiments/sims/smv/tests"
cd /workspace/smaug
# make all -j8
# make tracer -j8
cd ${TESTS}/cnn-1layer

. ./model_files

bmk_dir=`git rev-parse --show-toplevel`/../build/bin
num_PE=108
num_mac=64
# ${bmk_dir}/smaug-instrumented_${num_PE}PEs_${num_mac}macs \
#   ${topo_file} ${params_file} --sample-level=high --debug-level=2 --num-accels=1
${bmk_dir}/smaug-instrumented \
  ${topo_file} ${params_file} --sample-level=high --debug-level=2 --num-accels=1


cfg_home=`pwd`
gem5_dir=${ALADDIN_HOME}/../..
bmk_dir=`git rev-parse --show-toplevel`/../build/bin
output_dir=${cfg_home}/outputs_${num_PE}PEs_${num_mac}macs
# rm -r outputs_${num_PE}PEs_${num_mac}macs
mkdir -p ${output_dir}
echo "start simulation..."
# ${gem5_dir}/build/X86/gem5.opt \
#   --debug-flags=Aladdin,HybridDatapath \
#   --outdir=${output_dir} \
#   --stats-db-file=stats.db \
#   ${gem5_dir}/configs/aladdin/aladdin_se.py \
#   --num-cpus=2 \
#   --mem-size=4GB \
#   --mem-type=LPDDR4_3200_2x16  \
#   --sys-clock=1.25GHz \
#   --cpu-clock=2.5GHz \
#   --cpu-type=DerivO3CPU \
#   --ruby \
#   --access-backing-store \
#   --l2_size=2097152 \
#   --l2_assoc=16 \
#   --cacheline_size=32 \
#   --accel_cfg_file=gem5.cfg \
#   --fast-forward=10000000000 \
#   -c ${bmk_dir}/smaug_${num_PE}PEs_${num_mac}macs \
#   -o "${topo_file} ${params_file} --sample-level=high --gem5 --debug-level=0 --num-accels=1 --num-threads=1" \
#   > ${output_dir}/stdout 2> ${output_dir}/stderr

${gem5_dir}/build/X86/gem5.opt \
  --debug-flags=Aladdin,HybridDatapath \
  --outdir=${output_dir} \
  --stats-db-file=stats.db \
  ${gem5_dir}/configs/aladdin/aladdin_se.py \
  --num-cpus=2 \
  --mem-size=4GB \
  --mem-type=LPDDR4_3200_2x16  \
  --sys-clock=1.25GHz \
  --cpu-clock=2.5GHz \
  --cpu-type=DerivO3CPU \
  --ruby \
  --access-backing-store \
  --l2_size=2097152 \
  --l2_assoc=16 \
  --cacheline_size=32 \
  --accel_cfg_file=gem5.cfg \
  --fast-forward=10000000000 \
  -c ${bmk_dir}/smaug \
  -o "${topo_file} ${params_file} --sample-level=high --gem5 --debug-level=0 --num-accels=1 --num-threads=1" \
  > ${output_dir}/stdout 2> ${output_dir}/stderr

mv nnet_fwd_* ${output_dir}
# mv outputs outputs_${num_PE}PEs_${num_mac}macs