/* Main Simulation File */

#if defined(__cplusplus)
extern "C" {
#endif

#include "PVWindEES_model.h"
#include "simulation/solver/events.h"

#define prefixedName_performSimulation PVWindEES_performSimulation
#define prefixedName_updateContinuousSystem PVWindEES_updateContinuousSystem
#include <simulation/solver/perform_simulation.c.inc>

#define prefixedName_performQSSSimulation PVWindEES_performQSSSimulation
#include <simulation/solver/perform_qss_simulation.c.inc>


/* dummy VARINFO and FILEINFO */
const FILE_INFO dummyFILE_INFO = omc_dummyFileInfo;
const VAR_INFO dummyVAR_INFO = omc_dummyVarInfo;

int PVWindEES_input_function(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH

  
  TRACE_POP
  return 0;
}

int PVWindEES_input_function_init(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH

  
  TRACE_POP
  return 0;
}

int PVWindEES_input_function_updateStartValues(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH

  
  TRACE_POP
  return 0;
}

int PVWindEES_inputNames(DATA *data, char ** names){
  TRACE_PUSH

  
  TRACE_POP
  return 0;
}

int PVWindEES_data_function(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH

  TRACE_POP
  return 0;
}

int PVWindEES_dataReconciliationInputNames(DATA *data, char ** names){
  TRACE_PUSH

  
  TRACE_POP
  return 0;
}

int PVWindEES_output_function(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH

  
  TRACE_POP
  return 0;
}

int PVWindEES_setc_function(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH

  
  TRACE_POP
  return 0;
}


/*
equation index: 22
type: SIMPLE_ASSIGN
CF = 3.170979198376459e-08 * E_heat / P_load
*/
void PVWindEES_eqFunction_22(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,22};
  data->localData[0]->realVars[4] /* CF variable */ = (3.170979198376459e-08) * (DIVISION_SIM(data->localData[0]->realVars[1] /* E_heat STATE(1,P_heat) */,data->simulationInfo->realParameter[6] /* P_load PARAM */,"P_load",equationIndexes));
  TRACE_POP
}
/*
equation index: 23
type: SIMPLE_ASSIGN
SOC = E_ST_stored / E_ST_max
*/
void PVWindEES_eqFunction_23(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,23};
  data->localData[0]->realVars[15] /* SOC variable */ = DIVISION_SIM(data->localData[0]->realVars[0] /* E_ST_stored STATE(1) */,data->simulationInfo->realParameter[0] /* E_ST_max PARAM */,"E_ST_max",equationIndexes);
  TRACE_POP
}
/*
equation index: 24
type: SIMPLE_ASSIGN
Wind_out_ref.u = time
*/
void PVWindEES_eqFunction_24(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,24};
  data->localData[0]->realVars[16] /* Wind_out_ref.u variable */ = data->localData[0]->timeValue;
  TRACE_POP
}
/*
equation index: 25
type: SIMPLE_ASSIGN
Wind_out_ref.y[1] = Modelica.Blocks.Tables.Internal.getTable1DValue(Wind_out_ref.tableID, 1, Wind_out_ref.u)
*/
void PVWindEES_eqFunction_25(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,25};
  data->localData[0]->realVars[17] /* Wind_out_ref.y[1] variable */ = omc_Modelica_Blocks_Tables_Internal_getTable1DValue(threadData, data->simulationInfo->extObjs[1], ((modelica_integer) 1), data->localData[0]->realVars[16] /* Wind_out_ref.u variable */);
  TRACE_POP
}
/*
equation index: 26
type: SIMPLE_ASSIGN
P_wind_out = 1000.0 * P_wind_des * Wind_out_ref.y[1] / P_wind_ref
*/
void PVWindEES_eqFunction_26(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,26};
  data->localData[0]->realVars[14] /* P_wind_out variable */ = (1000.0) * ((data->simulationInfo->realParameter[9] /* P_wind_des PARAM */) * (DIVISION_SIM(data->localData[0]->realVars[17] /* Wind_out_ref.y[1] variable */,data->simulationInfo->realParameter[10] /* P_wind_ref PARAM */,"P_wind_ref",equationIndexes)));
  TRACE_POP
}
/*
equation index: 27
type: SIMPLE_ASSIGN
PV_out_ref.u = time
*/
void PVWindEES_eqFunction_27(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,27};
  data->localData[0]->realVars[5] /* PV_out_ref.u variable */ = data->localData[0]->timeValue;
  TRACE_POP
}
/*
equation index: 28
type: SIMPLE_ASSIGN
PV_out_ref.y[1] = Modelica.Blocks.Tables.Internal.getTable1DValue(PV_out_ref.tableID, 1, PV_out_ref.u)
*/
void PVWindEES_eqFunction_28(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,28};
  data->localData[0]->realVars[6] /* PV_out_ref.y[1] variable */ = omc_Modelica_Blocks_Tables_Internal_getTable1DValue(threadData, data->simulationInfo->extObjs[0], ((modelica_integer) 1), data->localData[0]->realVars[5] /* PV_out_ref.u variable */);
  TRACE_POP
}
/*
equation index: 29
type: SIMPLE_ASSIGN
P_pv_out = 1000.0 * P_pv_des * PV_out_ref.y[1] / P_pv_ref
*/
void PVWindEES_eqFunction_29(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,29};
  data->localData[0]->realVars[13] /* P_pv_out variable */ = (1000.0) * ((data->simulationInfo->realParameter[7] /* P_pv_des PARAM */) * (DIVISION_SIM(data->localData[0]->realVars[6] /* PV_out_ref.y[1] variable */,data->simulationInfo->realParameter[8] /* P_pv_ref PARAM */,"P_pv_ref",equationIndexes)));
  TRACE_POP
}
/*
equation index: 30
type: SIMPLE_ASSIGN
pv_wind_out = P_pv_out + P_wind_out
*/
void PVWindEES_eqFunction_30(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,30};
  data->localData[0]->realVars[18] /* pv_wind_out variable */ = data->localData[0]->realVars[13] /* P_pv_out variable */ + data->localData[0]->realVars[14] /* P_wind_out variable */;
  TRACE_POP
}
/*
equation index: 31
type: SIMPLE_ASSIGN
P_direct = if pv_wind_out > P_heater then P_heater else pv_wind_out
*/
void PVWindEES_eqFunction_31(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,31};
  modelica_boolean tmp0;
  RELATIONHYSTERESIS(tmp0, data->localData[0]->realVars[18] /* pv_wind_out variable */, data->simulationInfo->realParameter[5] /* P_heater PARAM */, 0, Greater);
  data->localData[0]->realVars[10] /* P_direct variable */ = (tmp0?data->simulationInfo->realParameter[5] /* P_heater PARAM */:data->localData[0]->realVars[18] /* pv_wind_out variable */);
  TRACE_POP
}
/*
equation index: 32
type: SIMPLE_ASSIGN
P_ST_in = if pv_wind_out > P_heater then if SOC < 0.99 then min(pv_wind_out - P_heater, P_ST_max) else 0.0 else 0.0
*/
void PVWindEES_eqFunction_32(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,32};
  modelica_boolean tmp1;
  modelica_boolean tmp2;
  modelica_boolean tmp3;
  modelica_real tmp4;
  RELATIONHYSTERESIS(tmp1, data->localData[0]->realVars[18] /* pv_wind_out variable */, data->simulationInfo->realParameter[5] /* P_heater PARAM */, 0, Greater);
  tmp3 = (modelica_boolean)tmp1;
  if(tmp3)
  {
    RELATIONHYSTERESIS(tmp2, data->localData[0]->realVars[15] /* SOC variable */, 0.99, 1, Less);
    tmp4 = (tmp2?fmin(data->localData[0]->realVars[18] /* pv_wind_out variable */ - data->simulationInfo->realParameter[5] /* P_heater PARAM */,data->simulationInfo->realParameter[4] /* P_ST_max PARAM */):0.0);
  }
  else
  {
    tmp4 = 0.0;
  }
  data->localData[0]->realVars[7] /* P_ST_in variable */ = tmp4;
  TRACE_POP
}
/*
equation index: 33
type: SIMPLE_ASSIGN
P_curt = pv_wind_out + (-P_direct) - P_ST_in
*/
void PVWindEES_eqFunction_33(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,33};
  data->localData[0]->realVars[9] /* P_curt variable */ = data->localData[0]->realVars[18] /* pv_wind_out variable */ + (-data->localData[0]->realVars[10] /* P_direct variable */) - data->localData[0]->realVars[7] /* P_ST_in variable */;
  TRACE_POP
}
/*
equation index: 34
type: SIMPLE_ASSIGN
P_ST_out = if pv_wind_out > P_heater then 0.0 else if SOC > 0.15 then max(P_heater - pv_wind_out, 0.0) else 0.0
*/
void PVWindEES_eqFunction_34(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,34};
  modelica_boolean tmp5;
  modelica_boolean tmp6;
  modelica_boolean tmp7;
  modelica_real tmp8;
  RELATIONHYSTERESIS(tmp5, data->localData[0]->realVars[18] /* pv_wind_out variable */, data->simulationInfo->realParameter[5] /* P_heater PARAM */, 0, Greater);
  tmp7 = (modelica_boolean)tmp5;
  if(tmp7)
  {
    tmp8 = 0.0;
  }
  else
  {
    RELATIONHYSTERESIS(tmp6, data->localData[0]->realVars[15] /* SOC variable */, 0.15, 2, Greater);
    tmp8 = (tmp6?fmax(data->simulationInfo->realParameter[5] /* P_heater PARAM */ - data->localData[0]->realVars[18] /* pv_wind_out variable */,0.0):0.0);
  }
  data->localData[0]->realVars[8] /* P_ST_out variable */ = tmp8;
  TRACE_POP
}
/*
equation index: 35
type: SIMPLE_ASSIGN
P_ele = P_direct + P_ST_out
*/
void PVWindEES_eqFunction_35(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,35};
  data->localData[0]->realVars[11] /* P_ele variable */ = data->localData[0]->realVars[10] /* P_direct variable */ + data->localData[0]->realVars[8] /* P_ST_out variable */;
  TRACE_POP
}
/*
equation index: 36
type: SIMPLE_ASSIGN
P_heat = P_ele * eff_heater
*/
void PVWindEES_eqFunction_36(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,36};
  data->localData[0]->realVars[12] /* P_heat variable */ = (data->localData[0]->realVars[11] /* P_ele variable */) * (data->simulationInfo->realParameter[17] /* eff_heater PARAM */);
  TRACE_POP
}
/*
equation index: 37
type: SIMPLE_ASSIGN
$DER.E_heat = P_heat
*/
void PVWindEES_eqFunction_37(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,37};
  data->localData[0]->realVars[3] /* der(E_heat) STATE_DER */ = data->localData[0]->realVars[12] /* P_heat variable */;
  TRACE_POP
}
/*
equation index: 38
type: SIMPLE_ASSIGN
$DER.E_ST_stored = P_ST_in * eff_ST_in - P_ST_out / eff_ST_out
*/
void PVWindEES_eqFunction_38(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,38};
  data->localData[0]->realVars[2] /* der(E_ST_stored) STATE_DER */ = (data->localData[0]->realVars[7] /* P_ST_in variable */) * (data->simulationInfo->realParameter[14] /* eff_ST_in PARAM */) - (DIVISION_SIM(data->localData[0]->realVars[8] /* P_ST_out variable */,data->simulationInfo->realParameter[15] /* eff_ST_out PARAM */,"eff_ST_out",equationIndexes));
  TRACE_POP
}
/*
equation index: 40
type: ALGORITHM

  assert(Wind_out_ref.tableName <> "NoName", "tableOnFile = true and no table name given");
*/
void PVWindEES_eqFunction_40(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,40};
  static const MMC_DEFSTRINGLIT(tmp11,6,"NoName");
  static const MMC_DEFSTRINGLIT(tmp12,42,"tableOnFile = true and no table name given");
  static int tmp13 = 0;
  {
    if(!(!stringEqual(data->simulationInfo->stringParameter[3] /* Wind_out_ref.tableName PARAM */, MMC_REFSTRINGLIT(tmp11))))
    {
      {
        FILE_INFO info = {"/usr/lib/omlibrary/Modelica 3.2.3/Blocks/Tables.mo",347,7,348,54,1};
        omc_assert_warning(info, "The following assertion has been violated %sat time %f\nWind_out_ref.tableName <> \"NoName\"", initial() ? "during initialization " : "", data->localData[0]->timeValue);
        omc_assert_withEquationIndexes(threadData, info, equationIndexes, MMC_STRINGDATA(MMC_REFSTRINGLIT(tmp12)));
      }
    }
  }
  TRACE_POP
}
/*
equation index: 39
type: ALGORITHM

  assert(PV_out_ref.tableName <> "NoName", "tableOnFile = true and no table name given");
*/
void PVWindEES_eqFunction_39(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,39};
  static const MMC_DEFSTRINGLIT(tmp16,6,"NoName");
  static const MMC_DEFSTRINGLIT(tmp17,42,"tableOnFile = true and no table name given");
  static int tmp18 = 0;
  {
    if(!(!stringEqual(data->simulationInfo->stringParameter[1] /* PV_out_ref.tableName PARAM */, MMC_REFSTRINGLIT(tmp16))))
    {
      {
        FILE_INFO info = {"/usr/lib/omlibrary/Modelica 3.2.3/Blocks/Tables.mo",347,7,348,54,1};
        omc_assert_warning(info, "The following assertion has been violated %sat time %f\nPV_out_ref.tableName <> \"NoName\"", initial() ? "during initialization " : "", data->localData[0]->timeValue);
        omc_assert_withEquationIndexes(threadData, info, equationIndexes, MMC_STRINGDATA(MMC_REFSTRINGLIT(tmp17)));
      }
    }
  }
  TRACE_POP
}

