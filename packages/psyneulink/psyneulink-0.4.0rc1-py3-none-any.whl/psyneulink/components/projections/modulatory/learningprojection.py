# Princeton University licenses this file to You under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.  You may obtain a copy of the License at:
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.


# *******************************************  LearningProjection **********************************************************

"""
.. _LearningProjection_Overview:

Overview
--------

A LearningProjection is a type of `ModulatoryProjection <ModulatoryProjection>` that projects from a `LearningMechanism`
to the *MATRIX* `ParameterState` of a `MappingProjection`.  It takes the `value <LearningSignal.value>` of a
`LearningSignal` of a `LearningMechanism`, and uses it to modify the value of the `matrix <MappingProjection.matrix>`
parameter of that MappingProjection.  All of the LearningProjections in a System, along with its other `learning
components <LearningMechanism_Learning_Configurations>`, can be displayed using the System's `show_graph
<System.show_graph>` method with its **show_learning** argument assigned as `True`.

.. _LearningProjection_Creation:

Creating a LearningProjection
------------------------------------

A LearningProjection can be created using any of the standard ways to `create a Projection <Projection_Creation>`,
or by including it in a `tuple <MappingProjection_Tuple_Specification>` that specifies the `matrix
<MappingProjection.matrix>` parameter of a `MappingProjection`.  LearningProjections are also created automatically,
along with the other `Components required for learning <LearningMechanism_Learning_Configurations>`, when learning is
specified for a `Process <Process_Learning_Sequence>` or a `System <System_Execution_Learning>`.

If a LearningProjection is created explicitly (using its constructor), and its **receiver** argument is not specified,
its initialization is `deferred <LearningProjection_Deferred_Initialization>`.  If it is included in the `matrix
specification <MappingProjection_Tuple_Specification>` for a `MappingProjection`, the *MATRIX* `ParameterState` for
the MappingProjection will be assigned as the LearningProjection's `receiver <LearningProjection.receiver>`.  If its
**sender** argument is not specified, its assignment depends on the **receiver**.  If the **receiver** belongs to a
MappingProjection that projects between two Mechanisms that are both in the same `Process <Process_Learning_Sequence>`
or `System <System_Execution_Learning>`, then the LearningProjection's `sender <LearningProjection.sender>` is assigned
to a `LearningSignal` of the `LearningMechanism` for the MappingProjection. If there is none, it is `created
<LearningMechanism_Creation>` along with any other components needed to implement learning for the MappingProjection
(see `LearningMechanism_Learning_Configurations`). Otherwise, the LearningProjection's initialization is `deferred
<LearningProjection_Deferred_Initialization>`.

.. _LearningProjection_Deferred_Initialization:

Deferred Initialization
~~~~~~~~~~~~~~~~~~~~~~~

When a LearningProjection is created, its full initialization is `deferred <Component_Deferred_Init>` until its
`sender <LearningProjection.sender>` and `receiver <LearningProjection.receiver>` have been fully specified.  This
allows a LearningProjection to be created before its `sender <LearningProjection.sender>` and/or `receiver
<LearningProjection.receiver>` have been created (e.g., before them in a script), by calling its constructor without
specifying its **sender** or **receiver** arguments. However, for the LearningProjection to be operational,
initialization must be completed by calling its `deferred_init` method.  This is not necessary if the
LearningProjection is included in a `tuple specification <MappingProjection_Tuple_Specification>` for the `matrix
<MappingProjection.matrix>` parameter of a `MappingProjection`, in which case deferred initialization is completed
automatically when the `LearningMechanism` associated with that MappingProjection is created for the `Process` or
`System` to which it belongs (see `LearningMechanism_Creation`).

.. _LearningProjection_Structure:

Structure
---------

.. _LearningProjection_Sender:

Sender
~~~~~~

The `sender <LearningProjection.sender>` of a LearningProjection is a `LearningSignal` of a `LearningMechanism`,
The `value <LearningSignal.value>` of the `sender <LearningProjection.sender>` -- a matrix of weight changes --
is used by the LearningProjection as its `variable <LearningProjection.variable>`;  this is also assigned to its
`learning_signal <LearningProjection.learning_signal>` attribute, and serves as the input to the LearningProjection's
`function <LearningProjection.function>`.

.. _LearningProjection_Function_and_Learning_Rate:

Function and learning_rate
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The default `function <LearningProjection.function>` of a LearningProjection is an identity function (`Linear` with
**slope**\\ =1 and **intercept**\\ =0).  However, its result can be modified by the LearningProjection's `learning_rate
<LearningProjection.learning_rate>` parameter (specified in the **learning_rate** argument of its constructor).
If specified, it is applied multiplicatively to the output of the LearningProjection's `function
<LearningProjection.function>`, and the result is assigned to the LearningProjection's `value
<LearningProjection.value>` and `weight_change_matrix <LearningProjection.weight_change_matrix>` attributes.  Thus,
the LearningProjection's `learning_rate <LearningProjection.learning_rate>` parameter can be used to modulate the the
`learning_signal <LearningProjection.learning_signal>` it receives, in addition to (and on top of) the effects of the
`learning_rate <LearningMechanism.learning_rate>` for the `LearningMechanism` from which it receives the
`learning_signal <LearningProjection.learning_signal>`. Specification of the `learning_rate
<LearningProjection.learning_rate>` for a LearningProjection supersedes any specification(s) of the
:keyword:`learning_rate` for any `Process <Process_Learning_Sequence>` and/or `System <System_Learning>` to which the
Projection belongs (see `learning_rate <LearningMechanism_Learning_Rate>` for additional details).  However, its
`learning_rate <LearningProjection.learning_rate>` can be specified by the `LearningSignal
<LearningSignal_Learning_Rate>` that is its `sender <LearningProjection.sender>`;  that specification takes precedence
over the direct specification of the `learning_rate <LearningProjection.learning_rate>` for the LearningProjection
(i.e., in the **learning_rate** argument of its constructor, or by direct assignment of a value to the attribute).  If a
`learning_rate <LearningProjection.learning_rate>` is not specified for the LearningProjection, then the result of its
`function <LearningProjection.function>` is assigned unmodified as the LearningProjection's `value
<LearningProjection.value>` (and `weight_change_matrix <LearningProjection.weight_change_matrix>` attributes.

.. _Learning_Weight_Exponent:

Weight and Exponent
~~~~~~~~~~~~~~~~~~~

Every LearningProjection has a `weight <LearningProjection.weight>` and `exponent <LearningProjection.exponent>`
attribute that are applied to its `value <LearningProjection.value>` before it is combined  with other
LearningProjections that modify the `ParameterState` for the `matrix <MappingProjection.matrix>` parameter of the
`MappingProjection` to which they project (see description under `Projection <Projection_Weight_Exponent>` for
additional details).

.. note::
   The `weight <MappingProjection.weight>` and `exponent <MappingProjection.exponent>` attributes of a
   LearningProjection are not commonly used, and are implemented largely for generalit and compatibility with other
   types of `Projection`.  They are distinct from, and are applied in addition to the LearningProjection's
   `learning_rate <LearningProjection.learning_rate>` attribute.  As noted under  `Projection
   <Projection_Weight_Exponent>`, they are not normalized and thus their effects aggregate if a ParameterState
   receives one or more LearningProjections with non-default values of their  `weight
   <MappingProjection.weight>` and `exponent <MappingProjection.exponent>` attributes.

.. _LearningProjection_Receiver:

Receiver
~~~~~~~~

The `receiver <LearningProjection.receiver>` of a LearningProject is the *MATRIX* `ParameterState` of a
`MappingProjection`, that uses the `weight_change_matrix <LearningProjection.weight_change_matrix>` provided by the
LearningProjection to modify the `matrix <MappingProjection.matrix>` parameter of the `MappingProjection` being
learned.

.. _LearningProjection_Execution:

Execution
---------

A LearningProjection cannot be executed directly.  It is executed when the *MATRIX* ParameterState to which it
projects is updated.  This occurs when the `learned_projection <LearningProjection.learned_projection>` (the
`MappingProjection` to which the *MATRIX* ParameterState belongs) is updated. Note that these events occur only
when the ProcessingMechanism that receives the `learned_projection <LearningProjection.learned_projection>` is
executed (see :ref:`Lazy Evaluation <LINK>` for an explanation of "lazy" updating). When the LearningProjection is
executed, its `function <LearningProjection.function>` gets the `learning_signal <LearningProjection.learning_signal>`
from its `sender <LearningProjection.sender>` and conveys that to its `receiver <LearningProjection.receiver>`,
possibly modified by a `learning_rate <LearningProjection.learning_rate>` if that is specified for it or its `sender
<LearningProjection.sender>` (see `above <LearningProjection_Function_and_Learning_Rate>`).

.. note::
   The changes to the `matrix <MappingProjection.matrix>` parameter of a `MappingProjection` in response to the
   execution of a LearningProjection are not applied until the `Mechanism <Mechanism>` that receives MappingProjection
   are next executed; see :ref:`Lazy Evaluation` for an explanation of "lazy" updating).


.. _LearningProjection_Class_Reference:

Class Reference
---------------

"""

