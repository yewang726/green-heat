/* update bound parameters and variable attributes (start, nominal, min, max) */
#include "PVWindEES_model.h"
#if defined(__cplusplus)
extern "C" {
#endif

OMC_DISABLE_OPT
int PVWindEES_updateBoundVariableAttributes(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  /* min ******************************************************** */
  
  infoStreamPrint(LOG_INIT, 1, "updating min-values");
  if (ACTIVE_STREAM(LOG_INIT)) messageClose(LOG_INIT);
  
  /* max ******************************************************** */
  
  infoStreamPrint(LOG_INIT, 1, "updating max-values");
  if (ACTIVE_STREAM(LOG_INIT)) messageClose(LOG_INIT);
  
  /* nominal **************************************************** */
  
  infoStreamPrint(LOG_INIT, 1, "updating nominal-values");
  if (ACTIVE_STREAM(LOG_INIT)) messageClose(LOG_INIT);
  
  /* start ****************************************************** */
  infoStreamPrint(LOG_INIT, 1, "updating primary start-values");
  if (ACTIVE_STREAM(LOG_INIT)) messageClose(LOG_INIT);
  
  TRACE_POP
  return 0;
}

void PVWindEES_updateBoundParameters_0(DATA *data, threadData_t *threadData);

/*
equation index: 41
type: SIMPLE_ASSIGN
PV_out_ref.fileName = table_file_pv
*/
OMC_DISABLE_OPT
static void PVWindEES_eqFunction_41(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,41};
  data->simulationInfo->stringParameter[0] /* PV_out_ref.fileName PARAM */ = data->simulationInfo->stringParameter[4] /* table_file_pv PARAM */;
  TRACE_POP
}

/*
equation index: 42
type: SIMPLE_ASSIGN
PV_out_ref.tableID = Modelica.Blocks.Types.ExternalCombiTable1D.constructor(PV_out_ref.tableName, if PV_out_ref.fileName <> "NoName" and not Modelica.Utilities.Strings.isEmpty(PV_out_ref.fileName) then PV_out_ref.fileName else "NoName", {{}}, {PV_out_ref.columns[1]}, Modelica.Blocks.Types.Smoothness.LinearSegments, PV_out_ref.extrapolation, PV_out_ref.verboseRead)
*/
OMC_DISABLE_OPT
static void PVWindEES_eqFunction_42(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,42};
  integer_array tmp1;
  array_alloc_scalar_integer_array(&tmp1, 1, (modelica_integer)data->simulationInfo->integerParameter[0] /* PV_out_ref.columns[1] PARAM */);
  data->simulationInfo->extObjs[0] = omc_Modelica_Blocks_Types_ExternalCombiTable1D_constructor(threadData, data->simulationInfo->stringParameter[1] /* PV_out_ref.tableName PARAM */, (((!stringEqual(data->simulationInfo->stringParameter[0] /* PV_out_ref.fileName PARAM */, _OMC_LIT3)) && (!omc_Modelica_Utilities_Strings_isEmpty(threadData, data->simulationInfo->stringParameter[0] /* PV_out_ref.fileName PARAM */)))?data->simulationInfo->stringParameter[0] /* PV_out_ref.fileName PARAM */:_OMC_LIT3), _OMC_LIT4, tmp1, 1, data->simulationInfo->integerParameter[1] /* PV_out_ref.extrapolation PARAM */, data->simulationInfo->booleanParameter[2] /* PV_out_ref.verboseRead PARAM */);
  TRACE_POP
}

/*
equation index: 43
type: SIMPLE_ASSIGN
Wind_out_ref.fileName = table_file_wind
*/
OMC_DISABLE_OPT
static void PVWindEES_eqFunction_43(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,43};
  data->simulationInfo->stringParameter[2] /* Wind_out_ref.fileName PARAM */ = data->simulationInfo->stringParameter[5] /* table_file_wind PARAM */;
  TRACE_POP
}

