/* file: neural_networks_prediction_types.h */
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
//  Implementation of neural network algorithm interface.
//--
*/

#ifndef __NEURAL_NETWORKS_PREDICTION_TYPES_H__
#define __NEURAL_NETWORKS_PREDICTION_TYPES_H__

#include "algorithms/algorithm.h"

#include "data_management/data/data_serialize.h"
#include "services/daal_defines.h"
#include "algorithms/neural_networks/layers/layer_forward.h"
#include "algorithms/neural_networks/neural_networks_prediction_input.h"
#include "algorithms/neural_networks/neural_networks_prediction_result.h"

namespace daal
{
namespace algorithms
{
/**
 * @defgroup neural_networks_prediction Prediction
 * \copydoc daal::algorithms::neural_networks::prediction
 * @ingroup neural_networks
 * @{
 */
/**
 * \brief Contains classes for prediction and prediction using neural network
 */
namespace neural_networks
{
/**
* \brief Contains classes for making prediction based on the trained model
*/
namespace prediction
{
/**
 * <a name="DAAL-ENUM-ALGORITHMS__NEURAL_NETWORKS__PREDICTION__METHOD"></a>
 * \brief Computation methods for the neural network model based prediction
 */
enum Method
{
    defaultDense = 0,     /*!< Feedforward neural network */
    feedforwardDense = 0  /*!< Feedforward neural network */
};

}
}
/** @} */
}
} // namespace daal

#endif
