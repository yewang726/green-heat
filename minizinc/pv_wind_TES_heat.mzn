% Use this editor as a MiniZinc scratch book
int: N;

set of int: tint = 1..N;     %number of intervals
set of int: tsamp = 1..N+1;    %number of sample points

float: DT;      % time difference between sample points (also, interval length) (s)
float: RM;      % renewable multiple
float: t_storage;   % storage hour (h)

float: eta_TES_in;   % charging efficiency of electrochemical battery
float: eta_TES_out;  % discharging efficiency of electrochemical battery 

float: P_heater; % design power of the heater (kW)
float: eta_heater; % efficiency of the heater, that converts electricity to heat

float: c_PV;    % unit cost of PV plant  USD/kW
float: c_Wind;     % unit cost of wind farm USD/kW
float: c_TES;    % unit cost of TES storage (USD/kWh_th)
float: c_heater; % unit cost of heater (USD/kW)

float: pv_ref_capa;    % power capacity of the reference PV plant (kW)
float: wind_ref_capa;    % power capacity of the reference wind plant (KW)

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
array[tint] of var float: P_heater_in;    % power input to the heater
array[tint] of var float: P_heater_out;    % thermal output from the heater
array[tint] of var float: P_heat_direct;    % heat from heater directly to the load
array[tint] of var float: P_heat;    % total heat into the load (kW)
var float: TES_capa;    % energy capacity of the TES (kWh)
array[tint] of var float: P_TES_in;      % power flow into the TES (kW)
array[tint] of var float: P_TES_out;     % power flow out of the TES (kW)
array[tsamp] of var float: TES_e_stored;  % thermal energy stored in the TES (kWh)

var float: obj; % objective is the capacity factor
%obj = sum(P_heat);
obj=sum(i in tint)(P_heat[i]);

%=== CONSTRAINTS ===
constraint TES_e_stored[1] = 0.2*TES_capa;
constraint r_pv <= 1;
constraint r_pv >= 0;
constraint pv_max=r_pv*RM*L[1];
constraint wind_max=(1-r_pv)*RM*L[1];
constraint TES_capa=L[1]*t_storage;
constraint CAPEX=c_PV * pv_max + c_Wind * wind_max + c_TES * TES_capa + c_heater*P_heater;

constraint forall(  i in tint  )(  pv_out[i] = pv_max/pv_ref_capa * pv_ref_out[i]  );
constraint forall(  i in tint  )(  wind_out[i] = wind_max/wind_ref_capa * wind_ref_out[i]  );
constraint forall(  i in tint  )(  pv_out[i] + wind_out[i] - P_curt[i] - P_heater_in[i] = 0  );
constraint forall(  i in tint  )(  P_heater_out[i] = P_heater_in[i] * eta_heater  );
constraint forall(  i in tint  )(  P_heater_out[i] = P_heat_direct[i] + P_TES_in[i] );
constraint forall(  i in tint  )(  P_heat[i] = P_heat_direct[i] + P_TES_out[i]  );

constraint forall(  i in tint  )(  P_curt[i] >= 0  );
constraint forall(  i in tint  )(  P_TES_in[i] >= 0 );
%constraint forall(  i in tint  )(  P_TES_in[i] - TES_pmax <= 0 );

constraint forall(  i in tint  )(  P_TES_out[i] >= 0 );
%constraint forall(  i in tint  )(  P_TES_out[i] - TES_pmax <= 0 );


constraint forall(  i in tint  )(  P_heater_in[i] >= 0  );
constraint forall(  i in tint  )(  P_heater_out[i] <= P_heater  );
constraint forall(  i in tint  )(  P_heat_direct[i] + P_TES_out[i] - L[i] <= 0  );

constraint forall(  i in tint  )(  TES_e_stored[i+1] = TES_e_stored[i] + ( P_TES_in[i] * eta_TES_in - P_TES_out[i]/eta_TES_out ) * DT  );
constraint forall(  i in tsamp  )(  TES_e_stored[i] >=  0.15*TES_capa  );
constraint forall(  i in tsamp  )(  TES_e_stored[i] <=  0.99*TES_capa  );  


solve maximize obj;

output  ["!"] ++
        ["CAPEX="] ++ [show(CAPEX)] ++ [";"] ++
        ["CF="] ++ [show(obj/sum(L))] ++ [";"] ++
        ["RM="] ++ [show(RM)] ++ [";"] ++
        ["t_storage="] ++ [show(t_storage)] ++ [";"] ++
        ["r_pv="] ++ [show(r_pv)] ++ [";"] ++
        ["pv_max="] ++ [show(pv_max)] ++ [";"] ++
        ["wind_max="] ++ [show(wind_max)] ++ [";"] ++
        ["TES_capa="] ++ [show(TES_capa)] ++ [";"]++
        ["P_heater="] ++ [show(P_heater)] ++ [";"] ++
        ["pv_out="] ++ [show(pv_out)] ++ [";"]++
        ["wind_out="] ++ [show(wind_out)] ++ [";"]++
        ["P_curt="] ++ [show(P_curt)] ++ [";"] ++
        ["P_heater_in="] ++ [show(P_heater_in)] ++ [";"] ++
        ["P_heater_out="] ++ [show(P_heater_out)] ++ [";"] ++
        ["P_heat_direct="] ++ [show(P_heat_direct)] ++ [";"] ++
        ["P_TES_in="] ++ [show(P_TES_in)] ++ [";"] ++
        ["P_TES_out="] ++ [show(P_TES_out)] ++ [";"] ++
        ["P_heat="] ++ [show(P_heat)] ++ [";"] ++
        ["TES_e_stored="] ++ [show(TES_e_stored)] ++ [";"] ++
        ["L="] ++ [show(L)] ++ [";"] ++
        ["!"];