/*
equation index: 44
type: SIMPLE_ASSIGN
Wind_out_ref.tableID = Modelica.Blocks.Types.ExternalCombiTable1D.constructor(Wind_out_ref.tableName, if Wind_out_ref.fileName <> "NoName" and not Modelica.Utilities.Strings.isEmpty(Wind_out_ref.fileName) then Wind_out_ref.fileName else "NoName", {{}}, {Wind_out_ref.columns[1]}, Modelica.Blocks.Types.Smoothness.LinearSegments, Wind_out_ref.extrapolation, Wind_out_ref.verboseRead)
*/
OMC_DISABLE_OPT
static void PVWindEES_eqFunction_44(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,44};
  integer_array tmp3;
  array_alloc_scalar_integer_array(&tmp3, 1, (modelica_integer)data->simulationInfo->integerParameter[4] /* Wind_out_ref.columns[1] PARAM */);
  data->simulationInfo->extObjs[1] = omc_Modelica_Blocks_Types_ExternalCombiTable1D_constructor(threadData, data->simulationInfo->stringParameter[3] /* Wind_out_ref.tableName PARAM */, (((!stringEqual(data->simulationInfo->stringParameter[2] /* Wind_out_ref.fileName PARAM */, _OMC_LIT3)) && (!omc_Modelica_Utilities_Strings_isEmpty(threadData, data->simulationInfo->stringParameter[2] /* Wind_out_ref.fileName PARAM */)))?data->simulationInfo->stringParameter[2] /* Wind_out_ref.fileName PARAM */:_OMC_LIT3), _OMC_LIT4, tmp3, 1, data->simulationInfo->integerParameter[5] /* Wind_out_ref.extrapolation PARAM */, data->simulationInfo->booleanParameter[5] /* Wind_out_ref.verboseRead PARAM */);
  TRACE_POP
}

/*
equation index: 45
type: SIMPLE_ASSIGN
Wind_out_ref.u_max = Modelica.Blocks.Tables.Internal.getTable1DAbscissaUmax(Wind_out_ref.tableID)
*/
OMC_DISABLE_OPT
static void PVWindEES_eqFunction_45(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,45};
  data->simulationInfo->realParameter[12] /* Wind_out_ref.u_max PARAM */ = omc_Modelica_Blocks_Tables_Internal_getTable1DAbscissaUmax(threadData, data->simulationInfo->extObjs[1]);
  TRACE_POP
}

/*
equation index: 46
type: SIMPLE_ASSIGN
Wind_out_ref.u_min = Modelica.Blocks.Tables.Internal.getTable1DAbscissaUmin(Wind_out_ref.tableID)
*/
OMC_DISABLE_OPT
static void PVWindEES_eqFunction_46(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,46};
  data->simulationInfo->realParameter[13] /* Wind_out_ref.u_min PARAM */ = omc_Modelica_Blocks_Tables_Internal_getTable1DAbscissaUmin(threadData, data->simulationInfo->extObjs[1]);
  TRACE_POP
}

/*
equation index: 51
type: SIMPLE_ASSIGN
PV_out_ref.u_max = Modelica.Blocks.Tables.Internal.getTable1DAbscissaUmax(PV_out_ref.tableID)
*/
OMC_DISABLE_OPT
static void PVWindEES_eqFunction_51(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,51};
  data->simulationInfo->realParameter[2] /* PV_out_ref.u_max PARAM */ = omc_Modelica_Blocks_Tables_Internal_getTable1DAbscissaUmax(threadData, data->simulationInfo->extObjs[0]);
  TRACE_POP
}

/*
equation index: 52
type: SIMPLE_ASSIGN
PV_out_ref.u_min = Modelica.Blocks.Tables.Internal.getTable1DAbscissaUmin(PV_out_ref.tableID)
*/
OMC_DISABLE_OPT
static void PVWindEES_eqFunction_52(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,52};
  data->simulationInfo->realParameter[3] /* PV_out_ref.u_min PARAM */ = omc_Modelica_Blocks_Tables_Internal_getTable1DAbscissaUmin(threadData, data->simulationInfo->extObjs[0]);
  TRACE_POP
}

