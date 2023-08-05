/* file: adaboost_training_batch.h */
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
//  Implementation of the interface for AdaBoost model-based training in the batch
//  processing mode
//--
*/

#ifndef __ADA_BOOST_TRAINING_BATCH_H__
#define __ADA_BOOST_TRAINING_BATCH_H__

#include "algorithms/boosting/boosting_training_batch.h"
#include "algorithms/boosting/adaboost_training_types.h"

namespace daal
{
namespace algorithms
{
namespace adaboost
{
namespace training
{

namespace interface1
{
/**
 * @defgroup adaboost_training_batch Batch
 * @ingroup adaboost_training
 * @{
 */
/**
 * <a name="DAAL-CLASS-ALGORITHMS__ADABOOST__TRAINING__BATCHCONTAINER"></a>
 * \brief Provides methods to run implementations of AdaBoost model-based training.
 *        It is associated with daal::algorithms::adaboost::training::Batch class
 *        and supports method to train AdaBoost model
 *
 * \tparam algorithmFPType  Data type to use in intermediate computations for the AdaBoost, double or float
 * \tparam method           AdaBoost model training method, \ref Method
 */
template<typename algorithmFPType, Method method, CpuType cpu>
class DAAL_EXPORT BatchContainer : public TrainingContainerIface<batch>
{
public:
    /**
     * Constructs a container for AdaBoost model-based training with a specified environment
     * \param[in] daalEnv   Environment object
     */
    BatchContainer(daal::services::Environment::env *daalEnv);
    /** Default destructor */
    ~BatchContainer();
    /**
     * Computes the result of AdaBoost model-based training in the batch processing mode
     */
    services::Status compute() DAAL_C11_OVERRIDE;
};

/**
 * <a name="DAAL-CLASS-ALGORITHMS__ADABOOST__TRAINING__BATCH"></a>
 * \brief Trains model of the AdaBoost algorithms in batch mode
 * <!-- \n<a href="DAAL-REF-ADABOOST-ALGORITHM">AdaBoost algorithm description and usage models</a> -->
 *
 * \tparam algorithmFPType  Data type to use in intermediate computations for the AdaBoost, double or float
 * \tparam method           AdaBoost computation method, \ref daal::algorithms::adaboost::training::Method
 *
 * \par Enumerations
 *      - \ref Method                           Enumeration of supported AdaBoost training methods
 *      - \ref classifier::training::InputId    Enumeration of supported input arguments of the AdaBoost training algorithm
 *      - \ref classifier::training::ResultId   Enumeration of supported AdaBoost training results
 *
 * \par References
 *      - \ref interface1::Model "Model" class
 *      - \ref classifier::training::interface1::Input "classifier::training::Input" class
 */
template<typename algorithmFPType = DAAL_ALGORITHM_FP_TYPE, Method method = defaultDense>
class DAAL_EXPORT Batch : public boosting::training::Batch
{
public:
    Parameter parameter;                        /*!< \ref interface1::Parameter "Parameters" of the algorithm */
    classifier::training::Input input;          /*!< %Input data structure */

    Batch()
    {
        initialize();
    }

    /**
     * Constructs an AdaBoost training algorithm by copying input objects and parameters
     * of another AdaBoost training algorithm
     * \param[in] other An algorithm to be used as the source to initialize the input objects
     *                  and parameters of the algorithm
     */
    Batch(const Batch<algorithmFPType, method> &other) : boosting::training::Batch(other),
        parameter(other.parameter), input(other.input)
    {
        initialize();
    }

    virtual ~Batch() {}

    /**
     * Get input objects for the AdaBoost training algorithm
     * \return %Input objects for the AdaBoost training algorithm
     */
    classifier::training::Input * getInput() DAAL_C11_OVERRIDE { return &input; }

    /**
     * Returns method of the algorithm
     * \return Method of the algorithm
     */
    virtual int getMethod() const DAAL_C11_OVERRIDE { return(int)method; }

    /**
     * Returns the structure that contains results of AdaBoost training
     * \return Structure that contains results of AdaBoost training
     */
    ResultPtr getResult()
    {
        return Result::cast(_result);
    }

    /**
     * Resets the training results of the classification algorithm
     */
    services::Status resetResult() DAAL_C11_OVERRIDE
    {
        _result.reset(new Result());
        DAAL_CHECK(_result, services::ErrorNullResult);
        _res = NULL;
        return services::Status();
    }

    /**
     * Returns a pointer to the newly allocated AdaBoost training algorithm with a copy of input objects
     * and parameters of this AdaBoost training algorithm
     * \return Pointer to the newly allocated algorithm
     */
    services::SharedPtr<Batch<algorithmFPType, method> > clone() const
    {
        return services::SharedPtr<Batch<algorithmFPType, method> >(cloneImpl());
    }

protected:
    virtual Batch<algorithmFPType, method> * cloneImpl() const DAAL_C11_OVERRIDE
    {
        return new Batch<algorithmFPType, method>(*this);
    }

    services::Status allocateResult() DAAL_C11_OVERRIDE
    {
        ResultPtr res = getResult();
        DAAL_CHECK(res, services::ErrorNullResult);
        services::Status s = res->template allocate<algorithmFPType>(&input, _par, method);
        _res = _result.get();
        return s;
    }

    void initialize()
    {
        _ac  = new __DAAL_ALGORITHM_CONTAINER(batch, BatchContainer, algorithmFPType, method)(&_env);
        _in  = &input;
        _par = &parameter;
        _result.reset(new Result());
    }
};
/** @} */
} // namespace interface1
using interface1::BatchContainer;
using interface1::Batch;

} // namespace daal::algorithms::adaboost::training
}
}
} // namespace daal
#endif // __ADA_BOOST_TRAINING_BATCH_H__
