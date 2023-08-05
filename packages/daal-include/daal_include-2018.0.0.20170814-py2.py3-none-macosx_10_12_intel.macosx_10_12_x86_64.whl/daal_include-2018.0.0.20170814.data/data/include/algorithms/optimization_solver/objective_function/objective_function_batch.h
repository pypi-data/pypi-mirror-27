/* file: objective_function_batch.h */
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
//  Implementation of the Objective function types.
//--
*/

#ifndef __OBJECTIVE_FUNCTION_BATCH_H__
#define __OBJECTIVE_FUNCTION_BATCH_H__

#include "algorithms/algorithm.h"
#include "data_management/data/numeric_table.h"
#include "data_management/data/homogen_numeric_table.h"
#include "services/daal_defines.h"
#include "objective_function_types.h"

namespace daal
{
namespace algorithms
{
namespace optimization_solver
{
namespace objective_function
{

namespace interface1
{
/** @defgroup objective_function_batch Batch
 * @ingroup objective_function
 * @{
 */
/**
 * <a name="DAAL-CLASS-ALGORITHMS__OPTIMIZATION_SOLVER__OBJECTIVE_FUNCTION__BATCH"></a>
 * \brief Interface for computing the Objective function in the batch processing mode.
 *
 * \par Enumerations
 *      - \ref InputId  Identifiers of input objects for the Objective function
 *      - \ref ResultId %Result identifiers for the Objective function
 *
 * \par References
 *      - Input class
 *      - Result class
 */
class DAAL_EXPORT Batch : public daal::algorithms::Analysis<batch>
{
public:
    /**
     *  Main constructor
     */
    Batch()
    {
        initialize();
    }

    /**
     * Constructs an Objective function by copying input objects and parameters
     * of another Objective function
     * \param[in] other An algorithm to be used as the source to initialize the input objects
     *                  and parameters of the algorithm
     */
    Batch(const Batch &other)
    {
        initialize();
    }

    /** Destructor */
    virtual ~Batch() {}

    /**
    * Returns the structure that contains results of the Objective function
    * \return Structure that contains results of the Objective function
    */
    virtual objective_function::ResultPtr getResult()
    {
        return _result;
    }

    /**
     * Sets the memory for storing results of the Objective function
     * \param[in] result  Structure for storing results of the Objective function
     *
     * \return Status of computations
     */
    virtual services::Status setResult(const objective_function::ResultPtr& result)
    {
        _result = result;
        _res = _result.get();
        return services::Status();
    }

    /**
     * Returns a pointer to the newly allocated Objective function algorithm with a copy of input objects
     * of this Objective function algorithm
     * \return Pointer to the newly allocated algorithm
     */
    services::SharedPtr<Batch> clone() const
    {
        return services::SharedPtr<Batch>(cloneImpl());
    }

protected:
    virtual Batch *cloneImpl() const DAAL_C11_OVERRIDE = 0;

    void initialize()
    {
        _result = objective_function::ResultPtr(new objective_function::Result());
    }

protected:
    objective_function::ResultPtr _result;
};
/** @} */
} // namespace interface1
using interface1::Batch;

} // namespace objective_function
} // namespace optimization_solver
} // namespace algorithm
} // namespace daal
#endif