/*
equation index: 57
type: SIMPLE_ASSIGN
P_heater = P_load / eff_heater
*/
OMC_DISABLE_OPT
static void PVWindEES_eqFunction_57(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,57};
  data->simulationInfo->realParameter[5] /* P_heater PARAM */ = DIVISION_SIM(data->simulationInfo->realParameter[6] /* P_load PARAM */,data->simulationInfo->realParameter[17] /* eff_heater PARAM */,"eff_heater",equationIndexes);
  TRACE_POP
}

/*
equation index: 58
type: SIMPLE_ASSIGN
eff_ST_out = sqrt(eff_ST_roundtrip)
*/
OMC_DISABLE_OPT
static void PVWindEES_eqFunction_58(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,58};
  modelica_real tmp4;
  tmp4 = data->simulationInfo->realParameter[16] /* eff_ST_roundtrip PARAM */;
  if(!(tmp4 >= 0.0))
  {
    FILE_INFO info = {"",0,0,0,0,0};
    omc_assert_warning(info, "The following assertion has been violated %sat time %f", initial() ? "during initialization " : "", data->localData[0]->timeValue);
    throwStreamPrintWithEquationIndexes(threadData, equationIndexes, "Model error: Argument of sqrt(eff_ST_roundtrip) was %g should be >= 0", tmp4);
  }
  data->simulationInfo->realParameter[15] /* eff_ST_out PARAM */ = sqrt(tmp4);
  TRACE_POP
}

/*
equation index: 59
type: SIMPLE_ASSIGN
eff_ST_in = sqrt(eff_ST_roundtrip)
*/
OMC_DISABLE_OPT
static void PVWindEES_eqFunction_59(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,59};
  modelica_real tmp5;
  tmp5 = data->simulationInfo->realParameter[16] /* eff_ST_roundtrip PARAM */;
  if(!(tmp5 >= 0.0))
  {
    FILE_INFO info = {"",0,0,0,0,0};
    omc_assert_warning(info, "The following assertion has been violated %sat time %f", initial() ? "during initialization " : "", data->localData[0]->timeValue);
    throwStreamPrintWithEquationIndexes(threadData, equationIndexes, "Model error: Argument of sqrt(eff_ST_roundtrip) was %g should be >= 0", tmp5);
  }
  data->simulationInfo->realParameter[14] /* eff_ST_in PARAM */ = sqrt(tmp5);
  TRACE_POP
}

/*
equation index: 60
type: SIMPLE_ASSIGN
E_ST_max = 3600.0 * P_heater * t_storage
*/
OMC_DISABLE_OPT
static void PVWindEES_eqFunction_60(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,60};
  data->simulationInfo->realParameter[0] /* E_ST_max PARAM */ = (3600.0) * ((data->simulationInfo->realParameter[5] /* P_heater PARAM */) * (data->simulationInfo->realParameter[18] /* t_storage PARAM */));
  TRACE_POP
}

/*
equation index: 61
type: SIMPLE_ASSIGN
P_wind_des = P_load * RM * (1.0 - F_pv)
*/
OMC_DISABLE_OPT
static void PVWindEES_eqFunction_61(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,61};
  data->simulationInfo->realParameter[9] /* P_wind_des PARAM */ = (data->simulationInfo->realParameter[6] /* P_load PARAM */) * ((data->simulationInfo->realParameter[11] /* RM PARAM */) * (1.0 - data->simulationInfo->realParameter[1] /* F_pv PARAM */));
  TRACE_POP
}

/*
equation index: 62
type: SIMPLE_ASSIGN
P_pv_des = P_load * RM * F_pv
*/
OMC_DISABLE_OPT
static void PVWindEES_eqFunction_62(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,62};
  data->simulationInfo->realParameter[7] /* P_pv_des PARAM */ = (data->simulationInfo->realParameter[6] /* P_load PARAM */) * ((data->simulationInfo->realParameter[11] /* RM PARAM */) * (data->simulationInfo->realParameter[1] /* F_pv PARAM */));
  TRACE_POP
}

