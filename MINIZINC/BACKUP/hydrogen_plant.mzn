% Use this editor as a MiniZinc scratch book
int: N;

set of int: tint = 1..N;     %number of intervals
set of int: tsamp = 1..N+1;    %number of sample points


float: DT;      %time difference between sample points (also, interval length) (s)
float: ETA_PV;  %efficiency of PV plant
float: ETA_W;   %efficienct of wind farm
float: ETA_EL;  %conversion efficiency of the electrolyser (kgH/s/W)
float: C_PV;    %unit cost of PV plant  $/W
float: C_W;     %unit cost of wind farm $/W
float: C_E;     %unit cost of electrolyser $/W
float: C_HS;    %unit cost of hydrogen storage $/(kg of H)
float: R;       %virtual hydrogen reserve for reduced capacity factor (kg of H)
  

array[tint] of float: W; %wind speed timeseries
array[tint] of float: S; %solar radiation timeseries
array[tint] of float: L; %load timeseries (kg of H per hour)



% === VARIABLES ===
float: p_pv;    %PV plant rated power
float: p_w;     %wind farm rated power
float: p_e;     %electrolyser rated power
float: e_hs;    %capacity of hydrogen storage cavern


array[tint] of var float: pv_out;    %power out of PV plant (W)
array[tint] of var float: w_out;     %power out of wind farm (W)
array[tint] of var float: pc;    %curtailed power (W)
array[tint] of var float: pe_in;    %power into the electrolyser (W)
array[tint] of var float: hr_out;   %hydrogen extracted from virtual reserve (kgH/s)
array[tsamp] of var float: sh;   %stored hydrogen in storage (kg)
array[tsamp] of var float: r;    %reserved hydrogen for load shut down (kg)


var float: obj;
obj = C_PV*p_pv + C_W*p_w + C_E*p_e + C_HS*e_hs;

%=== CONSTRAINTS ===
constraint r[1] = R;
constraint sh[1] = 0.5 * e_hs;

constraint p_pv >= 0;
constraint p_w >= 0;
constraint p_e >= 0;
constraint e_hs >= 0;

constraint forall(i in tint)(pv_out[i] = ETA_PV * p_pv * S[i]);
constraint forall(i in tint)(w_out[i] = p_w * (  (W[i]-0)/(20-0)  )^2  );

constraint forall(i in tint)(pv_out[i] + w_out[i] - pc[i] - pe_in[i]=0);
constraint forall(i in tint)(pc[i] >= 0);

constraint forall(i in tint)(pe_in[i] >= 0);
constraint forall(i in tint)(pe_in[i] - p_e<= 0);

constraint forall(i in tsamp)(sh[i] >= 0);
constraint forall(i in tsamp)(sh[i] - e_hs <= 0);
constraint forall(i in tsamp)(sh[i+1] = sh[i] + (pv_out[i]+w_out[i]-pc[i]) * ETA_EL* DT / 142e6 - (L[i]-hr_out[i])*DT);

constraint forall(i in tsamp)(r[i] >= 0);
constraint forall(i in tsamp)(r[i] <= R);
constraint forall(i in tsamp)(r[i+1] = r[i] - hr_out[i]*DT );
constraint forall(i in tint)(hr_out[i]>=0);


solve minimize obj;

%output [show(obj)]

output  ["p_pv="] ++ [show(p_pv)] ++ [";"] ++
        ["p_w="] ++ [show(p_pv)] ++ [";"] ++
        ["sh="] ++ [show(sh)] ++ [";"] ++
        ["r="] ++ [show(r)] ++ [";"];

