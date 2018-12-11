# PipeLayer is not applicable for emulator simulations, as their outer product
# requires ReRam access and thereby compiler access

## Use this for MLP benchmark
#net="mlpPanther"

## Use here for CNN benchmark
net=$1

# Setup config file based on network
cp "/home/fernando/Workspace/virtus/hp/dpe/dpe_emulate/include/$net/config.py" "/home/fernando/Workspace/virtus/hp/dpe/dpe_emulate/include/config.py"

# run panther - optimized (mixed precision)
suffix="panther"
cp "include/mlpPanther/constants_$suffix.py" "include/constants.py"
python src/dpe.py -n $net | tee "trace-$suffix.txt"
mv "/home/fernando/Workspace/virtus/hp/dpe/dpe_emulate/test/traces/$net" "/home/fernando/Workspace/virtus/hp/dpe/dpe_emulate/test/traces/$net-$suffix"
mv "trace-$suffix.txt" "/home/fernando/Workspace/virtus/hp/dpe/dpe_emulate/test/traces/trace-$net-$suffix"

# run allCMOS  - optimized (mixed precision)
suffix="digital"
cp "include/mlpPanther/constants_$suffix.py" "include/constants.py"
python src/dpe.py -n $net | tee "trace-$suffix.txt"
mv "/home/fernando/Workspace/virtus/hp/dpe/dpe_emulate/test/traces/$net" "/home/fernando/Workspace/virtus/hp/dpe/dpe_emulate/test/traces/$net-$suffix"
mv "trace-$suffix.txt" "/home/fernando/Workspace/virtus/hp/dpe/dpe_emulate/test/traces/trace-$net-$suffix"

# run cmosOP - optimized (mixed precision)
suffix="cmosOP"
cp "include/mlpPanther/constants_$suffix.py" "include/constants.py"
python src/dpe.py -n $net | tee "trace-$suffix.txt"
mv "/home/fernando/Workspace/virtus/hp/dpe/dpe_emulate/test/traces/$net" "/home/fernando/Workspace/virtus/hp/dpe/dpe_emulate/test/traces/$net-$suffix"
mv "trace-$suffix.txt" "/home/fernando/Workspace/virtus/hp/dpe/dpe_emulate/test/traces/trace-$net-$suffix"

# move all traces to $net folder
mkdir /home/fernando/Workspace/virtus/hp/dpe/dpe_emulate/test/traces/$net
#mv /home/fernando/Workspace/virtus/hp/dpe/dpe_emulate/test/traces/trace-* $net/
#mv /home/fernando/Workspace/virtus/hp/dpe/dpe_emulate/test/traces/$net-* $net/




