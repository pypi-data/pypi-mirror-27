/* file: logitboost_model.h */
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
//  Implementation of class defining LogitBoost model.
//--
*/

#ifndef __LOGIT_BOOST_MODEL_H__
#define __LOGIT_BOOST_MODEL_H__

#include "algorithms/algorithm.h"
#include "data_management/data/homogen_numeric_table.h"
#include "algorithms/boosting/boosting_model.h"

namespace daal
{
namespace algorithms
{
/**
 * \brief Contains classes for the LogitBoost classification algorithm
 */
namespace logitboost
{

/**
 * \brief Contains version 1.0 of Intel(R) Data Analytics Acceleration Library (Intel(R) DAAL) interface.
 */
namespace interface1
{
/**
 * @ingroup logitboost
 * @{
 */
/**
 * <a name="DAAL-STRUCT-ALGORITHMS__LOGITBOOST__PARAMETER"></a>
 * \brief LogitBoost algorithm parameters
 *
 * \snippet boosting/brownboost_model.h Parameter source code
 */
/* [Parameter source code] */
struct DAAL_EXPORT Parameter : public boosting::Parameter
{
    /** Default constructor */
    Parameter();

    /**
     * Constructs LogitBoost parameter structure
     * \param[in] wlTrainForParameter       Pointer to the training algorithm of the weak learner
     * \param[in] wlPredictForParameter     Pointer to the prediction algorithm of the weak learner
     * \param[in] acc                       Accuracy of the LogitBoost training algorithm
     * \param[in] maxIter                   Maximal number of terms in additive regression
     * \param[in] nC                        Number of classes in the training data set
     * \param[in] wThr                      Threshold to avoid degenerate cases when calculating weights W
     * \param[in] zThr                      Threshold to avoid degenerate cases when calculating responses Z
     */
    Parameter(const services::SharedPtr<weak_learner::training::Batch>&   wlTrainForParameter,
              const services::SharedPtr<weak_learner::prediction::Batch>& wlPredictForParameter,
              double acc = 0.0, size_t maxIter = 10, size_t nC = 0, double wThr = 1e-10, double zThr = 1e-10);

    double accuracyThreshold;       /*!< Accuracy of the LogitBoost training algorithm */
    size_t maxIterations;           /*!< Maximal number of terms in additive regression */
    size_t nClasses;                /*!< Number of classes */
    double weightsDegenerateCasesThreshold;     /*!< Threshold to avoid degenerate cases when  calculating weights W */
    double responsesDegenerateCasesThreshold;   /*!< Threshold to avoid degenerate cases when  calculating responses Z */

    services::Status check() const DAAL_C11_OVERRIDE;
};
/* [Parameter source code] */

/**
 * <a name="DAAL-CLASS-ALGORITHMS__LOGITBOOST__MODEL"></a>
 * \brief %Model of the classifier trained by the logitboost::training::Batch algorithm.
 *
 * \par References
 *      - \ref training::interface1::Batch "training::Batch" class
 *      - \ref prediction::interface1::Batch "prediction::Batch" class
 */
class DAAL_EXPORT Model : public boosting::Model
{
public:
    DECLARE_MODEL(Model, classifier::Model)

    /**
     * Constructs the LogitBoost model
     * \tparam modelFPType  Data type to store LogitBoost model data, double or float
     * \param[in] nFeatures Number of features in the dataset
     * \param[in] par       Pointer to the parameter structure of the LogitBoost algorithm
     * \param[in] dummy     Dummy variable for the templated constructor
     * \DAAL_DEPRECATED_USE{ Model::create }
     */
    template <typename modelFPType>
    DAAL_EXPORT Model(size_t nFeatures, const Parameter *par, modelFPType dummy);

    /**
     * Empty constructor for deserialization
     * \DAAL_DEPRECATED_USE{ Model::create }
     */
    Model() : boosting::Model(), _nIterations(0) { }

    /**
     * Constructs the LogitBoost model
     * \param[in]  nFeatures Number of features in the dataset
     * \param[in]  par       Pointer to the parameter structure of the LogitBoost algorithm
     * \param[out] stat      Status of the model construction
     */
    static services::SharedPtr<Model> create(size_t nFeatures, const Parameter *par,
                                             services::Status *stat = NULL);

    virtual ~Model() { }

    /**
     * Sets the number of iterations for the algorithm
     * @param nIterations   Number of iterations
     */
    void setIterations(size_t nIterations);

    /**
     * Returns the number of iterations done by the training algorithm
     * \return The number of iterations done by the training algorithm
     */
    size_t getIterations() const;

protected:
    size_t _nIterations;

    template<typename Archive, bool onDeserialize>
    services::Status serialImpl(Archive *arch)
    {
        boosting::Model::serialImpl<Archive, onDeserialize>(arch);
        arch->set(_nIterations);

        return services::Status();
    }

    services::Status serializeImpl(data_management::InputDataArchive *archive) DAAL_C11_OVERRIDE
    {
        serialImpl<data_management::InputDataArchive, false>(archive);

        return services::Status();
    }

    services::Status deserializeImpl(const data_management::OutputDataArchive *archive) DAAL_C11_OVERRIDE
    {
        serialImpl<const data_management::OutputDataArchive, true>(archive);

        return services::Status();
    }

    Model(size_t nFeatures, const Parameter *par, services::Status &st);
};
typedef services::SharedPtr<Model> ModelPtr;
/** @} */
} // namespace interface1
using interface1::Parameter;
using interface1::Model;
using interface1::ModelPtr;

} // namespace daal::algorithms::logitboost
}
} // namespace daal
#endif
