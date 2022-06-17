% Use this editor as a MiniZinc scratch book
int: N;

set of int: tint = 1..N;     %number of intervals
set of int: tsamp = 1..N+1;    %number of sample points

float: DT;      %time difference between sample points (also, interval length) (s)
float: ETA_EL;  %conversion efficiency of the electrolyser (kgH/s/W)
float: BAT_ETA_in;   %charging efficiency of electrochemical battery
float: BAT_ETA_out;  %discharging efficiency of electrochemical battery 
float: C_PV;    %unit cost of PV plant  $/W
float: C_W;     %unit cost of wind farm $/W
float: C_EL;     %unit cost of electrolyser $/W
float: C_HS;    %unit cost of hydrogen storage $/(kg of H)
float: C_BAT_energy;    %unit cost of battery storage ($/W.s)
float: C_BAT_power;    % unit cost of battery power capacpity ($/W)
float: R_CAPA;       %virtual hydrogen reserve for reduced capacity factor (kg of H)
float: pv_ref_capa;    %power capacity of the reference PV plant (W)
float: wind_ref_capa;    %power capacity of the reference wind plant (W)

%array[tint] of float: W; %wind speed timeseries
%array[tint] of float: S; %solar radiation timeseries
array[tint] of float: L; %load timeseries (kg of H per hour)
array[tint] of var float: pv_ref_out;    %power output from the reference PV plant (W)
array[tint] of var float: wind_ref_out;    %power output from the reference wind plant (W)

% === VARIABLES ===
var float: pv_max;    %PV plant rated power
var float: w_max;     %wind farm rated power
var float: el_max;     %electrolyser rated power
var float: hs_capa;    %capacity of hydrogen storage cavern
var float: bat_capa;    %energy capacity of the electrochemical battery (J)
var float: bat_pmax;    %power capacity of the electrochemical battery (W)

array[tint] of var float: pv_out;    %power out of PV plant (W)
array[tint] of var float: w_out;     %power out of wind farm (W)
array[tint] of var float: pc;    %curtailed power (W)
array[tint] of var float: el_pin_wpv;    %power into the electrolyser (W)
array[tint] of var float: r_hout;   %hydrogen extracted from virtual reserve (kgH/s)
array[tint] of var float: el_hout;    %hydrogen produced in each interval (kgH/s)
array[tint] of var float: el_pin;    %power flow into the electrolyser (W)
array[tint] of var float: bat_pin;      %power flow into the battery (W)
array[tint] of var float: bat_pout;     %power flow out of the battery (W)
array[tsamp] of var float: h_stored;   %stored hydrogen in storage (kg)
array[tsamp] of var float: r;    %reserved hydrogen for load shut down (kg)
array[tsamp] of var float: bat_e_stored;  %electrical energy stored in the battery (W.s)

var float: obj;
obj = C_PV * pv_max + C_W * w_max + C_EL * el_max + C_HS * hs_capa + C_BAT_energy * bat_capa + C_BAT_power * bat_pmax;

%=== CONSTRAINTS ===
constraint r[1] = R_CAPA;
%%constraint h_stored[1] = 20;
constraint h_stored[1] = h_stored[N];
constraint bat_e_stored[1] = 0;

constraint pv_max >= 0;
%%constraint pv_max <= 1e9;
constraint w_max >= 0;
%%constraint w_max <= 1e9;
constraint el_max >= 0;
%%constraint el_max <= 1e9;
constraint hs_capa >= 0;
%%constraint hs_capa <= 1e9;

constraint bat_capa >= 0;

constraint forall(  i in tint  )(  el_pin[i] = el_pin_wpv[i] + bat_pout[i] );

constraint forall(  i in tint  )(  pv_out[i] = pv_max/pv_ref_capa * pv_ref_out[i]  );
constraint forall(  i in tint  )(  w_out[i] = w_max/wind_ref_capa * wind_ref_out[i]  );

constraint forall(  i in tint  )(  pv_out[i] + w_out[i] - pc[i] - el_pin_wpv[i] - bat_pin[i] = 0  );
constraint forall(  i in tint  )(  pc[i] >= 0  );

constraint forall(  i in tint  )(  bat_pin[i] >= 0 );
constraint forall(  i in tint  )(  bat_pin[i] - bat_pmax <= 0 );

constraint forall(  i in tint  )(  bat_pout[i] >= 0 );
constraint forall(  i in tint  )(  bat_pout[i] - bat_pmax <= 0 );

constraint forall(  i in tint  )(  el_pin_wpv[i] >= 0  );
constraint forall(  i in tint  )(  el_pin_wpv[i] + bat_pout[i] - el_max <= 0  );

constraint forall(  i in tint  )(  bat_e_stored[i+1] = bat_e_stored[i] + ( bat_pin[i] * BAT_ETA_in - bat_pout[i]/BAT_ETA_out ) * DT  );
constraint forall(  i in tsamp  )(  bat_e_stored[i] >= 0 );
constraint forall(  i in tsamp  )(  bat_e_stored[i] - bat_capa <= 0 );  

constraint forall(  i in tsamp  )(  h_stored[i] >= 0  );
constraint forall(  i in tsamp  )(  h_stored[i] - hs_capa <= 0  );
constraint forall(  i in tint  )(   el_hout[i] = el_pin[i] * ETA_EL/ 142e6 );
constraint forall(  i in tint  )(   h_stored[i+1] = h_stored[i] + (el_hout[i] + r_hout[i] - L[i] )*DT  );

constraint forall(  i in tsamp  )(  r[i] >= 0  );
constraint forall(  i in tsamp  )(  r[i] <= R_CAPA  );
constraint forall(  i in tint  )(  r[i+1] = r[i] - r_hout[i]*DT  );
constraint forall(  i in tint  )(  r_hout[i]>=0  );
constraint forall(  i in tint  )(  r_hout[i]<=L[i]  );



solve minimize obj;

output  ["!"] ++
        ["CAPEX="] ++ [show(obj)] ++ [";"] ++
        ["pv_max="] ++ [show(pv_max)] ++ [";"] ++
        ["w_max="] ++ [show(w_max)] ++ [";"] ++
        ["el_max="] ++ [show(el_max)] ++ [";"] ++
        ["hs_max="] ++ [show(hs_capa)] ++ [";"]++
        ["bat_capa="] ++ [show(bat_capa)] ++ [";"]++
        ["bat_pmax="] ++ [show(bat_pmax)] ++ [";"]++
        ["pv_out="] ++ [show(pv_out)] ++ [";"]++
        ["w_out="] ++ [show(w_out)] ++ [";"]++
        ["pc="] ++ [show(pc)] ++ [";"] ++
        ["bat_pin="] ++ [show(bat_pin)] ++ [";"] ++
        ["bat_pout="] ++ [show(bat_pout)] ++ [";"] ++
        ["el_pin="] ++ [show(el_pin)] ++ [";"] ++
        ["he_out="] ++ [show(el_hout)] ++ [";"] ++
        ["hr_out="] ++ [show(r_hout)] ++ [";"] ++
        ["sh="] ++ [show(h_stored)] ++ [";"] ++
        ["r="] ++ [show(r)] ++ [";"] ++
        ["bat_e_stored="] ++ [show(bat_e_stored)] ++ [";"] ++
        ["L="] ++ [show(L)] ++ [";"] ++
        ["!"];

