/// n bit (4,8,12,16) Integarte and Fire Neuron

`include "/home/min/a/aankit/AA/CMOS_SNN/hardware/include/neuron_if.vh"
`include "/home/min/a/aankit/AA/CMOS_SNN/hardware/include/snn_types_pkg.vh"

import snn_types_pkg::*;

module neuron (input logic clk,
	         input logic nRST,
		 neuron_if neif);

   //local variables
   logic [2*WEIGHT_WIDTH-1 : 0] acc_temp, acc;
   //logic [WEIGHT_WIDTH-1 : 0] acc;
   //assign acc = acc_temp[(2*WEIGHT_WIDTH-1) : WEIGHT_WIDTH];  -- remove this comment and comment next line for bit discretiztaion
   assign acc = acc_temp;

   //output logic
   assign neif.spike_out = (acc >= THRESHOLD) ? 1 : 0;

   always_ff @ (posedge clk, negedge nRST) begin
      if (!nRST)
	 acc_temp <= 0;
      else if (neif.clken) begin   //clock gating signal
	 if (neif.clr)
	    acc_temp <= 0;
	 else
	    acc_temp <= acc_temp + neif.data_in;
      end
   end
endmodule