/*
equation index: 63
type: ALGORITHM

  assert(PV_out_ref.extrapolation >= Modelica.Blocks.Types.Extrapolation.HoldLastPoint and PV_out_ref.extrapolation <= Modelica.Blocks.Types.Extrapolation.NoExtrapolation, "Variable violating min/max constraint: Modelica.Blocks.Types.Extrapolation.HoldLastPoint <= PV_out_ref.extrapolation <= Modelica.Blocks.Types.Extrapolation.NoExtrapolation, has value: " + String(PV_out_ref.extrapolation, "d"));
*/
OMC_DISABLE_OPT
static void PVWindEES_eqFunction_63(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,63};
  modelica_boolean tmp6;
  modelica_boolean tmp7;
  static const MMC_DEFSTRINGLIT(tmp8,184,"Variable violating min/max constraint: Modelica.Blocks.Types.Extrapolation.HoldLastPoint <= PV_out_ref.extrapolation <= Modelica.Blocks.Types.Extrapolation.NoExtrapolation, has value: ");
  modelica_string tmp9;
  static int tmp10 = 0;
  modelica_metatype tmpMeta[1] __attribute__((unused)) = {0};
  if(!tmp10)
  {
    tmp6 = GreaterEq(data->simulationInfo->integerParameter[1] /* PV_out_ref.extrapolation PARAM */,1);
    tmp7 = LessEq(data->simulationInfo->integerParameter[1] /* PV_out_ref.extrapolation PARAM */,4);
    if(!(tmp6 && tmp7))
    {
      tmp9 = modelica_integer_to_modelica_string_format(data->simulationInfo->integerParameter[1] /* PV_out_ref.extrapolation PARAM */, (modelica_string) mmc_strings_len1[100]);
      tmpMeta[0] = stringAppend(MMC_REFSTRINGLIT(tmp8),tmp9);
      {
        FILE_INFO info = {"/usr/lib/omlibrary/Modelica 3.2.3/Blocks/Tables.mo",323,5,325,61,1};
        omc_assert_warning(info, "The following assertion has been violated %sat time %f\nPV_out_ref.extrapolation >= Modelica.Blocks.Types.Extrapolation.HoldLastPoint and PV_out_ref.extrapolation <= Modelica.Blocks.Types.Extrapolation.NoExtrapolation", initial() ? "during initialization " : "", data->localData[0]->timeValue);
        omc_assert_warning_withEquationIndexes(info, equationIndexes, MMC_STRINGDATA(tmpMeta[0]));
      }
      tmp10 = 1;
    }
  }
  TRACE_POP
}

/*
equation index: 64
type: ALGORITHM

  assert(Wind_out_ref.extrapolation >= Modelica.Blocks.Types.Extrapolation.HoldLastPoint and Wind_out_ref.extrapolation <= Modelica.Blocks.Types.Extrapolation.NoExtrapolation, "Variable violating min/max constraint: Modelica.Blocks.Types.Extrapolation.HoldLastPoint <= Wind_out_ref.extrapolation <= Modelica.Blocks.Types.Extrapolation.NoExtrapolation, has value: " + String(Wind_out_ref.extrapolation, "d"));
*/
OMC_DISABLE_OPT
static void PVWindEES_eqFunction_64(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,64};
  modelica_boolean tmp11;
  modelica_boolean tmp12;
  static const MMC_DEFSTRINGLIT(tmp13,186,"Variable violating min/max constraint: Modelica.Blocks.Types.Extrapolation.HoldLastPoint <= Wind_out_ref.extrapolation <= Modelica.Blocks.Types.Extrapolation.NoExtrapolation, has value: ");
  modelica_string tmp14;
  static int tmp15 = 0;
  modelica_metatype tmpMeta[1] __attribute__((unused)) = {0};
  if(!tmp15)
  {
    tmp11 = GreaterEq(data->simulationInfo->integerParameter[5] /* Wind_out_ref.extrapolation PARAM */,1);
    tmp12 = LessEq(data->simulationInfo->integerParameter[5] /* Wind_out_ref.extrapolation PARAM */,4);
    if(!(tmp11 && tmp12))
    {
      tmp14 = modelica_integer_to_modelica_string_format(data->simulationInfo->integerParameter[5] /* Wind_out_ref.extrapolation PARAM */, (modelica_string) mmc_strings_len1[100]);
      tmpMeta[0] = stringAppend(MMC_REFSTRINGLIT(tmp13),tmp14);
      {
        FILE_INFO info = {"/usr/lib/omlibrary/Modelica 3.2.3/Blocks/Tables.mo",323,5,325,61,1};
        omc_assert_warning(info, "The following assertion has been violated %sat time %f\nWind_out_ref.extrapolation >= Modelica.Blocks.Types.Extrapolation.HoldLastPoint and Wind_out_ref.extrapolation <= Modelica.Blocks.Types.Extrapolation.NoExtrapolation", initial() ? "during initialization " : "", data->localData[0]->timeValue);
        omc_assert_warning_withEquationIndexes(info, equationIndexes, MMC_STRINGDATA(tmpMeta[0]));
      }
      tmp15 = 1;
    }
  }
  TRACE_POP
}