import inspect

import numpy as np
import typecheck as tc

from psyneulink.components.component import InitStatus, parameter_keywords
from psyneulink.components.functions.function import BackPropagation, Linear, is_function_type
from psyneulink.components.mechanisms.adaptive.learning.learningmechanism import ERROR_SIGNAL, LearningMechanism
from psyneulink.components.mechanisms.processing.objectivemechanism import ObjectiveMechanism
from psyneulink.components.projections.modulatory.modulatoryprojection import ModulatoryProjection_Base
from psyneulink.components.projections.pathway.mappingprojection import MappingProjection
from psyneulink.components.projections.projection import Projection_Base, _is_projection_spec, projection_keywords
from psyneulink.components.states.modulatorysignals.learningsignal import LearningSignal
from psyneulink.components.states.outputstate import OutputState
from psyneulink.components.states.parameterstate import ParameterState
from psyneulink.globals.keywords import ENABLED, FUNCTION, FUNCTION_PARAMS, INITIALIZING, INTERCEPT, LEARNING, \
    LEARNING_PROJECTION, LEARNING_SIGNAL, MATRIX, PARAMETER_STATE, PARAMETER_STATES, PROJECTION_SENDER, SLOPE, NAME, \
    CONTEXT
from psyneulink.globals.preferences.componentpreferenceset import is_pref_set
from psyneulink.globals.preferences.preferenceset import PreferenceLevel
from psyneulink.globals.utilities import iscompatible, parameter_spec
from psyneulink.scheduling.timescale import CentralClock

