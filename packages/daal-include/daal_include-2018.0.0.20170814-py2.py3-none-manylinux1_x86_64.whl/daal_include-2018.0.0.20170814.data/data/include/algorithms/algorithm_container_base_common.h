/* file: algorithm_container_base_common.h */
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
//  Implementation of base classes defining algorithm interface.
//--
*/

#ifndef __ALGORITHM_CONTAINER_BASE_COMMON_H__
#define __ALGORITHM_CONTAINER_BASE_COMMON_H__

#include "services/daal_memory.h"
#include "services/daal_kernel_defines.h"
#include "services/error_handling.h"
#include "services/env_detect.h"
#include "algorithms/algorithm_types.h"
#include "algorithms/algorithm_kernel.h"

namespace daal
{
namespace algorithms
{

/**
 * @addtogroup base_algorithms
 * @{
 */
/**
* \brief Contains version 1.0 of Intel(R) Data Analytics Acceleration Library (Intel(R) DAAL) interface.
*/
namespace interface1
{

/**
 * <a name="DAAL-CLASS-ALGORITHMS__ALGORITHMCONTAINERIFACE"></a>
 * \brief Implements the abstract interface AlgorithmContainerIface. It is associated with the Algorithm class
 *        and supports the methods for computation and finalization of the algorithm results
 *        in the batch, distributed, and online modes.
 */
class AlgorithmContainerIface
{
public:
    DAAL_NEW_DELETE();

    virtual ~AlgorithmContainerIface() {}
};

/**
 * <a name="ALGORITHMS__ALGORITHMCONTAINERIFACEIMPL"></a>
 * \brief Implements the abstract interface AlgorithmContainerIfaceImpl. It is associated with the Algorithm class
 *        and supports the methods for computation and finalization of the algorithm results
 *        in the batch, distributed, and online modes.
 */
class AlgorithmContainerIfaceImpl : public AlgorithmContainerIface
{
public:
    /**
     * Default constructor
     * \param[in] daalEnv   Pointer to the structure that contains information about the environment
     */
    AlgorithmContainerIfaceImpl(daal::services::Environment::env *daalEnv) : _env(daalEnv), _errors(new services::ErrorCollection()), _kernel(NULL) {}

    virtual ~AlgorithmContainerIfaceImpl() {}

    /**
     * Sets the information about the environment
     * \param[in] daalEnv   Pointer to the structure that contains information about the environment
     */
    void setEnvironment(daal::services::Environment::env *daalEnv)
    {
        _env = daalEnv;
    }

    /**
     * Sets the collection of errors
     * \param[in] errors    Pointer to the collection of errors
     * \DAAL_DEPRECATED
     */
    void setErrorCollection(const services::ErrorCollectionPtr& errors)
    {
        _errors = errors;
        setKernelErrorCollection();
    }

    /**
     * Sets the collection of errors to kernels
     * \DAAL_DEPRECATED
     */
    void setKernelErrorCollection()
    {
        if(_kernel)
            _kernel->setErrorCollection(_errors->getErrors());
    }

protected:
    daal::services::Environment::env     *_env;
    services::ErrorCollectionPtr        _errors;

