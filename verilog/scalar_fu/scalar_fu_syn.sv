/////////////////////////////////////////////////////////////
// Created by: Synopsys DC Expert(TM) in wire load mode
// Version   : L-2016.03-SP2
// Date      : Mon Jul 17 23:16:39 2017
/////////////////////////////////////////////////////////////


module scalar_fu_DW01_add_1 ( A, B, CI, SUM, CO );
  input [8:0] A;
  input [8:0] B;
  output [8:0] SUM;
  input CI;
  output CO;
  wire   n1;
  wire   [8:1] carry;
  tri   [8:0] A;
  tri   [8:0] B;

  ADDF_X1M_A12TH U1_7 ( .A(A[7]), .B(B[7]), .CI(carry[7]), .CO(carry[8]), .S(
        SUM[7]) );
  ADDF_X1M_A12TH U1_6 ( .A(A[6]), .B(B[6]), .CI(carry[6]), .CO(carry[7]), .S(
        SUM[6]) );
  ADDF_X1M_A12TH U1_5 ( .A(A[5]), .B(B[5]), .CI(carry[5]), .CO(carry[6]), .S(
        SUM[5]) );
  ADDF_X1M_A12TH U1_4 ( .A(A[4]), .B(B[4]), .CI(carry[4]), .CO(carry[5]), .S(
        SUM[4]) );
  ADDF_X1M_A12TH U1_3 ( .A(A[3]), .B(B[3]), .CI(carry[3]), .CO(carry[4]), .S(
        SUM[3]) );
  ADDF_X1M_A12TH U1_2 ( .A(A[2]), .B(B[2]), .CI(carry[2]), .CO(carry[3]), .S(
        SUM[2]) );
  ADDF_X1M_A12TH U1_1 ( .A(A[1]), .B(B[1]), .CI(n1), .CO(carry[2]), .S(SUM[1])
         );
  ADDF_X1M_A12TH U1_8 ( .A(A[8]), .B(B[8]), .CI(carry[8]), .S(SUM[8]) );
  AND2_X1M_A12TH U1 ( .A(B[0]), .B(A[0]), .Y(n1) );
  XOR2_X1M_A12TH U2 ( .A(B[0]), .B(A[0]), .Y(SUM[0]) );
endmodule