OMC_DISABLE_OPT
int PVWindEES_functionDAE(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  int equationIndexes[1] = {0};
#if !defined(OMC_MINIMAL_RUNTIME)
  if (measure_time_flag) rt_tick(SIM_TIMER_DAE);
#endif

  data->simulationInfo->needToIterate = 0;
  data->simulationInfo->discreteCall = 1;
  PVWindEES_functionLocalKnownVars(data, threadData);
  PVWindEES_eqFunction_22(data, threadData);

  PVWindEES_eqFunction_23(data, threadData);

  PVWindEES_eqFunction_24(data, threadData);

  PVWindEES_eqFunction_25(data, threadData);

  PVWindEES_eqFunction_26(data, threadData);

  PVWindEES_eqFunction_27(data, threadData);

  PVWindEES_eqFunction_28(data, threadData);

  PVWindEES_eqFunction_29(data, threadData);

  PVWindEES_eqFunction_30(data, threadData);

  PVWindEES_eqFunction_31(data, threadData);

  PVWindEES_eqFunction_32(data, threadData);

  PVWindEES_eqFunction_33(data, threadData);

  PVWindEES_eqFunction_34(data, threadData);

  PVWindEES_eqFunction_35(data, threadData);

  PVWindEES_eqFunction_36(data, threadData);

  PVWindEES_eqFunction_37(data, threadData);

  PVWindEES_eqFunction_38(data, threadData);

  PVWindEES_eqFunction_40(data, threadData);

  PVWindEES_eqFunction_39(data, threadData);
  data->simulationInfo->discreteCall = 0;
  
#if !defined(OMC_MINIMAL_RUNTIME)
  if (measure_time_flag) rt_accumulate(SIM_TIMER_DAE);
#endif
  TRACE_POP
  return 0;
}


