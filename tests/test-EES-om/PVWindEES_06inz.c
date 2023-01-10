/* Initialization */
#include "PVWindEES_model.h"
#include "PVWindEES_11mix.h"
#include "PVWindEES_12jac.h"
#if defined(__cplusplus)
extern "C" {
#endif

void PVWindEES_functionInitialEquations_0(DATA *data, threadData_t *threadData);

/*
equation index: 1
type: SIMPLE_ASSIGN
E_ST_stored = $START.E_ST_stored
*/
void PVWindEES_eqFunction_1(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,1};
  data->localData[0]->realVars[0] /* E_ST_stored STATE(1) */ = data->modelData->realVarsData[0].attribute /* E_ST_stored STATE(1) */.start;
  TRACE_POP
}
extern void PVWindEES_eqFunction_27(DATA *data, threadData_t *threadData);

extern void PVWindEES_eqFunction_28(DATA *data, threadData_t *threadData);

extern void PVWindEES_eqFunction_29(DATA *data, threadData_t *threadData);

extern void PVWindEES_eqFunction_24(DATA *data, threadData_t *threadData);

extern void PVWindEES_eqFunction_25(DATA *data, threadData_t *threadData);

extern void PVWindEES_eqFunction_26(DATA *data, threadData_t *threadData);

extern void PVWindEES_eqFunction_30(DATA *data, threadData_t *threadData);

extern void PVWindEES_eqFunction_31(DATA *data, threadData_t *threadData);

extern void PVWindEES_eqFunction_23(DATA *data, threadData_t *threadData);

extern void PVWindEES_eqFunction_34(DATA *data, threadData_t *threadData);

extern void PVWindEES_eqFunction_35(DATA *data, threadData_t *threadData);

extern void PVWindEES_eqFunction_36(DATA *data, threadData_t *threadData);

extern void PVWindEES_eqFunction_32(DATA *data, threadData_t *threadData);

extern void PVWindEES_eqFunction_33(DATA *data, threadData_t *threadData);

extern void PVWindEES_eqFunction_38(DATA *data, threadData_t *threadData);

extern void PVWindEES_eqFunction_37(DATA *data, threadData_t *threadData);


/*
equation index: 18
type: SIMPLE_ASSIGN
E_heat = $START.E_heat
*/
void PVWindEES_eqFunction_18(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,18};
  data->localData[0]->realVars[1] /* E_heat STATE(1,P_heat) */ = data->modelData->realVarsData[1].attribute /* E_heat STATE(1,P_heat) */.start;
  TRACE_POP
}
extern void PVWindEES_eqFunction_22(DATA *data, threadData_t *threadData);


/*
equation index: 21
type: ALGORITHM

  assert(Wind_out_ref.tableName <> "NoName", "tableOnFile = true and no table name given");
*/
void PVWindEES_eqFunction_21(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,21};
  static const MMC_DEFSTRINGLIT(tmp2,6,"NoName");
  static const MMC_DEFSTRINGLIT(tmp3,42,"tableOnFile = true and no table name given");
  static int tmp4 = 0;
  {
    if(!(!stringEqual(data->simulationInfo->stringParameter[3] /* Wind_out_ref.tableName PARAM */, MMC_REFSTRINGLIT(tmp2))))
    {
      {
        FILE_INFO info = {"/usr/lib/omlibrary/Modelica 3.2.3/Blocks/Tables.mo",347,7,348,54,1};
        omc_assert_warning(info, "The following assertion has been violated %sat time %f\nWind_out_ref.tableName <> \"NoName\"", initial() ? "during initialization " : "", data->localData[0]->timeValue);
        omc_assert_withEquationIndexes(threadData, info, equationIndexes, MMC_STRINGDATA(MMC_REFSTRINGLIT(tmp3)));
      }
    }
  }
  TRACE_POP
}

/*
equation index: 20
type: ALGORITHM

  assert(PV_out_ref.tableName <> "NoName", "tableOnFile = true and no table name given");
*/
void PVWindEES_eqFunction_20(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,20};
  static const MMC_DEFSTRINGLIT(tmp7,6,"NoName");
  static const MMC_DEFSTRINGLIT(tmp8,42,"tableOnFile = true and no table name given");
  static int tmp9 = 0;
  {
    if(!(!stringEqual(data->simulationInfo->stringParameter[1] /* PV_out_ref.tableName PARAM */, MMC_REFSTRINGLIT(tmp7))))
    {
      {
        FILE_INFO info = {"/usr/lib/omlibrary/Modelica 3.2.3/Blocks/Tables.mo",347,7,348,54,1};
        omc_assert_warning(info, "The following assertion has been violated %sat time %f\nPV_out_ref.tableName <> \"NoName\"", initial() ? "during initialization " : "", data->localData[0]->timeValue);
        omc_assert_withEquationIndexes(threadData, info, equationIndexes, MMC_STRINGDATA(MMC_REFSTRINGLIT(tmp8)));
      }
    }
  }
  TRACE_POP
}
OMC_DISABLE_OPT
void PVWindEES_functionInitialEquations_0(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  PVWindEES_eqFunction_1(data, threadData);
  PVWindEES_eqFunction_27(data, threadData);
  PVWindEES_eqFunction_28(data, threadData);
  PVWindEES_eqFunction_29(data, threadData);
  PVWindEES_eqFunction_24(data, threadData);
  PVWindEES_eqFunction_25(data, threadData);
  PVWindEES_eqFunction_26(data, threadData);
  PVWindEES_eqFunction_30(data, threadData);
  PVWindEES_eqFunction_31(data, threadData);
  PVWindEES_eqFunction_23(data, threadData);
  PVWindEES_eqFunction_34(data, threadData);
  PVWindEES_eqFunction_35(data, threadData);
  PVWindEES_eqFunction_36(data, threadData);
  PVWindEES_eqFunction_32(data, threadData);
  PVWindEES_eqFunction_33(data, threadData);
  PVWindEES_eqFunction_38(data, threadData);
  PVWindEES_eqFunction_37(data, threadData);
  PVWindEES_eqFunction_18(data, threadData);
  PVWindEES_eqFunction_22(data, threadData);
  PVWindEES_eqFunction_21(data, threadData);
  PVWindEES_eqFunction_20(data, threadData);
  TRACE_POP
}

int PVWindEES_functionInitialEquations(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH

  data->simulationInfo->discreteCall = 1;
  PVWindEES_functionInitialEquations_0(data, threadData);
  data->simulationInfo->discreteCall = 0;
  
  TRACE_POP
  return 0;
}

/* No PVWindEES_functionInitialEquations_lambda0 function */

int PVWindEES_functionRemovedInitialEquations(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int *equationIndexes = NULL;
  double res = 0.0;

  
  TRACE_POP
  return 0;
}


#if defined(__cplusplus)
}
#endif