/*
equation index: 65
type: ALGORITHM

  assert(Wind_out_ref.smoothness >= Modelica.Blocks.Types.Smoothness.LinearSegments and Wind_out_ref.smoothness <= Modelica.Blocks.Types.Smoothness.MonotoneContinuousDerivative2, "Variable violating min/max constraint: Modelica.Blocks.Types.Smoothness.LinearSegments <= Wind_out_ref.smoothness <= Modelica.Blocks.Types.Smoothness.MonotoneContinuousDerivative2, has value: " + String(Wind_out_ref.smoothness, "d"));
*/
OMC_DISABLE_OPT
static void PVWindEES_eqFunction_65(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,65};
  modelica_boolean tmp16;
  modelica_boolean tmp17;
  static const MMC_DEFSTRINGLIT(tmp18,192,"Variable violating min/max constraint: Modelica.Blocks.Types.Smoothness.LinearSegments <= Wind_out_ref.smoothness <= Modelica.Blocks.Types.Smoothness.MonotoneContinuousDerivative2, has value: ");
  modelica_string tmp19;
  static int tmp20 = 0;
  modelica_metatype tmpMeta[1] __attribute__((unused)) = {0};
  if(!tmp20)
  {
    tmp16 = GreaterEq(data->simulationInfo->integerParameter[7] /* Wind_out_ref.smoothness PARAM */,1);
    tmp17 = LessEq(data->simulationInfo->integerParameter[7] /* Wind_out_ref.smoothness PARAM */,5);
    if(!(tmp16 && tmp17))
    {
      tmp19 = modelica_integer_to_modelica_string_format(data->simulationInfo->integerParameter[7] /* Wind_out_ref.smoothness PARAM */, (modelica_string) mmc_strings_len1[100]);
      tmpMeta[0] = stringAppend(MMC_REFSTRINGLIT(tmp18),tmp19);
      {
        FILE_INFO info = {"/usr/lib/omlibrary/Modelica 3.2.3/Blocks/Tables.mo",320,5,322,61,1};
        omc_assert_warning(info, "The following assertion has been violated %sat time %f\nWind_out_ref.smoothness >= Modelica.Blocks.Types.Smoothness.LinearSegments and Wind_out_ref.smoothness <= Modelica.Blocks.Types.Smoothness.MonotoneContinuousDerivative2", initial() ? "during initialization " : "", data->localData[0]->timeValue);
        omc_assert_warning_withEquationIndexes(info, equationIndexes, MMC_STRINGDATA(tmpMeta[0]));
      }
      tmp20 = 1;
    }
  }
  TRACE_POP
}