int PVWindEES_functionLocalKnownVars(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH

  
  TRACE_POP
  return 0;
}


/* forwarded equations */
extern void PVWindEES_eqFunction_23(DATA* data, threadData_t *threadData);
extern void PVWindEES_eqFunction_24(DATA* data, threadData_t *threadData);
extern void PVWindEES_eqFunction_25(DATA* data, threadData_t *threadData);
extern void PVWindEES_eqFunction_26(DATA* data, threadData_t *threadData);
extern void PVWindEES_eqFunction_27(DATA* data, threadData_t *threadData);
extern void PVWindEES_eqFunction_28(DATA* data, threadData_t *threadData);
extern void PVWindEES_eqFunction_29(DATA* data, threadData_t *threadData);
extern void PVWindEES_eqFunction_30(DATA* data, threadData_t *threadData);
extern void PVWindEES_eqFunction_31(DATA* data, threadData_t *threadData);
extern void PVWindEES_eqFunction_32(DATA* data, threadData_t *threadData);
extern void PVWindEES_eqFunction_34(DATA* data, threadData_t *threadData);
extern void PVWindEES_eqFunction_35(DATA* data, threadData_t *threadData);
extern void PVWindEES_eqFunction_36(DATA* data, threadData_t *threadData);
extern void PVWindEES_eqFunction_37(DATA* data, threadData_t *threadData);
extern void PVWindEES_eqFunction_38(DATA* data, threadData_t *threadData);

