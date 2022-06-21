% Use this editor as a MiniZinc scratch book
int: N;

set of int: tint = 1..N;     %number of intervals
set of int: tsamp = 1..N+1;    %number of sample points

float: DT;      % time difference between sample points (also, interval length) (s)
float: RM;      % renewable multiple
float: pv_ref_capa;    % power capacity of the reference PV plant (W)
float: C_PV;    % unit cost of PV plant  $/W
float: wind_ref_capa;    % power capacity of the reference wind plant (W)
float: C_Wind;     % unit cost of wind farm $/W
float: t_storage;   % storage hour (h)
float: BAT_ETA_in;   % charging efficiency of electrochemical battery
float: BAT_ETA_out;  % discharging efficiency of electrochemical battery 
float: C_BAT_energy;    % unit cost of battery storage ($/W.s)
float: C_BAT_power;    % unit cost of battery power capacpity ($/W)
float: P_heater; % design power of the heater (W), equal to the load
float: ETA_heater; % efficiency of the heater, that converts electricity to heat
float: C_heater; % unit cost of heater ($/W)
array[tint] of float: L; %load timeseries (W)
array[tint] of var float: pv_ref_out;    %power output from the reference PV plant (W)
array[tint] of var float: wind_ref_out;    %power output from the reference wind plant (W)


% === VARIABLES ===
var float: CAPEX; % total capital cost
var float: r_pv; % ratio of PV, r_pv=pv_max/(pv_max+wind_max) 
var float: pv_max;    % PV plant rated power
var float: wind_max;     % wind farm rated power
array[tint] of var float: pv_out;    % power out of PV plant (W)
array[tint] of var float: wind_out;     % power out of wind farm (W)
array[tint] of var float: P_curt;    % curtailed power (W)
array[tint] of var float: pv_wind_direct;    % power out from pv and wind that goes to heater directly
array[tint] of var float: P_ele;    % power into the heater (W)
array[tint] of var float: P_heat;    % heat into the load (W)
var float: bat_capa;    % energy capacity of the electrochemical battery (J)
var float: bat_pmax;    % power capacity of the electrochemical battery (W)
array[tint] of var float: P_st_in;      % power flow into the battery (W)
array[tint] of var float: P_st_out;     % power flow out of the battery (W)
array[tsamp] of var float: bat_e_stored;  % electrical energy stored in the battery (W.s)

var float: obj; % objective is the capacity factor
%obj = sum(P_heat);
obj=sum(i in tint)(P_heat[i]);

%=== CONSTRAINTS ===
constraint bat_e_stored[1] = 0;
constraint r_pv <= 1;
constraint r_pv >= 0;
constraint pv_max=r_pv*RM*L[1];
constraint wind_max=(1-r_pv)*RM*L[1];
constraint bat_capa=bat_pmax*t_storage*3600;
constraint CAPEX=C_PV * pv_max + C_Wind * wind_max + C_BAT_energy * bat_capa + C_BAT_power * bat_pmax + C_heater*P_heater;

constraint forall(  i in tint  )(  pv_out[i] = pv_max/pv_ref_capa * pv_ref_out[i]  );
constraint forall(  i in tint  )(  wind_out[i] = wind_max/wind_ref_capa * wind_ref_out[i]  );
constraint forall(  i in tint  )(  pv_out[i] + wind_out[i] - P_curt[i] - pv_wind_direct[i] - P_st_in[i] = 0  );
constraint forall(  i in tint  )(  P_ele[i] = pv_wind_direct[i] + P_st_out[i] );
constraint forall(  i in tint  )(  P_heat[i]=P_ele[i]*ETA_heater  );

constraint forall(  i in tint  )(  P_curt[i] >= 0  );
constraint forall(  i in tint  )(  P_st_in[i] >= 0 );
constraint forall(  i in tint  )(  P_st_in[i] - bat_pmax <= 0 );

constraint forall(  i in tint  )(  P_st_out[i] >= 0 );
constraint forall(  i in tint  )(  P_st_out[i] - bat_pmax <= 0 );

constraint forall(  i in tint  )(  pv_wind_direct[i] >= 0  );
constraint forall(  i in tint  )(  pv_wind_direct[i] + P_st_out[i] - P_heater <= 0  );

constraint forall(  i in tint  )(  bat_e_stored[i+1] = bat_e_stored[i] + ( P_st_in[i] * BAT_ETA_in - P_st_out[i]/BAT_ETA_out ) * DT  );
constraint forall(  i in tsamp  )(  bat_e_stored[i] >= 0 );
constraint forall(  i in tsamp  )(  bat_e_stored[i] - bat_capa <= 0 );  


solve maximize obj;

output  ["!"] ++
        ["CAPEX="] ++ [show(CAPEX)] ++ [";"] ++
        ["CF="] ++ [show(obj/sum(L))] ++ [";"] ++
        ["RM="] ++ [show(RM)] ++ [";"] ++
        ["t_storage="] ++ [show(t_storage)] ++ [";"] ++
        ["r_pv="] ++ [show(r_pv)] ++ [";"] ++
        ["pv_max="] ++ [show(pv_max)] ++ [";"] ++
        ["wind_max="] ++ [show(wind_max)] ++ [";"] ++
        ["bat_capa="] ++ [show(bat_capa)] ++ [";"]++
        ["bat_pmax="] ++ [show(bat_pmax)] ++ [";"]++
        ["pv_out="] ++ [show(pv_out)] ++ [";"]++
        ["wind_out="] ++ [show(wind_out)] ++ [";"]++
        ["P_curt="] ++ [show(P_curt)] ++ [";"] ++
        ["P_st_in="] ++ [show(P_st_in)] ++ [";"] ++
        ["P_st_out="] ++ [show(P_st_out)] ++ [";"] ++
        ["P_ele="] ++ [show(P_ele)] ++ [";"] ++
        ["P_heat="] ++ [show(P_heat)] ++ [";"] ++
        ["bat_e_stored="] ++ [show(bat_e_stored)] ++ [";"] ++
        ["L="] ++ [show(L)] ++ [";"] ++
        ["!"];