/*
equation index: 66
type: ALGORITHM

  assert(PV_out_ref.smoothness >= Modelica.Blocks.Types.Smoothness.LinearSegments and PV_out_ref.smoothness <= Modelica.Blocks.Types.Smoothness.MonotoneContinuousDerivative2, "Variable violating min/max constraint: Modelica.Blocks.Types.Smoothness.LinearSegments <= PV_out_ref.smoothness <= Modelica.Blocks.Types.Smoothness.MonotoneContinuousDerivative2, has value: " + String(PV_out_ref.smoothness, "d"));
*/
OMC_DISABLE_OPT
static void PVWindEES_eqFunction_66(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,66};
  modelica_boolean tmp21;
  modelica_boolean tmp22;
  static const MMC_DEFSTRINGLIT(tmp23,190,"Variable violating min/max constraint: Modelica.Blocks.Types.Smoothness.LinearSegments <= PV_out_ref.smoothness <= Modelica.Blocks.Types.Smoothness.MonotoneContinuousDerivative2, has value: ");
  modelica_string tmp24;
  static int tmp25 = 0;
  modelica_metatype tmpMeta[1] __attribute__((unused)) = {0};
  if(!tmp25)
  {
    tmp21 = GreaterEq(data->simulationInfo->integerParameter[3] /* PV_out_ref.smoothness PARAM */,1);
    tmp22 = LessEq(data->simulationInfo->integerParameter[3] /* PV_out_ref.smoothness PARAM */,5);
    if(!(tmp21 && tmp22))
    {
      tmp24 = modelica_integer_to_modelica_string_format(data->simulationInfo->integerParameter[3] /* PV_out_ref.smoothness PARAM */, (modelica_string) mmc_strings_len1[100]);
      tmpMeta[0] = stringAppend(MMC_REFSTRINGLIT(tmp23),tmp24);
      {
        FILE_INFO info = {"/usr/lib/omlibrary/Modelica 3.2.3/Blocks/Tables.mo",320,5,322,61,1};
        omc_assert_warning(info, "The following assertion has been violated %sat time %f\nPV_out_ref.smoothness >= Modelica.Blocks.Types.Smoothness.LinearSegments and PV_out_ref.smoothness <= Modelica.Blocks.Types.Smoothness.MonotoneContinuousDerivative2", initial() ? "during initialization " : "", data->localData[0]->timeValue);
        omc_assert_warning_withEquationIndexes(info, equationIndexes, MMC_STRINGDATA(tmpMeta[0]));
      }
      tmp25 = 1;
    }
  }
  TRACE_POP
}

/*
equation index: 67
type: ALGORITHM

  assert(eff_heater >= 0.0, "Variable violating min constraint: 0.0 <= eff_heater, has value: " + String(eff_heater, "g"));
*/
OMC_DISABLE_OPT
static void PVWindEES_eqFunction_67(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,67};
  modelica_boolean tmp26;
  static const MMC_DEFSTRINGLIT(tmp27,65,"Variable violating min constraint: 0.0 <= eff_heater, has value: ");
  modelica_string tmp28;
  static int tmp29 = 0;
  modelica_metatype tmpMeta[1] __attribute__((unused)) = {0};
  if(!tmp29)
  {
    tmp26 = GreaterEq(data->simulationInfo->realParameter[17] /* eff_heater PARAM */,0.0);
    if(!tmp26)
    {
      tmp28 = modelica_real_to_modelica_string_format(data->simulationInfo->realParameter[17] /* eff_heater PARAM */, (modelica_string) mmc_strings_len1[103]);
      tmpMeta[0] = stringAppend(MMC_REFSTRINGLIT(tmp27),tmp28);
      {
        FILE_INFO info = {"/media/yewang/Data/Work/Research/Topics/yewang/HILTCRC/repo/RenewableTherm/PVWindEES.mo",21,3,21,71,0};
        omc_assert_warning(info, "The following assertion has been violated %sat time %f\neff_heater >= 0.0", initial() ? "during initialization " : "", data->localData[0]->timeValue);
        omc_assert_warning_withEquationIndexes(info, equationIndexes, MMC_STRINGDATA(tmpMeta[0]));
      }
      tmp29 = 1;
    }
  }
  TRACE_POP
}

