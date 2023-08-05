/* file: qr_online.h */
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
//  Implementation of the interface for the QR decomposition algorithm in the
//  online processing mode
//--
*/

#ifndef __QR_STREAM_H__
#define __QR_STREAM_H__

#include "algorithms/algorithm.h"
#include "data_management/data/numeric_table.h"
#include "services/daal_defines.h"
#include "algorithms/qr/qr_types.h"

namespace daal
{
namespace algorithms
{
namespace qr
{

namespace interface1
{
/**
 * @defgroup qr_online Online
 * @ingroup qr_without_pivoting
 * @{
 */
/**
 * <a name="DAAL-CLASS-ALGORITHMS__QR__ONLINECONTAINER"></a>
 * \brief Provides methods to run implementations of the QR decomposition algorithm in the online processing mode.
 *
 * \tparam algorithmFPType  Data type to use in intermediate computations for the QR decomposition algorithm, double or float
 * \tparam method           Computation method, \ref daal::algorithms::qr::Method
 *
 */
template<typename algorithmFPType, Method method, CpuType cpu>
class OnlineContainer : public daal::algorithms::AnalysisContainerIface<online>
{
public:
   /**
     * Constructs a container for the QR decomposition algorithm with a specified environment
     * in the online processing mode
     * \param[in] daalEnv   Environment object
     */
    OnlineContainer(daal::services::Environment::env *daalEnv);
    /** Default destructor */
    virtual ~OnlineContainer();
    /**
     * Computes a partial result of the QR decomposition algorithm in the online processing mode
     */
    virtual services::Status compute() DAAL_C11_OVERRIDE;
    /**
     * Computes the result of the QR decomposition algorithm in the online processing mode
     */
    virtual services::Status finalizeCompute() DAAL_C11_OVERRIDE;
};

/**
 * <a name="DAAL-CLASS-ALGORITHMS__QR__ONLINE"></a>
 * \brief Computes the results of the QR decomposition algorithm in the online processing mode.
 * <!-- \n<a href="DAAL-REF-QR-ALGORITHM">QR decomposition algorithm description and usage models</a> -->
 *
 * \tparam algorithmFPType  Data type to use in intermediate computations for the QR decomposition algorithm, double or float
 * \tparam method           Computation method, \ref daal::algorithms::qr::Method
 *
 * \par Enumerations
 *      - \ref Method   Computation methods for the QR decomposition algorithm
 */
template<typename algorithmFPType = DAAL_ALGORITHM_FP_TYPE, Method method = defaultDense>
class Online : public daal::algorithms::Analysis<online>
{
public:
    typedef OnlinePartialResult PartialResult;
    typedef OnlinePartialResultPtr PartialResultPtr;

    Input     input;     /*!< Input object */
    Parameter parameter; /*!< QR parameters */

    Online()
    {
        initialize();
    }

    /**
     * Constructs a QR decomposition algorithm by copying input objects and parameters
     * of another QR decomposition algorithm
     * \param[in] other An algorithm to be used as the source to initialize the input objects
     *                  and parameters of the algorithm
     */
    Online(const Online<algorithmFPType, method> &other) : input(other.input), parameter(other.parameter)
    {
        initialize();
    }

    /**
    * Returns method of the algorithm
    * \return Method of the algorithm
    */
    virtual int getMethod() const DAAL_C11_OVERRIDE { return(int)method; }

    /**
     * Returns the structure that contains the results of the QR decomposition algorithm
     * \return Structure that contains the results of the QR decomposition algorithm
     */
    ResultPtr getResult()
    {
        return _result;
    }

    /**
     * Returns the structure that contains partial results of the QR decomposition algorithm
     * \return Structure that contains partial results of the QR decomposition algorithm
     */
    PartialResultPtr getPartialResult()
    {
        return _partialResult;
    }

    /**
     * Registers user-allocated memory to store the results of the QR decomposition algorithm
     * \return Structure to store the results of the QR decomposition algorithm
     */
    services::Status setResult(const ResultPtr& res)
    {
        DAAL_CHECK(res, services::ErrorNullResult)
        _result = res;
        _res = _result.get();
        return services::Status();
    }

    /**
     * Registers user-allocated memory to store partial results of the QR decomposition algorithm
     * \param[in] partialResult Structure for storing partial results of the QR decomposition algorithm
     * \param[in] initFlag Flag that specifies whether the partial results are initialized
     * \return Structure to store partial results of the QR decomposition algorithm
     */
    services::Status setPartialResult(const PartialResultPtr &partialResult, bool initFlag = false)
    {
        _partialResult = partialResult;
        _pres = _partialResult.get();
        setInitFlag(initFlag);
        return services::Status();
    }

    /**
     * Returns a pointer to the newly allocated QR decomposition algorithm
     * with a copy of input objects and parameters of this QR decomposition algorithm
     * \return Pointer to the newly allocated algorithm
     */
    services::SharedPtr<Online<algorithmFPType, method> > clone() const
    {
        return services::SharedPtr<Online<algorithmFPType, method> >(cloneImpl());
    }

protected:
    virtual Online<algorithmFPType, method> * cloneImpl() const DAAL_C11_OVERRIDE
    {
        return new Online<algorithmFPType, method>(*this);
    }

    virtual services::Status allocateResult() DAAL_C11_OVERRIDE
    {
        _result.reset(new Result());
        services::Status s = _result->allocate<algorithmFPType>(_pres, 0, 0);
        _res = _result.get();
        return s;
    }

    virtual services::Status allocatePartialResult() DAAL_C11_OVERRIDE
    {
        _partialResult.reset(new PartialResult());
        services::Status s = _partialResult->allocate<algorithmFPType>(_in, 0, 0);
        _pres = _partialResult.get();
        return s;
    }

    virtual services::Status initializePartialResult() DAAL_C11_OVERRIDE
    {
        services::Status s = _partialResult->initialize<algorithmFPType>(_in, 0, 0);
        _pres = _partialResult.get();
        return s;
    }

    void initialize()
    {
        Analysis<online>::_ac = new __DAAL_ALGORITHM_CONTAINER(online, OnlineContainer, algorithmFPType, method)(&_env);
        _in   = &input;
        _par  = &parameter;
    }

private:
    PartialResultPtr _partialResult;
    ResultPtr        _result;
};
/** @} */
} // namespace interface1
using interface1::OnlineContainer;
using interface1::Online;

} // namespace daal::algorithms::qr
} // namespace daal::algorithms
} // namespace daal
#endif
