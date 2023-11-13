module top(in_data, out_data);
  input [2:0] in_data;
  wire [2:0] in_data;
  output out_data;
  wire out_data;
  reg _0_;
  always_ff @(POLARITY_0 in_data[0], POLARITY_1 in_data[1])
    if (!in_data[1]) _0_ <= 1'b1;
    else _0_ <= in_data[2];
  assign out_data = _0_;
endmodule
