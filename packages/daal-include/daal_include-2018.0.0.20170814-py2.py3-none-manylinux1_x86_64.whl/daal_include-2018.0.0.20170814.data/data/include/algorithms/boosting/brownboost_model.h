/* file: brownboost_model.h */
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
//  Implementation of class defining Brown Boost model.
//--
*/

#ifndef __BROWN_BOOST_MODEL_H__
#define __BROWN_BOOST_MODEL_H__

#include "algorithms/algorithm.h"
#include "data_management/data/homogen_numeric_table.h"
#include "algorithms/boosting/boosting_model.h"

namespace daal
{
namespace algorithms
{
/**
 * \brief Contains classes for the BrownBoost classification algorithm
 */
namespace brownboost
{

/**
 * \brief Contains version 1.0 of Intel(R) Data Analytics Acceleration Library (Intel(R) DAAL) interface.
 */
namespace interface1
{
/**
 * @ingroup brownboost
 * @{
 */
/**
 * <a name="DAAL-STRUCT-ALGORITHMS__BROWNBOOST__PARAMETER"></a>
 * \brief BrownBoost algorithm parameters
 *
 * \snippet boosting/brownboost_model.h Parameter source code
 */
/* [Parameter source code] */
struct DAAL_EXPORT Parameter : public boosting::Parameter
{
    /** Default constructor */
    Parameter();

    /**
     * Constructs BrownBoost parameter structure
     * \param[in] wlTrainForParameter       Pointer to the training algorithm of the weak learner
     * \param[in] wlPredictForParameter     Pointer to the prediction algorithm of the weak learner
     * \param[in] acc                       Accuracy of the BrownBoost training algorithm
     * \param[in] maxIter                   Maximal number of iterations of the BrownBoost training algorithm
     * \param[in] nrAcc                     Accuracy threshold for Newton-Raphson iterations in the BrownBoost training algorithm
     * \param[in] nrMaxIter                 Maximal number of Newton-Raphson iterations in the BrownBoost training algorithm
     * \param[in] dcThreshold               Threshold needed  to avoid degenerate cases in the BrownBoost training algorithm
     */
    Parameter(services::SharedPtr<weak_learner::training::Batch>   wlTrainForParameter,
              services::SharedPtr<weak_learner::prediction::Batch> wlPredictForParameter,
              double acc = 0.3, size_t maxIter = 10, double nrAcc = 1.0e-3, size_t nrMaxIter = 100, double dcThreshold = 1.0e-2);

    double accuracyThreshold;       /*!< Accuracy of the BrownBoost training algorithm */
    size_t maxIterations;           /*!< Maximal number of iterations of the BrownBoost training algorithm */
    double newtonRaphsonAccuracyThreshold;  /*!< Accuracy threshold for Newton-Raphson iterations in the BrownBoost training algorithm */
    size_t newtonRaphsonMaxIterations;      /*!< Maximal number of Newton-Raphson iterations in the BrownBoost training algorithm */
    double degenerateCasesThreshold;        /*!< Threshold needed to avoid degenerate cases in the BrownBoost training algorithm */

    services::Status check() const DAAL_C11_OVERRIDE;
};
/* [Parameter source code] */

/**
 * <a name="DAAL-CLASS-ALGORITHMS__BROWNBOOST__MODEL"></a>
 * \brief %Model of the classifier trained by the brownboost::training::Batch algorithm.
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
     *  Constructs the BrownBoost %Model
     * \tparam modelFPType  Data type to store BrownBoost model data, double or float
     * \param[in] nFeatures Number of features in the dataset
     * \param[in] dummy     Dummy variable for the templated constructor
     * \DAAL_DEPRECATED_USE{ Model::create }
     */
    template <typename modelFPType>
    DAAL_EXPORT Model(size_t nFeatures, modelFPType dummy);

    /**
     * Empty constructor for deserialization
     * \DAAL_DEPRECATED_USE{ Model::create }
     */
    Model() : boosting::Model(), _alpha() { }


    /**
     * Constructs the BrownBoost model
     * \tparam modelFPType  Data type to store BrownBoost model data, double or float
     * \param[in]  nFeatures Number of features in the dataset
     * \param[out] stat      Status of the model construction
     */
    template<typename modelFPType>
    DAAL_EXPORT static services::SharedPtr<Model> create(size_t nFeatures, services::Status *stat = NULL);

    virtual ~Model() { }

    /**
     *  Returns a pointer to the array of weights of weak learners constructed
     *  during training of the BrownBoost algorithm.
     *  The size of the array equals the number of weak learners
     *  \return Array of weights of weak learners.
     */
    data_management::NumericTablePtr getAlpha();

protected:
    data_management::NumericTablePtr _alpha;     /* Boosting coefficients table */

    template<typename Archive, bool onDeserialize>
    services::Status serialImpl(Archive *arch)
    {
        boosting::Model::serialImpl<Archive, onDeserialize>(arch);
        arch->setSharedPtrObj(_alpha);

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

    template <typename modelFPType>
    DAAL_EXPORT Model(size_t nFeatures, modelFPType dummy, services::Status &st);

}; // class Model
typedef services::SharedPtr<Model> ModelPtr;
/** @} */
} // namespace interface1
using interface1::Parameter;
using interface1::Model;
using interface1::ModelPtr;

} // namespace daal::algorithms::brownboost
}
} // namespace daal
#endif
