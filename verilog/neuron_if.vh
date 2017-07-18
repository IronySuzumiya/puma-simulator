//Neuron Interface
`ifndef NEURON_IF_VH
`define NEURON_IF_VH

`include "/home/min/a/aankit/AA/CMOS_SNN/hardware/include/snn_types_pkg.vh"
import snn_types_pkg::*;

interface neuron_if ();
		      
   logic spike_out;
   logic clken, clr;
   logic [WEIGHT_WIDTH-1:0] data_in;

   modport ne (
      input data_in, clken, clr,
      output spike_out
   );

   modport tb (
      output data_in, clken, clr,
      input spike_out
   );

endinterface

`endif //NEURON_IF_VH
   