static void functionODE_system0(DATA *data, threadData_t *threadData)
{
    PVWindEES_eqFunction_23(data, threadData);

    PVWindEES_eqFunction_24(data, threadData);

    PVWindEES_eqFunction_25(data, threadData);

    PVWindEES_eqFunction_26(data, threadData);

    PVWindEES_eqFunction_27(data, threadData);

    PVWindEES_eqFunction_28(data, threadData);

    PVWindEES_eqFunction_29(data, threadData);

    PVWindEES_eqFunction_30(data, threadData);

    PVWindEES_eqFunction_31(data, threadData);

    PVWindEES_eqFunction_32(data, threadData);

    PVWindEES_eqFunction_34(data, threadData);

    PVWindEES_eqFunction_35(data, threadData);

    PVWindEES_eqFunction_36(data, threadData);

    PVWindEES_eqFunction_37(data, threadData);

    PVWindEES_eqFunction_38(data, threadData);
}

int PVWindEES_functionODE(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
#if !defined(OMC_MINIMAL_RUNTIME)
  if (measure_time_flag) rt_tick(SIM_TIMER_FUNCTION_ODE);
#endif

  
  data->simulationInfo->callStatistics.functionODE++;
  
  PVWindEES_functionLocalKnownVars(data, threadData);
  functionODE_system0(data, threadData);

#if !defined(OMC_MINIMAL_RUNTIME)
  if (measure_time_flag) rt_accumulate(SIM_TIMER_FUNCTION_ODE);
#endif

  TRACE_POP
  return 0;
}

