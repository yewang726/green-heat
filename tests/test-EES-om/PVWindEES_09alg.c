/* Algebraic */
#include "PVWindEES_model.h"

#ifdef __cplusplus
extern "C" {
#endif


/* forwarded equations */
extern void PVWindEES_eqFunction_22(DATA* data, threadData_t *threadData);
extern void PVWindEES_eqFunction_33(DATA* data, threadData_t *threadData);
extern void PVWindEES_eqFunction_40(DATA* data, threadData_t *threadData);
extern void PVWindEES_eqFunction_39(DATA* data, threadData_t *threadData);

static void functionAlg_system0(DATA *data, threadData_t *threadData)
{
    PVWindEES_eqFunction_22(data, threadData);

    PVWindEES_eqFunction_33(data, threadData);

    PVWindEES_eqFunction_40(data, threadData);

    PVWindEES_eqFunction_39(data, threadData);
}
/* for continuous time variables */
int PVWindEES_functionAlgebraics(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH

#if !defined(OMC_MINIMAL_RUNTIME)
  if (measure_time_flag) rt_tick(SIM_TIMER_ALGEBRAICS);
#endif
  data->simulationInfo->callStatistics.functionAlgebraics++;

  functionAlg_system0(data, threadData);

  PVWindEES_function_savePreSynchronous(data, threadData);
  
#if !defined(OMC_MINIMAL_RUNTIME)
  if (measure_time_flag) rt_accumulate(SIM_TIMER_ALGEBRAICS);
#endif

  TRACE_POP
  return 0;
}

#ifdef __cplusplus
}
#endif
