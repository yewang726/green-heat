/* Events: Sample, Zero Crossings, Relations, Discrete Changes */
#include "PVWindEES_model.h"
#if defined(__cplusplus)
extern "C" {
#endif

/* Initializes the raw time events of the simulation using the now
   calcualted parameters. */
void PVWindEES_function_initSample(DATA *data, threadData_t *threadData)
{
  long i=0;
}

const char *PVWindEES_zeroCrossingDescription(int i, int **out_EquationIndexes)
{
  static const char *res[] = {"pv_wind_out > P_heater",
  "SOC < 0.99",
  "SOC > 0.15"};
  static const int occurEqs0[] = {1,31};
  static const int occurEqs1[] = {1,32};
  static const int occurEqs2[] = {1,34};
  static const int *occurEqs[] = {occurEqs0,occurEqs1,occurEqs2};
  *out_EquationIndexes = (int*) occurEqs[i];
  return res[i];
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
extern void PVWindEES_eqFunction_32(DATA* data, threadData_t *threadData);
extern void PVWindEES_eqFunction_34(DATA* data, threadData_t *threadData);
extern void PVWindEES_eqFunction_38(DATA* data, threadData_t *threadData);

int PVWindEES_function_ZeroCrossingsEquations(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH

  data->simulationInfo->callStatistics.functionZeroCrossingsEquations++;

  PVWindEES_eqFunction_23(data, threadData);

  PVWindEES_eqFunction_24(data, threadData);

  PVWindEES_eqFunction_25(data, threadData);

  PVWindEES_eqFunction_26(data, threadData);

  PVWindEES_eqFunction_27(data, threadData);

  PVWindEES_eqFunction_28(data, threadData);

  PVWindEES_eqFunction_29(data, threadData);

  PVWindEES_eqFunction_30(data, threadData);

  PVWindEES_eqFunction_32(data, threadData);

  PVWindEES_eqFunction_34(data, threadData);

  PVWindEES_eqFunction_38(data, threadData);
  
  TRACE_POP
  return 0;
}

int PVWindEES_function_ZeroCrossings(DATA *data, threadData_t *threadData, double *gout)
{
  TRACE_PUSH
  modelica_boolean tmp0;
  modelica_boolean tmp1;
  modelica_boolean tmp2;

#if !defined(OMC_MINIMAL_RUNTIME)
  if (measure_time_flag) rt_tick(SIM_TIMER_ZC);
#endif
  data->simulationInfo->callStatistics.functionZeroCrossings++;

  tmp0 = GreaterZC(data->localData[0]->realVars[18] /* pv_wind_out variable */, data->simulationInfo->realParameter[5] /* P_heater PARAM */, data->simulationInfo->storedRelations[0]);
  gout[0] = (tmp0) ? 1 : -1;
  tmp1 = LessZC(data->localData[0]->realVars[15] /* SOC variable */, 0.99, data->simulationInfo->storedRelations[1]);
  gout[1] = (tmp1) ? 1 : -1;
  tmp2 = GreaterZC(data->localData[0]->realVars[15] /* SOC variable */, 0.15, data->simulationInfo->storedRelations[2]);
  gout[2] = (tmp2) ? 1 : -1;

#if !defined(OMC_MINIMAL_RUNTIME)
  if (measure_time_flag) rt_accumulate(SIM_TIMER_ZC);
#endif

  TRACE_POP
  return 0;
}

const char *PVWindEES_relationDescription(int i)
{
  const char *res[] = {"pv_wind_out > P_heater",
  "SOC < 0.99",
  "SOC > 0.15"};
  return res[i];
}

int PVWindEES_function_updateRelations(DATA *data, threadData_t *threadData, int evalforZeroCross)
{
  TRACE_PUSH
  modelica_boolean tmp3;
  modelica_boolean tmp4;
  modelica_boolean tmp5;
  
  if(evalforZeroCross) {
    tmp3 = GreaterZC(data->localData[0]->realVars[18] /* pv_wind_out variable */, data->simulationInfo->realParameter[5] /* P_heater PARAM */, data->simulationInfo->storedRelations[0]);
    data->simulationInfo->relations[0] = tmp3;
    tmp4 = LessZC(data->localData[0]->realVars[15] /* SOC variable */, 0.99, data->simulationInfo->storedRelations[1]);
    data->simulationInfo->relations[1] = tmp4;
    tmp5 = GreaterZC(data->localData[0]->realVars[15] /* SOC variable */, 0.15, data->simulationInfo->storedRelations[2]);
    data->simulationInfo->relations[2] = tmp5;
  } else {
    data->simulationInfo->relations[0] = (data->localData[0]->realVars[18] /* pv_wind_out variable */ > data->simulationInfo->realParameter[5] /* P_heater PARAM */);
    data->simulationInfo->relations[1] = (data->localData[0]->realVars[15] /* SOC variable */ < 0.99);
    data->simulationInfo->relations[2] = (data->localData[0]->realVars[15] /* SOC variable */ > 0.15);
  }
  
  TRACE_POP
  return 0;
}

#if defined(__cplusplus)
}
#endif

