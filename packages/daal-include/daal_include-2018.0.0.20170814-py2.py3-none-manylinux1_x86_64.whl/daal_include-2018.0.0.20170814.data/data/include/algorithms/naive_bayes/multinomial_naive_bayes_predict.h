/* file: multinomial_naive_bayes_predict.h */
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
//  Implementation of the interface for multinomial naive Bayes model-based prediction
//  in the batch processing mode
//--
*/

#ifndef __NAIVE_BAYES_PREDICT_H__
#define __NAIVE_BAYES_PREDICT_H__

#include "algorithms/algorithm.h"
#include "data_management/data/numeric_table.h"
#include "services/daal_defines.h"
#include "multinomial_naive_bayes_predict_types.h"
#include "algorithms/classifier/classifier_predict.h"

namespace daal
{
namespace algorithms
{
namespace multinomial_naive_bayes
{
namespace prediction
{

/**
 * \brief Contains version 1.0 of the Intel(R) Data Analytics Acceleration Library (Intel(R) DAAL) interface
 */
namespace interface1
{
/**
 * @defgroup multinomial_naive_bayes_prediction_batch Batch
 * @ingroup multinomial_naive_bayes_prediction
 * @{
 */
/**
 * <a name="DAAL-CLASS-ALGORITHMS__MULTINOMIAL_NAIVE_BAYES__PREDICTION__BATCHCONTAINER"></a>
 * \brief Runs the prediction based on the multinomial naive Bayes model
 *
 * \tparam algorithmFPType  Data type to use in intermediate computations for prediction based on the multinomial naive Bayes model, double or float
 * \tparam method           Multinomial naive Bayes prediction method, \ref Method
 */
template<typename algorithmFPType, prediction::Method method, CpuType cpu>
class DAAL_EXPORT BatchContainer : public PredictionContainerIface
{
public:
    /**
     * Constructs a container for multinomial naive Bayes model-based prediction with a specified environment
     * in the batch processing mode
     * \param[in] daalEnv   Environment object
     */
    BatchContainer(daal::services::Environment::env *daalEnv);
    /** Default destructor */
    ~BatchContainer();
    /**
     * Computes the result of multinomial naive Bayes model-based prediction in the batch processing mode
     *
     * \return Status of computations
     */
    services::Status compute() DAAL_C11_OVERRIDE;
};

/**
 * <a name="DAAL-CLASS-ALGORITHMS__MULTINOMIAL_NAIVE_BAYES__PREDICTION__BATCH"></a>
 *  \brief Predicts the results of the multinomial naive Bayes classification
 *  <!-- \n<a href="DAAL-REF-MULTINOMNAIVEBAYES-ALGORITHM">Multinomial naive Bayes algorithm description and usage models</a> -->
 *
 *  \tparam algorithmFPType  Data type to use in intermediate computations for prediction based on the multinomial naive Bayes model, double or float
 *  \tparam method           Multinomial naive Bayes prediction method, \ref Method
 *
 *  \par Enumerations
 *      - \ref Method Multinomial naive Bayes prediction methods
 */
template<typename algorithmFPType = DAAL_ALGORITHM_FP_TYPE, prediction::Method method = defaultDense>
class Batch : public classifier::prediction::Batch
{
public:
    Input input;                /*!< %Input objects of the algorithm */
    Parameter parameter;        /*!< \ref interface1::Parameter "Parameters" of the prediction algorithm */
    /**
     * Default constructor
     * \param nClasses  Number of classes
     */
    Batch(size_t nClasses) : parameter(nClasses)
    {
        initialize();
    }

    /**
     * Constructs multinomial naive Bayes prediction algorithm by copying input objects and parameters
     * of another multinomial naive Bayes prediction algorithm
     * \param[in] other An algorithm to be used as the source to initialize the input objects
     *                  and parameters of the algorithm
     */
    Batch(const Batch<algorithmFPType, method> &other) :
        classifier::prediction::Batch(other), parameter(other.parameter), input(other.input)
    {
        initialize();
    }

    virtual ~Batch() {}

    /**
     * Get input objects for the multinomial naive Bayes prediction algorithm
     * \return %Input objects for the multinomial naive Bayes prediction algorithm
     */
    Input * getInput() DAAL_C11_OVERRIDE { return &input; }

    /**
     * Returns method of the algorithm
     * \return Method of the algorithm
     */
    virtual int getMethod() const DAAL_C11_OVERRIDE { return(int)method; }

    /**
     * Returns a pointer to the newly allocated multinomial naive Bayes prediction algorithm
     * with a copy of input objects and parameters of this multinomial naive Bayes prediction algorithm
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
        services::Status s = _result->allocate<algorithmFPType>(&input, &parameter, (int) method);
        _res = _result.get();
        return s;
    }

    void initialize()
    {
        _in = &input;
        _ac = new __DAAL_ALGORITHM_CONTAINER(batch, BatchContainer, algorithmFPType, method)(&_env);
        _par = &parameter;
    }
};
/** @} */
} // namespace interface1
using interface1::BatchContainer;
using interface1::Batch;

} // namespace prediction
} // namespace multinomial_naive_bayes
} // namespace algorithms
} // namespace daal
#endif