    Kernel *_kernel;
};

/**
 * <a name="DAAL-CLASS-ALGORITHMS__ALGORITHMCONTAINER"></a>
 * \brief Abstract interface class that provides virtual methods to access and run implementations
 *        of the algorithms. It is associated with the Algorithm class
 *        and supports the methods for computation and finalization of the algorithm results
 *        in the batch, distributed, and online modes.
 *        The methods of the container are defined in derivative containers defined for each algorithm.
 * \tparam mode Computation mode of the algorithm, \ref ComputeMode
 */
template<ComputeMode mode> class AlgorithmContainer : public AlgorithmContainerIfaceImpl
{
public:
    /**
     * Default constructor
     * \param[in] daalEnv   Pointer to the structure that contains information about the environment
     */
    AlgorithmContainer(daal::services::Environment::env *daalEnv) : AlgorithmContainerIfaceImpl(daalEnv) {}

    virtual ~AlgorithmContainer() {}

    /**
     * Computes final results of the algorithm in the %batch mode,
     * or partial results of the algorithm in %online and %distributed modes.
     * This method behaves similarly to compute method of the Algorithm class.
     */
    virtual services::Status compute() = 0;

    /**
     * Computes final results of the algorithm using partial results in %online and %distributed modes.
     * This method behaves similarly to finalizeCompute method of the Algorithm class.
     */
    virtual services::Status finalizeCompute() = 0;

    /**
     * Setups internal datastructures for compute function.
     */
    virtual services::Status setupCompute() = 0;

    /**
     * Resets internal datastructures for compute function.
     */
    virtual services::Status resetCompute() = 0;

    /**
     * Setups internal datastructures for finalizeCompute function.
     */
    virtual services::Status setupFinalizeCompute() = 0;

    /**
     * Resets internal datastructures for finalizeCompute function.
     */
    virtual services::Status resetFinalizeCompute() = 0;
};

/**
 * <a name="DAAL-CLASS-ALGORITHMS__ALGORITHMCONTAINERIMPL"></a>
 * \brief Abstract interface class that provides virtual methods to access and run implementations
 *        of the algorithms. It is associated with the Algorithm class
 *        and supports the methods for computation and finalization of the algorithm results
 *        in the batch, distributed, and online modes.
 *        The methods of the container are defined in derivative containers defined for each algorithm.
 * \tparam mode Computation mode of the algorithm, \ref ComputeMode
 */
template<ComputeMode mode> class AlgorithmContainerImpl : public AlgorithmContainer<mode>
{
public:
    /**
     * Default constructor
     * \param[in] daalEnv   Pointer to the structure that contains information about the environment
     */
    AlgorithmContainerImpl(daal::services::Environment::env *daalEnv = 0) : AlgorithmContainer<mode>(daalEnv), _in(0), _pres(0), _res(0), _par(0) {}

    virtual ~AlgorithmContainerImpl() {}

    /**
     * Sets arguments of the algorithm
     * \param[in] in    Pointer to the input arguments of the algorithm
     * \param[in] pres  Pointer to the partial results of the algorithm
     * \param[in] par   Pointer to the parameters of the algorithm
     */
    void setArguments(Input *in, PartialResult *pres, Parameter *par)
    {
        _in   = in;
        _pres = pres;
        _par  = par;
    }

    /**
     * Sets partial results of the algorithm
     * \param[in] pres   Pointer to the partial results of the algorithm
     */
    void setPartialResult(PartialResult *pres)
    {
        _pres = pres;
    }

    /**
     * Sets final results of the algorithm
     * \param[in] res   Pointer to the final results of the algorithm
     */
    void setResult(Result *res)
    {
        _res = res;
    }

    /**
     * Retrieves final results of the algorithm
     * \return   Pointer to the final results of the algorithm
     */
    Result *getResult() const
    {
        return _res;
    }

    virtual services::Status setupCompute() DAAL_C11_OVERRIDE { return services::Status();  }

    virtual services::Status resetCompute() DAAL_C11_OVERRIDE { return services::Status(); }

    virtual services::Status setupFinalizeCompute() DAAL_C11_OVERRIDE { return services::Status(); }

    virtual services::Status resetFinalizeCompute() DAAL_C11_OVERRIDE { return services::Status(); }

protected:
    Input                                *_in;
    PartialResult                        *_pres;
    Result                               *_res;
    Parameter                            *_par;
};

/**
 * <a name="DAAL-CLASS-ALGORITHMS__ALGORITHMDISPATCHCONTAINER"></a>
 * \brief Implements a container to dispatch algorithms to cpu-specific implementations.
 *
 *
 * \tparam mode                 Computation mode of the algorithm, \ref ComputeMode
 * \tparam sse2Container        Implementation for Intel(R) Streaming SIMD Extensions 2 (Intel(R) SSE2)
 * \tparam ssse3Container       Implementation for Supplemental Streaming SIMD Extensions 3 (SSSE3)
 * \tparam sse42Container       Implementation for Intel(R) Streaming SIMD Extensions 42 (Intel(R) SSE42)
 * \tparam avxContainer         Implementation for Intel(R) Advanced Vector Extensions (Intel(R) AVX)
 * \tparam avx2Container        Implementation for Intel(R) Advanced Vector Extensions 2 (Intel(R) AVX2)
 * \tparam avx512_micContainer  Implementation for Intel(R) Xeon Phi(TM) processors/coprocessors based on Intel(R) Advanced Vector
 *                              Extensions 512 (Intel(R) AVX512)
 * \tparam avx512Container      Implementation for Intel(R) Xeon(R) processors based on Intel AVX-512
 */
template<ComputeMode mode,
    typename sse2Container
    DAAL_KERNEL_SSSE3_ONLY(typename ssse3Container)
    DAAL_KERNEL_SSE42_ONLY(typename sse42Container)
    DAAL_KERNEL_AVX_ONLY(typename avxContainer)
    DAAL_KERNEL_AVX2_ONLY(typename avx2Container)
    DAAL_KERNEL_AVX512_mic_ONLY(typename avx512_micContainer)
    DAAL_KERNEL_AVX512_ONLY(typename avx512Container)
>
class DAAL_EXPORT AlgorithmDispatchContainer : public AlgorithmContainerImpl<mode>
{
public:
    /**
     * Default constructor
     * \param[in] daalEnv   Pointer to the structure that contains information about the environment
     */
    AlgorithmDispatchContainer(daal::services::Environment::env *daalEnv);