/* forward the main in the simulation runtime */
extern int _main_SimulationRuntime(int argc, char**argv, DATA *data, threadData_t *threadData);

#include "PVWindEES_12jac.h"
#include "PVWindEES_13opt.h"

struct OpenModelicaGeneratedFunctionCallbacks PVWindEES_callback = {
   (int (*)(DATA *, threadData_t *, void *)) PVWindEES_performSimulation,    /* performSimulation */
   (int (*)(DATA *, threadData_t *, void *)) PVWindEES_performQSSSimulation,    /* performQSSSimulation */
   PVWindEES_updateContinuousSystem,    /* updateContinuousSystem */
   PVWindEES_callExternalObjectDestructors,    /* callExternalObjectDestructors */
   NULL,    /* initialNonLinearSystem */
   NULL,    /* initialLinearSystem */
   NULL,    /* initialMixedSystem */
   #if !defined(OMC_NO_STATESELECTION)
   PVWindEES_initializeStateSets,
   #else
   NULL,
   #endif    /* initializeStateSets */
   PVWindEES_initializeDAEmodeData,
   PVWindEES_functionODE,
   PVWindEES_functionAlgebraics,
   PVWindEES_functionDAE,
   PVWindEES_functionLocalKnownVars,
   PVWindEES_input_function,
   PVWindEES_input_function_init,
   PVWindEES_input_function_updateStartValues,
   PVWindEES_data_function,
   PVWindEES_output_function,
   PVWindEES_setc_function,
   PVWindEES_function_storeDelayed,
   PVWindEES_updateBoundVariableAttributes,
   PVWindEES_functionInitialEquations,
   1, /* useHomotopy - 0: local homotopy (equidistant lambda), 1: global homotopy (equidistant lambda), 2: new global homotopy approach (adaptive lambda), 3: new local homotopy approach (adaptive lambda)*/
   NULL,
   PVWindEES_functionRemovedInitialEquations,
   PVWindEES_updateBoundParameters,
   PVWindEES_checkForAsserts,
   PVWindEES_function_ZeroCrossingsEquations,
   PVWindEES_function_ZeroCrossings,
   PVWindEES_function_updateRelations,
   PVWindEES_zeroCrossingDescription,
   PVWindEES_relationDescription,
   PVWindEES_function_initSample,
   PVWindEES_INDEX_JAC_A,
   PVWindEES_INDEX_JAC_B,
   PVWindEES_INDEX_JAC_C,
   PVWindEES_INDEX_JAC_D,
   PVWindEES_INDEX_JAC_F,
   PVWindEES_initialAnalyticJacobianA,
   PVWindEES_initialAnalyticJacobianB,
   PVWindEES_initialAnalyticJacobianC,
   PVWindEES_initialAnalyticJacobianD,
   PVWindEES_initialAnalyticJacobianF,
   PVWindEES_functionJacA_column,
   PVWindEES_functionJacB_column,
   PVWindEES_functionJacC_column,
   PVWindEES_functionJacD_column,
   PVWindEES_functionJacF_column,
   PVWindEES_linear_model_frame,
   PVWindEES_linear_model_datarecovery_frame,
   PVWindEES_mayer,
   PVWindEES_lagrange,
   PVWindEES_pickUpBoundsForInputsInOptimization,
   PVWindEES_setInputData,
   PVWindEES_getTimeGrid,
   PVWindEES_symbolicInlineSystem,
   PVWindEES_function_initSynchronous,
   PVWindEES_function_updateSynchronous,
   PVWindEES_function_equationsSynchronous,
   PVWindEES_inputNames,
   PVWindEES_dataReconciliationInputNames,
   NULL,
   NULL,
   NULL,
   -1

};

