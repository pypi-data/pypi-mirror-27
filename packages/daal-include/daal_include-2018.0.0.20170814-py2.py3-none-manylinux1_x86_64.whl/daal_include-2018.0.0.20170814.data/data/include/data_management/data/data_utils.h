/* file: data_utils.h */
/*******************************************************************************
* Copyright 2014-2017 Intel Corporation
* All Rights Reserved.
*
* If this  software was obtained  under the  Intel Simplified  Software License,
* the following terms apply:
*
* The source code,  information  and material  ("Material") contained  herein is
* owned by Intel Corporation or its  suppliers or licensors,  and  title to such
* Material remains with Intel  Corporation or its  suppliers or  licensors.  The
* Material  contains  proprietary  information  of  Intel or  its suppliers  and
* licensors.  The Material is protected by  worldwide copyright  laws and treaty
* provisions.  No part  of  the  Material   may  be  used,  copied,  reproduced,
* modified, published,  uploaded, posted, transmitted,  distributed or disclosed
* in any way without Intel's prior express written permission.  No license under
* any patent,  copyright or other  intellectual property rights  in the Material
* is granted to  or  conferred  upon  you,  either   expressly,  by implication,
* inducement,  estoppel  or  otherwise.  Any  license   under such  intellectual
* property rights must be express and approved by Intel in writing.
*
* Unless otherwise agreed by Intel in writing,  you may not remove or alter this
* notice or  any  other  notice   embedded  in  Materials  by  Intel  or Intel's
* suppliers or licensors in any way.
*
*
* If this  software  was obtained  under the  Apache License,  Version  2.0 (the
* "License"), the following terms apply:
*
* You may  not use this  file except  in compliance  with  the License.  You may
* obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
*
*
* Unless  required  by   applicable  law  or  agreed  to  in  writing,  software
* distributed under the License  is distributed  on an  "AS IS"  BASIS,  WITHOUT
* WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
*
* See the   License  for the   specific  language   governing   permissions  and
* limitations under the License.
*******************************************************************************/

/*
//++
//  Implementation of data dictionary utilities.
//--
*/

#ifndef __DATA_UTILS_H__
#define __DATA_UTILS_H__

#include <string>
#include <climits>
#include <cfloat>
#include "services/daal_defines.h"