    virtual ~AlgorithmDispatchContainer() { delete _cntr; }

    virtual services::Status compute() DAAL_C11_OVERRIDE
    {
        _cntr->setArguments(this->_in, this->_pres, this->_par);
        return _cntr->compute();
    }

    virtual services::Status finalizeCompute() DAAL_C11_OVERRIDE
    {
        _cntr->setArguments(this->_in, this->_pres, this->_par);
        _cntr->setResult(this->_res);
        return _cntr->finalizeCompute();
    }

    virtual services::Status setupCompute() DAAL_C11_OVERRIDE
    {
        _cntr->setArguments(this->_in, this->_pres, this->_par);
        _cntr->setResult(this->_res);
        _cntr->setErrorCollection(this->_errors);
        return _cntr->setupCompute();
    }

    virtual services::Status resetCompute() DAAL_C11_OVERRIDE
    {
        return _cntr->resetCompute();
    }

protected:
    AlgorithmContainerImpl<mode> *_cntr;
};

#define __DAAL_ALGORITHM_CONTAINER(Mode, ContainerTemplate, ...)         \
    AlgorithmDispatchContainer< Mode,                                    \
        ContainerTemplate<__VA_ARGS__, sse2>                             \
        DAAL_KERNEL_SSSE3_CONTAINER(ContainerTemplate, __VA_ARGS__)      \
        DAAL_KERNEL_SSE42_CONTAINER(ContainerTemplate, __VA_ARGS__)      \
        DAAL_KERNEL_AVX_CONTAINER(ContainerTemplate, __VA_ARGS__)        \
        DAAL_KERNEL_AVX2_CONTAINER(ContainerTemplate, __VA_ARGS__)       \
        DAAL_KERNEL_AVX512_mic_CONTAINER(ContainerTemplate, __VA_ARGS__) \
        DAAL_KERNEL_AVX512_CONTAINER(ContainerTemplate, __VA_ARGS__)>

/** @} */
} // namespace interface1
using interface1::AlgorithmContainerImpl;
using interface1::AlgorithmDispatchContainer;

}
}
#endif