module scalar_fu_DW_mult_tc_0 ( a, b, product );
  input [7:0] a;
  input [7:0] b;
  output [15:0] product;
  wire   n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13, n14, n15, n16,
         n17, n18, n19, n20, n21, n22, n23, n24, n25, n26, n27, n28, n29, n30,
         n31, n32, n33, n34, n35, n36, n37, n38, n39, n40, n41, n42, n43, n44,
         n45, n46, n47, n48, n49, n50, n51, n52, n53, n54, n55, n56, n57, n58,
         n59, n60, n61, n62, n63, n64, n65, n67, n68, n69, n70, n71, n72, n73,
         n74, n75, n76, n77, n79, n80, n81, n82, n83, n84, n85, n86, n87, n88,
         n89, n90, n91, n92, n194, n195, n196, n197, n198, n199, n200, n201,
         n202, n203, n204, n205, n206, n207, n208, n209, n210, n211, n212,
         n213, n214, n215, n216, n217, n218, n219, n220, n221, n222, n223,
         n224, n225, n226, n227, n228, n229, n230, n231, n232, n233, n234,
         n235, n236, n237, n238, n239, n240, n241, n242, n243, n244, n245,
         n246, n247, n248, n249;
  tri   \b[7] ;
  tri   \b[6] ;
  tri   \b[5] ;
  tri   \b[4] ;
  tri   \b[3] ;
  tri   \b[2] ;
  tri   \b[1] ;
  tri   \b[0] ;
  tri   \a[0] ;
  tri   \a[1] ;
  tri   \a[2] ;
  tri   \a[3] ;
  tri   \a[4] ;
  tri   \a[5] ;
  tri   \a[6] ;
  tri   \a[7] ;

  ADDF_X1M_A12TH U2 ( .A(n15), .B(n61), .CI(n2), .CO(n1), .S(product[14]) );
  ADDF_X1M_A12TH U3 ( .A(n16), .B(n17), .CI(n3), .CO(n2), .S(product[13]) );
  ADDF_X1M_A12TH U4 ( .A(n18), .B(n19), .CI(n4), .CO(n3), .S(product[12]) );
  ADDF_X1M_A12TH U5 ( .A(n20), .B(n23), .CI(n5), .CO(n4), .S(product[11]) );
  ADDF_X1M_A12TH U6 ( .A(n27), .B(n24), .CI(n6), .CO(n5), .S(product[10]) );
  ADDF_X1M_A12TH U7 ( .A(n33), .B(n28), .CI(n7), .CO(n6), .S(product[9]) );
  ADDF_X1M_A12TH U8 ( .A(n39), .B(n34), .CI(n8), .CO(n7), .S(product[8]) );
  ADDF_X1M_A12TH U9 ( .A(n45), .B(n40), .CI(n9), .CO(n8), .S(product[7]) );
  ADDF_X1M_A12TH U10 ( .A(n49), .B(n46), .CI(n10), .CO(n9), .S(product[6]) );
  ADDF_X1M_A12TH U11 ( .A(n52), .B(n50), .CI(n11), .CO(n10), .S(product[5]) );
  ADDF_X1M_A12TH U12 ( .A(n55), .B(n54), .CI(n12), .CO(n11), .S(product[4]) );
  ADDF_X1M_A12TH U13 ( .A(n59), .B(n56), .CI(n13), .CO(n12), .S(product[3]) );
  ADDF_X1M_A12TH U14 ( .A(n84), .B(n91), .CI(n14), .CO(n13), .S(product[2]) );
  ADDH_X1M_A12TH U15 ( .A(n92), .B(n60), .CO(n14), .S(product[1]) );
  ADDF_X1M_A12TH U17 ( .A(n21), .B(n62), .CI(n69), .CO(n17), .S(n18) );
  ADDF_X1M_A12TH U18 ( .A(n63), .B(n22), .CI(n25), .CO(n19), .S(n20) );
  ADDF_X1M_A12TH U20 ( .A(n77), .B(n29), .CI(n26), .CO(n23), .S(n24) );
  ADDF_X1M_A12TH U21 ( .A(n31), .B(n70), .CI(n64), .CO(n25), .S(n26) );
  ADDF_X1M_A12TH U22 ( .A(n37), .B(n35), .CI(n30), .CO(n27), .S(n28) );
  ADDF_X1M_A12TH U23 ( .A(n71), .B(n65), .CI(n32), .CO(n29), .S(n30) );
  ADDF_X1M_A12TH U25 ( .A(n38), .B(n41), .CI(n36), .CO(n33), .S(n34) );
  ADDF_X1M_A12TH U26 ( .A(n72), .B(n85), .CI(n43), .CO(n35), .S(n36) );
  ADDF_X1M_A12TH U29 ( .A(n47), .B(n44), .CI(n42), .CO(n39), .S(n40) );
  ADDF_X1M_A12TH U30 ( .A(n86), .B(n73), .CI(n79), .CO(n41), .S(n42) );
  ADDH_X1M_A12TH U31 ( .A(n57), .B(n67), .CO(n43), .S(n44) );
  ADDF_X1M_A12TH U32 ( .A(n74), .B(n51), .CI(n48), .CO(n45), .S(n46) );
  ADDF_X1M_A12TH U33 ( .A(n68), .B(n87), .CI(n80), .CO(n47), .S(n48) );
  ADDF_X1M_A12TH U34 ( .A(n88), .B(n81), .CI(n53), .CO(n49), .S(n50) );
  ADDH_X1M_A12TH U35 ( .A(n58), .B(n75), .CO(n51), .S(n52) );
  ADDF_X1M_A12TH U36 ( .A(n76), .B(n89), .CI(n82), .CO(n53), .S(n54) );
  ADDH_X1M_A12TH U37 ( .A(n83), .B(n90), .CO(n55), .S(n56) );
  XNOR2_X1M_A12TH U145 ( .A(a[4]), .B(a[3]), .Y(n216) );
  XNOR2_X1M_A12TH U146 ( .A(a[6]), .B(a[5]), .Y(n228) );
  NAND2_X1M_A12TH U147 ( .A(a[1]), .B(n194), .Y(n197) );
  INV_X1M_A12TH U148 ( .A(a[0]), .Y(n194) );
  INV_X1M_A12TH U149 ( .A(b[0]), .Y(n195) );
  INV_X0P5B_A12TH U150 ( .A(n1), .Y(product[15]) );
  NOR2_X0P5A_A12TH U151 ( .A(n194), .B(n195), .Y(product[0]) );
  OAI22_X0P5M_A12TH U152 ( .A0(n196), .A1(n194), .B0(b[0]), .B1(n197), .Y(n92)
         );
  OAI22_X0P5M_A12TH U153 ( .A0(n198), .A1(n194), .B0(n196), .B1(n197), .Y(n91)
         );
  XOR2_X0P5M_A12TH U154 ( .A(b[1]), .B(n199), .Y(n196) );
  OAI22_X0P5M_A12TH U155 ( .A0(n200), .A1(n194), .B0(n198), .B1(n197), .Y(n90)
         );
  XOR2_X0P5M_A12TH U156 ( .A(b[2]), .B(n199), .Y(n198) );
  OAI22_X0P5M_A12TH U157 ( .A0(n201), .A1(n194), .B0(n200), .B1(n197), .Y(n89)
         );
  XOR2_X0P5M_A12TH U158 ( .A(b[3]), .B(n199), .Y(n200) );
  OAI22_X0P5M_A12TH U159 ( .A0(n202), .A1(n194), .B0(n201), .B1(n197), .Y(n88)
         );
  XOR2_X0P5M_A12TH U160 ( .A(b[4]), .B(n199), .Y(n201) );
  OAI22_X0P5M_A12TH U161 ( .A0(n203), .A1(n194), .B0(n202), .B1(n197), .Y(n87)
         );
  XOR2_X0P5M_A12TH U162 ( .A(b[5]), .B(n199), .Y(n202) );
  OAI22_X0P5M_A12TH U163 ( .A0(n204), .A1(n194), .B0(n203), .B1(n197), .Y(n86)
         );
  XOR2_X0P5M_A12TH U164 ( .A(b[6]), .B(n199), .Y(n203) );
  AO21_X0P5M_A12TH U165 ( .A0(n194), .A1(n197), .B0(n204), .Y(n85) );
  XNOR2_X0P5M_A12TH U166 ( .A(b[7]), .B(a[1]), .Y(n204) );
  NOR2_X0P5A_A12TH U167 ( .A(n205), .B(n195), .Y(n84) );
  OAI22_X0P5M_A12TH U168 ( .A0(n205), .A1(n206), .B0(n207), .B1(n208), .Y(n83)
         );
  XOR2_X0P5M_A12TH U169 ( .A(a[3]), .B(n195), .Y(n207) );
  OAI22_X0P5M_A12TH U170 ( .A0(n205), .A1(n209), .B0(n206), .B1(n208), .Y(n82)
         );
  XNOR2_X0P5M_A12TH U171 ( .A(b[1]), .B(a[3]), .Y(n206) );
  OAI22_X0P5M_A12TH U172 ( .A0(n205), .A1(n210), .B0(n209), .B1(n208), .Y(n81)
         );
  XNOR2_X0P5M_A12TH U173 ( .A(b[2]), .B(a[3]), .Y(n209) );
  OAI22_X0P5M_A12TH U174 ( .A0(n205), .A1(n211), .B0(n210), .B1(n208), .Y(n80)
         );
  XNOR2_X0P5M_A12TH U175 ( .A(b[3]), .B(a[3]), .Y(n210) );
  OAI22_X0P5M_A12TH U176 ( .A0(n205), .A1(n212), .B0(n211), .B1(n208), .Y(n79)
         );
  XNOR2_X0P5M_A12TH U177 ( .A(b[4]), .B(a[3]), .Y(n211) );
  OAI21_X0P5M_A12TH U178 ( .A0(n213), .A1(n214), .B0(n215), .Y(n77) );
  NOR2_X0P5A_A12TH U179 ( .A(n216), .B(n195), .Y(n76) );
  OAI22_X0P5M_A12TH U180 ( .A0(n216), .A1(n217), .B0(n218), .B1(n219), .Y(n75)
         );
  XOR2_X0P5M_A12TH U181 ( .A(a[5]), .B(n195), .Y(n218) );
  OAI22_X0P5M_A12TH U182 ( .A0(n216), .A1(n220), .B0(n217), .B1(n219), .Y(n74)
         );
  XNOR2_X0P5M_A12TH U183 ( .A(b[1]), .B(a[5]), .Y(n217) );
  OAI22_X0P5M_A12TH U184 ( .A0(n216), .A1(n221), .B0(n220), .B1(n219), .Y(n73)
         );
  XNOR2_X0P5M_A12TH U185 ( .A(b[2]), .B(a[5]), .Y(n220) );
  OAI22_X0P5M_A12TH U186 ( .A0(n216), .A1(n222), .B0(n221), .B1(n219), .Y(n72)
         );
  XNOR2_X0P5M_A12TH U187 ( .A(b[3]), .B(a[5]), .Y(n221) );
  OAI22_X0P5M_A12TH U188 ( .A0(n216), .A1(n223), .B0(n222), .B1(n219), .Y(n71)
         );
  XNOR2_X0P5M_A12TH U189 ( .A(b[4]), .B(a[5]), .Y(n222) );
  OAI22_X0P5M_A12TH U190 ( .A0(n216), .A1(n224), .B0(n223), .B1(n219), .Y(n70)
         );
  XNOR2_X0P5M_A12TH U191 ( .A(b[5]), .B(a[5]), .Y(n223) );
  OAI21B_X0P5M_A12TH U192 ( .A0(n225), .A1(n226), .B0N(n227), .Y(n69) );
  NOR2_X0P5A_A12TH U193 ( .A(n228), .B(n195), .Y(n68) );
  OAI22_X0P5M_A12TH U194 ( .A0(n228), .A1(n229), .B0(n230), .B1(n231), .Y(n67)
         );
  XOR2_X0P5M_A12TH U195 ( .A(a[7]), .B(n195), .Y(n230) );
  OAI22_X0P5M_A12TH U196 ( .A0(n228), .A1(n232), .B0(n233), .B1(n231), .Y(n65)
         );
  OAI22_X0P5M_A12TH U197 ( .A0(n228), .A1(n234), .B0(n232), .B1(n231), .Y(n64)
         );
  XNOR2_X0P5M_A12TH U198 ( .A(b[3]), .B(a[7]), .Y(n232) );
  OAI22_X0P5M_A12TH U199 ( .A0(n228), .A1(n235), .B0(n234), .B1(n231), .Y(n63)
         );
  XNOR2_X0P5M_A12TH U200 ( .A(b[4]), .B(a[7]), .Y(n234) );
  OAI22_X0P5M_A12TH U201 ( .A0(n228), .A1(n236), .B0(n235), .B1(n231), .Y(n62)
         );
  XNOR2_X0P5M_A12TH U202 ( .A(b[5]), .B(a[7]), .Y(n235) );
  OAI21B_X0P5M_A12TH U203 ( .A0(n237), .A1(n238), .B0N(n239), .Y(n61) );
  OAI21_X0P5M_A12TH U204 ( .A0(b[0]), .A1(n199), .B0(n197), .Y(n60) );
  INV_X0P5B_A12TH U205 ( .A(a[1]), .Y(n199) );
  INV_X0P5B_A12TH U206 ( .A(n240), .Y(n59) );
  AOI32_X0P5M_A12TH U207 ( .A0(n214), .A1(n195), .A2(a[3]), .B0(n213), .B1(
        a[3]), .Y(n240) );
  INV_X0P5B_A12TH U208 ( .A(n241), .Y(n58) );
  AOI32_X0P5M_A12TH U209 ( .A0(n226), .A1(n195), .A2(a[5]), .B0(n225), .B1(
        a[5]), .Y(n241) );
  INV_X0P5B_A12TH U210 ( .A(n219), .Y(n225) );
  INV_X0P5B_A12TH U211 ( .A(n216), .Y(n226) );
  INV_X0P5B_A12TH U212 ( .A(n242), .Y(n57) );
  AOI32_X0P5M_A12TH U213 ( .A0(n238), .A1(n195), .A2(a[7]), .B0(n237), .B1(
        a[7]), .Y(n242) );
  INV_X0P5B_A12TH U214 ( .A(n231), .Y(n237) );
  INV_X0P5B_A12TH U215 ( .A(n228), .Y(n238) );
  XNOR2_X0P5M_A12TH U216 ( .A(n243), .B(n244), .Y(n38) );
  NAND2_X0P5A_A12TH U217 ( .A(n243), .B(n244), .Y(n37) );
  AOI22_X0P5M_A12TH U218 ( .A0(n214), .A1(n245), .B0(n246), .B1(n213), .Y(n244) );
  INV_X0P5B_A12TH U219 ( .A(n212), .Y(n246) );
  XNOR2_X0P5M_A12TH U220 ( .A(b[5]), .B(a[3]), .Y(n212) );
  OA22_X0P5M_A12TH U221 ( .A0(n228), .A1(n233), .B0(n229), .B1(n231), .Y(n243)
         );
  XNOR2_X0P5M_A12TH U222 ( .A(b[1]), .B(a[7]), .Y(n229) );
  XNOR2_X0P5M_A12TH U223 ( .A(b[2]), .B(a[7]), .Y(n233) );
  INV_X0P5B_A12TH U224 ( .A(n32), .Y(n31) );
  AOI22_X0P5M_A12TH U225 ( .A0(n214), .A1(n215), .B0(n245), .B1(n213), .Y(n32)
         );
  INV_X0P5B_A12TH U226 ( .A(n208), .Y(n213) );
  NAND2_X0P5A_A12TH U227 ( .A(n205), .B(n247), .Y(n208) );
  XOR2_X0P5M_A12TH U228 ( .A(a[3]), .B(a[2]), .Y(n247) );
  INV_X0P5B_A12TH U229 ( .A(n214), .Y(n205) );
  XOR2_X0P5M_A12TH U230 ( .A(b[6]), .B(a[3]), .Y(n245) );
  XOR2_X0P5M_A12TH U231 ( .A(b[7]), .B(a[3]), .Y(n215) );
  XOR2_X0P5M_A12TH U232 ( .A(a[2]), .B(a[1]), .Y(n214) );
  INV_X0P5B_A12TH U233 ( .A(n21), .Y(n22) );
  OAI22_X0P5M_A12TH U234 ( .A0(n216), .A1(n227), .B0(n224), .B1(n219), .Y(n21)
         );
  NAND2_X0P5A_A12TH U235 ( .A(n216), .B(n248), .Y(n219) );
  XOR2_X0P5M_A12TH U236 ( .A(a[5]), .B(a[4]), .Y(n248) );
  XNOR2_X0P5M_A12TH U237 ( .A(b[6]), .B(a[5]), .Y(n224) );
  XNOR2_X0P5M_A12TH U238 ( .A(b[7]), .B(a[5]), .Y(n227) );
  INV_X0P5B_A12TH U239 ( .A(n15), .Y(n16) );
  OAI22_X0P5M_A12TH U240 ( .A0(n228), .A1(n239), .B0(n236), .B1(n231), .Y(n15)
         );
  NAND2_X0P5A_A12TH U241 ( .A(n228), .B(n249), .Y(n231) );
  XOR2_X0P5M_A12TH U242 ( .A(a[7]), .B(a[6]), .Y(n249) );
  XNOR2_X0P5M_A12TH U243 ( .A(b[6]), .B(a[7]), .Y(n236) );
  XNOR2_X0P5M_A12TH U244 ( .A(b[7]), .B(a[7]), .Y(n239) );