#define _OMC_LIT_RESOURCE_0_name_data "Complex"
#define _OMC_LIT_RESOURCE_0_dir_data "/usr/lib/omlibrary"
static const MMC_DEFSTRINGLIT(_OMC_LIT_RESOURCE_0_name,7,_OMC_LIT_RESOURCE_0_name_data);
static const MMC_DEFSTRINGLIT(_OMC_LIT_RESOURCE_0_dir,18,_OMC_LIT_RESOURCE_0_dir_data);

#define _OMC_LIT_RESOURCE_1_name_data "Modelica"
#define _OMC_LIT_RESOURCE_1_dir_data "/usr/lib/omlibrary/Modelica 3.2.3"
static const MMC_DEFSTRINGLIT(_OMC_LIT_RESOURCE_1_name,8,_OMC_LIT_RESOURCE_1_name_data);
static const MMC_DEFSTRINGLIT(_OMC_LIT_RESOURCE_1_dir,33,_OMC_LIT_RESOURCE_1_dir_data);

#define _OMC_LIT_RESOURCE_2_name_data "ModelicaServices"
#define _OMC_LIT_RESOURCE_2_dir_data "/usr/lib/omlibrary/ModelicaServices 3.2.3"
static const MMC_DEFSTRINGLIT(_OMC_LIT_RESOURCE_2_name,16,_OMC_LIT_RESOURCE_2_name_data);
static const MMC_DEFSTRINGLIT(_OMC_LIT_RESOURCE_2_dir,41,_OMC_LIT_RESOURCE_2_dir_data);

