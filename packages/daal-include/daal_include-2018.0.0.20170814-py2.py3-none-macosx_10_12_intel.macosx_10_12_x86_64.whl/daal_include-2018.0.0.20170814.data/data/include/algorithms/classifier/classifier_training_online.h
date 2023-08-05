/* file: classifier_training_online.h */
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
//  Implementation of the interface for the classifier model training algorithm.
//--
*/

#ifndef __CLASSIFIER_TRAINING_ONLINE_H__
#define __CLASSIFIER_TRAINING_ONLINE_H__

#include "services/daal_defines.h"

namespace daal
{
namespace algorithms
{
namespace classifier
{
namespace training
{

namespace interface1
{
/**
 * @defgroup classifier_training_online Online
 * @ingroup training
 * @{
 */
/**
 * <a name="DAAL-CLASS-ALGORITHMS__CLASSIFIER__TRAINING__ONLINE"></a>
 *  \brief Algorithm class for training the classifier model in the online processing mode
 *
 * \par Enumerations
 *      - \ref InputId  %Input objects of the classifier model training algorithm
 *      - \ref ResultId Results of the classifier model training algorithm
 *
 * \par References
 *      - \ref interface1::Parameter "Parameter" class
 *      - \ref interface1::Model "Model" class
 */
class DAAL_EXPORT Online : public Training<online>
{
public:
    Input input;     /*!< %Input objects of the algorithm */

    Online()
    {
        initialize();
    }

    /**
     * Constructs a classifier training algorithm by copying input objects and parameters
     * of another classifier training algorithm
     * \param[in] other An algorithm to be used as the source to initialize the input objects
     *                  and parameters of the algorithm
     */
    Online(const Online &other) : input(other.input)
    {
        initialize();
    }

    virtual ~Online() {}

    /**
     * Registers user-allocated memory for storing partial training results
     * \param[in] partialResult Structure for storing partial results
     * \param[in] initFlag Flag if partial result initialized or not
     */
    services::Status setPartialResult(const PartialResultPtr &partialResult, bool initFlag = false)
    {
        _partialResult = partialResult;
        _pres = _partialResult.get();
        setInitFlag(initFlag);
        return services::Status();
    }

    /**
     * Registers user-allocated memory for storing results of the classifier model training algorithm
     * \param[in] res    Structure for storing results of the classifier model training algorithm
     */
    services::Status setResult(const ResultPtr& res)
    {
        DAAL_CHECK(res, services::ErrorNullResult)
        _result = res;
        _res = _result.get();
        return services::Status();
    }

    /**
     * Returns the structure that contains computed partial results of the classification algorithm
     * \return Structure that contains computed partial results
     */
    PartialResultPtr getPartialResult() { return _partialResult; }

    /**
     * Returns the structure that contains results of the classification algorithm
     * \return Structure that contains computed results
     */
    ResultPtr getResult() { return _result; }

    /**
     * Returns a pointer to the newly allocated classifier training algorithm with a copy of input objects
     * and parameters of this classifier training algorithm
     * \return Pointer to the newly allocated algorithm
     */
    services::SharedPtr<Online> clone() const
    {
        return services::SharedPtr<Online>(cloneImpl());
    }

protected:
    PartialResultPtr _partialResult;
    ResultPtr _result;

    void initialize()
    {
        _in = &input;
    }
    virtual Online * cloneImpl() const DAAL_C11_OVERRIDE = 0;
};
/** @} */
} // namespace interface1
using interface1::Online;

}
}
}
}
#endif
