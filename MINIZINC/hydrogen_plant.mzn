% Use this editor as a MiniZinc scratch book
int: N;

set of int: tint = 1..N;     %number of intervals
set of int: tsamp = 1..N+1;    %number of sample points

float: DT;      %time difference between sample points (also, interval length) (s)
float: EL_ETA;  %conversion efficiency of the electrolyser (kgH/s/kW)
float: BAT_ETA_in;   %charging efficiency of electrochemical battery
float: BAT_ETA_out;  %discharging efficiency of electrochemical battery 
float: C_PV;    %unit cost of PV plant  $/kW
float: C_WIND;     %unit cost of wind farm $/kW
float: C_EL;     %unit cost of electrolyser $/kW
float: C_HSTORAGE;    %unit cost of hydrogen storage $/(kg of H)
float: C_BAT_ENERGY;    %unit cost of battery storage ($/kWh)
float: C_BAT_POWER;    % unit cost of battery power capacpity ($/kW)
float: RES_H;       %virtual hydrogen reserve for reduced capacity factor (kg of H)
float: PV_REF;    %power capacity of the reference PV plant (kW)
float: WIND_REF;    %power capacity of the reference wind plant (kW)

array[tint] of float: LOAD; %load timeseries (kg of H per hour)
array[tint] of var float: PV_REF_POUT;    %power output from the reference PV plant (kW)
array[tint] of var float: WIND_REF_POUT;    %power output from the reference wind plant (kW)

% === VARIABLES ===
var float: pv_max;    %PV plant rated power (kW)
var float: wind_max;     %wind farm rated power (kW)
var float: el_max;     %electrolyser rated power (kW)
var float: storage_h_capa;    %capacity of hydrogen storage cavern (kg of H2)
var float: bat_e_capa;    %energy capacity of the electrochemical battery (kWh)
var float: bat_p_max;    %power capacity of the electrochemical battery (kW)

array[tint] of var float: pv_pout;    %power out of PV plant (kW)
array[tint] of var float: wind_pout;     %power out of wind farm (kW)
array[tint] of var float: curtail_p;    %curtailed power (kW)
array[tint] of var float: el_pin_pvwind;    %power from wind and pv into the electrolyser (kW)
array[tint] of var float: res_hout;   %hydrogen extracted from virtual reserve (kgH/s)
array[tint] of var float: el_hout;    %hydrogen produced in each interval (kgH/s)
array[tint] of var float: el_pin;    %power flow into the electrolyser (kW)
array[tint] of var float: bat_pin;      %power flow into the battery (kW)
array[tint] of var float: bat_pout;     %power flow out of the battery (kW)
array[tsamp] of var float: storage_h;   %stored hydrogen in storage (kg)
array[tsamp] of var float: res_h;    %reserved hydrogen for load shut down (kg)
array[tsamp] of var float: bat_e;  %electrical energy stored in the battery (kWh)

var float: capex;
capex = C_PV * pv_max + C_WIND * wind_max + C_EL * el_max + C_HSTORAGE * storage_h_capa + C_BAT_ENERGY * bat_e_capa + C_BAT_POWER * bat_p_max;

%=== CONSTRAINTS ===
constraint res_h[1] = RES_H;
constraint storage_h[1] = storage_h[N];
constraint bat_e[1] = 0;

constraint pv_max >= 0;
%%constraint pv_max <= 1e9;
constraint wind_max >= 0;
%%constraint w_max <= 1e9;
constraint el_max >= 0;
%%constraint el_max <= 1e9;
constraint storage_h_capa >= 0;
%%constraint hs_capa <= 1e9;

constraint bat_e_capa >= 0;

constraint forall(  i in tint  )(  el_pin[i] = el_pin_pvwind[i] + bat_pout[i] );

constraint forall(  i in tint  )(  pv_pout[i] = pv_max/PV_REF * PV_REF_POUT[i]  );
constraint forall(  i in tint  )(  wind_pout[i] = wind_max/WIND_REF * WIND_REF_POUT[i]  );

constraint forall(  i in tint  )(  pv_pout[i] + wind_pout[i] - curtail_p[i] - el_pin_pvwind[i] - bat_pin[i] = 0  );
constraint forall(  i in tint  )(  curtail_p[i] >= 0  );

constraint forall(  i in tint  )(  bat_pin[i] >= 0 );
constraint forall(  i in tint  )(  bat_pin[i] - bat_p_max <= 0 );

constraint forall(  i in tint  )(  bat_pout[i] >= 0 );
constraint forall(  i in tint  )(  bat_pout[i] - bat_p_max <= 0 );

constraint forall(  i in tint  )(  el_pin_pvwind[i] >= 0  );
constraint forall(  i in tint  )(  el_pin_pvwind[i] + bat_pout[i] - el_max <= 0  );

constraint forall(  i in tint  )(  bat_e[i+1] = bat_e[i] + ( bat_pin[i] * BAT_ETA_in - bat_pout[i]/BAT_ETA_out ) * DT  );
constraint forall(  i in tsamp  )(  bat_e[i] >= 0 );
constraint forall(  i in tsamp  )(  bat_e[i] - bat_e_capa <= 0 );  

constraint forall(  i in tsamp  )(  storage_h[i] >= 0  );
constraint forall(  i in tsamp  )(  storage_h[i] - storage_h_capa <= 0  );
constraint forall(  i in tint  )(   el_hout[i] = el_pin[i]/3600* EL_ETA/ 39.4 );  %% high calorific value of H2 = 39.4 kWh/kg
constraint forall(  i in tint  )(   storage_h[i+1] = storage_h[i] + (el_hout[i] + res_hout[i] - LOAD[i] )*DT*3600  );

constraint forall(  i in tsamp  )(  res_h[i] >= 0  );
constraint forall(  i in tsamp  )(  res_h[i] <= RES_H  );
constraint forall(  i in tint  )(  res_h[i+1] = res_h[i] - res_hout[i]*DT*3600  );
constraint forall(  i in tint  )(  res_hout[i]>=0  );
constraint forall(  i in tint  )(  res_hout[i]<=LOAD[i]  );



solve minimize capex;

output  ["!"] ++
        ["CAPEX="] ++ [show(capex)] ++ [";"] ++
        ["pv_max="] ++ [show(pv_max)] ++ [";"] ++
        ["wind_max="] ++ [show(wind_max)] ++ [";"] ++
        ["el_max="] ++ [show(el_max)] ++ [";"] ++
        ["storage_h_max="] ++ [show(storage_h_capa)] ++ [";"]++
        ["bat_e_capa="] ++ [show(bat_e_capa)] ++ [";"]++
        ["bat_p_max="] ++ [show(bat_p_max)] ++ [";"]++
        ["pv_pout="] ++ [show(pv_pout)] ++ [";"]++
        ["wind_pout="] ++ [show(wind_pout)] ++ [";"]++
        ["curtail_p="] ++ [show(curtail_p)] ++ [";"] ++
        ["bat_pin="] ++ [show(bat_pin)] ++ [";"] ++
        ["bat_pout="] ++ [show(bat_pout)] ++ [";"] ++
        ["el_pin="] ++ [show(el_pin)] ++ [";"] ++
        ["el_hout="] ++ [show(el_hout)] ++ [";"] ++
        ["res_hout="] ++ [show(res_hout)] ++ [";"] ++
        ["storage_h="] ++ [show(storage_h)] ++ [";"] ++
        ["reserve="] ++ [show(res_h)] ++ [";"] ++
        ["bat_e="] ++ [show(bat_e)] ++ [";"] ++
        ["LOAD="] ++ [show(LOAD)] ++ [";"] ++
        ["!"];

