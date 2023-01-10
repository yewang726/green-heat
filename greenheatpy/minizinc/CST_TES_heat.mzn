% Use this editor as a MiniZinc scratch book
int: N;

set of int: tint = 1..N;     %number of intervals
set of int: tsamp = 1..N+1;    %number of sample points

float: DT;      % time difference between sample points (also, interval length) (s)

float: t_storage;   % storage hour (h)

float: eta_TES_in;   % charging efficiency of electrochemical battery
float: eta_TES_out;  % discharging efficiency of electrochemical battery 


array[tint] of float: L; %load timeseries (kW)
array[tint] of var float: P_recv_out;    % thermal power output from the receiver (kW)


% === VARIABLES ===
var float: TES_capa;    % energy capacity of the TES (kWh)
var float: TES_pmax;    % power capacity of the TES (kW)
array[tint] of var float: P_curt;    % curtailed power (kW)
array[tint] of var float: P_direct;    % power from receiver directly goes to the load (kW)
array[tint] of var float: P_TES_in;      % power flow into the TES (kW)
array[tint] of var float: P_TES_out;     % power flow out of the TES (kW)
array[tint] of var float: P_heat;    % total heat into the load (kW)
array[tsamp] of var float: TES_e_stored;  % thermal energy stored in the TES (kWh)

var float: obj; % objective is the capacity factor
%obj = sum(P_heat);
obj=sum(i in tint)(P_heat[i]);

%=== CONSTRAINTS ===
constraint TES_e_stored[1] = 0;
constraint TES_capa=TES_pmax*t_storage;
constraint TES_pmax=L[1];

constraint forall(  i in tint  )(  P_recv_out[i] - P_curt[i] - P_TES_in[i] - P_direct[i] = 0  );
constraint forall(  i in tint  )(  P_heat[i] = P_direct[i] + P_TES_out[i] );

constraint forall(  i in tint  )(  P_TES_in[i] >= 0 );
%constraint forall(  i in tint  )(  P_TES_in[i] - TES_pmax <= 0 );

constraint forall(  i in tint  )(  P_TES_out[i] >= 0 );
constraint forall(  i in tint  )(  P_TES_out[i] - TES_pmax <= 0 );

constraint forall(  i in tint  )(  P_curt[i] >= 0  );
constraint forall(  i in tint  )(  P_direct[i] + P_TES_out[i] - L[i] <= 0  );

constraint forall(  i in tint  )(  TES_e_stored[i+1] = TES_e_stored[i] + ( P_TES_in[i] * eta_TES_in - P_TES_out[i]/eta_TES_out ) * DT  );
constraint forall(  i in tsamp  )(  TES_e_stored[i] >= 0 );
constraint forall(  i in tsamp  )(  TES_e_stored[i] - TES_capa <= 0 );  


solve maximize obj;

output  ["!"] ++
        ["CF="] ++ [show(obj/sum(L))] ++ [";"] ++
        ["t_storage="] ++ [show(t_storage)] ++ [";"] ++
        ["TES_capa="] ++ [show(TES_capa)] ++ [";"]++
        ["TES_pmax="] ++ [show(TES_pmax)] ++ [";"]++
        ["P_curt="] ++ [show(P_curt)] ++ [";"] ++
        ["P_recv_out="] ++ [show(P_recv_out)] ++ [";"] ++
        ["P_direct="] ++ [show(P_direct)] ++ [";"] ++
        ["P_TES_in="] ++ [show(P_TES_in)] ++ [";"] ++
        ["P_TES_out="] ++ [show(P_TES_out)] ++ [";"] ++
        ["P_heat="] ++ [show(P_heat)] ++ [";"] ++
        ["TES_e_stored="] ++ [show(TES_e_stored)] ++ [";"] ++
        ["L="] ++ [show(L)] ++ [";"] ++
        ["!"];

