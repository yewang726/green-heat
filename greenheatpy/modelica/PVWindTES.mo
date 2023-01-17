model PVWindTES
  import SI = Modelica.SIunits;
  
  parameter SI.Power P_load = 500e6 "system thermal load"; 
  
  parameter Real RM=2 "Renewable multiple";
  parameter Real F_pv=0.5 "Fraction of PV"; 
  parameter SI.Power P_pv_des = P_load*RM*F_pv "Capacity of the PV system";
  parameter SI.Power P_wind_des = P_load*RM*(1-F_pv) "Capacity of the Wind system";
  parameter SI.Power P_pv_ref = 1e6 "Capacity of the referenced PV system from the SAM model";
  parameter SI.Power P_wind_ref = 320e6 "Capacity of the referenced Wind system from the SAM model";
    
  parameter Real t_storage(unit = "h")  = 8 "Hours of storage";
  //parameter SI.Power P_ST_max = 650e6 "The maximal charging power of the electric storage";  
  parameter SI.Energy E_ST_max = P_load*3600*t_storage " The maximal capacity of the electric storage";  
  parameter SI.Efficiency eff_ST_roundtrip = 0.99"Round trip efficiency of the electric storage";       
  parameter SI.Efficiency eff_ST_in = sqrt(eff_ST_roundtrip) "Charging efficiency";  
  parameter SI.Efficiency eff_ST_out = sqrt(eff_ST_roundtrip) "Discharging efficiency";  
  
  parameter SI.Power P_heater_max = 1000e6 "The maximal charging power of the battery"; 
  parameter SI.Efficiency eff_heater = 0.99 "Efficiency of the heater";  
  
  parameter String table_file_pv=Modelica.Utilities.Files.loadResource("/media/yewang/Data/Work/Research/Topics/yewang/HILTCRC/repo/data/weather/motab/PV_out_ref_Newman.motab");
  parameter String table_file_wind=Modelica.Utilities.Files.loadResource("/media/yewang/Data/Work/Research/Topics/yewang/HILTCRC/repo/data/weather/motab/Wind_out_ref_Newman.motab");  
  
  Modelica.Blocks.Tables.CombiTable1Ds PV_out_ref (
      tableOnFile=true, 
      tableName="PV_out_ref", 
      smoothness=Modelica.Blocks.Types.Smoothness.LinearSegments,
      columns=2:2, 
      fileName=table_file_pv);
      
  Modelica.Blocks.Tables.CombiTable1Ds Wind_out_ref (
      tableOnFile=true, 
      tableName="Wind_out_ref", 
      smoothness=Modelica.Blocks.Types.Smoothness.LinearSegments,
      columns=2:2, 
      fileName=table_file_wind);      
      
      
  SI.Power P_pv_out "output power from pv";
  SI.Power P_wind_out "output power from wind";
  SI.Power pv_wind_out "output power from both pv and wind";
  
  SI.Power P_heat "Heat goes to the load";  
  SI.Power P_heater_in "Electricity power goes to the heater"; 
  SI.Power P_heater_out "Thermal power goes out from the heater";   
  SI.Power P_direct "Heat directly from heater to the load";      
  SI.Power P_curt1 "Curtailment due to the inputs exceed heater maximumal power"; 
  SI.Power P_curt2 "Curtailment due to storage is full";      
  SI.Power P_ST_in "Charging power";      
  SI.Power P_ST_out "Discharging power";
  SI.Energy E_ST_stored "Stored energy";  
  SI.Energy E_heat "Annual heat production";      
  Real SOC(start=0) "State of charge"; 
  Real CF "Capacity factor";    

equation
  P_pv_out=P_pv_des/P_pv_ref*PV_out_ref.y[1]*1000;
  PV_out_ref.u=time;  
  
  P_wind_out=P_wind_des/P_wind_ref*Wind_out_ref.y[1]*1000;
  Wind_out_ref.u=time;  
  
  pv_wind_out=P_pv_out+P_wind_out;

  P_heat= P_ST_out + P_direct;
  P_heater_out=P_heater_in *eff_heater;  
  P_curt1=max(pv_wind_out - P_heater_max, 0);
  pv_wind_out = P_curt1+P_curt2+P_heater_in;
 
  if P_heater_out>P_load then
      P_direct=P_load;
      P_ST_out=0;     
      if SOC<0.99 then 
          P_ST_in = P_heater_out - P_load;
          P_curt2=0;
      else 
          P_ST_in = 0;
          P_curt2=P_heater_out - P_load;
      end if;
  else 
      P_direct=P_heater_out;
      P_ST_in=0;
      P_curt2=0;
      if SOC>0.01 then 
          P_ST_out= max(P_load - P_heater_out, 0);
      else 
          P_ST_out =0;        
      end if;
 end if;
             
  SOC=E_ST_stored/E_ST_max;
  der(E_ST_stored)=P_ST_in*eff_ST_in-P_ST_out/eff_ST_out;
  der(E_heat)= P_heat;
  CF=E_heat/(P_load*365*24*3600);

end PVWindTES;
