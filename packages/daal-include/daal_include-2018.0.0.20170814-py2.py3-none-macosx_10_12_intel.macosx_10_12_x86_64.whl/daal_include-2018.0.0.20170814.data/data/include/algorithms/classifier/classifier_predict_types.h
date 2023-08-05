/* file: classifier_predict_types.h */
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
//  Implementation of the base classes used in the prediction stage
//  of the classifier algorithm
//--
*/

#ifndef __CLASSIFIER_PREDICT_TYPES_H__
#define __CLASSIFIER_PREDICT_TYPES_H__

#include "algorithms/algorithm.h"
#include "algorithms/classifier/classifier_model.h"

#include "data_management/data/homogen_numeric_table.h"

namespace daal
{
namespace algorithms
{
namespace classifier
{
/**
 * @defgroup prediction Prediction
 * \copydoc daal::algorithms::classifier::prediction
 * @ingroup classifier
 * @{
 */
/**
 * \brief Contains classes for making prediction based on the classifier model
 */
namespace prediction
{
/**
 * <a name="DAAL-ENUM-ALGORITHMS__CLASSIFIER__PREDICTION__NUMERICTABLEINPUTID"></a>
 * Available identifiers of input NumericTable objects in the prediction stage
 * of the classification algorithm
 */
enum NumericTableInputId
{
    data,                      /*!< Input data set */
    lastNumericTableInputId = data
};

/**
 * <a name="DAAL-ENUM-ALGORITHMS__CLASSIFIER__PREDICTION__MODELINPUTID"></a>
 * Available identifiers of input Model objects in the prediction stage
 * of the classification algorithm
 */
enum ModelInputId
{
    model = lastNumericTableInputId + 1,               /*!< Input model trained by the classification algorithm */
    lastModelInputId = model
};

/**
 * <a name="DAAL-ENUM-ALGORITHMS__CLASSIFIER__PREDICTION__RESULTID"></a>
 * Available identifiers of results obtained in the prediction stage of the classification algorithm
 */
enum ResultId
{
    prediction,           /*!< Prediction results */
    lastResultId = prediction
};

/**
 * \brief Contains version 1.0 of the Intel(R) Data Analytics Acceleration Library (Intel(R) DAAL) interface.
 */
namespace interface1
{
/**
 * <a name="DAAL-CLASS-ALGORITHMS__CLASSIFIER__PREDICTION__INPUTIFACE"></a>
 * \brief Base class for working with input objects in the prediction stage of the classification algorithm
 */
class DAAL_EXPORT InputIface : public daal::algorithms::Input
{
public:
    InputIface(size_t nElements);
    InputIface(const InputIface& other) : daal::algorithms::Input(other){}

    virtual ~InputIface() {}
    /**
     * Returns the number of rows in the input data set
     * \return Number of rows in the input data set
     */
    virtual size_t getNumberOfRows() const = 0;
};

/**
 * <a name="DAAL-CLASS-ALGORITHMS__CLASSIFIER__PREDICTION__INPUT"></a>
 * \brief Input objects in the prediction stage of the classification algorithm
 */
class DAAL_EXPORT Input : public InputIface
{
public:
    Input();
    Input(const Input& other) : InputIface(other){}
    virtual ~Input() {}

    /**
     * Returns the number of rows in the input data set
     * \return Number of rows in the input data set
     */
    size_t getNumberOfRows() const DAAL_C11_OVERRIDE;

    /**
     * Returns the input Numeric Table object in the prediction stage of the classification algorithm
     * \param[in] id    Identifier of the input NumericTable object
     * \return          Input object that corresponds to the given identifier
     */
    data_management::NumericTablePtr get(NumericTableInputId id) const;

    /**
     * Returns the input Model object in the prediction stage of the classification algorithm
     * \param[in] id    Identifier of the input Model object
     * \return          Input object that corresponds to the given identifier
     */
    classifier::ModelPtr get(ModelInputId id) const;

    /**
     * Sets the input NumericTable object in the prediction stage of the classification algorithm
     * \param[in] id    Identifier of the input object
     * \param[in] ptr   Pointer to the input object
     */
    void set(NumericTableInputId id, const data_management::NumericTablePtr &ptr);

    /**
     * Sets the input Model object in the prediction stage of the classifier algorithm
     * \param[in] id    Identifier of the input object
     * \param[in] ptr   Pointer to the input object
     */
    void set(ModelInputId id, const ModelPtr &ptr);

    /**
     * Checks the correctness of the input object
     * \param[in] parameter Pointer to the structure of the algorithm parameters
     * \param[in] method    Computation method
     */
    services::Status check(const daal::algorithms::Parameter *parameter, int method) const DAAL_C11_OVERRIDE;

protected:
    services::Status checkImpl(const daal::algorithms::Parameter *parameter) const;
};

/**
 * <a name="DAAL-CLASS-ALGORITHMS__CLASSIFIER__PREDICTION__RESULT"></a>
 * \brief Provides methods to access prediction results obtained with the compute() method
 *        of the classifier prediction algorithm in the batch processing mode
 */
class DAAL_EXPORT Result : public daal::algorithms::Result
{
public:
    DECLARE_SERIALIZABLE_CAST(Result);
    Result();

    /**
     * Returns the prediction result of the classification algorithm
     * \param[in] id   Identifier of the prediction result, \ref ResultId
     * \return         Prediction result that corresponds to the given identifier
     */
    data_management::NumericTablePtr get(ResultId id) const;

    /**
     * Sets the prediction result of the classification algorithm
     * \param[in] id    Identifier of the prediction result, \ref ResultId
     * \param[in] value Pointer to the prediction result
     */
    void set(ResultId id, const data_management::NumericTablePtr &value);

    /**
     * Allocates memory for storing prediction results of the classification algorithm
     * \tparam  algorithmFPType     Data type for storing prediction results
     * \param[in] input     Pointer to the input objects of the classification algorithm
     * \param[in] parameter Pointer to the parameters of the classification algorithm
     * \param[in] method    Computation method
     */
    template <typename algorithmFPType>
    DAAL_EXPORT services::Status allocate(const daal::algorithms::Input *input, const daal::algorithms::Parameter *parameter, const int method);

    /**
     * Checks the correctness of the Result object
     * \param[in] input     Pointer to the the input object
     * \param[in] parameter Pointer to the algorithm parameters
     * \param[in] method    Computation method
     */
    services::Status check(const daal::algorithms::Input *input, const daal::algorithms::Parameter *parameter,
                           int method) const DAAL_C11_OVERRIDE;

protected:
    services::Status checkImpl(const daal::algorithms::Input *input, const daal::algorithms::Parameter *parameter) const;

    /** \private */
    template<typename Archive, bool onDeserialize>
    services::Status serialImpl(Archive *arch)
    {
        daal::algorithms::Result::serialImpl<Archive, onDeserialize>(arch);

        return services::Status();
    }

    services::Status serializeImpl(data_management::InputDataArchive  *arch) DAAL_C11_OVERRIDE
    {
        serialImpl<data_management::InputDataArchive, false>(arch);

        return services::Status();
    }

    services::Status deserializeImpl(const data_management::OutputDataArchive *arch) DAAL_C11_OVERRIDE
    {
        serialImpl<const data_management::OutputDataArchive, true>(arch);

        return services::Status();
    }
};
typedef services::SharedPtr<Result> ResultPtr;
} // namespace interface1
using interface1::InputIface;
using interface1::Input;
using interface1::Result;
using interface1::ResultPtr;
}
/** @} */
}
}
}
#endif
