#include "omc_simulation_settings.h"
#include "PVWindEES_functions.h"
#ifdef __cplusplus
extern "C" {
#endif

#include "PVWindEES_includes.h"


modelica_real omc_Modelica_Blocks_Tables_Internal_getTable1DAbscissaUmax(threadData_t *threadData, modelica_complex _tableID)
{
  void * _tableID_ext;
  double _uMax_ext;
  modelica_real _uMax;
  // _uMax has no default value.
  _tableID_ext = (void *)_tableID;
  _uMax_ext = ModelicaStandardTables_CombiTable1D_maximumAbscissa(_tableID_ext);
  _uMax = (modelica_real)_uMax_ext;
  return _uMax;
}
modelica_metatype boxptr_Modelica_Blocks_Tables_Internal_getTable1DAbscissaUmax(threadData_t *threadData, modelica_metatype _tableID)
{
  modelica_real _uMax;
  modelica_metatype out_uMax;
  _uMax = omc_Modelica_Blocks_Tables_Internal_getTable1DAbscissaUmax(threadData, _tableID);
  out_uMax = mmc_mk_rcon(_uMax);
  return out_uMax;
}

modelica_real omc_Modelica_Blocks_Tables_Internal_getTable1DAbscissaUmin(threadData_t *threadData, modelica_complex _tableID)
{
  void * _tableID_ext;
  double _uMin_ext;
  modelica_real _uMin;
  // _uMin has no default value.
  _tableID_ext = (void *)_tableID;
  _uMin_ext = ModelicaStandardTables_CombiTable1D_minimumAbscissa(_tableID_ext);
  _uMin = (modelica_real)_uMin_ext;
  return _uMin;
}
modelica_metatype boxptr_Modelica_Blocks_Tables_Internal_getTable1DAbscissaUmin(threadData_t *threadData, modelica_metatype _tableID)
{
  modelica_real _uMin;
  modelica_metatype out_uMin;
  _uMin = omc_Modelica_Blocks_Tables_Internal_getTable1DAbscissaUmin(threadData, _tableID);
  out_uMin = mmc_mk_rcon(_uMin);
  return out_uMin;
}

modelica_real omc_Modelica_Blocks_Tables_Internal_getTable1DValue(threadData_t *threadData, modelica_complex _tableID, modelica_integer _icol, modelica_real _u)
{
  void * _tableID_ext;
  int _icol_ext;
  double _u_ext;
  double _y_ext;
  modelica_real _y;
  // _y has no default value.
  _tableID_ext = (void *)_tableID;

  _icol_ext = (int)_icol;

  _u_ext = (double)_u;
  _y_ext = ModelicaStandardTables_CombiTable1D_getValue(_tableID_ext, _icol_ext, _u_ext);
  _y = (modelica_real)_y_ext;
  return _y;
}
modelica_metatype boxptr_Modelica_Blocks_Tables_Internal_getTable1DValue(threadData_t *threadData, modelica_metatype _tableID, modelica_metatype _icol, modelica_metatype _u)
{
  modelica_integer tmp1;
  modelica_real tmp2;
  modelica_real _y;
  modelica_metatype out_y;
  tmp1 = mmc_unbox_integer(_icol);
  tmp2 = mmc_unbox_real(_u);
  _y = omc_Modelica_Blocks_Tables_Internal_getTable1DValue(threadData, _tableID, tmp1, tmp2);
  out_y = mmc_mk_rcon(_y);
  return out_y;
}

modelica_complex omc_Modelica_Blocks_Types_ExternalCombiTable1D_constructor(threadData_t *threadData, modelica_string _tableName, modelica_string _fileName, real_array _table, integer_array _columns, modelica_integer _smoothness, modelica_integer _extrapolation, modelica_boolean _verboseRead)
{
  integer_array _columns_packed;
  int _smoothness_ext;
  int _extrapolation_ext;
  int _verboseRead_ext;
  void *_table_c89;
  void *_columns_c89;
  void * _externalCombiTable1D_ext;
  modelica_complex _externalCombiTable1D;
  // _externalCombiTable1D has no default value.
  pack_alloc_integer_array(&_columns, &_columns_packed);

  _smoothness_ext = (int)_smoothness;

  _extrapolation_ext = (int)_extrapolation;

  _verboseRead_ext = (int)_verboseRead;
  _table_c89 = (void*) data_of_real_c89_array(&(_table));
  _columns_c89 = (void*) data_of_integer_c89_array(&(_columns_packed));
  _externalCombiTable1D_ext = ModelicaStandardTables_CombiTable1D_init2(MMC_STRINGDATA(_fileName), MMC_STRINGDATA(_tableName), (const double*) _table_c89, size_of_dimension_base_array(_table, ((modelica_integer) 1)), size_of_dimension_base_array(_table, ((modelica_integer) 2)), (const int*) _columns_c89, size_of_dimension_base_array(_columns, ((modelica_integer) 1)), _smoothness_ext, _extrapolation_ext, _verboseRead_ext);
  _externalCombiTable1D = (modelica_complex)_externalCombiTable1D_ext;
  return _externalCombiTable1D;
}
modelica_metatype boxptr_Modelica_Blocks_Types_ExternalCombiTable1D_constructor(threadData_t *threadData, modelica_metatype _tableName, modelica_metatype _fileName, modelica_metatype _table, modelica_metatype _columns, modelica_metatype _smoothness, modelica_metatype _extrapolation, modelica_metatype _verboseRead)
{
  modelica_integer tmp1;
  modelica_integer tmp2;
  modelica_integer tmp3;
  modelica_complex _externalCombiTable1D;
  tmp1 = mmc_unbox_integer(_smoothness);
  tmp2 = mmc_unbox_integer(_extrapolation);
  tmp3 = mmc_unbox_integer(_verboseRead);
  _externalCombiTable1D = omc_Modelica_Blocks_Types_ExternalCombiTable1D_constructor(threadData, _tableName, _fileName, *((base_array_t*)_table), *((base_array_t*)_columns), tmp1, tmp2, tmp3);
  /* skip box _externalCombiTable1D; ExternalObject Modelica.Blocks.Types.ExternalCombiTable1D */
  return _externalCombiTable1D;
}

void omc_Modelica_Blocks_Types_ExternalCombiTable1D_destructor(threadData_t *threadData, modelica_complex _externalCombiTable1D)
{
  void * _externalCombiTable1D_ext;
  _externalCombiTable1D_ext = (void *)_externalCombiTable1D;
  ModelicaStandardTables_CombiTable1D_close(_externalCombiTable1D_ext);
  return;
}
void boxptr_Modelica_Blocks_Types_ExternalCombiTable1D_destructor(threadData_t *threadData, modelica_metatype _externalCombiTable1D)
{
  omc_Modelica_Blocks_Types_ExternalCombiTable1D_destructor(threadData, _externalCombiTable1D);
  return;
}

DLLExport
modelica_boolean omc_Modelica_Utilities_Strings_isEmpty(threadData_t *threadData, modelica_string _string)
{
  modelica_boolean _result;
  modelica_integer _nextIndex;
  modelica_integer _len;
  _tailrecursive: OMC_LABEL_UNUSED
  // _result has no default value.
  // _nextIndex has no default value.
  // _len has no default value.
  _nextIndex = omc_Modelica_Utilities_Strings_Advanced_skipWhiteSpace(threadData, _string, ((modelica_integer) 1));

  _len = omc_Modelica_Utilities_Strings_length(threadData, _string);

  if(((_len < ((modelica_integer) 1)) || (_nextIndex > _len)))
  {
    _result = 1;
  }
  else
  {
    _result = 0;
  }
  _return: OMC_LABEL_UNUSED
  return _result;
}
modelica_metatype boxptr_Modelica_Utilities_Strings_isEmpty(threadData_t *threadData, modelica_metatype _string)
{
  modelica_boolean _result;
  modelica_metatype out_result;
  _result = omc_Modelica_Utilities_Strings_isEmpty(threadData, _string);
  out_result = mmc_mk_icon(_result);
  return out_result;
}

modelica_integer omc_Modelica_Utilities_Strings_length(threadData_t *threadData, modelica_string _string)
{
  int _result_ext;
  modelica_integer _result;
  // _result has no default value.
  _result_ext = ModelicaStrings_length(MMC_STRINGDATA(_string));
  _result = (modelica_integer)_result_ext;
  return _result;
}
modelica_metatype boxptr_Modelica_Utilities_Strings_length(threadData_t *threadData, modelica_metatype _string)
{
  modelica_integer _result;
  modelica_metatype out_result;
  _result = omc_Modelica_Utilities_Strings_length(threadData, _string);
  out_result = mmc_mk_icon(_result);
  return out_result;
}

modelica_integer omc_Modelica_Utilities_Strings_Advanced_skipWhiteSpace(threadData_t *threadData, modelica_string _string, modelica_integer _startIndex)
{
  int _startIndex_ext;
  int _nextIndex_ext;
  modelica_integer _nextIndex;
  // _nextIndex has no default value.
  _startIndex_ext = (int)_startIndex;
  _nextIndex_ext = ModelicaStrings_skipWhiteSpace(MMC_STRINGDATA(_string), _startIndex_ext);
  _nextIndex = (modelica_integer)_nextIndex_ext;
  return _nextIndex;
}
modelica_metatype boxptr_Modelica_Utilities_Strings_Advanced_skipWhiteSpace(threadData_t *threadData, modelica_metatype _string, modelica_metatype _startIndex)
{
  modelica_integer tmp1;
  modelica_integer _nextIndex;
  modelica_metatype out_nextIndex;
  tmp1 = mmc_unbox_integer(_startIndex);
  _nextIndex = omc_Modelica_Utilities_Strings_Advanced_skipWhiteSpace(threadData, _string, tmp1);
  out_nextIndex = mmc_mk_icon(_nextIndex);
  return out_nextIndex;
}

#ifdef __cplusplus
}
#endif
