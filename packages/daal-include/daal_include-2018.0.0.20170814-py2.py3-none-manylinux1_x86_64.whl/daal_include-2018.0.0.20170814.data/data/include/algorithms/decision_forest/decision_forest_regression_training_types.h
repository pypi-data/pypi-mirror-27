/* file: decision_forest_regression_training_types.h */
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
//  Implementation of the decision forest regression training algorithm interface
//--
*/

#ifndef __DECISION_FOREST_REGRESSION_TRAINIG_TYPES_H__
#define __DECISION_FOREST_REGRESSION_TRAINIG_TYPES_H__

#include "algorithms/algorithm.h"
#include "data_management/data/numeric_table.h"
#include "data_management/data/data_serialize.h"
#include "services/daal_defines.h"
#include "algorithms/decision_forest/decision_forest_regression_model.h"
#include "algorithms/decision_forest/decision_forest_training_parameter.h"
#include "algorithms/regression/regression_training_types.h"

namespace daal
{
namespace algorithms
{
/**
 * \brief Contains classes of the decision forest algorithm
 */
namespace decision_forest
{
namespace regression
{
/**
 * @defgroup decision_forest_regression_training Training
 * \copydoc daal::algorithms::decision_forest::regression::training
 * @ingroup decision_forest_regression
 * @{
 */
/**
 * \brief Contains a class for decision forest model-based training
 */
namespace training
{
/**
 * <a name="DAAL-ENUM-ALGORITHMS__DECISION_FOREST__REGRESSION__TRAINING__METHOD"></a>
 * \brief Computation methods for decision forest regression model-based training
 */
enum Method
{
    defaultDense = 0  /*!< Bagging, random choice of features, variance-based impurity */
};

/**
 * <a name="DAAL-ENUM-ALGORITHMS__DECISION_FOREST__REGRESSION__TRAINING__INPUTID"></a>
 * \brief Available identifiers of input objects for decision forest model-based training
 */
enum InputId
{
    data              = algorithms::regression::training::data,               /*!< %Input data table */
    dependentVariable = algorithms::regression::training::dependentVariables, /*!< %Values of the dependent variable for the input data */
    lastInputId       = dependentVariable
};

/**
 * <a name="DAAL-ENUM-ALGORITHMS__DECISION_FOREST__REGRESSION__TRAINING__RESULTID"></a>
 * \brief Available identifiers of the result of decision forest model-based training
 */
enum ResultId
{
    model = algorithms::regression::training::model,   /*!< decision forest model */
    lastResultId = model
};

/**
* <a name="DAAL-ENUM-ALGORITHMS__DECISION_FOREST__REGRESSION__TRAINING__RESULT_NUMERIC_TABLEID"></a>
* \brief Available identifiers of the result of decision forest model-based training
*/
enum ResultNumericTableId
{
    outOfBagError = lastResultId + 1, /*!< %Numeric table 1x1 containing out-of-bag error computed when computeOutOfBagError option is on */
    variableImportance,               /*!< %Numeric table 1x(number of features) containing variable importance value.
                                          Computed when parameter.varImportance != none */
    lastResultNumericTableId = variableImportance
};

/**
 * \brief Contains version 1.0 of the Intel(R) Data Analytics Acceleration Library (Intel(R) DAAL) interface
 */
namespace interface1
{
/**
 * <a name="DAAL-CLASS-ALGORITHMS__DECISION_FOREST__REGRESSION__PARAMETER"></a>
 * \brief Parameters for the decision forest algorithm
 *
 * \snippet decision_forest/decision_forest_regression_training_types.h Parameter source code
 */
/* [Parameter source code] */
class DAAL_EXPORT Parameter : public daal::algorithms::Parameter, public daal::algorithms::decision_forest::training::Parameter
{
public:
    Parameter();
    services::Status check() const DAAL_C11_OVERRIDE;
};
/* [Parameter source code] */

/**
 * <a name="DAAL-CLASS-ALGORITHMS__DECISION_FOREST__REGRESSSION__TRAINING__INPUT"></a>
 * \brief %Input objects for decision forest model-based training
 */
class DAAL_EXPORT Input : public algorithms::regression::training::Input
{
public:
    /** Default constructor */
    Input();

    /** Copy constructor */
    Input(const Input& other) : algorithms::regression::training::Input(other){}

    virtual ~Input() {};

    /**
     * Returns an input object for decision forest model-based training
     * \param[in] id    Identifier of the input object
     * \return          %Input object that corresponds to the given identifier
     */
    data_management::NumericTablePtr get(InputId id) const;

    /**
     * Sets an input object for decision forest model-based training
     * \param[in] id      Identifier of the input object
     * \param[in] value   Pointer to the object
     */
    void set(InputId id, const data_management::NumericTablePtr &value);

    /**
    * Checks an input object for the decision forest algorithm
    * \param[in] par     Algorithm parameter
    * \param[in] method  Computation method
    * \return Status of checking
    */
    services::Status check(const daal::algorithms::Parameter *par, int method) const DAAL_C11_OVERRIDE;
};

/**
 * <a name="DAAL-CLASS-ALGORITHMS__DECISION_FOREST__REGRESSSION__TRAINING__RESULT"></a>
 * \brief Provides methods to access the result obtained with the compute() method
 *        of decision forest model-based training
 */
class DAAL_EXPORT Result : public algorithms::regression::training::Result
{
public:
    DECLARE_SERIALIZABLE_CAST(Result)
    Result();

    /**
     * Allocates memory to store the result of decision forest model-based training
     * \param[in] input Pointer to an object containing the input data
     * \param[in] method Computation method for the algorithm
     * \param[in] parameter %Parameter of decision forest model-based training
     * \return Status of allocation
     */
    template<typename algorithmFPType>
    DAAL_EXPORT services::Status allocate(const daal::algorithms::Input *input, const Parameter *parameter, const int method);

    /**
     * Returns the result of decision forest model-based training
     * \param[in] id    Identifier of the result
     * \return          Result that corresponds to the given identifier
     */
    decision_forest::regression::ModelPtr get(ResultId id) const;

    /**
     * Sets the result of decision forest model-based training
     * \param[in] id      Identifier of the result
     * \param[in] value   Result
     */
    void set(ResultId id, const ModelPtr &value);

    /**
     * Returns the result of decision forest model-based training
     * \param[in] id    Identifier of the result
     * \return          Result that corresponds to the given identifier
     */
    data_management::NumericTablePtr get(ResultNumericTableId id) const;

    /**
     * Sets the result of decision forest model-based training
     * \param[in] id      Identifier of the result
     * \param[in] value   Result
     */
    void set(ResultNumericTableId id, const data_management::NumericTablePtr &value);

    /**
     * Checks the result of decision forest model-based training
     * \param[in] input   %Input object for the algorithm
     * \param[in] par     %Parameter of the algorithm
     * \param[in] method  Computation method
     * \return Status of checking
     */
    services::Status check(const daal::algorithms::Input *input, const daal::algorithms::Parameter *par, int method) const DAAL_C11_OVERRIDE;

protected:
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
using interface1::Parameter;
using interface1::Input;
using interface1::Result;
using interface1::ResultPtr;

} // namespace training
/** @} */
} // namespace regression
}
}
} // namespace daal
#endif
