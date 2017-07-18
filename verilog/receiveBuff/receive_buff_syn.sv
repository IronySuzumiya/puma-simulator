/////////////////////////////////////////////////////////////
// Created by: Synopsys DC Expert(TM) in wire load mode
// Version   : L-2016.03-SP2
// Date      : Tue Jul 18 18:44:02 2017
/////////////////////////////////////////////////////////////


module receive_buff ( clk, nrst, \rbif.ren , \rbif.wen , \rbif.empty , 
        \rbif.full , \rbif.hit , \rbif.data_in , \rbif.tag_in , 
        \rbif.data_out  );
  inout [7:0] \rbif.data_in ;
  inout [7:0] \rbif.tag_in ;
  inout [7:0] \rbif.data_out ;
  input clk, nrst;
  inout \rbif.ren ,  \rbif.wen ,  \rbif.empty ,  \rbif.full ,  \rbif.hit ;
  wire   \tagfile[7][7] , \tagfile[7][6] , \tagfile[7][5] , \tagfile[7][4] ,
         \tagfile[7][3] , \tagfile[7][2] , \tagfile[7][1] , \tagfile[7][0] ,
         \tagfile[6][7] , \tagfile[6][6] , \tagfile[6][5] , \tagfile[6][4] ,
         \tagfile[6][3] , \tagfile[6][2] , \tagfile[6][1] , \tagfile[6][0] ,
         \tagfile[5][7] , \tagfile[5][6] , \tagfile[5][5] , \tagfile[5][4] ,
         \tagfile[5][3] , \tagfile[5][2] , \tagfile[5][1] , \tagfile[5][0] ,
         \tagfile[4][7] , \tagfile[4][6] , \tagfile[4][5] , \tagfile[4][4] ,
         \tagfile[4][3] , \tagfile[4][2] , \tagfile[4][1] , \tagfile[4][0] ,
         \tagfile[3][7] , \tagfile[3][6] , \tagfile[3][5] , \tagfile[3][4] ,
         \tagfile[3][3] , \tagfile[3][2] , \tagfile[3][1] , \tagfile[3][0] ,
         \tagfile[2][7] , \tagfile[2][6] , \tagfile[2][5] , \tagfile[2][4] ,
         \tagfile[2][3] , \tagfile[2][2] , \tagfile[2][1] , \tagfile[2][0] ,
         \tagfile[1][7] , \tagfile[1][6] , \tagfile[1][5] , \tagfile[1][4] ,
         \tagfile[1][3] , \tagfile[1][2] , \tagfile[1][1] , \tagfile[1][0] ,
         \tagfile[0][7] , \tagfile[0][6] , \tagfile[0][5] , \tagfile[0][4] ,
         \tagfile[0][3] , \tagfile[0][2] , \tagfile[0][1] , \tagfile[0][0] ,
         N192, N198, N204, n49, n50, n51, n52, n53, n54, n55, n56, n57, n58,
         n59, n60, n61, n62, n63, n64, n65, n66, n67, n68, n69, n70, n71, n72,
         n73, n74, n75, n76, n77, n78, n79, n80, n81, n82, n83, n84, n85, n86,
         n87, n88, n89, n90, n91, n92, n93, n94, n95, n96, n97, n98, n99, n100,
         n101, n102, n103, n104, n105, n106, n107, n108, n109, n110, n111,
         n112, n113, n114, n115, n116, n117, n118, n119, n120, n121, n122,
         n123, n124, n125, n126, n127, n128, n129, n130, n131, n132, n133,
         n134, n135, n136, n137, n138, n139, n140, n141, n142, n143, n144,
         n145, n146, n147, n148, n149, n150, n151, n152, n153, n154, n155,
         n156, n157, n158, n159, n160, n161, n162, n163, n164, n166, n167,
         n168, n169, n171, n172, n173, n175, n176, n177, n179, n180, n182,
         n183, n184, n185, n186, n187, n188, n189, n190, n191, n192, n193,
         n194, n195, n196, n197, n198, n199, n200, n201, n202, n203, n204,
         n205, n206, n207, n208, n209, n210, n211, n212, n213, n214, n215,
         n216, n217, n218, n219, n220, n221, n222, n223, n224, n225, n226,
         n227, n228, n229, n230, n231, n232, n233, n234, n235, n236, n237,
         n238, n239, n240, n241, n242, n243, n244, n245, n246, n247, n248,
         n249, n250, n251, n252, n253, n254, n255, n256, n257, n258, n259,
         n260, n261, n262, n263, n264, n265, n266, n267, n268, n269, n270,
         n271, n272, n273, n274, n275, n276, n277, n278, n279, n280, n281,
         n282, n283, n284, n285, n286, n287, n288, n289, n290, n291, n292,
         n293, n294, n295, n296, n297, n298, n299, n300, n301, n302, n303,
         n304, n305, n306, n307, n308, n309, n310, n311, n312, n313, n314,
         n315, n316, n317, n318, n319, n320, n321, n322, n323, n324, n325,
         n326, n327, n328, n329, n330, n331, n332, n333, n334, n335, n336,
         n337, n338, n339, n340, n341, n342, n343, n344, n345, n346, n347,
         n348, n349, n350, n351, n352, n353, n354, n355, n356, n357, n358,
         n359, n360, n361, n362, n363, n364, n365, n366, n367, n368, n369,
         n370, n371, n372, n373, n374, n375, n376, n377, n378, n379, n380,
         n381, n382, n383, n384, n385, n386, n387, n388, n389, n390, n391,
         n392, n393, n394, n395, n396, n397, n398, n399, n400, n401, n402,
         n403, n404, n405, n406, n407, n408, n409, n410, n411, n412, n413,
         n414, n415, n416, n417, n418, n419, n420, n421, n422, n423, n424,
         n425, n426, n427, n428, n429, n430, n431, n432, n433, n434, n435,
         n436, n437, n438, n439, n440, n441, n442, n443, n444, n445, n446,
         n447, n448, n449, n450, n451, n452, n453, n454, n455, n456, n457,
         n458, n459, n460, n461, n462, n463, n464, n465, n466, n467, n468,
         n469, n470, n471, n472, n473;
  wire   [7:0] validfile;
  wire   [7:0] match;
  tri   \rbif.ren ;
  tri   \rbif.wen ;
  tri   \rbif.empty ;
  tri   \rbif.full ;
  tri   \rbif.hit ;
  tri   [7:0] \rbif.data_in ;
  tri   [7:0] \rbif.tag_in ;
  tri   [7:0] \rbif.data_out ;

  DFFQ_X1M_A12TH \tagfile_reg[0][0]  ( .D(n466), .CK(clk), .Q(\tagfile[0][0] )
         );
  DFFQ_X1M_A12TH \tagfile_reg[3][5]  ( .D(n397), .CK(clk), .Q(\tagfile[3][5] )
         );
  DFFQ_X1M_A12TH \tagfile_reg[3][4]  ( .D(n398), .CK(clk), .Q(\tagfile[3][4] )
         );
  DFFQ_X1M_A12TH \tagfile_reg[3][3]  ( .D(n399), .CK(clk), .Q(\tagfile[3][3] )
         );
  DFFQ_X1M_A12TH \tagfile_reg[3][2]  ( .D(n400), .CK(clk), .Q(\tagfile[3][2] )
         );
  DFFQ_X1M_A12TH \tagfile_reg[3][1]  ( .D(n401), .CK(clk), .Q(\tagfile[3][1] )
         );
  DFFQ_X1M_A12TH \tagfile_reg[3][0]  ( .D(n402), .CK(clk), .Q(\tagfile[3][0] )
         );
  DFFQ_X1M_A12TH \tagfile_reg[4][4]  ( .D(n379), .CK(clk), .Q(\tagfile[4][4] )
         );
  DFFQ_X1M_A12TH \tagfile_reg[4][3]  ( .D(n380), .CK(clk), .Q(\tagfile[4][3] )
         );
  DFFQ_X1M_A12TH \tagfile_reg[4][2]  ( .D(n381), .CK(clk), .Q(\tagfile[4][2] )
         );
  DFFQ_X1M_A12TH \tagfile_reg[4][1]  ( .D(n382), .CK(clk), .Q(\tagfile[4][1] )
         );
  DFFQ_X1M_A12TH \tagfile_reg[4][0]  ( .D(n383), .CK(clk), .Q(\tagfile[4][0] )
         );
  DFFQ_X1M_A12TH \tagfile_reg[4][5]  ( .D(n386), .CK(clk), .Q(\tagfile[4][5] )
         );
  DFFQ_X1M_A12TH \tagfile_reg[5][5]  ( .D(n365), .CK(clk), .Q(\tagfile[5][5] )
         );
  DFFQ_X1M_A12TH \tagfile_reg[5][4]  ( .D(n366), .CK(clk), .Q(\tagfile[5][4] )
         );
  DFFQ_X1M_A12TH \tagfile_reg[5][3]  ( .D(n367), .CK(clk), .Q(\tagfile[5][3] )
         );
  DFFQ_X1M_A12TH \tagfile_reg[5][2]  ( .D(n368), .CK(clk), .Q(\tagfile[5][2] )
         );
  DFFQ_X1M_A12TH \tagfile_reg[5][1]  ( .D(n369), .CK(clk), .Q(\tagfile[5][1] )
         );
  DFFQ_X1M_A12TH \tagfile_reg[5][0]  ( .D(n370), .CK(clk), .Q(\tagfile[5][0] )
         );
  DFFQ_X1M_A12TH \tagfile_reg[6][5]  ( .D(n349), .CK(clk), .Q(\tagfile[6][5] )
         );
  DFFQ_X1M_A12TH \tagfile_reg[6][4]  ( .D(n350), .CK(clk), .Q(\tagfile[6][4] )
         );
  DFFQ_X1M_A12TH \tagfile_reg[6][3]  ( .D(n351), .CK(clk), .Q(\tagfile[6][3] )
         );
  DFFQ_X1M_A12TH \tagfile_reg[6][2]  ( .D(n352), .CK(clk), .Q(\tagfile[6][2] )
         );
  DFFQ_X1M_A12TH \tagfile_reg[6][1]  ( .D(n353), .CK(clk), .Q(\tagfile[6][1] )
         );
  DFFQ_X1M_A12TH \tagfile_reg[6][0]  ( .D(n354), .CK(clk), .Q(\tagfile[6][0] )
         );
  DFFQ_X1M_A12TH \tagfile_reg[7][5]  ( .D(n333), .CK(clk), .Q(\tagfile[7][5] )
         );
  DFFQ_X1M_A12TH \tagfile_reg[7][4]  ( .D(n334), .CK(clk), .Q(\tagfile[7][4] )
         );
  DFFQ_X1M_A12TH \tagfile_reg[7][3]  ( .D(n335), .CK(clk), .Q(\tagfile[7][3] )
         );
  DFFQ_X1M_A12TH \tagfile_reg[7][2]  ( .D(n336), .CK(clk), .Q(\tagfile[7][2] )
         );
  DFFQ_X1M_A12TH \tagfile_reg[7][1]  ( .D(n337), .CK(clk), .Q(\tagfile[7][1] )
         );
  DFFQ_X1M_A12TH \tagfile_reg[7][0]  ( .D(n338), .CK(clk), .Q(\tagfile[7][0] )
         );
  DFFQ_X1M_A12TH \tagfile_reg[2][5]  ( .D(n413), .CK(clk), .Q(\tagfile[2][5] )
         );
  DFFQ_X1M_A12TH \tagfile_reg[2][4]  ( .D(n414), .CK(clk), .Q(\tagfile[2][4] )
         );
  DFFQ_X1M_A12TH \tagfile_reg[2][3]  ( .D(n415), .CK(clk), .Q(\tagfile[2][3] )
         );
  DFFQ_X1M_A12TH \tagfile_reg[2][2]  ( .D(n416), .CK(clk), .Q(\tagfile[2][2] )
         );
  DFFQ_X1M_A12TH \tagfile_reg[2][1]  ( .D(n417), .CK(clk), .Q(\tagfile[2][1] )
         );
  DFFQ_X1M_A12TH \tagfile_reg[2][0]  ( .D(n418), .CK(clk), .Q(\tagfile[2][0] )
         );
  DFFQ_X1M_A12TH \tagfile_reg[1][5]  ( .D(n429), .CK(clk), .Q(\tagfile[1][5] )
         );
  DFFQ_X1M_A12TH \tagfile_reg[1][4]  ( .D(n430), .CK(clk), .Q(\tagfile[1][4] )
         );
  DFFQ_X1M_A12TH \tagfile_reg[1][3]  ( .D(n431), .CK(clk), .Q(\tagfile[1][3] )
         );
  DFFQ_X1M_A12TH \tagfile_reg[1][2]  ( .D(n432), .CK(clk), .Q(\tagfile[1][2] )
         );
  DFFQ_X1M_A12TH \tagfile_reg[1][1]  ( .D(n433), .CK(clk), .Q(\tagfile[1][1] )
         );
  DFFQ_X1M_A12TH \tagfile_reg[1][0]  ( .D(n434), .CK(clk), .Q(\tagfile[1][0] )
         );
  DFFQ_X1M_A12TH \tagfile_reg[0][5]  ( .D(n445), .CK(clk), .Q(\tagfile[0][5] )
         );
  DFFQ_X1M_A12TH \tagfile_reg[0][4]  ( .D(n446), .CK(clk), .Q(\tagfile[0][4] )
         );
  DFFQ_X1M_A12TH \tagfile_reg[0][3]  ( .D(n447), .CK(clk), .Q(\tagfile[0][3] )
         );
  DFFQ_X1M_A12TH \tagfile_reg[0][2]  ( .D(n448), .CK(clk), .Q(\tagfile[0][2] )
         );
  DFFQ_X1M_A12TH \tagfile_reg[0][1]  ( .D(n449), .CK(clk), .Q(\tagfile[0][1] )
         );
  DFFQ_X1M_A12TH \tagfile_reg[3][7]  ( .D(n395), .CK(clk), .Q(\tagfile[3][7] )
         );
  DFFQ_X1M_A12TH \tagfile_reg[3][6]  ( .D(n396), .CK(clk), .Q(\tagfile[3][6] )
         );
  DFFQ_X1M_A12TH \tagfile_reg[4][7]  ( .D(n384), .CK(clk), .Q(\tagfile[4][7] )
         );
  DFFQ_X1M_A12TH \tagfile_reg[4][6]  ( .D(n385), .CK(clk), .Q(\tagfile[4][6] )
         );
  DFFQ_X1M_A12TH \tagfile_reg[5][7]  ( .D(n363), .CK(clk), .Q(\tagfile[5][7] )
         );
  DFFQ_X1M_A12TH \tagfile_reg[5][6]  ( .D(n364), .CK(clk), .Q(\tagfile[5][6] )
         );
  DFFQ_X1M_A12TH \tagfile_reg[6][7]  ( .D(n347), .CK(clk), .Q(\tagfile[6][7] )
         );
  DFFQ_X1M_A12TH \tagfile_reg[6][6]  ( .D(n348), .CK(clk), .Q(\tagfile[6][6] )
         );
  DFFQ_X1M_A12TH \tagfile_reg[7][7]  ( .D(n331), .CK(clk), .Q(\tagfile[7][7] )
         );
  DFFQ_X1M_A12TH \tagfile_reg[7][6]  ( .D(n332), .CK(clk), .Q(\tagfile[7][6] )
         );
  DFFQ_X1M_A12TH \tagfile_reg[2][7]  ( .D(n411), .CK(clk), .Q(\tagfile[2][7] )
         );
  DFFQ_X1M_A12TH \tagfile_reg[2][6]  ( .D(n412), .CK(clk), .Q(\tagfile[2][6] )
         );
  DFFQ_X1M_A12TH \tagfile_reg[1][7]  ( .D(n427), .CK(clk), .Q(\tagfile[1][7] )
         );
  DFFQ_X1M_A12TH \tagfile_reg[1][6]  ( .D(n428), .CK(clk), .Q(\tagfile[1][6] )
         );
  DFFQ_X1M_A12TH \tagfile_reg[0][7]  ( .D(n443), .CK(clk), .Q(\tagfile[0][7] )
         );
  DFFQ_X1M_A12TH \tagfile_reg[0][6]  ( .D(n444), .CK(clk), .Q(\tagfile[0][6] )
         );
  DFFQ_X1M_A12TH \match_reg[7]  ( .D(n330), .CK(clk), .Q(match[7]) );
  DFFRPQ_X1M_A12TH \validfile_reg[7]  ( .D(n465), .CK(clk), .R(n126), .Q(
        validfile[7]) );
  DFFQ_X1M_A12TH \match_reg[5]  ( .D(n328), .CK(clk), .Q(match[5]) );
  DFFQ_X1M_A12TH \match_reg[6]  ( .D(n329), .CK(clk), .Q(match[6]) );
  DFFQ_X1M_A12TH \match_reg[4]  ( .D(n327), .CK(clk), .Q(match[4]) );
  DFFQ_X1M_A12TH \match_reg[2]  ( .D(n325), .CK(clk), .Q(match[2]) );
  DFFQ_X1M_A12TH \match_reg[1]  ( .D(n324), .CK(clk), .Q(match[1]) );
  DFFQ_X1M_A12TH \match_reg[3]  ( .D(n326), .CK(clk), .Q(match[3]) );
  DFFRPQ_X1M_A12TH \validfile_reg[5]  ( .D(n459), .CK(clk), .R(n126), .Q(
        validfile[5]) );
  DFFRPQ_X1M_A12TH \validfile_reg[4]  ( .D(n460), .CK(clk), .R(n126), .Q(
        validfile[4]) );
  DFFRPQ_X1M_A12TH \validfile_reg[0]  ( .D(n464), .CK(clk), .R(n126), .Q(
        validfile[0]) );
  DFFRPQ_X1M_A12TH \validfile_reg[6]  ( .D(n458), .CK(clk), .R(n126), .Q(
        validfile[6]) );
  DFFQN_X1M_A12TH \datafile_reg[4][7]  ( .D(n387), .CK(clk), .QN(n73) );
  DFFQN_X1M_A12TH \datafile_reg[4][6]  ( .D(n388), .CK(clk), .QN(n74) );
  DFFQN_X1M_A12TH \datafile_reg[4][5]  ( .D(n389), .CK(clk), .QN(n75) );
  DFFQN_X1M_A12TH \datafile_reg[4][4]  ( .D(n390), .CK(clk), .QN(n76) );
  DFFQN_X1M_A12TH \datafile_reg[4][3]  ( .D(n391), .CK(clk), .QN(n77) );
  DFFQN_X1M_A12TH \datafile_reg[4][2]  ( .D(n392), .CK(clk), .QN(n78) );
  DFFQN_X1M_A12TH \datafile_reg[4][1]  ( .D(n393), .CK(clk), .QN(n79) );
  DFFQN_X1M_A12TH \datafile_reg[4][0]  ( .D(n394), .CK(clk), .QN(n80) );
  DFFQN_X1M_A12TH \datafile_reg[6][7]  ( .D(n355), .CK(clk), .QN(n57) );
  DFFQN_X1M_A12TH \datafile_reg[6][6]  ( .D(n356), .CK(clk), .QN(n58) );
  DFFQN_X1M_A12TH \datafile_reg[6][5]  ( .D(n357), .CK(clk), .QN(n59) );
  DFFQN_X1M_A12TH \datafile_reg[6][4]  ( .D(n358), .CK(clk), .QN(n60) );
  DFFQN_X1M_A12TH \datafile_reg[6][3]  ( .D(n359), .CK(clk), .QN(n61) );
  DFFQN_X1M_A12TH \datafile_reg[6][2]  ( .D(n360), .CK(clk), .QN(n62) );
  DFFQN_X1M_A12TH \datafile_reg[6][1]  ( .D(n361), .CK(clk), .QN(n63) );
  DFFQN_X1M_A12TH \datafile_reg[6][0]  ( .D(n362), .CK(clk), .QN(n64) );
  DFFQN_X1M_A12TH \datafile_reg[2][7]  ( .D(n419), .CK(clk), .QN(n89) );
  DFFQN_X1M_A12TH \datafile_reg[2][6]  ( .D(n420), .CK(clk), .QN(n90) );
  DFFQN_X1M_A12TH \datafile_reg[2][5]  ( .D(n421), .CK(clk), .QN(n91) );
  DFFQN_X1M_A12TH \datafile_reg[2][4]  ( .D(n422), .CK(clk), .QN(n92) );
  DFFQN_X1M_A12TH \datafile_reg[2][3]  ( .D(n423), .CK(clk), .QN(n93) );
  DFFQN_X1M_A12TH \datafile_reg[2][2]  ( .D(n424), .CK(clk), .QN(n94) );
  DFFQN_X1M_A12TH \datafile_reg[2][1]  ( .D(n425), .CK(clk), .QN(n95) );
  DFFQN_X1M_A12TH \datafile_reg[2][0]  ( .D(n426), .CK(clk), .QN(n96) );
  DFFQN_X1M_A12TH \datafile_reg[1][7]  ( .D(n435), .CK(clk), .QN(n97) );
  DFFQN_X1M_A12TH \datafile_reg[1][6]  ( .D(n436), .CK(clk), .QN(n98) );
  DFFQN_X1M_A12TH \datafile_reg[1][5]  ( .D(n437), .CK(clk), .QN(n99) );
  DFFQN_X1M_A12TH \datafile_reg[1][4]  ( .D(n438), .CK(clk), .QN(n100) );
  DFFQN_X1M_A12TH \datafile_reg[1][3]  ( .D(n439), .CK(clk), .QN(n101) );
  DFFQN_X1M_A12TH \datafile_reg[1][2]  ( .D(n440), .CK(clk), .QN(n102) );
  DFFQN_X1M_A12TH \datafile_reg[1][1]  ( .D(n441), .CK(clk), .QN(n103) );
  DFFQN_X1M_A12TH \datafile_reg[1][0]  ( .D(n442), .CK(clk), .QN(n104) );
  DFFQ_X1M_A12TH \match_reg[0]  ( .D(n323), .CK(clk), .Q(match[0]) );
  DFFQN_X1M_A12TH \datafile_reg[0][0]  ( .D(n457), .CK(clk), .QN(n112) );
  DFFQN_X1M_A12TH \datafile_reg[3][7]  ( .D(n403), .CK(clk), .QN(n81) );
  DFFQN_X1M_A12TH \datafile_reg[3][6]  ( .D(n404), .CK(clk), .QN(n82) );
  DFFQN_X1M_A12TH \datafile_reg[3][5]  ( .D(n405), .CK(clk), .QN(n83) );
  DFFQN_X1M_A12TH \datafile_reg[3][4]  ( .D(n406), .CK(clk), .QN(n84) );
  DFFQN_X1M_A12TH \datafile_reg[3][3]  ( .D(n407), .CK(clk), .QN(n85) );
  DFFQN_X1M_A12TH \datafile_reg[3][2]  ( .D(n408), .CK(clk), .QN(n86) );
  DFFQN_X1M_A12TH \datafile_reg[3][1]  ( .D(n409), .CK(clk), .QN(n87) );
  DFFQN_X1M_A12TH \datafile_reg[3][0]  ( .D(n410), .CK(clk), .QN(n88) );
  DFFQN_X1M_A12TH \datafile_reg[5][7]  ( .D(n371), .CK(clk), .QN(n65) );
  DFFQN_X1M_A12TH \datafile_reg[5][6]  ( .D(n372), .CK(clk), .QN(n66) );
  DFFQN_X1M_A12TH \datafile_reg[5][5]  ( .D(n373), .CK(clk), .QN(n67) );
  DFFQN_X1M_A12TH \datafile_reg[5][4]  ( .D(n374), .CK(clk), .QN(n68) );
  DFFQN_X1M_A12TH \datafile_reg[5][3]  ( .D(n375), .CK(clk), .QN(n69) );
  DFFQN_X1M_A12TH \datafile_reg[5][2]  ( .D(n376), .CK(clk), .QN(n70) );
  DFFQN_X1M_A12TH \datafile_reg[5][1]  ( .D(n377), .CK(clk), .QN(n71) );
  DFFQN_X1M_A12TH \datafile_reg[5][0]  ( .D(n378), .CK(clk), .QN(n72) );
  DFFQN_X1M_A12TH \datafile_reg[7][7]  ( .D(n339), .CK(clk), .QN(n49) );
  DFFQN_X1M_A12TH \datafile_reg[7][6]  ( .D(n340), .CK(clk), .QN(n50) );
  DFFQN_X1M_A12TH \datafile_reg[7][5]  ( .D(n341), .CK(clk), .QN(n51) );
  DFFQN_X1M_A12TH \datafile_reg[7][4]  ( .D(n342), .CK(clk), .QN(n52) );
  DFFQN_X1M_A12TH \datafile_reg[7][3]  ( .D(n343), .CK(clk), .QN(n53) );
  DFFQN_X1M_A12TH \datafile_reg[7][2]  ( .D(n344), .CK(clk), .QN(n54) );
  DFFQN_X1M_A12TH \datafile_reg[7][1]  ( .D(n345), .CK(clk), .QN(n55) );
  DFFQN_X1M_A12TH \datafile_reg[7][0]  ( .D(n346), .CK(clk), .QN(n56) );
  DFFQN_X1M_A12TH \datafile_reg[0][7]  ( .D(n450), .CK(clk), .QN(n105) );
  DFFQN_X1M_A12TH \datafile_reg[0][6]  ( .D(n451), .CK(clk), .QN(n106) );
  DFFQN_X1M_A12TH \datafile_reg[0][5]  ( .D(n452), .CK(clk), .QN(n107) );
  DFFQN_X1M_A12TH \datafile_reg[0][4]  ( .D(n453), .CK(clk), .QN(n108) );
  DFFQN_X1M_A12TH \datafile_reg[0][3]  ( .D(n454), .CK(clk), .QN(n109) );
  DFFQN_X1M_A12TH \datafile_reg[0][2]  ( .D(n455), .CK(clk), .QN(n110) );
  DFFQN_X1M_A12TH \datafile_reg[0][1]  ( .D(n456), .CK(clk), .QN(n111) );
  DFFRPQ_X1M_A12TH \validfile_reg[1]  ( .D(n463), .CK(clk), .R(n126), .Q(
        validfile[1]) );
  DFFRPQ_X1M_A12TH \validfile_reg[2]  ( .D(n462), .CK(clk), .R(n126), .Q(
        validfile[2]) );
  DFFRPQ_X1M_A12TH \validfile_reg[3]  ( .D(n461), .CK(clk), .R(n126), .Q(
        validfile[3]) );
  OR2_X1M_A12TH C1379 ( .A(N204), .B(match[0]), .Y(\rbif.hit ) );
  OR4_X1M_A12TH U346 ( .A(n294), .B(n293), .C(n292), .D(n291), .Y(
        \rbif.data_out [7]) );
  OR4_X1M_A12TH U347 ( .A(n298), .B(n297), .C(n296), .D(n295), .Y(
        \rbif.data_out [6]) );
  OR4_X1M_A12TH U348 ( .A(n302), .B(n301), .C(n300), .D(n299), .Y(
        \rbif.data_out [5]) );
  OR4_X1M_A12TH U349 ( .A(n306), .B(n305), .C(n304), .D(n303), .Y(
        \rbif.data_out [4]) );
  OR4_X1M_A12TH U350 ( .A(n310), .B(n309), .C(n308), .D(n307), .Y(
        \rbif.data_out [3]) );
  OR4_X1M_A12TH U351 ( .A(n314), .B(n313), .C(n312), .D(n311), .Y(
        \rbif.data_out [2]) );
  OR4_X1M_A12TH U352 ( .A(n318), .B(n317), .C(n316), .D(n315), .Y(
        \rbif.data_out [1]) );
  OR4_X1M_A12TH U353 ( .A(n322), .B(n321), .C(n320), .D(n319), .Y(
        \rbif.data_out [0]) );
  INV_X1M_A12TH I_0 ( .A(N192), .Y(\rbif.empty ) );
  AND2_X1M_A12TH C1372 ( .A(N198), .B(validfile[0]), .Y(\rbif.full ) );
  NAND3_X1M_A12TH U368 ( .A(n113), .B(n118), .C(n162), .Y(n467) );
  NAND3_X1M_A12TH U369 ( .A(n249), .B(n121), .C(n162), .Y(n468) );
  NAND2_X1M_A12TH U370 ( .A(n166), .B(n162), .Y(n469) );
  NOR2_X1M_A12TH U371 ( .A(n172), .B(n126), .Y(n470) );
  NOR3_X1M_A12TH U372 ( .A(n126), .B(validfile[1]), .C(n177), .Y(n471) );
  INV_X1M_A12TH U373 ( .A(n167), .Y(n168) );
  INV_X1M_A12TH U374 ( .A(n470), .Y(n171) );
  INV_X1M_A12TH U375 ( .A(n467), .Y(n173) );
  INV_X1M_A12TH U376 ( .A(n468), .Y(n180) );
  INV_X1M_A12TH U377 ( .A(n469), .Y(n164) );
  INV_X1M_A12TH U378 ( .A(n152), .Y(n153) );
  INV_X1M_A12TH U379 ( .A(n472), .Y(n175) );
  INV_X1M_A12TH U380 ( .A(n471), .Y(n179) );
  INV_X1M_A12TH U381 ( .A(n187), .Y(n113) );
  NOR2XB_X1M_A12TH U382 ( .BN(n162), .A(n163), .Y(n152) );
  BUFH_X1M_A12TH U383 ( .A(n176), .Y(n473) );
  BUFH_X1M_A12TH U384 ( .A(n176), .Y(n472) );
  AO21A1AI2_X1M_A12TH U385 ( .A0(n143), .A1(n222), .B0(n118), .C0(n223), .Y(
        n461) );
  NAND2_X1M_A12TH U386 ( .A(n184), .B(n222), .Y(n223) );
  OAI21_X1M_A12TH U387 ( .A0(n187), .A1(n224), .B0(n185), .Y(n222) );
  AO21A1AI2_X1M_A12TH U388 ( .A0(n141), .A1(n235), .B0(n119), .C0(n236), .Y(
        n462) );
  NAND2_X1M_A12TH U389 ( .A(n184), .B(n235), .Y(n236) );
  OAI21_X1M_A12TH U390 ( .A0(n120), .A1(n177), .B0(n185), .Y(n235) );
  AO21A1AI2_X1M_A12TH U391 ( .A0(n139), .A1(n247), .B0(n120), .C0(n248), .Y(
        n463) );
  NAND2_X1M_A12TH U392 ( .A(n184), .B(n247), .Y(n248) );
  NAND2_X1M_A12TH U393 ( .A(n177), .B(n185), .Y(n247) );
  AO21A1AI2_X1M_A12TH U394 ( .A0(n145), .A1(n210), .B0(n117), .C0(n211), .Y(
        n460) );
  NAND2_X1M_A12TH U395 ( .A(n184), .B(n210), .Y(n211) );
  NAND2_X1M_A12TH U396 ( .A(n172), .B(n185), .Y(n210) );
  AO21A1AI2_X1M_A12TH U397 ( .A0(n149), .A1(n182), .B0(n115), .C0(n183), .Y(
        n458) );
  NAND2_X1M_A12TH U398 ( .A(n184), .B(n182), .Y(n183) );
  NAND2XB_X1M_A12TH U399 ( .BN(n166), .A(n185), .Y(n182) );
  AO21A1AI2_X1M_A12TH U400 ( .A0(n151), .A1(n272), .B0(n114), .C0(n273), .Y(
        n465) );
  NAND2_X1M_A12TH U401 ( .A(n184), .B(n272), .Y(n273) );
  NAND2_X1M_A12TH U402 ( .A(n185), .B(n163), .Y(n272) );
  AO21A1AI2_X1M_A12TH U403 ( .A0(n147), .A1(n198), .B0(n116), .C0(n199), .Y(
        n459) );
  NAND2_X1M_A12TH U404 ( .A(n184), .B(n198), .Y(n199) );
  NAND2_X1M_A12TH U405 ( .A(n185), .B(n169), .Y(n198) );
  NOR2XB_X1M_A12TH U406 ( .BN(n162), .A(n169), .Y(n167) );
  NAND3_X1M_A12TH U407 ( .A(n124), .B(n123), .C(n285), .Y(n130) );
  NOR2_X1M_A12TH U408 ( .A(n224), .B(n126), .Y(n162) );
  INV_X1M_A12TH U409 ( .A(n224), .Y(n184) );
  NAND4_X1M_A12TH U410 ( .A(validfile[2]), .B(validfile[1]), .C(validfile[0]), 
        .D(n249), .Y(n187) );
  NAND2XB_X1M_A12TH U411 ( .BN(\rbif.empty ), .A(\rbif.ren ), .Y(n185) );
  NAND4B_X1M_A12TH U412 ( .AN(n186), .B(n113), .C(validfile[6]), .D(n114), .Y(
        n163) );
  NOR2_X1M_A12TH U413 ( .A(n137), .B(\rbif.empty ), .Y(n136) );
  NAND4_X1M_A12TH U414 ( .A(n184), .B(n113), .C(validfile[3]), .D(n117), .Y(
        n172) );
  NAND4_X1M_A12TH U415 ( .A(n113), .B(validfile[4]), .C(validfile[3]), .D(n116), .Y(n169) );
  NAND4B_X1M_A12TH U416 ( .AN(n177), .B(validfile[1]), .C(nrst), .D(n119), .Y(
        n176) );
  NAND3_X1M_A12TH U417 ( .A(validfile[0]), .B(n249), .C(n184), .Y(n177) );
  XOR2_X1M_A12TH U418 ( .A(\tagfile[0][6] ), .B(\rbif.tag_in [6]), .Y(n267) );
  XOR2_X1M_A12TH U419 ( .A(\tagfile[1][6] ), .B(\rbif.tag_in [6]), .Y(n255) );
  XOR2_X1M_A12TH U420 ( .A(\tagfile[2][6] ), .B(\rbif.tag_in [6]), .Y(n242) );
  XOR2_X1M_A12TH U421 ( .A(\tagfile[3][6] ), .B(\rbif.tag_in [6]), .Y(n230) );
  XOR2_X1M_A12TH U422 ( .A(\tagfile[4][6] ), .B(\rbif.tag_in [6]), .Y(n217) );
  XOR2_X1M_A12TH U423 ( .A(\tagfile[5][6] ), .B(\rbif.tag_in [6]), .Y(n205) );
  XOR2_X1M_A12TH U424 ( .A(\tagfile[6][6] ), .B(\rbif.tag_in [6]), .Y(n193) );
  XOR2_X1M_A12TH U425 ( .A(\tagfile[7][6] ), .B(\rbif.tag_in [6]), .Y(n279) );
  XOR2_X1M_A12TH U426 ( .A(\tagfile[0][7] ), .B(\rbif.tag_in [7]), .Y(n266) );
  XOR2_X1M_A12TH U427 ( .A(\tagfile[1][7] ), .B(\rbif.tag_in [7]), .Y(n254) );
  XOR2_X1M_A12TH U428 ( .A(\tagfile[2][7] ), .B(\rbif.tag_in [7]), .Y(n241) );
  XOR2_X1M_A12TH U429 ( .A(\tagfile[3][7] ), .B(\rbif.tag_in [7]), .Y(n229) );
  XOR2_X1M_A12TH U430 ( .A(\tagfile[4][7] ), .B(\rbif.tag_in [7]), .Y(n216) );
  XOR2_X1M_A12TH U431 ( .A(\tagfile[5][7] ), .B(\rbif.tag_in [7]), .Y(n204) );
  XOR2_X1M_A12TH U432 ( .A(\tagfile[6][7] ), .B(\rbif.tag_in [7]), .Y(n192) );
  XOR2_X1M_A12TH U433 ( .A(\tagfile[7][7] ), .B(\rbif.tag_in [7]), .Y(n278) );
  NOR3_X1M_A12TH U434 ( .A(n186), .B(validfile[6]), .C(n187), .Y(n166) );
  XNOR2_X1M_A12TH U435 ( .A(\tagfile[0][3] ), .B(\rbif.tag_in [3]), .Y(n271)
         );
  XNOR2_X1M_A12TH U436 ( .A(\tagfile[1][3] ), .B(\rbif.tag_in [3]), .Y(n259)
         );
  XNOR2_X1M_A12TH U437 ( .A(\tagfile[2][3] ), .B(\rbif.tag_in [3]), .Y(n246)
         );
  XNOR2_X1M_A12TH U438 ( .A(\tagfile[3][3] ), .B(\rbif.tag_in [3]), .Y(n234)
         );
  XNOR2_X1M_A12TH U439 ( .A(\tagfile[4][3] ), .B(\rbif.tag_in [3]), .Y(n221)
         );
  XNOR2_X1M_A12TH U440 ( .A(\tagfile[5][3] ), .B(\rbif.tag_in [3]), .Y(n209)
         );
  XNOR2_X1M_A12TH U441 ( .A(\tagfile[6][3] ), .B(\rbif.tag_in [3]), .Y(n197)
         );
  XNOR2_X1M_A12TH U442 ( .A(\tagfile[7][3] ), .B(\rbif.tag_in [3]), .Y(n283)
         );
  NAND3_X1M_A12TH U443 ( .A(validfile[4]), .B(validfile[3]), .C(validfile[5]), 
        .Y(n186) );
  OAI22_X1M_A12TH U444 ( .A0(n160), .A1(n468), .B0(n180), .B1(n111), .Y(n456)
         );
  OAI22_X1M_A12TH U445 ( .A0(n159), .A1(n468), .B0(n180), .B1(n110), .Y(n455)
         );
  OAI22_X1M_A12TH U446 ( .A0(n158), .A1(n468), .B0(n180), .B1(n109), .Y(n454)
         );
  OAI22_X1M_A12TH U447 ( .A0(n157), .A1(n468), .B0(n180), .B1(n108), .Y(n453)
         );
  OAI22_X1M_A12TH U448 ( .A0(n156), .A1(n468), .B0(n180), .B1(n107), .Y(n452)
         );
  OAI22_X1M_A12TH U449 ( .A0(n155), .A1(n468), .B0(n180), .B1(n106), .Y(n451)
         );
  OAI22_X1M_A12TH U450 ( .A0(n154), .A1(n468), .B0(n180), .B1(n105), .Y(n450)
         );
  OAI22_X1M_A12TH U451 ( .A0(n153), .A1(n161), .B0(n152), .B1(n56), .Y(n346)
         );
  OAI22_X1M_A12TH U452 ( .A0(n153), .A1(n160), .B0(n152), .B1(n55), .Y(n345)
         );
  OAI22_X1M_A12TH U453 ( .A0(n153), .A1(n159), .B0(n152), .B1(n54), .Y(n344)
         );
  OAI22_X1M_A12TH U454 ( .A0(n153), .A1(n158), .B0(n152), .B1(n53), .Y(n343)
         );
  OAI22_X1M_A12TH U455 ( .A0(n153), .A1(n157), .B0(n152), .B1(n52), .Y(n342)
         );
  OAI22_X1M_A12TH U456 ( .A0(n153), .A1(n156), .B0(n152), .B1(n51), .Y(n341)
         );
  OAI22_X1M_A12TH U457 ( .A0(n153), .A1(n155), .B0(n152), .B1(n50), .Y(n340)
         );
  OAI22_X1M_A12TH U458 ( .A0(n153), .A1(n154), .B0(n152), .B1(n49), .Y(n339)
         );
  OAI22_X1M_A12TH U459 ( .A0(n161), .A1(n168), .B0(n167), .B1(n72), .Y(n378)
         );
  OAI22_X1M_A12TH U460 ( .A0(n160), .A1(n168), .B0(n167), .B1(n71), .Y(n377)
         );
  OAI22_X1M_A12TH U461 ( .A0(n159), .A1(n168), .B0(n167), .B1(n70), .Y(n376)
         );
  OAI22_X1M_A12TH U462 ( .A0(n158), .A1(n168), .B0(n167), .B1(n69), .Y(n375)
         );
  OAI22_X1M_A12TH U463 ( .A0(n157), .A1(n168), .B0(n167), .B1(n68), .Y(n374)
         );
  OAI22_X1M_A12TH U464 ( .A0(n156), .A1(n168), .B0(n167), .B1(n67), .Y(n373)
         );
  OAI22_X1M_A12TH U465 ( .A0(n155), .A1(n168), .B0(n167), .B1(n66), .Y(n372)
         );
  OAI22_X1M_A12TH U466 ( .A0(n154), .A1(n168), .B0(n167), .B1(n65), .Y(n371)
         );
  OAI22_X1M_A12TH U467 ( .A0(n161), .A1(n467), .B0(n173), .B1(n88), .Y(n410)
         );
  OAI22_X1M_A12TH U468 ( .A0(n160), .A1(n467), .B0(n173), .B1(n87), .Y(n409)
         );
  OAI22_X1M_A12TH U469 ( .A0(n159), .A1(n467), .B0(n173), .B1(n86), .Y(n408)
         );
  OAI22_X1M_A12TH U470 ( .A0(n158), .A1(n467), .B0(n173), .B1(n85), .Y(n407)
         );
  OAI22_X1M_A12TH U471 ( .A0(n157), .A1(n467), .B0(n173), .B1(n84), .Y(n406)
         );
  OAI22_X1M_A12TH U472 ( .A0(n156), .A1(n467), .B0(n173), .B1(n83), .Y(n405)
         );
  OAI22_X1M_A12TH U473 ( .A0(n155), .A1(n467), .B0(n173), .B1(n82), .Y(n404)
         );
  OAI22_X1M_A12TH U474 ( .A0(n154), .A1(n467), .B0(n173), .B1(n81), .Y(n403)
         );
  OAI22_X1M_A12TH U475 ( .A0(n161), .A1(n468), .B0(n180), .B1(n112), .Y(n457)
         );
  OAI22_X1M_A12TH U476 ( .A0(n161), .A1(n179), .B0(n471), .B1(n104), .Y(n442)
         );
  OAI22_X1M_A12TH U477 ( .A0(n160), .A1(n179), .B0(n471), .B1(n103), .Y(n441)
         );
  OAI22_X1M_A12TH U478 ( .A0(n159), .A1(n179), .B0(n471), .B1(n102), .Y(n440)
         );
  OAI22_X1M_A12TH U479 ( .A0(n158), .A1(n179), .B0(n471), .B1(n101), .Y(n439)
         );
  OAI22_X1M_A12TH U480 ( .A0(n157), .A1(n179), .B0(n471), .B1(n100), .Y(n438)
         );
  OAI22_X1M_A12TH U481 ( .A0(n156), .A1(n179), .B0(n471), .B1(n99), .Y(n437)
         );
  OAI22_X1M_A12TH U482 ( .A0(n155), .A1(n179), .B0(n471), .B1(n98), .Y(n436)
         );
  OAI22_X1M_A12TH U483 ( .A0(n154), .A1(n179), .B0(n471), .B1(n97), .Y(n435)
         );
  OAI22_X1M_A12TH U484 ( .A0(n161), .A1(n472), .B0(n175), .B1(n96), .Y(n426)
         );
  OAI22_X1M_A12TH U485 ( .A0(n160), .A1(n472), .B0(n175), .B1(n95), .Y(n425)
         );
  OAI22_X1M_A12TH U486 ( .A0(n159), .A1(n472), .B0(n175), .B1(n94), .Y(n424)
         );
  OAI22_X1M_A12TH U487 ( .A0(n158), .A1(n472), .B0(n175), .B1(n93), .Y(n423)
         );
  OAI22_X1M_A12TH U488 ( .A0(n157), .A1(n472), .B0(n175), .B1(n92), .Y(n422)
         );
  OAI22_X1M_A12TH U489 ( .A0(n156), .A1(n473), .B0(n175), .B1(n91), .Y(n421)
         );
  OAI22_X1M_A12TH U490 ( .A0(n155), .A1(n473), .B0(n175), .B1(n90), .Y(n420)
         );
  OAI22_X1M_A12TH U491 ( .A0(n154), .A1(n473), .B0(n175), .B1(n89), .Y(n419)
         );
  OAI22_X1M_A12TH U492 ( .A0(n161), .A1(n469), .B0(n164), .B1(n64), .Y(n362)
         );
  OAI22_X1M_A12TH U493 ( .A0(n160), .A1(n469), .B0(n164), .B1(n63), .Y(n361)
         );
  OAI22_X1M_A12TH U494 ( .A0(n159), .A1(n469), .B0(n164), .B1(n62), .Y(n360)
         );
  OAI22_X1M_A12TH U495 ( .A0(n158), .A1(n469), .B0(n164), .B1(n61), .Y(n359)
         );
  OAI22_X1M_A12TH U496 ( .A0(n157), .A1(n469), .B0(n164), .B1(n60), .Y(n358)
         );
  OAI22_X1M_A12TH U497 ( .A0(n156), .A1(n469), .B0(n164), .B1(n59), .Y(n357)
         );
  OAI22_X1M_A12TH U498 ( .A0(n155), .A1(n469), .B0(n164), .B1(n58), .Y(n356)
         );
  OAI22_X1M_A12TH U499 ( .A0(n154), .A1(n469), .B0(n164), .B1(n57), .Y(n355)
         );
  OAI22_X1M_A12TH U500 ( .A0(n161), .A1(n171), .B0(n470), .B1(n80), .Y(n394)
         );
  OAI22_X1M_A12TH U501 ( .A0(n160), .A1(n171), .B0(n470), .B1(n79), .Y(n393)
         );
  OAI22_X1M_A12TH U502 ( .A0(n159), .A1(n171), .B0(n470), .B1(n78), .Y(n392)
         );
  OAI22_X1M_A12TH U503 ( .A0(n158), .A1(n171), .B0(n470), .B1(n77), .Y(n391)
         );
  OAI22_X1M_A12TH U504 ( .A0(n157), .A1(n171), .B0(n470), .B1(n76), .Y(n390)
         );
  OAI22_X1M_A12TH U505 ( .A0(n156), .A1(n171), .B0(n470), .B1(n75), .Y(n389)
         );
  OAI22_X1M_A12TH U506 ( .A0(n155), .A1(n171), .B0(n470), .B1(n74), .Y(n388)
         );
  OAI22_X1M_A12TH U507 ( .A0(n154), .A1(n171), .B0(n470), .B1(n73), .Y(n387)
         );
  INV_X1M_A12TH U508 ( .A(validfile[1]), .Y(n120) );
  INV_X1M_A12TH U509 ( .A(validfile[0]), .Y(n121) );
  INV_X1M_A12TH U510 ( .A(validfile[3]), .Y(n118) );
  INV_X1M_A12TH U511 ( .A(validfile[7]), .Y(n114) );
  INV_X1M_A12TH U512 ( .A(validfile[4]), .Y(n117) );
  INV_X1M_A12TH U513 ( .A(validfile[2]), .Y(n119) );
  AND4_X1M_A12TH U514 ( .A(n262), .B(n263), .C(n264), .D(n265), .Y(n135) );
  XNOR2_X1M_A12TH U515 ( .A(\tagfile[0][5] ), .B(\rbif.tag_in [5]), .Y(n263)
         );
  XNOR2_X1M_A12TH U516 ( .A(\tagfile[0][4] ), .B(\rbif.tag_in [4]), .Y(n265)
         );
  NOR2_X1M_A12TH U517 ( .A(n266), .B(n267), .Y(n264) );
  AND4_X1M_A12TH U518 ( .A(n250), .B(n251), .C(n252), .D(n253), .Y(n139) );
  XNOR2_X1M_A12TH U519 ( .A(\tagfile[1][5] ), .B(\rbif.tag_in [5]), .Y(n251)
         );
  XNOR2_X1M_A12TH U520 ( .A(\tagfile[1][4] ), .B(\rbif.tag_in [4]), .Y(n253)
         );
  NOR2_X1M_A12TH U521 ( .A(n254), .B(n255), .Y(n252) );
  AND4_X1M_A12TH U522 ( .A(n237), .B(n238), .C(n239), .D(n240), .Y(n141) );
  XNOR2_X1M_A12TH U523 ( .A(\tagfile[2][5] ), .B(\rbif.tag_in [5]), .Y(n238)
         );
  XNOR2_X1M_A12TH U524 ( .A(\tagfile[2][4] ), .B(\rbif.tag_in [4]), .Y(n240)
         );
  NOR2_X1M_A12TH U525 ( .A(n241), .B(n242), .Y(n239) );
  AND4_X1M_A12TH U526 ( .A(n225), .B(n226), .C(n227), .D(n228), .Y(n143) );
  XNOR2_X1M_A12TH U527 ( .A(\tagfile[3][5] ), .B(\rbif.tag_in [5]), .Y(n226)
         );
  XNOR2_X1M_A12TH U528 ( .A(\tagfile[3][4] ), .B(\rbif.tag_in [4]), .Y(n228)
         );
  NOR2_X1M_A12TH U529 ( .A(n229), .B(n230), .Y(n227) );
  AND4_X1M_A12TH U530 ( .A(n212), .B(n213), .C(n214), .D(n215), .Y(n145) );
  XNOR2_X1M_A12TH U531 ( .A(\tagfile[4][5] ), .B(\rbif.tag_in [5]), .Y(n213)
         );
  XNOR2_X1M_A12TH U532 ( .A(\tagfile[4][4] ), .B(\rbif.tag_in [4]), .Y(n215)
         );
  NOR2_X1M_A12TH U533 ( .A(n216), .B(n217), .Y(n214) );
  AND4_X1M_A12TH U534 ( .A(n200), .B(n201), .C(n202), .D(n203), .Y(n147) );
  XNOR2_X1M_A12TH U535 ( .A(\tagfile[5][5] ), .B(\rbif.tag_in [5]), .Y(n201)
         );
  XNOR2_X1M_A12TH U536 ( .A(\tagfile[5][4] ), .B(\rbif.tag_in [4]), .Y(n203)
         );
  NOR2_X1M_A12TH U537 ( .A(n204), .B(n205), .Y(n202) );
  AND4_X1M_A12TH U538 ( .A(n188), .B(n189), .C(n190), .D(n191), .Y(n149) );
  XNOR2_X1M_A12TH U539 ( .A(\tagfile[6][5] ), .B(\rbif.tag_in [5]), .Y(n189)
         );
  XNOR2_X1M_A12TH U540 ( .A(\tagfile[6][4] ), .B(\rbif.tag_in [4]), .Y(n191)
         );
  NOR2_X1M_A12TH U541 ( .A(n192), .B(n193), .Y(n190) );
  AND4_X1M_A12TH U542 ( .A(n274), .B(n275), .C(n276), .D(n277), .Y(n151) );
  XNOR2_X1M_A12TH U543 ( .A(\tagfile[7][5] ), .B(\rbif.tag_in [5]), .Y(n275)
         );
  XNOR2_X1M_A12TH U544 ( .A(\tagfile[7][4] ), .B(\rbif.tag_in [4]), .Y(n277)
         );
  NOR2_X1M_A12TH U545 ( .A(n278), .B(n279), .Y(n276) );
  AO21A1AI2_X1M_A12TH U546 ( .A0(n135), .A1(n260), .B0(n121), .C0(n261), .Y(
        n464) );
  NAND2_X1M_A12TH U547 ( .A(n184), .B(n260), .Y(n261) );
  OAI21_X1M_A12TH U548 ( .A0(\rbif.full ), .A1(n224), .B0(n185), .Y(n260) );
  INV_X1M_A12TH U549 ( .A(validfile[5]), .Y(n116) );
  INV_X1M_A12TH U550 ( .A(validfile[6]), .Y(n115) );
  NOR3_X1M_A12TH U551 ( .A(n288), .B(n114), .C(n186), .Y(N198) );
  NAND3_X1M_A12TH U552 ( .A(validfile[2]), .B(validfile[1]), .C(validfile[6]), 
        .Y(n288) );
  INV_X1M_A12TH U553 ( .A(\rbif.full ), .Y(n249) );
  AND4_X1M_A12TH U554 ( .A(n268), .B(n269), .C(n270), .D(n271), .Y(n262) );
  XNOR2_X1M_A12TH U555 ( .A(\tagfile[0][0] ), .B(\rbif.tag_in [0]), .Y(n268)
         );
  XNOR2_X1M_A12TH U556 ( .A(\tagfile[0][1] ), .B(\rbif.tag_in [1]), .Y(n269)
         );
  XNOR2_X1M_A12TH U557 ( .A(\tagfile[0][2] ), .B(\rbif.tag_in [2]), .Y(n270)
         );
  AND4_X1M_A12TH U558 ( .A(n256), .B(n257), .C(n258), .D(n259), .Y(n250) );
  XNOR2_X1M_A12TH U559 ( .A(\tagfile[1][0] ), .B(\rbif.tag_in [0]), .Y(n256)
         );
  XNOR2_X1M_A12TH U560 ( .A(\tagfile[1][1] ), .B(\rbif.tag_in [1]), .Y(n257)
         );
  XNOR2_X1M_A12TH U561 ( .A(\tagfile[1][2] ), .B(\rbif.tag_in [2]), .Y(n258)
         );
  AND4_X1M_A12TH U562 ( .A(n243), .B(n244), .C(n245), .D(n246), .Y(n237) );
  XNOR2_X1M_A12TH U563 ( .A(\tagfile[2][0] ), .B(\rbif.tag_in [0]), .Y(n243)
         );
  XNOR2_X1M_A12TH U564 ( .A(\tagfile[2][1] ), .B(\rbif.tag_in [1]), .Y(n244)
         );
  XNOR2_X1M_A12TH U565 ( .A(\tagfile[2][2] ), .B(\rbif.tag_in [2]), .Y(n245)
         );
  AND4_X1M_A12TH U566 ( .A(n231), .B(n232), .C(n233), .D(n234), .Y(n225) );
  XNOR2_X1M_A12TH U567 ( .A(\tagfile[3][0] ), .B(\rbif.tag_in [0]), .Y(n231)
         );
  XNOR2_X1M_A12TH U568 ( .A(\tagfile[3][1] ), .B(\rbif.tag_in [1]), .Y(n232)
         );
  XNOR2_X1M_A12TH U569 ( .A(\tagfile[3][2] ), .B(\rbif.tag_in [2]), .Y(n233)
         );
  AND4_X1M_A12TH U570 ( .A(n218), .B(n219), .C(n220), .D(n221), .Y(n212) );
  XNOR2_X1M_A12TH U571 ( .A(\tagfile[4][0] ), .B(\rbif.tag_in [0]), .Y(n218)
         );
  XNOR2_X1M_A12TH U572 ( .A(\tagfile[4][1] ), .B(\rbif.tag_in [1]), .Y(n219)
         );
  XNOR2_X1M_A12TH U573 ( .A(\tagfile[4][2] ), .B(\rbif.tag_in [2]), .Y(n220)
         );
  AND4_X1M_A12TH U574 ( .A(n206), .B(n207), .C(n208), .D(n209), .Y(n200) );
  XNOR2_X1M_A12TH U575 ( .A(\tagfile[5][0] ), .B(\rbif.tag_in [0]), .Y(n206)
         );
  XNOR2_X1M_A12TH U576 ( .A(\tagfile[5][1] ), .B(\rbif.tag_in [1]), .Y(n207)
         );
  XNOR2_X1M_A12TH U577 ( .A(\tagfile[5][2] ), .B(\rbif.tag_in [2]), .Y(n208)
         );
  AND4_X1M_A12TH U578 ( .A(n194), .B(n195), .C(n196), .D(n197), .Y(n188) );
  XNOR2_X1M_A12TH U579 ( .A(\tagfile[6][0] ), .B(\rbif.tag_in [0]), .Y(n194)
         );
  XNOR2_X1M_A12TH U580 ( .A(\tagfile[6][1] ), .B(\rbif.tag_in [1]), .Y(n195)
         );
  XNOR2_X1M_A12TH U581 ( .A(\tagfile[6][2] ), .B(\rbif.tag_in [2]), .Y(n196)
         );
  AND4_X1M_A12TH U582 ( .A(n280), .B(n281), .C(n282), .D(n283), .Y(n274) );
  XNOR2_X1M_A12TH U583 ( .A(\tagfile[7][0] ), .B(\rbif.tag_in [0]), .Y(n280)
         );
  XNOR2_X1M_A12TH U584 ( .A(\tagfile[7][1] ), .B(\rbif.tag_in [1]), .Y(n281)
         );
  XNOR2_X1M_A12TH U585 ( .A(\tagfile[7][2] ), .B(\rbif.tag_in [2]), .Y(n282)
         );
  NAND4_X1M_A12TH U586 ( .A(n121), .B(n120), .C(n289), .D(n290), .Y(N192) );
  NOR2_X1M_A12TH U587 ( .A(validfile[3]), .B(validfile[2]), .Y(n289) );
  AND4_X1M_A12TH U588 ( .A(n117), .B(n116), .C(n115), .D(n114), .Y(n290) );
  AO22_X1M_A12TH U589 ( .A0(\rbif.tag_in [0]), .A1(n471), .B0(n179), .B1(
        \tagfile[1][0] ), .Y(n434) );
  AO22_X1M_A12TH U590 ( .A0(\rbif.tag_in [1]), .A1(n471), .B0(n179), .B1(
        \tagfile[1][1] ), .Y(n433) );
  AO22_X1M_A12TH U591 ( .A0(\rbif.tag_in [2]), .A1(n471), .B0(n179), .B1(
        \tagfile[1][2] ), .Y(n432) );
  AO22_X1M_A12TH U592 ( .A0(\rbif.tag_in [3]), .A1(n471), .B0(n179), .B1(
        \tagfile[1][3] ), .Y(n431) );
  AO22_X1M_A12TH U593 ( .A0(\rbif.tag_in [4]), .A1(n471), .B0(n179), .B1(
        \tagfile[1][4] ), .Y(n430) );
  AO22_X1M_A12TH U594 ( .A0(\rbif.tag_in [5]), .A1(n471), .B0(n179), .B1(
        \tagfile[1][5] ), .Y(n429) );
  AO22_X1M_A12TH U595 ( .A0(\rbif.tag_in [6]), .A1(n471), .B0(n179), .B1(
        \tagfile[1][6] ), .Y(n428) );
  AO22_X1M_A12TH U596 ( .A0(\rbif.tag_in [7]), .A1(n471), .B0(n179), .B1(
        \tagfile[1][7] ), .Y(n427) );
  AO22_X1M_A12TH U597 ( .A0(\rbif.tag_in [0]), .A1(n152), .B0(n153), .B1(
        \tagfile[7][0] ), .Y(n338) );
  AO22_X1M_A12TH U598 ( .A0(\rbif.tag_in [1]), .A1(n152), .B0(n153), .B1(
        \tagfile[7][1] ), .Y(n337) );
  AO22_X1M_A12TH U599 ( .A0(\rbif.tag_in [2]), .A1(n152), .B0(n153), .B1(
        \tagfile[7][2] ), .Y(n336) );
  AO22_X1M_A12TH U600 ( .A0(\rbif.tag_in [3]), .A1(n152), .B0(n153), .B1(
        \tagfile[7][3] ), .Y(n335) );
  AO22_X1M_A12TH U601 ( .A0(\rbif.tag_in [4]), .A1(n152), .B0(n153), .B1(
        \tagfile[7][4] ), .Y(n334) );
  AO22_X1M_A12TH U602 ( .A0(\rbif.tag_in [5]), .A1(n152), .B0(n153), .B1(
        \tagfile[7][5] ), .Y(n333) );
  AO22_X1M_A12TH U603 ( .A0(\rbif.tag_in [6]), .A1(n152), .B0(n153), .B1(
        \tagfile[7][6] ), .Y(n332) );
  AO22_X1M_A12TH U604 ( .A0(\rbif.tag_in [7]), .A1(n152), .B0(n153), .B1(
        \tagfile[7][7] ), .Y(n331) );
  AO22_X1M_A12TH U605 ( .A0(\rbif.tag_in [0]), .A1(n175), .B0(n473), .B1(
        \tagfile[2][0] ), .Y(n418) );
  AO22_X1M_A12TH U606 ( .A0(\rbif.tag_in [1]), .A1(n175), .B0(n473), .B1(
        \tagfile[2][1] ), .Y(n417) );
  AO22_X1M_A12TH U607 ( .A0(\rbif.tag_in [2]), .A1(n175), .B0(n473), .B1(
        \tagfile[2][2] ), .Y(n416) );
  AO22_X1M_A12TH U608 ( .A0(\rbif.tag_in [3]), .A1(n175), .B0(n473), .B1(
        \tagfile[2][3] ), .Y(n415) );
  AO22_X1M_A12TH U609 ( .A0(\rbif.tag_in [4]), .A1(n175), .B0(n473), .B1(
        \tagfile[2][4] ), .Y(n414) );
  AO22_X1M_A12TH U610 ( .A0(\rbif.tag_in [5]), .A1(n175), .B0(n473), .B1(
        \tagfile[2][5] ), .Y(n413) );
  AO22_X1M_A12TH U611 ( .A0(\rbif.tag_in [6]), .A1(n175), .B0(n473), .B1(
        \tagfile[2][6] ), .Y(n412) );
  AO22_X1M_A12TH U612 ( .A0(\rbif.tag_in [7]), .A1(n175), .B0(n473), .B1(
        \tagfile[2][7] ), .Y(n411) );
  AO22_X1M_A12TH U613 ( .A0(\rbif.tag_in [0]), .A1(n173), .B0(n467), .B1(
        \tagfile[3][0] ), .Y(n402) );
  AO22_X1M_A12TH U614 ( .A0(\rbif.tag_in [1]), .A1(n173), .B0(n467), .B1(
        \tagfile[3][1] ), .Y(n401) );
  AO22_X1M_A12TH U615 ( .A0(\rbif.tag_in [2]), .A1(n173), .B0(n467), .B1(
        \tagfile[3][2] ), .Y(n400) );
  AO22_X1M_A12TH U616 ( .A0(\rbif.tag_in [3]), .A1(n173), .B0(n467), .B1(
        \tagfile[3][3] ), .Y(n399) );
  AO22_X1M_A12TH U617 ( .A0(\rbif.tag_in [4]), .A1(n173), .B0(n467), .B1(
        \tagfile[3][4] ), .Y(n398) );
  AO22_X1M_A12TH U618 ( .A0(\rbif.tag_in [5]), .A1(n173), .B0(n467), .B1(
        \tagfile[3][5] ), .Y(n397) );
  AO22_X1M_A12TH U619 ( .A0(\rbif.tag_in [6]), .A1(n173), .B0(n467), .B1(
        \tagfile[3][6] ), .Y(n396) );
  AO22_X1M_A12TH U620 ( .A0(\rbif.tag_in [7]), .A1(n173), .B0(n467), .B1(
        \tagfile[3][7] ), .Y(n395) );
  AO22_X1M_A12TH U621 ( .A0(\rbif.tag_in [1]), .A1(n180), .B0(n468), .B1(
        \tagfile[0][1] ), .Y(n449) );
  AO22_X1M_A12TH U622 ( .A0(\rbif.tag_in [2]), .A1(n180), .B0(n468), .B1(
        \tagfile[0][2] ), .Y(n448) );
  AO22_X1M_A12TH U623 ( .A0(\rbif.tag_in [3]), .A1(n180), .B0(n468), .B1(
        \tagfile[0][3] ), .Y(n447) );
  AO22_X1M_A12TH U624 ( .A0(\rbif.tag_in [4]), .A1(n180), .B0(n468), .B1(
        \tagfile[0][4] ), .Y(n446) );
  AO22_X1M_A12TH U625 ( .A0(\rbif.tag_in [5]), .A1(n180), .B0(n468), .B1(
        \tagfile[0][5] ), .Y(n445) );
  AO22_X1M_A12TH U626 ( .A0(\rbif.tag_in [6]), .A1(n180), .B0(n468), .B1(
        \tagfile[0][6] ), .Y(n444) );
  AO22_X1M_A12TH U627 ( .A0(\rbif.tag_in [7]), .A1(n180), .B0(n468), .B1(
        \tagfile[0][7] ), .Y(n443) );
  AO22_X1M_A12TH U628 ( .A0(\rbif.tag_in [0]), .A1(n180), .B0(n468), .B1(
        \tagfile[0][0] ), .Y(n466) );
  AO22_X1M_A12TH U629 ( .A0(\rbif.tag_in [0]), .A1(n164), .B0(n469), .B1(
        \tagfile[6][0] ), .Y(n354) );
  AO22_X1M_A12TH U630 ( .A0(\rbif.tag_in [1]), .A1(n164), .B0(n469), .B1(
        \tagfile[6][1] ), .Y(n353) );
  AO22_X1M_A12TH U631 ( .A0(\rbif.tag_in [2]), .A1(n164), .B0(n469), .B1(
        \tagfile[6][2] ), .Y(n352) );
  AO22_X1M_A12TH U632 ( .A0(\rbif.tag_in [3]), .A1(n164), .B0(n469), .B1(
        \tagfile[6][3] ), .Y(n351) );
  AO22_X1M_A12TH U633 ( .A0(\rbif.tag_in [4]), .A1(n164), .B0(n469), .B1(
        \tagfile[6][4] ), .Y(n350) );
  AO22_X1M_A12TH U634 ( .A0(\rbif.tag_in [5]), .A1(n164), .B0(n469), .B1(
        \tagfile[6][5] ), .Y(n349) );
  AO22_X1M_A12TH U635 ( .A0(\rbif.tag_in [6]), .A1(n164), .B0(n469), .B1(
        \tagfile[6][6] ), .Y(n348) );
  AO22_X1M_A12TH U636 ( .A0(\rbif.tag_in [7]), .A1(n164), .B0(n469), .B1(
        \tagfile[6][7] ), .Y(n347) );
  AO22_X1M_A12TH U637 ( .A0(\rbif.tag_in [0]), .A1(n167), .B0(n168), .B1(
        \tagfile[5][0] ), .Y(n370) );
  AO22_X1M_A12TH U638 ( .A0(\rbif.tag_in [1]), .A1(n167), .B0(n168), .B1(
        \tagfile[5][1] ), .Y(n369) );
  AO22_X1M_A12TH U639 ( .A0(\rbif.tag_in [2]), .A1(n167), .B0(n168), .B1(
        \tagfile[5][2] ), .Y(n368) );
  AO22_X1M_A12TH U640 ( .A0(\rbif.tag_in [3]), .A1(n167), .B0(n168), .B1(
        \tagfile[5][3] ), .Y(n367) );
  AO22_X1M_A12TH U641 ( .A0(\rbif.tag_in [4]), .A1(n167), .B0(n168), .B1(
        \tagfile[5][4] ), .Y(n366) );
  AO22_X1M_A12TH U642 ( .A0(\rbif.tag_in [5]), .A1(n167), .B0(n168), .B1(
        \tagfile[5][5] ), .Y(n365) );
  AO22_X1M_A12TH U643 ( .A0(\rbif.tag_in [6]), .A1(n167), .B0(n168), .B1(
        \tagfile[5][6] ), .Y(n364) );
  AO22_X1M_A12TH U644 ( .A0(\rbif.tag_in [7]), .A1(n167), .B0(n168), .B1(
        \tagfile[5][7] ), .Y(n363) );
  AO22_X1M_A12TH U645 ( .A0(\rbif.tag_in [5]), .A1(n470), .B0(n171), .B1(
        \tagfile[4][5] ), .Y(n386) );
  AO22_X1M_A12TH U646 ( .A0(\rbif.tag_in [6]), .A1(n470), .B0(n171), .B1(
        \tagfile[4][6] ), .Y(n385) );
  AO22_X1M_A12TH U647 ( .A0(\rbif.tag_in [7]), .A1(n470), .B0(n171), .B1(
        \tagfile[4][7] ), .Y(n384) );
  AO22_X1M_A12TH U648 ( .A0(\rbif.tag_in [0]), .A1(n470), .B0(n171), .B1(
        \tagfile[4][0] ), .Y(n383) );
  AO22_X1M_A12TH U649 ( .A0(\rbif.tag_in [1]), .A1(n470), .B0(n171), .B1(
        \tagfile[4][1] ), .Y(n382) );
  AO22_X1M_A12TH U650 ( .A0(\rbif.tag_in [2]), .A1(n470), .B0(n171), .B1(
        \tagfile[4][2] ), .Y(n381) );
  AO22_X1M_A12TH U651 ( .A0(\rbif.tag_in [3]), .A1(n470), .B0(n171), .B1(
        \tagfile[4][3] ), .Y(n380) );
  AO22_X1M_A12TH U652 ( .A0(\rbif.tag_in [4]), .A1(n470), .B0(n171), .B1(
        \tagfile[4][4] ), .Y(n379) );
  INV_X1M_A12TH U653 ( .A(n134), .Y(n323) );
  AOI32_X1M_A12TH U654 ( .A0(n135), .A1(n136), .A2(validfile[0]), .B0(match[0]), .B1(n137), .Y(n134) );
  INV_X1M_A12TH U655 ( .A(n138), .Y(n324) );
  AOI32_X1M_A12TH U656 ( .A0(n139), .A1(n136), .A2(validfile[1]), .B0(match[1]), .B1(n137), .Y(n138) );
  INV_X1M_A12TH U657 ( .A(n140), .Y(n325) );
  AOI32_X1M_A12TH U658 ( .A0(n141), .A1(n136), .A2(validfile[2]), .B0(match[2]), .B1(n137), .Y(n140) );
  INV_X1M_A12TH U659 ( .A(n142), .Y(n326) );
  AOI32_X1M_A12TH U660 ( .A0(n143), .A1(n136), .A2(validfile[3]), .B0(match[3]), .B1(n137), .Y(n142) );
  INV_X1M_A12TH U661 ( .A(n144), .Y(n327) );
  AOI32_X1M_A12TH U662 ( .A0(n145), .A1(n136), .A2(validfile[4]), .B0(match[4]), .B1(n137), .Y(n144) );
  INV_X1M_A12TH U663 ( .A(n146), .Y(n328) );
  AOI32_X1M_A12TH U664 ( .A0(n147), .A1(n136), .A2(validfile[5]), .B0(match[5]), .B1(n137), .Y(n146) );
  INV_X1M_A12TH U665 ( .A(n148), .Y(n329) );
  AOI32_X1M_A12TH U666 ( .A0(n149), .A1(n136), .A2(validfile[6]), .B0(match[6]), .B1(n137), .Y(n148) );
  INV_X1M_A12TH U667 ( .A(n150), .Y(n330) );
  AOI32_X1M_A12TH U668 ( .A0(n151), .A1(n136), .A2(validfile[7]), .B0(match[7]), .B1(n137), .Y(n150) );
  NAND3XXB_X1M_A12TH U669 ( .CN(match[1]), .A(n125), .B(match[2]), .Y(n128) );
  NAND3_X1M_A12TH U670 ( .A(n285), .B(n124), .C(match[6]), .Y(n131) );
  NAND2_X1M_A12TH U671 ( .A(match[3]), .B(n284), .Y(n127) );
  NAND2_X1M_A12TH U672 ( .A(match[5]), .B(n285), .Y(n132) );
  NAND2_X1M_A12TH U673 ( .A(match[1]), .B(n125), .Y(n129) );
  NAND2_X1M_A12TH U674 ( .A(match[4]), .B(n286), .Y(n133) );
  NAND2XB_X1M_A12TH U675 ( .BN(\rbif.ren ), .A(\rbif.wen ), .Y(n224) );
  NAND2_X1M_A12TH U676 ( .A(\rbif.ren ), .B(nrst), .Y(n137) );
  INV_X1M_A12TH U677 ( .A(\rbif.data_in [0]), .Y(n161) );
  INV_X1M_A12TH U678 ( .A(\rbif.data_in [1]), .Y(n160) );
  INV_X1M_A12TH U679 ( .A(\rbif.data_in [2]), .Y(n159) );
  INV_X1M_A12TH U680 ( .A(\rbif.data_in [3]), .Y(n158) );
  INV_X1M_A12TH U681 ( .A(\rbif.data_in [4]), .Y(n157) );
  INV_X1M_A12TH U682 ( .A(\rbif.data_in [5]), .Y(n156) );
  INV_X1M_A12TH U683 ( .A(\rbif.data_in [6]), .Y(n155) );
  INV_X1M_A12TH U684 ( .A(\rbif.data_in [7]), .Y(n154) );
  OAI22_X1M_A12TH U685 ( .A0(n130), .A1(n56), .B0(n131), .B1(n64), .Y(n321) );
  OAI22_X1M_A12TH U686 ( .A0(n130), .A1(n55), .B0(n131), .B1(n63), .Y(n317) );
  OAI22_X1M_A12TH U687 ( .A0(n130), .A1(n54), .B0(n131), .B1(n62), .Y(n313) );
  OAI22_X1M_A12TH U688 ( .A0(n130), .A1(n53), .B0(n131), .B1(n61), .Y(n309) );
  OAI22_X1M_A12TH U689 ( .A0(n130), .A1(n52), .B0(n131), .B1(n60), .Y(n305) );
  OAI22_X1M_A12TH U690 ( .A0(n130), .A1(n51), .B0(n131), .B1(n59), .Y(n301) );
  OAI22_X1M_A12TH U691 ( .A0(n130), .A1(n50), .B0(n131), .B1(n58), .Y(n297) );
  OAI22_X1M_A12TH U692 ( .A0(n130), .A1(n49), .B0(n131), .B1(n57), .Y(n293) );
  NOR3_X1M_A12TH U693 ( .A(match[1]), .B(match[2]), .C(match[0]), .Y(n284) );
  NOR2XB_X1M_A12TH U694 ( .BN(n286), .A(match[4]), .Y(n285) );
  INV_X1M_A12TH U695 ( .A(match[0]), .Y(n125) );
  NOR2XB_X1M_A12TH U696 ( .BN(n284), .A(match[3]), .Y(n286) );
  INV_X1M_A12TH U697 ( .A(match[5]), .Y(n124) );
  INV_X1M_A12TH U698 ( .A(match[6]), .Y(n123) );
  OAI22_X1M_A12TH U699 ( .A0(n112), .A1(n125), .B0(n129), .B1(n104), .Y(n320)
         );
  OAI22_X1M_A12TH U700 ( .A0(n132), .A1(n72), .B0(n133), .B1(n80), .Y(n322) );
  OAI22_X1M_A12TH U701 ( .A0(n127), .A1(n88), .B0(n128), .B1(n96), .Y(n319) );
  OAI22_X1M_A12TH U702 ( .A0(n125), .A1(n111), .B0(n129), .B1(n103), .Y(n316)
         );
  OAI22_X1M_A12TH U703 ( .A0(n132), .A1(n71), .B0(n133), .B1(n79), .Y(n318) );
  OAI22_X1M_A12TH U704 ( .A0(n127), .A1(n87), .B0(n128), .B1(n95), .Y(n315) );
  OAI22_X1M_A12TH U705 ( .A0(n125), .A1(n110), .B0(n129), .B1(n102), .Y(n312)
         );
  OAI22_X1M_A12TH U706 ( .A0(n132), .A1(n70), .B0(n133), .B1(n78), .Y(n314) );
  OAI22_X1M_A12TH U707 ( .A0(n127), .A1(n86), .B0(n128), .B1(n94), .Y(n311) );
  OAI22_X1M_A12TH U708 ( .A0(n125), .A1(n109), .B0(n129), .B1(n101), .Y(n308)
         );
  OAI22_X1M_A12TH U709 ( .A0(n132), .A1(n69), .B0(n133), .B1(n77), .Y(n310) );
  OAI22_X1M_A12TH U710 ( .A0(n127), .A1(n85), .B0(n128), .B1(n93), .Y(n307) );
  OAI22_X1M_A12TH U711 ( .A0(n125), .A1(n108), .B0(n129), .B1(n100), .Y(n304)
         );
  OAI22_X1M_A12TH U712 ( .A0(n132), .A1(n68), .B0(n133), .B1(n76), .Y(n306) );
  OAI22_X1M_A12TH U713 ( .A0(n127), .A1(n84), .B0(n128), .B1(n92), .Y(n303) );
  OAI22_X1M_A12TH U714 ( .A0(n125), .A1(n107), .B0(n129), .B1(n99), .Y(n300)
         );
  OAI22_X1M_A12TH U715 ( .A0(n132), .A1(n67), .B0(n133), .B1(n75), .Y(n302) );
  OAI22_X1M_A12TH U716 ( .A0(n127), .A1(n83), .B0(n128), .B1(n91), .Y(n299) );
  OAI22_X1M_A12TH U717 ( .A0(n125), .A1(n106), .B0(n129), .B1(n98), .Y(n296)
         );
  OAI22_X1M_A12TH U718 ( .A0(n132), .A1(n66), .B0(n133), .B1(n74), .Y(n298) );
  OAI22_X1M_A12TH U719 ( .A0(n127), .A1(n82), .B0(n128), .B1(n90), .Y(n295) );
  OAI22_X1M_A12TH U720 ( .A0(n125), .A1(n105), .B0(n129), .B1(n97), .Y(n292)
         );
  OAI22_X1M_A12TH U721 ( .A0(n132), .A1(n65), .B0(n133), .B1(n73), .Y(n294) );
  OAI22_X1M_A12TH U722 ( .A0(n127), .A1(n81), .B0(n128), .B1(n89), .Y(n291) );
  OR4_X1M_A12TH U723 ( .A(match[2]), .B(match[3]), .C(match[1]), .D(n287), .Y(
        N204) );
  NAND4B_X1M_A12TH U724 ( .AN(match[4]), .B(n122), .C(n124), .D(n123), .Y(n287) );
  INV_X1M_A12TH U725 ( .A(match[7]), .Y(n122) );
  INV_X1M_A12TH U726 ( .A(nrst), .Y(n126) );
endmodule

