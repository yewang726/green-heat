% Use this editor as a MiniZinc scratch book
int: N;

set of int: tint = 1..N;     %number of intervals
set of int: tsamp = 1..N+1;    %number of sample points

float: DT;      % time difference between sample points (also, interval length) (s)
float: RM;      % renewable multiple
float: pv_ref_capa;    % power capacity of the reference PV plant (kW)
float: C_PV;    % unit cost of PV plant  USD/kW
float: wind_ref_capa;    % power capacity of the reference wind plant (KW)
float: C_Wind;     % unit cost of wind farm USD/kW
float: t_storage;   % storage hour (h)
float: bat_pmax;    % power of the battery (kW)
float: BAT_ETA_in;   % charging efficiency of electrochemical battery
float: BAT_ETA_out;  % discharging efficiency of electrochemical battery 
float: C_BAT_energy;    % unit cost of battery storage (USD/kWh)
float: C_BAT_power;    % unit cost of battery power capacpity (USD/kW)
float: P_heater; % design power of the heater (kW)
float: ETA_heater; % efficiency of the heater, that converts electricity to heat
float: C_heater; % unit cost of heater (USD/kW)
array[tint] of float: L; %load timeseries (kW)
array[tint] of var float: pv_ref_out;    % power output from the reference PV plant (kW)
array[tint] of var float: wind_ref_out;    % power output from the reference wind plant (kW)


% === VARIABLES ===
var float: CAPEX; % total capital cost (USD)
var float: r_pv; % ratio of PV, r_pv=pv_max/(pv_max+wind_max) 
var float: pv_max;    % PV plant rated power (kW)
var float: wind_max;     % wind farm rated power (kW)
array[tint] of var float: pv_out;    % power out of PV plant (kW)
array[tint] of var float: wind_out;     % power out of wind farm (kW)
array[tint] of var float: P_curt;    % curtailed power (kW)
array[tint] of var float: pv_wind_direct;    % power out from pv and wind that goes to heater directly
array[tint] of var float: P_ele;    % power into the heater (kW)
array[tint] of var float: P_heat;    % heat into the load (kW)
var float: bat_capa;    % energy capacity of the electrochemical battery (kWh)
array[tint] of var float: P_bat_in;      % power flow into the battery (kW)
array[tint] of var float: P_bat_out;     % power flow out of the battery (kW)
array[tsamp] of var float: bat_e_stored;  % electrical energy stored in the battery (kWh)

var float: obj; % objective is the capacity factor
%obj = sum(P_heat);
obj=sum(i in tint)(P_heat[i]);

%=== CONSTRAINTS ===
constraint bat_e_stored[1] = 0;
constraint r_pv <= 1;
constraint r_pv >= 0;
constraint pv_max=r_pv*RM*L[1];
constraint wind_max=(1-r_pv)*RM*L[1];
constraint bat_capa=P_heater*t_storage;
constraint CAPEX=C_PV * pv_max + C_Wind * wind_max + C_BAT_energy * bat_capa + C_BAT_power * bat_pmax + C_heater*P_heater;

constraint forall(  i in tint  )(  pv_out[i] = pv_max/pv_ref_capa * pv_ref_out[i]  );
constraint forall(  i in tint  )(  wind_out[i] = wind_max/wind_ref_capa * wind_ref_out[i]  );
constraint forall(  i in tint  )(  pv_out[i] + wind_out[i] - P_curt[i] - pv_wind_direct[i] - P_bat_in[i] = 0  );
constraint forall(  i in tint  )(  P_ele[i] = pv_wind_direct[i] + P_bat_out[i] );
constraint forall(  i in tint  )(  P_heat[i]=P_ele[i]*ETA_heater  );

constraint forall(  i in tint  )(  P_curt[i] >= 0  );
constraint forall(  i in tint  )(  P_bat_in[i] >= 0 );
constraint forall(  i in tint  )(  P_bat_in[i] - bat_pmax <= 0 );

constraint forall(  i in tint  )(  P_bat_out[i] >= 0 );
constraint forall(  i in tint  )(  P_bat_out[i] - bat_pmax <= 0 );

constraint forall(  i in tint  )(  pv_wind_direct[i] >= 0  );
constraint forall(  i in tint  )(  pv_wind_direct[i] + P_bat_out[i] - P_heater <= 0  );

constraint forall(  i in tint  )(  bat_e_stored[i+1] = bat_e_stored[i] + ( P_bat_in[i] * BAT_ETA_in - P_bat_out[i]/BAT_ETA_out ) * DT  );
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
        ["P_bat_in="] ++ [show(P_bat_in)] ++ [";"] ++
        ["P_bat_out="] ++ [show(P_bat_out)] ++ [";"] ++
        ["P_ele="] ++ [show(P_ele)] ++ [";"] ++
        ["P_heat="] ++ [show(P_heat)] ++ [";"] ++
        ["bat_e_stored="] ++ [show(bat_e_stored)] ++ [";"] ++
        ["L="] ++ [show(L)] ++ [";"] ++
        ["!"];