endmodule


module scalar_fu ( \scif.a , \scif.b , \scif.c , \scif.aluop , \scif.out  );
  inout [7:0] \scif.a ;
  inout [7:0] \scif.b ;
  inout [7:0] \scif.c ;
  inout [2:0] \scif.aluop ;
  inout [15:0] \scif.out ;
  wire   N25, N26, N27, N28, N29, N30, N31, N32, N33, N50, N51, N52, N53, N54,
         N55, N56, N57, N58, N59, N60, N61, N62, N63, N64, N65, N66, N67, N68,
         N69, N70, N71, N72, N73, N74, N75, N76, N77, N78, N79, N80, N81, N82,
         N83, N84, N85, N86, N87, N88, N89, N98, N99, N100, N101, N102, N103,
         N104, N49, N48, N47, N46, N45, N44, N43, N42, N41, N40, N39, N38, N37,
         N36, N35, N34, n9, n29, n30, n32, n33, n35, n36, n37, n39, n41, n43,
         n45, n47, n49, n52, n53, n54, n55, n56, n57, n58, n59, n60, n61, n62,
         n63, n64, n65, n66, n67, n68, n69, n70, n71, n72, n73, n74, n75, n76,
         n77, n78, n79, n80, n81, n82, n83, n84, n85, n86, n87, n88, n89, n90,
         n91, n92, n93, n94, n95, n96, n97, n98, n99, n100, n101, n102, n103,
         n104, n105, n106, n107, n108, n109, n110, n111, n112, n113, n114,
         n115, n116, n117, n118, n119, n120, n121, n122, n123, n124, n125,
         n126, n127, n128, n129, n130, n131, n132, n133, n134, n135, n136,
         n137, n138, n139, n140, n141, n142, n143, n144, n145, n146, n147,
         n148, n149, n150, n151, n152, n153, n154, n155, n156, n157, n158,
         n159, n160, n161, n162, n163, n164, n165, n166, n167, n168, n169,
         n170, n171, n172, n173, n174, n175, n176, n177, n178, n179, n180,
         n181, n182, n183, n184, n185, n186, n187, n188, n189, n190, n191,
         n192, n193, n194, n195, n196, n197, n198, n199, n200, n201, n202,
         n203, n204, n205, n206, n207, n208, n209, n210, n211, n212;
  wire   [15:1] \add_10/carry ;
  tri   [7:0] \scif.a ;
  tri   [7:0] \scif.b ;
  tri   [7:0] \scif.c ;
  tri   \scif.aluop[2] ;
  tri   \scif.aluop[1] ;
  tri   \scif.aluop[0] ;
  tri   [15:0] \scif.out ;
  tri   N105;
  tran( N105, \scif.a  [7]);

  scalar_fu_DW01_add_1 add_9 ( .A({N105, N105, \scif.a [6:0]}), .B({
        \scif.b [7], \scif.b }), .CI(n9), .SUM({N33, N32, N31, N30, N29, N28, 
        N27, N26, N25}) );
  scalar_fu_DW_mult_tc_0 mult_11 ( .a({N105, \scif.a [6:0]}), .b(\scif.b ), 
        .product({N81, N80, N79, N78, N77, N76, N75, N74, N73, N72, N71, N70, 
        N69, N68, N67, N66}) );
  INV_X1M_A12TH U59 ( .A(n56), .Y(\scif.out [15]) );
  OAI211_X0P5M_A12TH U67 ( .A0(n29), .A1(n80), .B0(n65), .C0(n64), .Y(
        \scif.out [7]) );
  OAI211_X1M_A12TH U74 ( .A0(n29), .A1(n80), .B0(n79), .C0(n78), .Y(
        \scif.out [0]) );
  OAI211_X1M_A12TH U68 ( .A0(n29), .A1(n80), .B0(n67), .C0(n66), .Y(
        \scif.out [6]) );
  OAI211_X1M_A12TH U69 ( .A0(n29), .A1(n80), .B0(n69), .C0(n68), .Y(
        \scif.out [5]) );
  OAI211_X1M_A12TH U71 ( .A0(n29), .A1(n80), .B0(n73), .C0(n72), .Y(
        \scif.out [3]) );
  OAI211_X1M_A12TH U72 ( .A0(n29), .A1(n80), .B0(n75), .C0(n74), .Y(
        \scif.out [2]) );
  OAI211_X1M_A12TH U73 ( .A0(n29), .A1(n80), .B0(n77), .C0(n76), .Y(
        \scif.out [1]) );
  OAI211_X1M_A12TH U70 ( .A0(n29), .A1(n80), .B0(n71), .C0(n70), .Y(
        \scif.out [4]) );
  INV_X1M_A12TH U60 ( .A(n57), .Y(\scif.out [14]) );
  INV_X1M_A12TH U61 ( .A(n58), .Y(\scif.out [13]) );
  INV_X1M_A12TH U62 ( .A(n59), .Y(\scif.out [12]) );
  INV_X1M_A12TH U63 ( .A(n60), .Y(\scif.out [11]) );
  INV_X1M_A12TH U64 ( .A(n61), .Y(\scif.out [10]) );
  INV_X1M_A12TH U65 ( .A(n62), .Y(\scif.out [9]) );
  INV_X1M_A12TH U66 ( .A(n63), .Y(\scif.out [8]) );
  NOR3_X1M_A12TH U76 ( .A(\scif.aluop [0]), .B(\scif.aluop [2]), .C(n54), .Y(
        n81) );
  NOR3_X1M_A12TH U77 ( .A(\scif.aluop [1]), .B(\scif.aluop [2]), .C(
        \scif.aluop [0]), .Y(n82) );
  NOR3_X1M_A12TH U78 ( .A(\scif.c [7]), .B(\scif.c [6]), .C(\scif.c [5]), .Y(
        n83) );
  NOR3_X1M_A12TH U79 ( .A(\scif.b [7]), .B(\scif.b [6]), .C(\scif.b [5]), .Y(
        n84) );
  OR3_X1M_A12TH U80 ( .A(n174), .B(\scif.b [4]), .C(n180), .Y(n85) );
  OR3_X1M_A12TH U81 ( .A(n181), .B(\scif.b [4]), .C(n180), .Y(n86) );
  OR3_X1M_A12TH U82 ( .A(n140), .B(\scif.b [4]), .C(n180), .Y(n87) );
  OR3_X1M_A12TH U83 ( .A(n142), .B(\scif.b [4]), .C(n180), .Y(n88) );
  OR3_X1M_A12TH U84 ( .A(n148), .B(\scif.b [4]), .C(n180), .Y(n89) );
  OR3_X1M_A12TH U85 ( .A(n155), .B(\scif.b [4]), .C(n180), .Y(n90) );
  OR3_X1M_A12TH U86 ( .A(n158), .B(\scif.b [4]), .C(n180), .Y(n91) );
  OR3_X1M_A12TH U87 ( .A(n161), .B(\scif.b [4]), .C(n180), .Y(n92) );
  INV_X1M_A12TH U88 ( .A(n33), .Y(n52) );
  MXIT2_X0P7M_A12TH U89 ( .A(n93), .B(n99), .S0(n107), .Y(n112) );
  MXIT2_X0P7M_A12TH U90 ( .A(n106), .B(n105), .S0(n107), .Y(n115) );
  MXIT2_X0P7M_A12TH U91 ( .A(n138), .B(n144), .S0(n152), .Y(n156) );
  MXIT2_X0P7M_A12TH U92 ( .A(n151), .B(n150), .S0(n152), .Y(n159) );
  MXIT2_X0P7M_A12TH U93 ( .A(n99), .B(n98), .S0(n107), .Y(n126) );
  MXIT2_X0P7M_A12TH U94 ( .A(n105), .B(n104), .S0(n107), .Y(n131) );
  MXIT2_X0P7M_A12TH U95 ( .A(n98), .B(n101), .S0(n107), .Y(n113) );
  MXIT2_X0P7M_A12TH U96 ( .A(n104), .B(n108), .S0(n107), .Y(n116) );
  MXIT2_X0P7M_A12TH U97 ( .A(n144), .B(n143), .S0(n152), .Y(n170) );
  MXIT2_X0P7M_A12TH U98 ( .A(n150), .B(n149), .S0(n152), .Y(n175) );
  MXIT2_X0P7M_A12TH U99 ( .A(n143), .B(n146), .S0(n152), .Y(n157) );
  MXIT2_X0P7M_A12TH U100 ( .A(n149), .B(n153), .S0(n152), .Y(n160) );
  INV_X1M_A12TH U101 ( .A(n83), .Y(n136) );
  INV_X1M_A12TH U102 ( .A(n84), .Y(n180) );
  NAND2_X1M_A12TH U103 ( .A(n106), .B(n107), .Y(n118) );
  NAND2_X1M_A12TH U104 ( .A(n151), .B(n152), .Y(n162) );
  NAND2_X1M_A12TH U105 ( .A(n93), .B(n107), .Y(n100) );
  NAND2_X1M_A12TH U106 ( .A(n138), .B(n152), .Y(n145) );
  AND4_X1M_A12TH U107 ( .A(n129), .B(n83), .C(n133), .D(n124), .Y(N34) );
  INV_X1M_A12TH U108 ( .A(n190), .Y(n192) );
  AOI221_X1M_A12TH U109 ( .A0(N58), .A1(n30), .B0(N74), .B1(n81), .C0(n49), 
        .Y(n63) );
  OAI211_X1M_A12TH U110 ( .A0(n33), .A1(n85), .B0(n35), .C0(n36), .Y(n49) );
  AOI221_X1M_A12TH U111 ( .A0(N59), .A1(n30), .B0(N75), .B1(n81), .C0(n47), 
        .Y(n62) );
  OAI211_X1M_A12TH U112 ( .A0(n33), .A1(n86), .B0(n35), .C0(n36), .Y(n47) );
  AOI221_X1M_A12TH U113 ( .A0(N60), .A1(n30), .B0(N76), .B1(n81), .C0(n45), 
        .Y(n61) );
  OAI211_X1M_A12TH U114 ( .A0(n33), .A1(n87), .B0(n35), .C0(n36), .Y(n45) );
  AOI221_X1M_A12TH U115 ( .A0(N61), .A1(n30), .B0(N77), .B1(n81), .C0(n43), 
        .Y(n60) );
  OAI211_X1M_A12TH U116 ( .A0(n33), .A1(n88), .B0(n35), .C0(n36), .Y(n43) );
  AOI221_X1M_A12TH U117 ( .A0(N62), .A1(n30), .B0(N78), .B1(n81), .C0(n41), 
        .Y(n59) );
  OAI211_X1M_A12TH U118 ( .A0(n33), .A1(n89), .B0(n35), .C0(n36), .Y(n41) );
  AOI221_X1M_A12TH U119 ( .A0(N63), .A1(n30), .B0(N79), .B1(n81), .C0(n39), 
        .Y(n58) );
  OAI211_X1M_A12TH U120 ( .A0(n33), .A1(n90), .B0(n35), .C0(n36), .Y(n39) );
  AOI221_X1M_A12TH U121 ( .A0(N64), .A1(n30), .B0(N80), .B1(n81), .C0(n37), 
        .Y(n57) );
  OAI211_X1M_A12TH U122 ( .A0(n33), .A1(n91), .B0(n35), .C0(n36), .Y(n37) );
  NOR3_X1M_A12TH U123 ( .A(\scif.aluop [0]), .B(\scif.aluop [1]), .C(n55), .Y(
        n53) );
  NAND3_X1M_A12TH U124 ( .A(\scif.aluop [0]), .B(n55), .C(\scif.aluop [1]), 
        .Y(n33) );
  NAND2_X1M_A12TH U125 ( .A(N105), .B(n53), .Y(n35) );
  AOI22_X1M_A12TH U126 ( .A0(N102), .A1(n53), .B0(N86), .B1(n52), .Y(n71) );
  AOI222_X1M_A12TH U127 ( .A0(N29), .A1(n82), .B0(N70), .B1(n81), .C0(N54), 
        .C1(n30), .Y(n70) );
  AND4_X1M_A12TH U128 ( .A(n165), .B(n84), .C(n177), .D(n168), .Y(N86) );
  AOI22_X1M_A12TH U129 ( .A0(N83), .A1(n52), .B0(N99), .B1(n53), .Y(n77) );
  AOI222_X1M_A12TH U130 ( .A0(N26), .A1(n82), .B0(N67), .B1(n81), .C0(N51), 
        .C1(n30), .Y(n76) );
  AND4_X1M_A12TH U131 ( .A(n179), .B(n84), .C(n177), .D(n168), .Y(N83) );
  MXIT2_X0P7M_A12TH U132 ( .A(n126), .B(n100), .S0(\scif.c [2]), .Y(n121) );
  MXIT2_X0P7M_A12TH U133 ( .A(n131), .B(n118), .S0(\scif.c [2]), .Y(n122) );
  MXIT2_X0P7M_A12TH U134 ( .A(n113), .B(n112), .S0(\scif.c [2]), .Y(n123) );
  MXIT2_X0P7M_A12TH U135 ( .A(n116), .B(n115), .S0(\scif.c [2]), .Y(n125) );
  MXIT2_X0P7M_A12TH U136 ( .A(n170), .B(n145), .S0(\scif.b [2]), .Y(n165) );
  MXIT2_X0P7M_A12TH U137 ( .A(n175), .B(n162), .S0(\scif.b [2]), .Y(n166) );
  MXIT2_X0P7M_A12TH U138 ( .A(n157), .B(n156), .S0(\scif.b [2]), .Y(n167) );
  MXIT2_X0P7M_A12TH U139 ( .A(n160), .B(n159), .S0(\scif.b [2]), .Y(n169) );
  MXIT2_X0P7M_A12TH U140 ( .A(n191), .B(n193), .S0(\scif.b [1]), .Y(n202) );
  MXIT2_X0P7M_A12TH U141 ( .A(n197), .B(N105), .S0(\scif.b [1]), .Y(n205) );
  MXIT2_X0P7M_A12TH U142 ( .A(n193), .B(N105), .S0(\scif.b [1]), .Y(n208) );
  MXIT2_X0P7M_A12TH U143 ( .A(\scif.a [2]), .B(\scif.a [3]), .S0(\scif.b [0]), 
        .Y(n190) );
  MXIT2_X0P7M_A12TH U144 ( .A(n196), .B(n211), .S0(n210), .Y(N100) );
  MXIT2_X0P7M_A12TH U145 ( .A(n195), .B(N105), .S0(\scif.b [3]), .Y(n196) );
  MXIT2_X0P7M_A12TH U146 ( .A(n194), .B(n208), .S0(\scif.b [2]), .Y(n195) );
  MXIT2_X0P7M_A12TH U147 ( .A(n192), .B(n191), .S0(\scif.b [1]), .Y(n194) );
  MXIT2_X0P7M_A12TH U148 ( .A(n204), .B(n211), .S0(n210), .Y(N102) );
  MXIT2_X0P7M_A12TH U149 ( .A(n203), .B(N105), .S0(\scif.b [3]), .Y(n204) );
  MXIT2_X0P7M_A12TH U150 ( .A(n202), .B(n211), .S0(\scif.b [2]), .Y(n203) );
  MXIT2_X0P7M_A12TH U151 ( .A(n207), .B(n211), .S0(n210), .Y(N103) );
  MXIT2_X0P7M_A12TH U152 ( .A(n206), .B(N105), .S0(\scif.b [3]), .Y(n207) );
  MXIT2_X0P7M_A12TH U153 ( .A(n205), .B(n211), .S0(\scif.b [2]), .Y(n206) );
  MXIT2_X0P7M_A12TH U154 ( .A(n212), .B(n211), .S0(n210), .Y(N104) );
  MXIT2_X0P7M_A12TH U155 ( .A(n209), .B(N105), .S0(\scif.b [3]), .Y(n212) );
  MXIT2_X0P7M_A12TH U156 ( .A(n208), .B(n211), .S0(\scif.b [2]), .Y(n209) );
  NAND2_X1M_A12TH U157 ( .A(N33), .B(n82), .Y(n36) );
  AND3_X1M_A12TH U158 ( .A(n54), .B(n55), .C(\scif.aluop [0]), .Y(n30) );
  MXIT2_X0P7M_A12TH U159 ( .A(\scif.a [0]), .B(\scif.a [1]), .S0(\scif.b [0]), 
        .Y(n182) );
  MXIT2_X0P7M_A12TH U160 ( .A(n101), .B(\scif.b [7]), .S0(n107), .Y(n127) );
  MXIT2_X0P7M_A12TH U161 ( .A(n146), .B(N105), .S0(n152), .Y(n171) );
  MXIT2_X0P7M_A12TH U162 ( .A(n153), .B(N105), .S0(n152), .Y(n176) );
  MXIT2_X0P7M_A12TH U163 ( .A(n108), .B(\scif.b [7]), .S0(n107), .Y(n132) );
  MXIT2_X0P7M_A12TH U164 ( .A(n201), .B(n211), .S0(n210), .Y(N101) );
  MXIT2_X0P7M_A12TH U165 ( .A(n200), .B(N105), .S0(\scif.b [3]), .Y(n201) );
  MXIT2_X0P7M_A12TH U166 ( .A(n199), .B(n211), .S0(\scif.b [2]), .Y(n200) );
  MXIT2_X0P7M_A12TH U167 ( .A(n198), .B(n197), .S0(\scif.b [1]), .Y(n199) );
  MXIT2_X0P7M_A12TH U168 ( .A(n185), .B(n211), .S0(n210), .Y(N98) );
  MXIT2_X0P7M_A12TH U169 ( .A(n184), .B(N105), .S0(\scif.b [3]), .Y(n185) );
  MXIT2_X0P7M_A12TH U170 ( .A(n183), .B(n202), .S0(\scif.b [2]), .Y(n184) );
  MXT2_X1M_A12TH U171 ( .A(n182), .B(n190), .S0(\scif.b [1]), .Y(n183) );
  MXIT2_X0P7M_A12TH U172 ( .A(n189), .B(n211), .S0(n210), .Y(N99) );
  MXIT2_X0P7M_A12TH U173 ( .A(n188), .B(N105), .S0(\scif.b [3]), .Y(n189) );
  MXIT2_X0P7M_A12TH U174 ( .A(n187), .B(n205), .S0(\scif.b [2]), .Y(n188) );
  MXIT2_X0P7M_A12TH U175 ( .A(n186), .B(n198), .S0(\scif.b [1]), .Y(n187) );
  OR4_X1M_A12TH U176 ( .A(\scif.b [5]), .B(\scif.b [4]), .C(\scif.b [7]), .D(
        \scif.b [6]), .Y(n210) );
  INV_X1M_A12TH U177 ( .A(\scif.c [4]), .Y(n124) );
  INV_X1M_A12TH U178 ( .A(\scif.b [4]), .Y(n168) );
  MXIT2_X0P7M_A12TH U179 ( .A(n165), .B(n147), .S0(n177), .Y(n148) );
  MXIT2_X0P7M_A12TH U180 ( .A(n211), .B(n171), .S0(\scif.b [2]), .Y(n147) );
  MXIT2_X0P7M_A12TH U181 ( .A(n166), .B(n154), .S0(n177), .Y(n155) );
  MXIT2_X0P7M_A12TH U182 ( .A(n211), .B(n176), .S0(\scif.b [2]), .Y(n154) );
  MXIT2_X0P7M_A12TH U183 ( .A(n167), .B(N105), .S0(n177), .Y(n158) );
  MXIT2_X0P7M_A12TH U184 ( .A(n173), .B(n172), .S0(n177), .Y(n174) );
  MXIT2_X0P7M_A12TH U185 ( .A(n171), .B(n170), .S0(\scif.b [2]), .Y(n172) );
  MXIT2_X0P7M_A12TH U186 ( .A(n179), .B(n178), .S0(n177), .Y(n181) );
  MXIT2_X0P7M_A12TH U187 ( .A(n176), .B(n175), .S0(\scif.b [2]), .Y(n178) );
  MXIT2_X0P7M_A12TH U188 ( .A(n163), .B(n139), .S0(n177), .Y(n140) );
  MXIT2_X0P7M_A12TH U189 ( .A(n211), .B(n157), .S0(\scif.b [2]), .Y(n139) );
  MXIT2_X0P7M_A12TH U190 ( .A(n164), .B(n141), .S0(n177), .Y(n142) );
  MXIT2_X0P7M_A12TH U191 ( .A(n211), .B(n160), .S0(\scif.b [2]), .Y(n141) );
  MXT2_X1M_A12TH U192 ( .A(\scif.b [1]), .B(\scif.b [0]), .S0(\scif.c [0]), 
        .Y(n106) );
  MXT2_X1M_A12TH U193 ( .A(\scif.a [1]), .B(\scif.a [0]), .S0(\scif.b [0]), 
        .Y(n151) );
  ADDF_X1M_A12TH U194 ( .A(N105), .B(N42), .CI(\add_10/carry [8]), .CO(
        \add_10/carry [9]), .S(N58) );
  NOR3_X1M_A12TH U195 ( .A(n130), .B(\scif.c [4]), .C(n136), .Y(N42) );
  MXIT2_X0P7M_A12TH U196 ( .A(n129), .B(n128), .S0(n133), .Y(n130) );
  MXIT2_X0P7M_A12TH U197 ( .A(n127), .B(n126), .S0(\scif.c [2]), .Y(n128) );
  ADDF_X1M_A12TH U198 ( .A(N105), .B(N43), .CI(\add_10/carry [9]), .CO(
        \add_10/carry [10]), .S(N59) );
  NOR3_X1M_A12TH U199 ( .A(n137), .B(\scif.c [4]), .C(n136), .Y(N43) );
  MXIT2_X0P7M_A12TH U200 ( .A(n135), .B(n134), .S0(n133), .Y(n137) );
  MXIT2_X0P7M_A12TH U201 ( .A(n132), .B(n131), .S0(\scif.c [2]), .Y(n134) );
  ADDF_X1M_A12TH U202 ( .A(N105), .B(N44), .CI(\add_10/carry [10]), .CO(
        \add_10/carry [11]), .S(N60) );
  NOR3_X1M_A12TH U203 ( .A(n95), .B(\scif.c [4]), .C(n136), .Y(N44) );
  MXIT2_X0P7M_A12TH U204 ( .A(n119), .B(n94), .S0(n133), .Y(n95) );
  MXIT2_X0P7M_A12TH U205 ( .A(n109), .B(n113), .S0(\scif.c [2]), .Y(n94) );
  ADDF_X1M_A12TH U206 ( .A(N105), .B(N45), .CI(\add_10/carry [11]), .CO(
        \add_10/carry [12]), .S(N61) );
  NOR3_X1M_A12TH U207 ( .A(n97), .B(\scif.c [4]), .C(n136), .Y(N45) );
  MXIT2_X0P7M_A12TH U208 ( .A(n120), .B(n96), .S0(n133), .Y(n97) );
  MXIT2_X0P7M_A12TH U209 ( .A(n109), .B(n116), .S0(\scif.c [2]), .Y(n96) );
  ADDF_X1M_A12TH U210 ( .A(N105), .B(N46), .CI(\add_10/carry [12]), .CO(
        \add_10/carry [13]), .S(N62) );
  NOR3_X1M_A12TH U211 ( .A(n103), .B(\scif.c [4]), .C(n136), .Y(N46) );
  MXIT2_X0P7M_A12TH U212 ( .A(n121), .B(n102), .S0(n133), .Y(n103) );
  MXIT2_X0P7M_A12TH U213 ( .A(n109), .B(n127), .S0(\scif.c [2]), .Y(n102) );
  ADDF_X1M_A12TH U214 ( .A(N105), .B(N47), .CI(\add_10/carry [13]), .CO(
        \add_10/carry [14]), .S(N63) );
  NOR3_X1M_A12TH U215 ( .A(n111), .B(\scif.c [4]), .C(n136), .Y(N47) );
  MXIT2_X0P7M_A12TH U216 ( .A(n122), .B(n110), .S0(n133), .Y(n111) );
  MXIT2_X0P7M_A12TH U217 ( .A(n109), .B(n132), .S0(\scif.c [2]), .Y(n110) );
  ADDF_X1M_A12TH U218 ( .A(\scif.a [1]), .B(N35), .CI(\add_10/carry [1]), .CO(
        \add_10/carry [2]), .S(N51) );
  AND4_X1M_A12TH U219 ( .A(n135), .B(n83), .C(n133), .D(n124), .Y(N35) );
  ADDF_X1M_A12TH U220 ( .A(\scif.a [2]), .B(N36), .CI(\add_10/carry [2]), .CO(
        \add_10/carry [3]), .S(N52) );
  AND4_X1M_A12TH U221 ( .A(n119), .B(n83), .C(n133), .D(n124), .Y(N36) );
  ADDF_X1M_A12TH U222 ( .A(\scif.a [3]), .B(N37), .CI(\add_10/carry [3]), .CO(
        \add_10/carry [4]), .S(N53) );
  AND4_X1M_A12TH U223 ( .A(n120), .B(n83), .C(n133), .D(n124), .Y(N37) );
  ADDF_X1M_A12TH U224 ( .A(\scif.a [4]), .B(N38), .CI(\add_10/carry [4]), .CO(
        \add_10/carry [5]), .S(N54) );
  AND4_X1M_A12TH U225 ( .A(n121), .B(n83), .C(n133), .D(n124), .Y(N38) );
  ADDF_X1M_A12TH U226 ( .A(\scif.a [5]), .B(N39), .CI(\add_10/carry [5]), .CO(
        \add_10/carry [6]), .S(N55) );
  AND4_X1M_A12TH U227 ( .A(n122), .B(n83), .C(n133), .D(n124), .Y(N39) );
  ADDF_X1M_A12TH U228 ( .A(\scif.a [6]), .B(N40), .CI(\add_10/carry [6]), .CO(
        \add_10/carry [7]), .S(N56) );
  AND4_X1M_A12TH U229 ( .A(n123), .B(n83), .C(n133), .D(n124), .Y(N40) );
  ADDF_X1M_A12TH U230 ( .A(N105), .B(N41), .CI(\add_10/carry [7]), .CO(
        \add_10/carry [8]), .S(N57) );
  AND4_X1M_A12TH U231 ( .A(n125), .B(n83), .C(n133), .D(n124), .Y(N41) );
  ADDF_X1M_A12TH U232 ( .A(N105), .B(N48), .CI(\add_10/carry [14]), .CO(
        \add_10/carry [15]), .S(N64) );
  NOR3_X1M_A12TH U233 ( .A(n114), .B(\scif.c [4]), .C(n136), .Y(N48) );
  MXIT2_X0P7M_A12TH U234 ( .A(n123), .B(\scif.b [7]), .S0(n133), .Y(n114) );
  MXT2_X1M_A12TH U235 ( .A(\scif.b [2]), .B(\scif.b [1]), .S0(\scif.c [0]), 
        .Y(n99) );
  MXT2_X1M_A12TH U236 ( .A(\scif.b [4]), .B(\scif.b [3]), .S0(\scif.c [0]), 
        .Y(n98) );
  MXT2_X1M_A12TH U237 ( .A(\scif.b [3]), .B(\scif.b [2]), .S0(\scif.c [0]), 
        .Y(n105) );
  MXT2_X1M_A12TH U238 ( .A(\scif.b [5]), .B(\scif.b [4]), .S0(\scif.c [0]), 
        .Y(n104) );
  MXT2_X1M_A12TH U239 ( .A(\scif.b [6]), .B(\scif.b [5]), .S0(\scif.c [0]), 
        .Y(n101) );
  MXT2_X1M_A12TH U240 ( .A(\scif.b [7]), .B(\scif.b [6]), .S0(\scif.c [0]), 
        .Y(n108) );
  MXT2_X1M_A12TH U241 ( .A(\scif.a [2]), .B(\scif.a [1]), .S0(\scif.b [0]), 
        .Y(n144) );
  MXT2_X1M_A12TH U242 ( .A(\scif.a [3]), .B(\scif.a [2]), .S0(\scif.b [0]), 
        .Y(n150) );
  MXT2_X1M_A12TH U243 ( .A(\scif.a [4]), .B(\scif.a [3]), .S0(\scif.b [0]), 
        .Y(n143) );
  MXT2_X1M_A12TH U244 ( .A(\scif.a [5]), .B(\scif.a [4]), .S0(\scif.b [0]), 
        .Y(n149) );
  MXT2_X1M_A12TH U245 ( .A(\scif.a [6]), .B(\scif.a [5]), .S0(\scif.b [0]), 
        .Y(n146) );
  MXT2_X1M_A12TH U246 ( .A(N105), .B(\scif.a [6]), .S0(\scif.b [0]), .Y(n153)
         );
  MXT2_X1M_A12TH U247 ( .A(\scif.a [3]), .B(\scif.a [4]), .S0(\scif.b [0]), 
        .Y(n198) );
  MXT2_X1M_A12TH U248 ( .A(\scif.a [4]), .B(\scif.a [5]), .S0(\scif.b [0]), 
        .Y(n191) );
  MXT2_X1M_A12TH U249 ( .A(\scif.a [5]), .B(\scif.a [6]), .S0(\scif.b [0]), 
        .Y(n197) );
  MXT2_X1M_A12TH U250 ( .A(\scif.a [6]), .B(N105), .S0(\scif.b [0]), .Y(n193)
         );
  NOR2_X1M_A12TH U251 ( .A(n112), .B(\scif.c [2]), .Y(n119) );
  NOR2_X1M_A12TH U252 ( .A(n115), .B(\scif.c [2]), .Y(n120) );
  NOR2_X1M_A12TH U253 ( .A(n156), .B(\scif.b [2]), .Y(n163) );
  NOR2_X1M_A12TH U254 ( .A(n159), .B(\scif.b [2]), .Y(n164) );
  NOR3_X1M_A12TH U255 ( .A(n117), .B(\scif.c [4]), .C(n136), .Y(N49) );
  MXIT2_X0P7M_A12TH U256 ( .A(n125), .B(\scif.b [7]), .S0(n133), .Y(n117) );
  INV_X1M_A12TH U257 ( .A(\scif.c [3]), .Y(n133) );
  INV_X1M_A12TH U258 ( .A(\scif.b [3]), .Y(n177) );
  NOR2XB_X1M_A12TH U259 ( .BN(\scif.b [0]), .A(\scif.c [0]), .Y(n93) );
  NOR2XB_X1M_A12TH U260 ( .BN(\scif.a [0]), .A(\scif.b [0]), .Y(n138) );
  AOI22_X1M_A12TH U261 ( .A0(N100), .A1(n53), .B0(N84), .B1(n52), .Y(n75) );
  AOI222_X1M_A12TH U262 ( .A0(N27), .A1(n82), .B0(N68), .B1(n81), .C0(N52), 
        .C1(n30), .Y(n74) );
  AND4_X1M_A12TH U263 ( .A(n163), .B(n84), .C(n177), .D(n168), .Y(N84) );
  AOI22_X1M_A12TH U264 ( .A0(N101), .A1(n53), .B0(N85), .B1(n52), .Y(n73) );
  AOI222_X1M_A12TH U265 ( .A0(N28), .A1(n82), .B0(N69), .B1(n81), .C0(N53), 
        .C1(n30), .Y(n72) );
  AND4_X1M_A12TH U266 ( .A(n164), .B(n84), .C(n177), .D(n168), .Y(N85) );
  AOI22_X1M_A12TH U267 ( .A0(N103), .A1(n53), .B0(N87), .B1(n52), .Y(n69) );
  AOI222_X1M_A12TH U268 ( .A0(N30), .A1(n82), .B0(N71), .B1(n81), .C0(N55), 
        .C1(n30), .Y(n68) );
  AND4_X1M_A12TH U269 ( .A(n166), .B(n84), .C(n177), .D(n168), .Y(N87) );
  AOI22_X1M_A12TH U270 ( .A0(N104), .A1(n53), .B0(N88), .B1(n52), .Y(n67) );
  AOI222_X1M_A12TH U271 ( .A0(N31), .A1(n82), .B0(N72), .B1(n81), .C0(N56), 
        .C1(n30), .Y(n66) );
  AND4_X1M_A12TH U272 ( .A(n167), .B(n84), .C(n177), .D(n168), .Y(N88) );
  AOI22_X1M_A12TH U273 ( .A0(N82), .A1(n52), .B0(N98), .B1(n53), .Y(n79) );
  AOI222_X1M_A12TH U274 ( .A0(N25), .A1(n82), .B0(N66), .B1(n81), .C0(N50), 
        .C1(n30), .Y(n78) );
  AND4_X1M_A12TH U275 ( .A(n173), .B(n84), .C(n177), .D(n168), .Y(N82) );
  AOI21B_X1M_A12TH U276 ( .A0(N89), .A1(n52), .B0N(n35), .Y(n65) );
  AOI222_X1M_A12TH U277 ( .A0(N32), .A1(n82), .B0(N73), .B1(n81), .C0(N57), 
        .C1(n30), .Y(n64) );
  AND4_X1M_A12TH U278 ( .A(n169), .B(n84), .C(n177), .D(n168), .Y(N89) );
  MXT2_X1M_A12TH U279 ( .A(\scif.a [1]), .B(\scif.a [2]), .S0(\scif.b [0]), 
        .Y(n186) );
  NOR2_X1M_A12TH U280 ( .A(n118), .B(\scif.c [2]), .Y(n135) );
  NOR2_X1M_A12TH U281 ( .A(n162), .B(\scif.b [2]), .Y(n179) );
  NOR2_X1M_A12TH U282 ( .A(n100), .B(\scif.c [2]), .Y(n129) );
  NOR2_X1M_A12TH U283 ( .A(n145), .B(\scif.b [2]), .Y(n173) );
  INV_X1M_A12TH U284 ( .A(N105), .Y(n211) );
  INV_X1M_A12TH U285 ( .A(\scif.b [7]), .Y(n109) );
  INV_X1M_A12TH U286 ( .A(\scif.c [1]), .Y(n107) );
  INV_X1M_A12TH U287 ( .A(\scif.b [1]), .Y(n152) );
  INV_X1M_A12TH U288 ( .A(\scif.aluop [2]), .Y(n55) );
  AOI221_X1M_A12TH U289 ( .A0(N65), .A1(n30), .B0(N81), .B1(n81), .C0(n32), 
        .Y(n56) );
  OAI211_X1M_A12TH U290 ( .A0(n33), .A1(n92), .B0(n35), .C0(n36), .Y(n32) );
  ADDF_X1M_A12TH U291 ( .A(N105), .B(N49), .CI(\add_10/carry [15]), .S(N65) );
  MXIT2_X0P7M_A12TH U292 ( .A(n169), .B(N105), .S0(n177), .Y(n161) );
  INV_X1M_A12TH U293 ( .A(\scif.aluop [1]), .Y(n54) );
  OAI21_X1M_A12TH U294 ( .A0(\scif.aluop [1]), .A1(\scif.aluop [0]), .B0(
        \scif.aluop [2]), .Y(n80) );
  TIELO_X1M_A12TH U295 ( .Y(n9) );
  TIEHI_X1M_A12TH U296 ( .Y(n29) );
  AND2_X0P5M_A12TH U297 ( .A(\scif.a [0]), .B(N34), .Y(\add_10/carry [1]) );
  XOR2_X0P5M_A12TH U298 ( .A(N34), .B(\scif.a [0]), .Y(N50) );
endmodule

