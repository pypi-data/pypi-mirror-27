/* file: env_detect.h */
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
//  Implementation of the class used for environment detection.
//--
*/

#ifndef __ENV_DETECT_H__
#define __ENV_DETECT_H__

#include "services/base.h"
#include "services/daal_defines.h"

namespace daal
{
/**
 * @defgroup env_detect Managing the Computational Environment
 * \brief Provides methods to interact with the environment, including processor detection and control by the number of threads.
 * @ingroup services
 * @{
 */
/**
 * <a name="DAAL-ENUM-CPUTYPE"></a>
 * Supported types of processor architectures
 */
enum CpuType
{
    sse2          = 0,  /*!< Intel(R) Streaming SIMD Extensions 2 (Intel(R) SSE2) */
    ssse3         = 1,  /*!< Supplemental Streaming SIMD Extensions 3 (SSSE3) */
    sse42         = 2,  /*!< Intel(R) Streaming SIMD Extensions 4.2 (Intel(R) SSE4.2) */
    avx           = 3,  /*!< Intel(R) Advanced Vector Extensions (Intel(R) AVX) */
    avx2          = 4,  /*!< Intel(R) Advanced Vector Extensions 2 (Intel(R) AVX2) */
    avx512_mic    = 5,  /*!< Intel(R) Xeon Phi(TM) processors/coprocessors based on Intel(R) Advanced Vector Extensions 512 (Intel(R) AVX-512) */
    avx512        = 6,  /*!< Intel(R) Xeon(R) processors based on Intel(R) Advanced Vector Extensions 512 (Intel(R) AVX-512) */
    avx512_mic_e1 = 7,  /*!< Intel(R) Xeon Phi(TM) processors based on Intel(R) Advanced Vector Extensions 512 (Intel(R) AVX-512) with support of AVX512_4FMAPS and AVX512_4VNNIW instruction groups. Should be used as parameter for setCpuId function only. Can`t be received as return value of setCpuId, setCpuId and enableInstructionsSet functions. */
    lastCpuType = avx512_mic_e1
};

namespace services
{
namespace interface1
{

/**
 * <a name="DAAL-CLASS-SERVICES__ENVIRONMENT"></a>
 * \brief Class that provides methods to interact with the environment, including processor detection and control by the number of threads
 */
class DAAL_EXPORT Environment : public Base
{
public:
    /**
    * <a name="DAAL-CLASS-_ENVSTRUCT"></a>
    * \brief The environment structure
    */
    typedef struct _envStruct
    {
        bool cpuid_init_flag;
        size_t cpuid;
    } env;

    /**
     *  Returns the environment instance
     *  \return The environment instance
     */
    static Environment *getInstance();

    /**
     *  Decreases the instance counter
     *  \return The return code
     *  \DAAL_DEPRECATED
     */
    DAAL_DEPRECATED static int freeInstance();

    /**
     * <a name="DAAL-ENUM-SERVICES__CPUTYPEENABLE"></a>
     * \brief CPU types
     */
    enum CpuTypeEnable
    {
        cpu_default = 0,    /*!< Default processor type */
        avx512_mic = 1,     /*!< Intel(R) Xeon Phi(TM) processors/coprocessors based on Intel(R) Advanced Vector Extensions 512 (Intel(R) AVX-512) \DAAL_DEPRECATED */
        avx512 = 2,         /*!< Intel(R) Xeon(R) processors based on Intel(R) Advanced Vector Extensions 512 (Intel(R) AVX-512) \DAAL_DEPRECATED */
        avx512_mic_e1 = 4   /*!< Intel(R) Xeon Phi(TM) processors based on Intel(R) Advanced Vector Extensions 512 (Intel(R) AVX-512) with support of AVX512_4FMAPS and AVX512_4VNNIW instruction groups */
    };

    /**
    *  Detects the processor type
    *  \param[in] enable  An enabling flag \DAAL_DEPRECATED
    *  \return The CPU ID
    */
    int getCpuId(int enable = cpu_default);

    /**
    *  Restrict dispatching to the required code path
    *  \param[in] cpuid  CPU ID
    *  \return  CPU ID if success; -1 if error
    */
    int setCpuId(int cpuid);

    /**
    *  Enable dispatching for new Intel(R) architectures
    *  \param[in] enable  An enabling flag
    *  \return  CPU ID
    */
    int enableInstructionsSet(int enable);

    /**
     * <a name="DAAL-ENUM-SERVICES__LIBRARYTHREADINGTYPE"></a>
     * The threading mode of the library
     */
    enum LibraryThreadingType
    {
        MultiThreaded = 0,  /*!< Multi-threaded mode */
        SingleThreaded = 1  /*!< Single-threaded mode */
    };

    /**
    *  Sets the threading mode on Windows*
    *  \param[in] type  The threading mode of the library
    */
    void setDynamicLibraryThreadingTypeOnWindows( LibraryThreadingType type );

    /**
    *  Sets the number of threads to use
    *  \param[in] numThreads   The number of threads
    */
    void setNumberOfThreads(const size_t numThreads);

    /**
    *  Enables thread pinning
    *  \param[in] enableThreadPinningFlag   Flag to thread pinning enable
    */
    void enableThreadPinning( bool enableThreadPinningFlag = true);

    /**
    *  Returns the number of used threads
    *  \return The number of used threads
    */
    size_t getNumberOfThreads() const;

    /**
     * Limits the amount of memory of the given type available to internal function calls
     * \param[in] type   Memory type
     * \param[in] limit  Limit in megabytes
     */
    int setMemoryLimit(MemType type, size_t limit);

private:
    Environment();
    Environment(const Environment &e);
    ~Environment();

    void _cpu_detect(int);

    env _env;

    void *_init;
};
} // namespace interface1

using interface1::Environment;

}
/** @} */
}
#endif