/*
equation index: 68
type: ALGORITHM

  assert(eff_ST_roundtrip >= 0.0, "Variable violating min constraint: 0.0 <= eff_ST_roundtrip, has value: " + String(eff_ST_roundtrip, "g"));
*/
OMC_DISABLE_OPT
static void PVWindEES_eqFunction_68(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,68};
  modelica_boolean tmp30;
  static const MMC_DEFSTRINGLIT(tmp31,71,"Variable violating min constraint: 0.0 <= eff_ST_roundtrip, has value: ");
  modelica_string tmp32;
  static int tmp33 = 0;
  modelica_metatype tmpMeta[1] __attribute__((unused)) = {0};
  if(!tmp33)
  {
    tmp30 = GreaterEq(data->simulationInfo->realParameter[16] /* eff_ST_roundtrip PARAM */,0.0);
    if(!tmp30)
    {
      tmp32 = modelica_real_to_modelica_string_format(data->simulationInfo->realParameter[16] /* eff_ST_roundtrip PARAM */, (modelica_string) mmc_strings_len1[103]);
      tmpMeta[0] = stringAppend(MMC_REFSTRINGLIT(tmp31),tmp32);
      {
        FILE_INFO info = {"/media/yewang/Data/Work/Research/Topics/yewang/HILTCRC/repo/RenewableTherm/PVWindEES.mo",16,3,16,98,0};
        omc_assert_warning(info, "The following assertion has been violated %sat time %f\neff_ST_roundtrip >= 0.0", initial() ? "during initialization " : "", data->localData[0]->timeValue);
        omc_assert_warning_withEquationIndexes(info, equationIndexes, MMC_STRINGDATA(tmpMeta[0]));
      }
      tmp33 = 1;
    }
  }
  TRACE_POP
}

/*
equation index: 69
type: ALGORITHM

  assert(eff_ST_out >= 0.0, "Variable violating min constraint: 0.0 <= eff_ST_out, has value: " + String(eff_ST_out, "g"));
*/
OMC_DISABLE_OPT
static void PVWindEES_eqFunction_69(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,69};
  modelica_boolean tmp34;
  static const MMC_DEFSTRINGLIT(tmp35,65,"Variable violating min constraint: 0.0 <= eff_ST_out, has value: ");
  modelica_string tmp36;
  static int tmp37 = 0;
  modelica_metatype tmpMeta[1] __attribute__((unused)) = {0};
  if(!tmp37)
  {
    tmp34 = GreaterEq(data->simulationInfo->realParameter[15] /* eff_ST_out PARAM */,0.0);
    if(!tmp34)
    {
      tmp36 = modelica_real_to_modelica_string_format(data->simulationInfo->realParameter[15] /* eff_ST_out PARAM */, (modelica_string) mmc_strings_len1[103]);
      tmpMeta[0] = stringAppend(MMC_REFSTRINGLIT(tmp35),tmp36);
      {
        FILE_INFO info = {"/media/yewang/Data/Work/Research/Topics/yewang/HILTCRC/repo/RenewableTherm/PVWindEES.mo",18,3,18,87,0};
        omc_assert_warning(info, "The following assertion has been violated %sat time %f\neff_ST_out >= 0.0", initial() ? "during initialization " : "", data->localData[0]->timeValue);
        omc_assert_warning_withEquationIndexes(info, equationIndexes, MMC_STRINGDATA(tmpMeta[0]));
      }
      tmp37 = 1;
    }
  }
  TRACE_POP
}