namespace daal
{
namespace data_management
{
/**
 * \brief Contains classes for Intel(R) Data Analytics Acceleration Library numeric types
 */
namespace data_feature_utils
{
/**
 * @ingroup data_model
 * @{
 */
enum IndexNumType
{
    DAAL_FLOAT32 = 0,
    DAAL_FLOAT64 = 1,
    DAAL_INT32_S = 2,
    DAAL_INT32_U = 3,
    DAAL_INT64_S = 4,
    DAAL_INT64_U = 5,
    DAAL_INT8_S  = 6,
    DAAL_INT8_U  = 7,
    DAAL_INT16_S = 8,
    DAAL_INT16_U = 9,
    DAAL_OTHER_T = 10
};
const int NumOfIndexNumTypes = (int)DAAL_OTHER_T;

enum InternalNumType  { DAAL_SINGLE = 0, DAAL_DOUBLE = 1, DAAL_INT32 = 2, DAAL_OTHER = 0xfffffff };
enum PMMLNumType      { DAAL_GEN_FLOAT = 0, DAAL_GEN_DOUBLE = 1, DAAL_GEN_INTEGER = 2, DAAL_GEN_BOOLEAN = 3,
                        DAAL_GEN_STRING = 4, DAAL_GEN_UNKNOWN = 0xfffffff
                      };
enum FeatureType      { DAAL_CATEGORICAL = 0, DAAL_ORDINAL = 1, DAAL_CONTINUOUS = 2 };

/**
 * Convert from a given C++ type to InternalNumType
 * \return Converted numeric type
 */
template<typename T> inline IndexNumType getIndexNumType() { return DAAL_OTHER_T; }
template<> inline IndexNumType getIndexNumType<float>()            { return DAAL_FLOAT32; }
template<> inline IndexNumType getIndexNumType<double>()           { return DAAL_FLOAT64; }
template<> inline IndexNumType getIndexNumType<int>()              { return DAAL_INT32_S; }
template<> inline IndexNumType getIndexNumType<unsigned int>()     { return DAAL_INT32_U; }
template<> inline IndexNumType getIndexNumType<DAAL_INT64>()       { return DAAL_INT64_S; }
template<> inline IndexNumType getIndexNumType<DAAL_UINT64>()      { return DAAL_INT64_U; }
template<> inline IndexNumType getIndexNumType<char>()             { return DAAL_INT8_S;  }
template<> inline IndexNumType getIndexNumType<unsigned char>()    { return DAAL_INT8_U;  }
template<> inline IndexNumType getIndexNumType<short>()            { return DAAL_INT16_S; }
template<> inline IndexNumType getIndexNumType<unsigned short>()   { return DAAL_INT16_U; }

template<> inline IndexNumType getIndexNumType<long>()
{ return (IndexNumType)(DAAL_INT32_S + (sizeof(long) / 4 - 1) * 2); }

#if (defined(__APPLE__) || defined(__MACH__)) && !defined(__x86_64__)
template<> inline IndexNumType getIndexNumType<unsigned long>()
{ return (IndexNumType)(DAAL_INT32_U + (sizeof(unsigned long) / 4 - 1) * 2); }
#endif

#if !(defined(_WIN32) || defined(_WIN64)) && defined(__x86_64__)
template<> inline IndexNumType getIndexNumType<size_t>()
{ return (IndexNumType)(DAAL_INT32_U + (sizeof(size_t) / 4 - 1) * 2); }
#endif

/**
 * \return Internal numeric type
 */
template<typename T>
inline InternalNumType getInternalNumType()          { return DAAL_OTHER;  }
template<>
inline InternalNumType getInternalNumType<int>()     { return DAAL_INT32;  }
template<>
inline InternalNumType getInternalNumType<double>()  { return DAAL_DOUBLE; }
template<>
inline InternalNumType getInternalNumType<float>()   { return DAAL_SINGLE; }

/**
 * \return PMMLNumType
 */
template<typename T>
inline PMMLNumType getPMMLNumType()                { return DAAL_GEN_UNKNOWN; }
template<>
inline PMMLNumType getPMMLNumType<int>()           { return DAAL_GEN_INTEGER; }
template<>
inline PMMLNumType getPMMLNumType<double>()        { return DAAL_GEN_DOUBLE;  }
template<>
inline PMMLNumType getPMMLNumType<float>()         { return DAAL_GEN_FLOAT;   }
template<>
inline PMMLNumType getPMMLNumType<bool>()          { return DAAL_GEN_BOOLEAN; }
template<>
inline PMMLNumType getPMMLNumType<char *>()         { return DAAL_GEN_STRING;  }
template<>
inline PMMLNumType getPMMLNumType<std::string>()   { return DAAL_GEN_STRING;  }

/**
 * \return The maximum value of type T
 */
template<typename T>
inline T      getMaxVal()          { return 0;  }
template<>
inline int    getMaxVal<int>()     { return INT_MAX; }
template<>
inline double getMaxVal<double>()  { return DBL_MAX; }
template<>
inline float  getMaxVal<float>()   { return FLT_MAX; }

/**
 * \return The minimum positive value of type T
 */
template<typename T>
inline T      getMinVal()          { return 0;  }
template<>
inline int    getMinVal<int>()     { return INT_MIN; }
template<>
inline double getMinVal<double>()  { return DBL_MIN; }
template<>
inline float  getMinVal<float>()   { return FLT_MIN; }

/**
 * \return The difference between 1.0 and the next value of type T
 */
template<typename T>
inline T      getEpsilonVal()          { return 0;  }
template<>
inline double getEpsilonVal<double>()  { return DBL_EPSILON; }
template<>
inline float  getEpsilonVal<float>()   { return FLT_EPSILON; }

typedef void(*vectorConvertFuncType)(size_t n, void *src, void *dst);
typedef void(*vectorStrideConvertFuncType)(size_t n, void *src, size_t srcByteStride, void *dst, size_t dstByteStride);

DAAL_EXPORT data_feature_utils::vectorConvertFuncType getVectorUpCast(int, int);
DAAL_EXPORT data_feature_utils::vectorConvertFuncType getVectorDownCast(int, int);

DAAL_EXPORT data_feature_utils::vectorStrideConvertFuncType getVectorStrideUpCast(int, int);
DAAL_EXPORT data_feature_utils::vectorStrideConvertFuncType getVectorStrideDownCast(int, int);

/** @} */

} // namespace data_feature_utils
#define DataFeatureUtils data_feature_utils
}
} // namespace daal
#endif
