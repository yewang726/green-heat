model PVWindEES
  import SI = Modelica.SIunits;
  
  parameter SI.Power P_load = 500e6 "system thermal load"; 
  
  parameter Real RM=2 "Renewable multiple";
  parameter Real F_pv=0.6 "Fraction of PV"; 
  parameter SI.Power P_pv_des = P_load*RM*F_pv "Capacity of the PV system";
  parameter SI.Power P_wind_des = P_load*RM*(1-F_pv) "Capacity of the Wind system";
  parameter SI.Power P_pv_ref = 1e6 "Capacity of the referenced PV system from the SAM model";
  parameter SI.Power P_wind_ref = 320e6 "Capacity of the referenced Wind system from the SAM model";
    
  parameter Real t_storage(unit = "h")  = 8 "Hours of storage";
  parameter SI.Power P_ST_max = 650e6 "The maximal charging power of the electric storage";  
  parameter SI.Energy E_ST_max = P_heater*3600*t_storage " The maximal capacity of the electric storage";  
  parameter SI.Efficiency eff_ST_roundtrip = 0.82 "Round trip efficiency of the electric storage";       
  parameter SI.Efficiency eff_ST_in = sqrt(eff_ST_roundtrip) "Charging efficiency";  
  parameter SI.Efficiency eff_ST_out = sqrt(eff_ST_roundtrip) "Discharging efficiency";  
  
  parameter SI.Power P_heater = P_load/eff_heater "The maximal charging power of the battery"; 
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
  SI.Power P_ele "Electricity power goes to the heater";  
  SI.Power P_direct "Electricity directly from pv or wind";      
  SI.Power P_curt "Curtailment";   
  SI.Power P_ST_in "Charging power";      
  SI.Power P_ST_out "Discharging power";
  SI.Energy E_ST_stored "Stored energy";  
  SI.Energy E_heat "Annual heat production";      
  Real SOC(start=0.5) "State of charge"; 
  Real CF "Capacity factor";    

equation
  P_pv_out=P_pv_des/P_pv_ref*PV_out_ref.y[1]*1000;
  PV_out_ref.u=time;  
  
  P_wind_out=P_wind_des/P_wind_ref*Wind_out_ref.y[1]*1000;
  Wind_out_ref.u=time;  
  
  pv_wind_out=P_pv_out+P_wind_out;

  P_heat=P_ele*eff_heater;
  P_ele=P_direct+P_ST_out;
  P_curt=pv_wind_out - P_direct - P_ST_in;  
    
  if pv_wind_out>P_heater then
      P_direct=P_heater;
      P_ST_out=0;     
      if SOC<0.99 then P_ST_in = min(pv_wind_out - P_heater, P_ST_max);
      else P_ST_in = 0;
      end if;
  else 
      P_direct=pv_wind_out;
      P_ST_in=0;
      if SOC>0.15 then P_ST_out= max(P_heater - pv_wind_out, 0);
      else P_ST_out =0;        
      end if;
 end if;
            
  SOC=E_ST_stored/E_ST_max;
  der(E_ST_stored)=P_ST_in*eff_ST_in-P_ST_out/eff_ST_out;
  der(E_heat)= P_heat;
  CF=E_heat/(P_load*365*24*3600);

end PVWindEES;