__all__ = [
    'DefaultTrainingMechanism', 'LearningProjection', 'LearningProjectionError', 'WT_MATRIX_RECEIVERS_DIM', 'WT_MATRIX_SENDER_DIM',
]

# Params:

parameter_keywords.update({LEARNING_PROJECTION, LEARNING})
projection_keywords.update({LEARNING_PROJECTION, LEARNING})

WT_MATRIX_SENDER_DIM = 0
WT_MATRIX_RECEIVERS_DIM = 1

DefaultTrainingMechanism = ObjectiveMechanism


class LearningProjectionError(Exception):
    def __init__(self, error_value):
        self.error_value = error_value

    def __str__(self):
        return repr(self.error_value)


class LearningProjection(ModulatoryProjection_Base):
    """
    LearningProjection(               \
                 sender=None,         \
                 receiver=None,       \
                 learning_function,   \
                 learning_rate=None,  \
                 weight=None,         \
                 exponent=None,       \
                 params=None,         \
                 name=None,           \
                 prefs=None)

    Subclass of `ModulatoryProjection <ModulatoryProjection>` that modulates the value of a `ParameterState` for the
    `matrix <MappingProjection.matrix>` parameter of a `MappingProjection`.

    COMMENT:
        Description:
            The LearningProjection class is a componentType in the Projection category of Function.
            It implements a Projection from the LEARNING_SIGNAL outputState of a LearningMechanism to the MATRIX
            parameterState of a MappingProjection that modifies its matrix parameter.
            It's function takes the output of a LearningMechanism (its learning_signal attribute), and provides this
            to the parameterState to which it projects, possibly scaled by the LearningProjection's learning_rate.

        Class attributes:
            + className = LEARNING_PROJECTION
            + componentType = PROJECTION
            + paramClassDefaults (dict) :
                default
                + FUNCTION (Function): default Linear
                + FUNCTION_PARAMS (dict):
                    + SLOPE (value) : default 1
                    + INTERCEPT (value) : default 0

            + classPreference (PreferenceSet): LearningProjectionPreferenceSet, instantiated in __init__()
            + classPreferenceLevel (PreferenceLevel): PreferenceLevel.TYPE

        Class methods:
            None
    COMMENT

    Arguments
    ---------

    sender : Optional[LearningMechanism or LearningSignal]
        specifies the source of the `learning_signal <LearningProjection.learning_signal>` for the LearningProjection;
        if it is not specified, and cannot be `inferred from context <LearningProjection_Creation>`, initialization is
        `deferred <LearningProjection_Deferred_Initialization>`.

    receiver : Optional[MappingProjection or ParameterState for matrix parameter of one]
        specifies the *MATRIX* `ParameterState` (or the `MappingProjection` that owns it) for the `matrix
        <MappingProjection.matrix>` of the `learned_projection <LearningProjection.learned_projection>` to be
        modified by the LearningProjection; if it is not specified, and cannot be `inferred from context
        <LearningProjection_Creation>`, initialization is `deferred <LearningProjection_Deferred_Initialization>`.

    function : TransferFunction : default Linear(slope=1, intercept=0)
        specifies the function used to convert the `learning_signal` to the `weight_change_matrix
        <LearningProjection.weight_change_matrix>`, prior to applying the `learning_rate
        <LearningProjection.learning_rate>`.

    learning_function : Optional[LearningFunction or function] : default BackPropagation
        specifies a function to be used for learning by the `LearningMechanism` to which the
        LearningProjection's `sender <LearningProjection.sender>` belongs.

        .. note::
           the **learning_function** argument is implemented to preserve backward compatibility with previous versions;
           its use is not advised.

    learning_rate : Optional[float or int]
        if specified, it is applied multiplicatively to the `learning_signal <LearningProjection.learning_signal>`
        received from the `sender <LearningProjection.sender>`; specification of the `learning_rate
        <LearningProjection.learning_rate>` for a LearningProjection supersedes any specification(s) of the
        :keyword:`learning_rate` for any `Process <Process_Learning_Sequence>` and/or `System <System_Learning>` to
        which the LearningProjection belongs, and is applied in addition to any effects of the `learning_rate
        <LearningMechanism.learning_rate>` for the `LearningMechanism` from which the LearningProjection receives its
        `learning_signal <LearningProjection.learning_signal>` (see `LearningProjection_Function_and_Learning_Rate` for
        additional details).

    weight : number : default None
       specifies the value by which to multiply the LearningProjection's `value <LearningProjection.value>`
       before combining it with others (see `weight <LearningProjection.weight>` for additional details).

    exponent : number : default None
       specifies the value by which to exponentiate the LearningProjection's `value <LearningProjection.value>`
       before combining it with others (see `exponent <LearningProjection.exponent>` for additional details).

    params : Dict[param keyword, param value] : default None
        a `parameter dictionary <ParameterState_Specification>` that specifies the parameters for the
        Projection, its function, and/or a custom function and its parameters. By default, it contains an entry for
        the Projection's default `function <LearningProjection.function>` and parameter assignments.  Values specified
        for parameters in the dictionary override any assigned to those parameters in arguments of the constructor.

    name : str : default see ModulatoryProjection `name <ModulatoryProjection.name>`
        specifies the name of the LearningProjection.

    prefs : PreferenceSet or specification dict : default Projection.classPreferences
        specifies the `PreferenceSet` for the LearningProjection; see `prefs <LearningProjection.prefs>` for details.


    Attributes
    ----------

    componentType : LEARNING_PROJECTION

    sender : LearningSignal
        source of `learning_signal <LearningProjection.learning_signal>`
        (see `LearningProjection_Sender` for additional details).

    receiver : MATRIX ParameterState of a MappingProjection
        *MATRIX* `ParameterState` for the `matrix <MappingProjection.MappingProjection.matrix>` parameter of the
        `learned_projection <LearningProjection.learned_projection>` (see `LearningProjection_Receiver` for additional
        details).

    learned_projection : MappingProjection
        the `MappingProjection` to which LearningProjection's `receiver <LearningProjection.receiver>` belongs.

    variable : 2d np.array
        same as `learning_signal <LearningProjection.learning_signal>`.

    learning_enabled : bool : default True
        determines whether the `value <LearningProjection.value>` of the LearningProjection is used to modify
        the `learned_projection <LearningProjection.learned_projection>` when the latter is executed;  its value is
        set by the value of the `learning_enabled <LearningMechanism.learning_enabled>` attribute of the
        `LearningMechanism` to which the LearningProjection's `sender <LearningProjection.sender>` belongs.

    learning_signal : 2d np.array
        the `value <LearningSignal.value>` of the LearningProjection's `sender <LearningProjectoin.sender>`: a matrix of
        weight changes calculated by the `LearningMechanism` to which the `sender <LearningProjection.sender>` belongs;
        rows correspond to the `sender <MappingProjection.sender>` of the `learned_projection <LearningProjection>`,
        and columns to its `receiver <MappingProjection.receiver>` (i.e., the input and output of the
        `learned_projection <LearningProjection>`, respectively).

    function : Function
        assigns the `learning_signal` received from the `sender <LearningProjection.sender>` to the
        LearningProjection's `value <LearningProjection.value>`, possibly modified by its `learning_rate
        <LearningProjection.learning_rate>`; the default in an identity function.

    learning_rate : float or `None`
        determines the learning_rate for the LearningProjection.  If specified, it is applied multiplicatively to the
        `learning_signal <LearningProjection.learning_signal>`; its specification may be superseded by the
        `learning_rate <LearningSignal.learning_rate>` of its `sender <LearningProjection.sender>`
        (see `LearningProjection_Function_and_Learning_Rate` for additional details);

    weight_change_matrix : 2d np.array
        output of the LearningProjection's `function <LearningProjection.function>`, possibly modified by its
        `learning_rate <LearningProjection.learning_rate>`;  reflects the matrix of weight changes to be made to the
        `matrix <MappingProjection.matrix>` parameter of the `learned_projection
        <LearningProjection.learned_projection>` (rows correspond to the `sender <MappingProjection.sender>` of the
        `learned_projection <LearningProjection.learned_projection>`, columns to its `receiver
        <MappingProjection.receiver>` (i.e., the input and output of the `learned_projection
        <LearningProjection.learned_projection>`, respectively).

    value : 2d np.array
        same as `weight_change_matrix`.

    weight : number
       multiplies the `value <LearningProjection.value>` of the LearningProjection after applying `exponent
       <LearningProjection.exponent>`, and before combining it with any others that project to the `ParameterState`
       for the `matrix <MappingProjection.matrix>` parameter of the same `MappingProjection` to determine how that
       MappingProjection's `matrix <MappingProjection.matrix>` is modified (see `description above
       <LearningProjection_Weight_and_Exponent>` for additional details, including relationship to `learning_rate
       <LearningProjection.learning_rate>`).

    exponent : number
        exponentiates the `value <LearningProjection.value>` of the LearningProjection, before applying `weight
        <ControlProjection.weight>`, and before combining it with any others that project to the `ParameterState`
       for the `matrix <MappingProjection.matrix>` parameter of the same `MappingProjection` to determine how that
       MappingProjection's `matrix <MappingProjection.matrix>` is modified (see `description above
       <LearningProjection_Weight_and_Exponent>` for additional details, including relationship to `learning_rate
       <LearningProjection.learning_rate>`).

    name : str
        name of the LearningProjection; if it is not specified in the **name** argument of its constructor,
        a default name is assigned (see ModulatoryProjection `name <ModulatoryProjection.name>`;
        also see `Naming` for conventions regarding duplicate names).

    prefs : PreferenceSet or specification dict
        the `PreferenceSet` for the LearningProjection; if it is not specified in the **prefs** argument of the
        constructor, a default is assigned using `classPreferences` defined in __init__.py (see :doc:`PreferenceSet
        <LINK>` for details).

    """

    componentType = LEARNING_PROJECTION
    className = componentType
    suffix = " " + className

    classPreferenceLevel = PreferenceLevel.TYPE

    class sockets:
        sender=[LEARNING_SIGNAL]
        receiver=[PARAMETER_STATE]

    class ClassDefaults(ModulatoryProjection_Base.ClassDefaults):
        variable = None

    paramClassDefaults = Projection_Base.paramClassDefaults.copy()
    paramClassDefaults.update({PROJECTION_SENDER: LearningMechanism,
                               PARAMETER_STATES: NotImplemented, # This suppresses parameterStates
                               FUNCTION: Linear,
                               FUNCTION_PARAMS:
                                   {SLOPE: 1,
                                    INTERCEPT: 0},
                               })

    @tc.typecheck
    def __init__(self,
                 sender:tc.optional(tc.any(LearningSignal, LearningMechanism))=None,
                 receiver:tc.optional(tc.any(ParameterState, MappingProjection))=None,
                 learning_function:tc.optional(is_function_type)=BackPropagation,
                 # FIX: 10/3/17 - TEST IF THIS OK AND REINSTATE IF SO
                 # learning_signal_params:tc.optional(dict)=None,
                 learning_rate:tc.optional(tc.any(parameter_spec))=None,
                 weight=None,
                 exponent=None,
                 params:tc.optional(dict)=None,
                 name=None,
                 prefs:is_pref_set=None,
                 context=None):

        # IMPLEMENTATION NOTE:
        #     the learning_function argument is implemented to preserve the ability to pass a learning function
        #     specification from the specification of a LearningProjection (used to implement learning for a
        #     MappingProjection, e.g., in a tuple) to the LearningMechanism responsible for implementing the function

        # Assign args to params and functionParams dicts (kwConstants must == arg names)
        params = self._assign_args_to_param_dicts(learning_function=learning_function,
                                                  learning_rate=learning_rate,
                                                  # FIX: 10/3/17 - TEST IF THIS OK AND REINSTATE IF SO
                                                  # learning_signal_params=learning_signal_params,
                                                  weight=weight,
                                                  exponent=exponent,
                                                  params=params)

        # If receiver has not been assigned, defer init to State.instantiate_projection_to_state()
        if sender is None or receiver is None:
            # Flag for deferred initialization
            self.init_status = InitStatus.DEFERRED_INITIALIZATION
        super().__init__(sender=sender,
                         receiver=receiver,
                         weight=weight,
                         exponent=exponent,
                         params=params,
                         name=name,
                         prefs=prefs,
                         context=self)
        self.learning_enable = True


    def _validate_params(self, request_set, target_set=None, context=None):
        """Validate sender and receiver

        Insure `sender <LearningProjection>` is a LearningMechanism or the OutputState of one.
        Insure `receiver <LearningProjection>` is a MappingProjection or the matrix ParameterState of one.
        """

        # IMPLEMENTATION NOTE: IS TYPE CHECKING HERE REDUNDANT WITH typecheck IN __init__??

        super()._validate_params(request_set=request_set, target_set=target_set, context=context)

        if INITIALIZING in context:
            # VALIDATE SENDER
            sender = self.sender
            if isinstance(sender, LearningMechanism):
                if len(sender.learning_signals) > 1:
                    raise LearningProjectionError("PROGRAM ERROR: {} has more than one LearningSignal "
                                                  "which is not currently supported".format(sender.name))
                sender = self.sender = sender.learning_signals[0]

            if any(s in {OutputState, LearningSignal, LearningMechanism} for s in {sender, type(sender)}):
                # If it is the outputState of a LearningMechanism, check that it is a list or 1D np.array
                if isinstance(sender, OutputState):
                    if not isinstance(sender.value, (list, np.ndarray)):
                        raise LearningProjectionError("Sender for \'{}\' (OutputState of LearningMechanism \'{}\') "
                                                      "must be a list or 1D np.array".format(self.name, sender.name))
                    if not np.array(sender.value).ndim >= 1:
                        raise LearningProjectionError("OutputState of \'{}\' (LearningMechanism for \'{}\') must be "
                                                      "an ndarray with dim >= 1".format(sender.owner.name, self.name))
                # If specification is a LearningMechanism class, pass (it will be instantiated in _instantiate_sender)
                elif inspect.isclass(sender) and issubclass(sender,  LearningMechanism):
                    pass

            else:
                raise LearningProjectionError("The sender arg for {} ({}) must be a LearningMechanism, "
                                              "the OutputState or LearningSignal of one, or a reference to the class"
                                              .format(self.name, sender.name))


            # VALIDATE RECEIVER
            receiver = self.receiver
            if isinstance(receiver, MappingProjection):
                try:
                    receiver = self.receiver = receiver._parameter_states[MATRIX]
                except KeyError:
                    raise LearningProjectionError("The MappingProjection {} specified as the receiver for {} "
                                                  "has no MATRIX parameter state".format(receiver.name, self.name))
            if not any(s in {ParameterState, MappingProjection} for s in {receiver, type(receiver)}):
                raise LearningProjectionError("The receiver arg for {} must be a MappingProjection "
                                              "or the MATRIX parameterState of one."
                                              .format(PROJECTION_SENDER, sender, self.name, ))

    def _instantiate_sender(self, context=None):
        """Instantiate LearningMechanism
        """

        # LearningMechanism was specified by class or was not specified,
        #    so call composition for "automatic" instantiation of a LearningMechanism
        # Note: this also instantiates an ObjectiveMechanism if necessary and assigns it the necessary projections
        if not isinstance(self.sender, (OutputState, LearningMechanism)):
            from psyneulink.components.mechanisms.adaptive.learning.learningauxilliary \
                import _instantiate_learning_components
            _instantiate_learning_components(learning_projection=self,
                                             context=context + " " + self.name)

        if isinstance(self.sender, OutputState) and not isinstance(self.sender.owner, LearningMechanism):
            raise LearningProjectionError("Sender specified for LearningProjection {} ({}) is not a LearningMechanism".
                                          format(self.name, self.sender.owner.name))

        # This assigns self as an outgoing projection from the sender (LearningMechanism) outputState
        #    and formats self.instance_defaults.variable to be compatible with that outputState's value
        #    (i.e., its learning_signal)
        super()._instantiate_sender(context=context)

        if self.sender.learning_rate is not None:
            self.learning_rate = self.sender.learning_rate

    def _instantiate_receiver(self, context=None):
        """Validate that receiver has been assigned and is compatible with the output of function

        Notes:
        * _validate_params verifies that receiver is a parameterState for the matrix parameter of a MappingProjection.
        * _super()._instantiate_receiver verifies that the projection has not already been assigned to the receiver.

        """

        super()._instantiate_receiver(context=context)

        # Insure that the learning_signal is compatible with the receiver's weight matrix
        if not iscompatible(self.value, self.receiver.instance_defaults.variable):
            raise LearningProjectionError("The learning_signal of {} ({}) is not compatible with the matrix of "
                                          "the MappingProjection ({}) to which it is being assigned ({})".
                                          format(self.name,
                                                 self.value,
                                                 self.receiver.value,
                                                 self.receiver.owner.name))

        # Insure that learning_signal has the same shape as the receiver's weight matrix
        try:
            receiver_weight_matrix_shape = np.array(self.receiver.value).shape
        except TypeError:
            receiver_weight_matrix_shape = 1
        try:
            learning_signal_shape = np.array(self.value).shape
        except TypeError:
            learning_signal_shape = 1


        # FIX: SHOULD TEST WHETHER IT CAN BE USED, NOT WHETHER IT IS THE SAME SHAPE
        # # MODIFIED 3/8/17 OLD:
        # if receiver_weight_matrix_shape != learning_signal_shape:
        #     raise ProjectionError("Shape ({}) of learing_signal matrix for {} from {}"
        #                           " must match shape of the weight matrix ({}) for the receiver {}".
        #                           format(learning_signal_shape,
        #                                  self.name,
        #                                  self.sender.name,
        #                                  receiver_weight_matrix_shape,
        #                                  self.receiver.owner.name))
        # MODIFIED 3/8/17 END

        learning_mechanism = self.sender.owner
        learned_projection = self.receiver.owner

        # Check if learning_mechanism receives a projection from an ObjectiveMechanism;
        #    if it does, assign it to the objective_mechanism attribute for the projection being learned
        # # MODIFIED 9/22/17 OLD:
        # candidate_objective_mech = learning_mechanism.input_states[ERROR_SIGNAL].path_afferents[0].sender.owner
        # if isinstance(candidate_objective_mech, ObjectiveMechanism) and candidate_objective_mech._role is LEARNING:
        #     learned_projection.objective_mechanism = candidate_objective_mech
        # MODIFIED 9/22/17 NEW:
        try:
            candidate_objective_mech = learning_mechanism.input_states[ERROR_SIGNAL].path_afferents[0].sender.owner
            if isinstance(candidate_objective_mech, ObjectiveMechanism) and candidate_objective_mech._role is LEARNING:
                learned_projection.objective_mechanism = candidate_objective_mech
        except TypeError:
            # learning_mechanism does not receive from an ObjectiveMechanism
            #    (e.g., AutoAssociativeLearningMechanism, which receives straight from a ProcessingMechanism)
            pass
        # MODIFIED 9/22/17 END
        learned_projection.learning_mechanism = learning_mechanism
        learned_projection.has_learning_projection = True


    def execute(self, input=None, clock=CentralClock, time_scale=None, params=None, context=None):
        """
        :return: (2D np.array) self.weight_change_matrix
        """

        params = params or {}

        # Pass during initialization (since has not yet been fully initialized
        if self.init_status is InitStatus.DEFERRED_INITIALIZATION:
            return self.init_status

        # if self.learning_rate:
        #     params.update({SLOPE:self.learning_rate})

        self.weight_change_matrix = self.function(variable=self.sender.value,
                                                  params=params,
                                                  context=context)

        if self.learning_rate is not None:
            self.weight_change_matrix *= self.learning_rate


        if not INITIALIZING in context and self.reportOutputPref:
            print("\n{} weight change matrix: \n{}\n".format(self.name, self.weight_change_matrix))

        # TEST PRINT
        # print("\n@@@ WEIGHT CHANGES FOR {} TRIAL {}:\n{}".format(self.name, CentralClock.trial, self.value))
        # print("\n@@@ WEIGHT CHANGES CALCULATED FOR {} TRIAL {}".format(self.name, CentralClock.trial))
        # TEST DEBUG MULTILAYER
        # print("\n{}\n@@@ WEIGHT CHANGES FOR {} TRIAL {}:\n{}".
        #       format(self.__class__.__name__.upper(), self.name, CentralClock.trial, self.value))

        return self.value

    @property
    def learning_signal(self):
        return self.sender.value

    @property
    def weight_change_matrix(self):
        return self.value

    @weight_change_matrix.setter
    def weight_change_matrix(self,assignment):
        self.value = assignment
