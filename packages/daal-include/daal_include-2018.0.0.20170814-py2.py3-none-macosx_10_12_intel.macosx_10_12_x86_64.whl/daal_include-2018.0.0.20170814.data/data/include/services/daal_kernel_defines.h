/* file: daal_kernel_defines.h */
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
//  Common definitions.
//--
*/

#ifndef __DAAL_KERNEL_DEFINES_H__
#define __DAAL_KERNEL_DEFINES_H__

/** \file daal_kernel_defines.h */
/**
 * @ingroup services
 * @{
 */
#define DAAL_KERNELS_ALL

#ifdef DAAL_KERNELS_ALL
#define DAAL_KERNEL_SSSE3
#define DAAL_KERNEL_SSE42
#define DAAL_KERNEL_AVX
#define DAAL_KERNEL_AVX2
#define DAAL_KERNEL_AVX512_mic
#define DAAL_KERNEL_AVX512
#endif

#define DAAL_KERNEL_CONTAINER_TEMPL(ContainerTemplate, cpuType, ...) ContainerTemplate<__VA_ARGS__, cpuType>
#define DAAL_KERNEL_CONTAINER_CASE(ContainerTemplate, cpuType,...)\
    case cpuType: _cntr = (new DAAL_KERNEL_CONTAINER_TEMPL(ContainerTemplate, cpuType, __VA_ARGS__)(daalEnv)); break;

#ifdef DAAL_KERNEL_SSSE3
#define DAAL_KERNEL_SSSE3_ONLY(something) , something
#define DAAL_KERNEL_SSSE3_ONLY_CODE(...) __VA_ARGS__
#define DAAL_KERNEL_SSSE3_CONTAINER(ContainerTemplate, ...) , DAAL_KERNEL_CONTAINER_TEMPL(ContainerTemplate, ssse3, __VA_ARGS__)
#define DAAL_KERNEL_SSSE3_CONTAINER_CASE(ContainerTemplate, ...) DAAL_KERNEL_CONTAINER_CASE(ContainerTemplate, ssse3, __VA_ARGS__)
#else
#define DAAL_KERNEL_SSSE3_ONLY(something)
#define DAAL_KERNEL_SSSE3_ONLY_CODE(...)
#define DAAL_KERNEL_SSSE3_CONTAINER(ContainerTemplate, ...)
#define DAAL_KERNEL_SSSE3_CONTAINER_CASE(ContainerTemplate, ...)
#endif

#ifdef DAAL_KERNEL_SSE42
#define DAAL_KERNEL_SSE42_ONLY(something) , something
#define DAAL_KERNEL_SSE42_ONLY_CODE(...) __VA_ARGS__
#define DAAL_KERNEL_SSE42_CONTAINER(ContainerTemplate, ...) , DAAL_KERNEL_CONTAINER_TEMPL(ContainerTemplate, sse42, __VA_ARGS__)
#define DAAL_KERNEL_SSE42_CONTAINER_CASE(ContainerTemplate, ...) DAAL_KERNEL_CONTAINER_CASE(ContainerTemplate, sse42, __VA_ARGS__)
#else
#define DAAL_KERNEL_SSE42_ONLY(something)
#define DAAL_KERNEL_SSE42_ONLY_CODE(...)
#define DAAL_KERNEL_SSE42_CONTAINER(ContainerTemplate, ...)
#define DAAL_KERNEL_SSE42_CONTAINER_CASE(ContainerTemplate, ...)
#endif

#ifdef DAAL_KERNEL_AVX
#define DAAL_KERNEL_AVX_ONLY(something) , something
#define DAAL_KERNEL_AVX_ONLY_CODE(...) __VA_ARGS__
#define DAAL_KERNEL_AVX_CONTAINER(ContainerTemplate, ...) , DAAL_KERNEL_CONTAINER_TEMPL(ContainerTemplate, avx, __VA_ARGS__)
#define DAAL_KERNEL_AVX_CONTAINER_CASE(ContainerTemplate, ...) DAAL_KERNEL_CONTAINER_CASE(ContainerTemplate, avx, __VA_ARGS__)
#else
#define DAAL_KERNEL_AVX_ONLY(something)
#define DAAL_KERNEL_AVX_ONLY_CODE(...)
#define DAAL_KERNEL_AVX_CONTAINER(ContainerTemplate, ...)
#define DAAL_KERNEL_AVX_CONTAINER_CASE(ContainerTemplate, ...)
#endif

#ifdef DAAL_KERNEL_AVX2
#define DAAL_KERNEL_AVX2_ONLY(something) , something
#define DAAL_KERNEL_AVX2_ONLY_CODE(...) __VA_ARGS__
#define DAAL_KERNEL_AVX2_CONTAINER(ContainerTemplate, ...) , DAAL_KERNEL_CONTAINER_TEMPL(ContainerTemplate, avx2, __VA_ARGS__)
#define DAAL_KERNEL_AVX2_CONTAINER_CASE(ContainerTemplate, ...) DAAL_KERNEL_CONTAINER_CASE(ContainerTemplate, avx2, __VA_ARGS__)
#else
#define DAAL_KERNEL_AVX2_ONLY(something)
#define DAAL_KERNEL_AVX2_ONLY_CODE(...)
#define DAAL_KERNEL_AVX2_CONTAINER(ContainerTemplate, ...)
#define DAAL_KERNEL_AVX2_CONTAINER_CASE(ContainerTemplate, ...)
#endif

#ifdef DAAL_KERNEL_AVX512_mic
#define DAAL_KERNEL_AVX512_mic_ONLY(something) , something
#define DAAL_KERNEL_AVX512_mic_ONLY_CODE(...) __VA_ARGS__
#define DAAL_KERNEL_AVX512_mic_CONTAINER(ContainerTemplate, ...) , DAAL_KERNEL_CONTAINER_TEMPL(ContainerTemplate, avx512_mic, __VA_ARGS__)
#define DAAL_KERNEL_AVX512_mic_CONTAINER_CASE(ContainerTemplate, ...) DAAL_KERNEL_CONTAINER_CASE(ContainerTemplate, avx512_mic, __VA_ARGS__)
#else
#define DAAL_KERNEL_AVX512_mic_ONLY(something)
#define DAAL_KERNEL_AVX512_mic_ONLY_CODE(...)
#define DAAL_KERNEL_AVX512_mic_CONTAINER(ContainerTemplate, ...)
#define DAAL_KERNEL_AVX512_mic_CONTAINER_CASE(ContainerTemplate, ...)
#endif

#ifdef DAAL_KERNEL_AVX512
#define DAAL_KERNEL_AVX512_ONLY(something) , something
#define DAAL_KERNEL_AVX512_ONLY_CODE(...) __VA_ARGS__
#define DAAL_KERNEL_AVX512_CONTAINER(ContainerTemplate, ...) , DAAL_KERNEL_CONTAINER_TEMPL(ContainerTemplate, avx512, __VA_ARGS__)
#define DAAL_KERNEL_AVX512_CONTAINER_CASE(ContainerTemplate, ...) DAAL_KERNEL_CONTAINER_CASE(ContainerTemplate, avx512, __VA_ARGS__)
#else
#define DAAL_KERNEL_AVX512_ONLY(something)
#define DAAL_KERNEL_AVX512_ONLY_CODE(...)
#define DAAL_KERNEL_AVX512_CONTAINER(ContainerTemplate, ...)
#define DAAL_KERNEL_AVX512_CONTAINER_CASE(ContainerTemplate, ...)
#endif
/** @} */

#endif
