//Testbench for the Scalar Functional Unit
`include "scalar_fu_unit.vh"

`timescale 1ns/1ns

module scalar_fu_test;

   parameter PERIOD = 10;

   //Generate the clock
   logic CLK = 1;
   always #(PERIOD/2) CLK++;

   logic nRST;
   logic ren, wen;
   word_t ramstore, ramaddr, ramload;

   scalar_fu DUT (.clk,
		.ren(ren),
		.wen(wen),
		.ramstore(ramstore),
		.ramaddr(ramaddr),
		.ramload(ramload)
	       );

   initial begin

      $monitor("CLK = %b nRST = %b WEN = %b REN = %d ADDR = %d ramLOAD = %h ramSTORE = %d",
	       CLK, nRST, wen, ren, ramaddr, ramload, ramstore);

      nRST = 0; wen = 0; ren = 0; ramstore = 0; ramaddr = 0;

      #PERIOD
      nRST = 1; ren = 1; wen = 0; ramaddr = 1;

      #PERIOD
      ren = 1; wen = 0; ramaddr = 2;

      #PERIOD
      ren = 1; wen = 0; ramaddr = 3;

      #PERIOD
      ren = 0; wen = 1; ramaddr = 3; ramstore = 555;

      #PERIOD
      ren = 1; wen = 0; ramaddr = 3;

      #PERIOD
      ren = 1; wen = 0; ramaddr = 4;

      #PERIOD
      $finish;
   end

endmodule