#define _OMC_LIT_RESOURCE_3_name_data "PVWindEES"
#define _OMC_LIT_RESOURCE_3_dir_data "/media/yewang/Data/Work/Research/Topics/yewang/HILTCRC/repo/RenewableTherm"
static const MMC_DEFSTRINGLIT(_OMC_LIT_RESOURCE_3_name,9,_OMC_LIT_RESOURCE_3_name_data);
static const MMC_DEFSTRINGLIT(_OMC_LIT_RESOURCE_3_dir,74,_OMC_LIT_RESOURCE_3_dir_data);

#define _OMC_LIT_RESOURCE_4_name_data "SolarTherm"
#define _OMC_LIT_RESOURCE_4_dir_data "/home/yewang/.openmodelica/libraries/SolarTherm"
static const MMC_DEFSTRINGLIT(_OMC_LIT_RESOURCE_4_name,10,_OMC_LIT_RESOURCE_4_name_data);
static const MMC_DEFSTRINGLIT(_OMC_LIT_RESOURCE_4_dir,47,_OMC_LIT_RESOURCE_4_dir_data);

static const MMC_DEFSTRUCTLIT(_OMC_LIT_RESOURCES,10,MMC_ARRAY_TAG) {MMC_REFSTRINGLIT(_OMC_LIT_RESOURCE_0_name), MMC_REFSTRINGLIT(_OMC_LIT_RESOURCE_0_dir), MMC_REFSTRINGLIT(_OMC_LIT_RESOURCE_1_name), MMC_REFSTRINGLIT(_OMC_LIT_RESOURCE_1_dir), MMC_REFSTRINGLIT(_OMC_LIT_RESOURCE_2_name), MMC_REFSTRINGLIT(_OMC_LIT_RESOURCE_2_dir), MMC_REFSTRINGLIT(_OMC_LIT_RESOURCE_3_name), MMC_REFSTRINGLIT(_OMC_LIT_RESOURCE_3_dir), MMC_REFSTRINGLIT(_OMC_LIT_RESOURCE_4_name), MMC_REFSTRINGLIT(_OMC_LIT_RESOURCE_4_dir)}};
void PVWindEES_setupDataStruc(DATA *data, threadData_t *threadData)
{
  assertStreamPrint(threadData,0!=data, "Error while initialize Data");
  threadData->localRoots[LOCAL_ROOT_SIMULATION_DATA] = data;
  data->callback = &PVWindEES_callback;
  OpenModelica_updateUriMapping(threadData, MMC_REFSTRUCTLIT(_OMC_LIT_RESOURCES));
  data->modelData->modelName = "PVWindEES";
  data->modelData->modelFilePrefix = "PVWindEES";
  data->modelData->resultFileName = NULL;
  data->modelData->modelDir = "/media/yewang/Data/Work/Research/Topics/yewang/HILTCRC/repo/RenewableTherm";
  data->modelData->modelGUID = "{7eaea77f-c020-4a10-8175-65652f53b6da}";
  #if defined(OPENMODELICA_XML_FROM_FILE_AT_RUNTIME)
  data->modelData->initXMLData = NULL;
  data->modelData->modelDataXml.infoXMLData = NULL;
  #else
  #if defined(_MSC_VER) /* handle joke compilers */
  {
  /* for MSVC we encode a string like char x[] = {'a', 'b', 'c', '\0'} */
  /* because the string constant limit is 65535 bytes */
  static const char contents_init[] =
    #include "PVWindEES_init.c"
    ;
  static const char contents_info[] =
    #include "PVWindEES_info.c"
    ;
    data->modelData->initXMLData = contents_init;
    data->modelData->modelDataXml.infoXMLData = contents_info;
  }
  #else /* handle real compilers */
  data->modelData->initXMLData =
  #include "PVWindEES_init.c"
    ;
  data->modelData->modelDataXml.infoXMLData =
  #include "PVWindEES_info.c"
    ;
  #endif /* defined(_MSC_VER) */
  #endif /* defined(OPENMODELICA_XML_FROM_FILE_AT_RUNTIME) */
  data->modelData->runTestsuite = 0;
  
  data->modelData->nStates = 2;
  data->modelData->nVariablesReal = 19;
  data->modelData->nDiscreteReal = 0;
  data->modelData->nVariablesInteger = 0;
  data->modelData->nVariablesBoolean = 0;
  data->modelData->nVariablesString = 0;
  data->modelData->nParametersReal = 19;
  data->modelData->nParametersInteger = 8;
  data->modelData->nParametersBoolean = 6;
  data->modelData->nParametersString = 6;
  data->modelData->nInputVars = 0;
  data->modelData->nOutputVars = 0;
  
  data->modelData->nAliasReal = 0;
  data->modelData->nAliasInteger = 0;
  data->modelData->nAliasBoolean = 0;
  data->modelData->nAliasString = 0;
  
  data->modelData->nZeroCrossings = 3;
  data->modelData->nSamples = 0;
  data->modelData->nRelations = 3;
  data->modelData->nMathEvents = 0;
  data->modelData->nExtObjs = 2;
  
  data->modelData->modelDataXml.fileName = "PVWindEES_info.json";
  data->modelData->modelDataXml.modelInfoXmlLength = 0;
  data->modelData->modelDataXml.nFunctions = 8;
  data->modelData->modelDataXml.nProfileBlocks = 0;
  data->modelData->modelDataXml.nEquations = 71;
  data->modelData->nMixedSystems = 0;
  data->modelData->nLinearSystems = 0;
  data->modelData->nNonLinearSystems = 0;
  data->modelData->nStateSets = 0;
  data->modelData->nJacobians = 5;
  data->modelData->nOptimizeConstraints = 0;
  data->modelData->nOptimizeFinalConstraints = 0;
  
  data->modelData->nDelayExpressions = 0;
  
  data->modelData->nClocks = 0;
  data->modelData->nSubClocks = 0;
  
  data->modelData->nSensitivityVars = 0;
  data->modelData->nSensitivityParamVars = 0;
  data->modelData->nSetcVars = 0;
  data->modelData->ndataReconVars = 0;
  data->modelData->linearizationDumpLanguage =
  OMC_LINEARIZE_DUMP_LANGUAGE_MODELICA;
}

