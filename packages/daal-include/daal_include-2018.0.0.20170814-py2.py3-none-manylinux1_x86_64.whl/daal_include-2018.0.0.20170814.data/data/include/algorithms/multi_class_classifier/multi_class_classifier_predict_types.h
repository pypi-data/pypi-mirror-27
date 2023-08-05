/* file: multi_class_classifier_predict_types.h */
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
//  Multiclass classifier data types
//--
*/

#ifndef __MULTI_CLASS_CLASSIFIER_PREDICT_TYPES_H__
#define __MULTI_CLASS_CLASSIFIER_PREDICT_TYPES_H__

#include "algorithms/algorithm.h"
#include "algorithms/multi_class_classifier/multi_class_classifier_model.h"

namespace daal
{
namespace algorithms
{
namespace multi_class_classifier
{
/**
 * @defgroup multi_class_classifier_prediction Prediction
 * \copydoc daal::algorithms::multi_class_classifier::prediction
 * @ingroup multi_class_classifier
 * @{
 */
namespace prediction
{
/**
 * <a name="DAAL-ENUM-ALGORITHMS__MULTI_CLASS_CLASSIFIER__PREDICTION__METHOD"></a>
 * Computation methods for the multi-class classifier prediction algorithm
 */
enum Method
{
    defaultDense = 0,           /*!< Prediction method for the multi-class classifier proposed by Ting-Fan Wu et al. */
    multiClassClassifierWu = 0  /*!< Prediction method for the multi-class classifier proposed by Ting-Fan Wu et al. */
};

namespace interface1
{

/**
 * <a name="DAAL-CLASS-ALGORITHMS__MULTI_CLASS_CLASSIFIER__PREDICTION__INPUT"></a>
 * \brief Input objects in the prediction stage of the Multi-class classifier algorithm
 */
class DAAL_EXPORT Input : public classifier::prediction::Input
{
    typedef classifier::prediction::Input super;
public:
    Input();
    Input(const Input& other);
    virtual ~Input() {}

    using super::get;
    using super::set;

    /**
     * Returns the input Numeric Table object in the prediction stage of the classification algorithm
     * \param[in] id    Identifier of the input NumericTable object
     * \return          Input object that corresponds to the given identifier
     */
    data_management::NumericTablePtr get(classifier::prediction::NumericTableInputId id) const;

    /**
     * Returns the input Model object in the prediction stage of the Multi-class classifier algorithm
     * \param[in] id    Identifier of the input Model object
     * \return          Input object that corresponds to the given identifier
     */
    multi_class_classifier::ModelPtr get(classifier::prediction::ModelInputId id) const;

    /**
     * Sets the input NumericTable object in the prediction stage of the classification algorithm
     * \param[in] id    Identifier of the input object
     * \param[in] ptr   Pointer to the input object
     */
    void set(classifier::prediction::NumericTableInputId id, const data_management::NumericTablePtr &ptr);

    /**
     * Sets the input Model object in the prediction stage of the Multi-class classifier algorithm
     * \param[in] id    Identifier of the input object
     * \param[in] ptr   Pointer to the input object
     */
    void set(classifier::prediction::ModelInputId id, const multi_class_classifier::ModelPtr &ptr);

    /**
     * Checks the correctness of the input object
     * \param[in] parameter Pointer to the structure of the algorithm parameters
     * \param[in] method    Computation method
     *
     * \return Status of computation
     */
    services::Status check(const daal::algorithms::Parameter *parameter, int method) const DAAL_C11_OVERRIDE;
};

} // namespace interface1
using interface1::Input;

} // namespace prediction
/** @} */
} // namespace multi_class_classifier
} // namespace algorithms
} // namespace daal
#endif