/*
equation index: 70
type: ALGORITHM

  assert(eff_ST_in >= 0.0, "Variable violating min constraint: 0.0 <= eff_ST_in, has value: " + String(eff_ST_in, "g"));
*/
OMC_DISABLE_OPT
static void PVWindEES_eqFunction_70(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  const int equationIndexes[2] = {1,70};
  modelica_boolean tmp38;
  static const MMC_DEFSTRINGLIT(tmp39,64,"Variable violating min constraint: 0.0 <= eff_ST_in, has value: ");
  modelica_string tmp40;
  static int tmp41 = 0;
  modelica_metatype tmpMeta[1] __attribute__((unused)) = {0};
  if(!tmp41)
  {
    tmp38 = GreaterEq(data->simulationInfo->realParameter[14] /* eff_ST_in PARAM */,0.0);
    if(!tmp38)
    {
      tmp40 = modelica_real_to_modelica_string_format(data->simulationInfo->realParameter[14] /* eff_ST_in PARAM */, (modelica_string) mmc_strings_len1[103]);
      tmpMeta[0] = stringAppend(MMC_REFSTRINGLIT(tmp39),tmp40);
      {
        FILE_INFO info = {"/media/yewang/Data/Work/Research/Topics/yewang/HILTCRC/repo/RenewableTherm/PVWindEES.mo",17,3,17,83,0};
        omc_assert_warning(info, "The following assertion has been violated %sat time %f\neff_ST_in >= 0.0", initial() ? "during initialization " : "", data->localData[0]->timeValue);
        omc_assert_warning_withEquationIndexes(info, equationIndexes, MMC_STRINGDATA(tmpMeta[0]));
      }
      tmp41 = 1;
    }
  }
  TRACE_POP
}
OMC_DISABLE_OPT
void PVWindEES_updateBoundParameters_0(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  PVWindEES_eqFunction_41(data, threadData);
  PVWindEES_eqFunction_42(data, threadData);
  PVWindEES_eqFunction_43(data, threadData);
  PVWindEES_eqFunction_44(data, threadData);
  PVWindEES_eqFunction_45(data, threadData);
  PVWindEES_eqFunction_46(data, threadData);
  PVWindEES_eqFunction_51(data, threadData);
  PVWindEES_eqFunction_52(data, threadData);
  PVWindEES_eqFunction_57(data, threadData);
  PVWindEES_eqFunction_58(data, threadData);
  PVWindEES_eqFunction_59(data, threadData);
  PVWindEES_eqFunction_60(data, threadData);
  PVWindEES_eqFunction_61(data, threadData);
  PVWindEES_eqFunction_62(data, threadData);
  PVWindEES_eqFunction_63(data, threadData);
  PVWindEES_eqFunction_64(data, threadData);
  PVWindEES_eqFunction_65(data, threadData);
  PVWindEES_eqFunction_66(data, threadData);
  PVWindEES_eqFunction_67(data, threadData);
  PVWindEES_eqFunction_68(data, threadData);
  PVWindEES_eqFunction_69(data, threadData);
  PVWindEES_eqFunction_70(data, threadData);
  TRACE_POP
}
OMC_DISABLE_OPT
int PVWindEES_updateBoundParameters(DATA *data, threadData_t *threadData)
{
  TRACE_PUSH
  data->simulationInfo->integerParameter[2] /* PV_out_ref.nout PARAM */ = ((modelica_integer) 1);
  data->modelData->integerParameterData[2].time_unvarying = 1;
  data->simulationInfo->integerParameter[6] /* Wind_out_ref.nout PARAM */ = ((modelica_integer) 1);
  data->modelData->integerParameterData[6].time_unvarying = 1;
  data->simulationInfo->booleanParameter[0] /* PV_out_ref.tableOnFile PARAM */ = 1;
  data->modelData->booleanParameterData[0].time_unvarying = 1;
  data->simulationInfo->booleanParameter[1] /* PV_out_ref.verboseExtrapolation PARAM */ = 0;
  data->modelData->booleanParameterData[1].time_unvarying = 1;
  data->simulationInfo->booleanParameter[3] /* Wind_out_ref.tableOnFile PARAM */ = 1;
  data->modelData->booleanParameterData[3].time_unvarying = 1;
  data->simulationInfo->booleanParameter[4] /* Wind_out_ref.verboseExtrapolation PARAM */ = 0;
  data->modelData->booleanParameterData[4].time_unvarying = 1;
  data->simulationInfo->integerParameter[3] /* PV_out_ref.smoothness PARAM */ = 1;
  data->modelData->integerParameterData[3].time_unvarying = 1;
  data->simulationInfo->integerParameter[7] /* Wind_out_ref.smoothness PARAM */ = 1;
  data->modelData->integerParameterData[7].time_unvarying = 1;
  PVWindEES_updateBoundParameters_0(data, threadData);
  TRACE_POP
  return 0;
}

#if defined(__cplusplus)
}
#endif