static int rml_execution_failed()
{
  fflush(NULL);
  fprintf(stderr, "Execution failed!\n");
  fflush(NULL);
  return 1;
}

#if defined(threadData)
#undef threadData
#endif
/* call the simulation runtime main from our main! */
int main(int argc, char**argv)
{
  int res;
  DATA data;
  MODEL_DATA modelData;
  SIMULATION_INFO simInfo;
  data.modelData = &modelData;
  data.simulationInfo = &simInfo;
  measure_time_flag = 0;
  compiledInDAEMode = 0;
  compiledWithSymSolver = 0;
  MMC_INIT(0);
  omc_alloc_interface.init();
  {
    MMC_TRY_TOP()
  
    MMC_TRY_STACK()
  
    PVWindEES_setupDataStruc(&data, threadData);
    res = _main_SimulationRuntime(argc, argv, &data, threadData);
    
    MMC_ELSE()
    rml_execution_failed();
    fprintf(stderr, "Stack overflow detected and was not caught.\nSend us a bug report at https://trac.openmodelica.org/OpenModelica/newticket\n    Include the following trace:\n");
    printStacktraceMessages();
    fflush(NULL);
    return 1;
    MMC_CATCH_STACK()
    
    MMC_CATCH_TOP(return rml_execution_failed());
  }

  fflush(NULL);
  EXIT(res);
  return res;
}

#ifdef __cplusplus
}
#endif


