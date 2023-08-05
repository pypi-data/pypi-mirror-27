import pytest
import typecheck
import numpy as np
from psyneulink.components.component import ComponentError
from psyneulink.components.functions.function import BogaczEtAl, DriftDiffusionIntegrator, FunctionError, NormalDist
from psyneulink.library.mechanisms.processing.integrator.ddm import DDM, DDMError
from psyneulink.scheduling.timescale import TimeScale


# ======================================= FUNCTION TESTS ============================================

# VALID FUNCTIONS:

# ------------------------------------------------------------------------------------------------
# TEST 1
# function = Integrator


def test_DDM_Integrator():
    stim = 10
    T = DDM(
        name='DDM',
        function=DriftDiffusionIntegrator(
            initializer=20.0
        ),
        time_scale=TimeScale.TIME_STEP
    )
    val = float(T.execute(stim)[0])

    T.function_object.initializer = 30.0
    val2 = float(T.execute(stim)[0])
    # assert [val, val2]  == [10, 30]

# ------------------------------------------------------------------------------------------------
# TEST 2
# function = Bogacz


def test_DDM_Integrator_Bogacz():
    stim = 10
    T = DDM(
        name='DDM',
        function=BogaczEtAl()
    )
    val = float(T.execute(stim)[0])
    assert val == 1.0

# ------------------------------------------------------------------------------------------------
# # TEST 3
# # function = Navarro

# ******
# Requires matlab import
# ******


# def test_DDM_Integrator():
#     stim = 10
#     T = DDM(
#         name='DDM',
#         function=NavarroAndFuss()
#     )
#     val = float(T.execute(stim)[0])
#     assert val == 10


# ======================================= NOISE TESTS ============================================

# VALID NOISE:

# ------------------------------------------------------------------------------------------------
# TEST 1
# noise = Single float


def test_DDM_zero_noise():
    stim = 10
    T = DDM(
        name='DDM',
        function=DriftDiffusionIntegrator(
            noise=0.0,
            rate=1.0,
            time_step_size=1.0
        ),
        time_scale=TimeScale.TIME_STEP
    )
    val = float(T.execute(stim)[0])
    assert val == 10

# ------------------------------------------------------------------------------------------------
# TEST 2
# noise = Single float


def test_DDM_noise_0_5():
    stim = 10
    T = DDM(
        name='DDM',
        function=DriftDiffusionIntegrator(
            noise=0.5,
            rate=1.0,
            time_step_size=1.0
        )
    )

    val = float(T.execute(stim)[0])

    assert val == 9.308960184035778

# ------------------------------------------------------------------------------------------------
# TEST 3
# noise = Single float


def test_DDM_noise_2_0():
    stim = 10
    T = DDM(
        name='DDM',
        function=DriftDiffusionIntegrator(
            noise=2.0,
            rate=1.0,
            time_step_size=1.0
        )
    )
    val = float(T.execute(stim)[0])
    assert val == 8.617920368071555

# ------------------------------------------------------------------------------------------------

# INVALID NOISE:

# ------------------------------------------------------------------------------------------------
# TEST 1
# noise = Single int


def test_DDM_noise_int():
    with pytest.raises(FunctionError) as error_text:
        stim = 10
        T = DDM(
            name='DDM',
            function=DriftDiffusionIntegrator(

                noise=2,
                rate=1.0,
                time_step_size=1.0
            ),
            time_scale=TimeScale.TIME_STEP
        )
        float(T.execute(stim)[0])
    assert "DriftDiffusionIntegrator requires noise parameter to be a float" in str(error_text.value)

# ------------------------------------------------------------------------------------------------
# TEST 2
# noise = Single fn


def test_DDM_noise_fn():
    with pytest.raises(FunctionError) as error_text:
        stim = 10
        T = DDM(
            name='DDM',
            function=DriftDiffusionIntegrator(

                noise=NormalDist().function,
                rate=1.0,
                time_step_size=1.0
            ),
            time_scale=TimeScale.TIME_STEP
        )
        float(T.execute(stim)[0])
    assert "DriftDiffusionIntegrator requires noise parameter to be a float" in str(error_text.value)

# ======================================= INPUT TESTS ============================================

# VALID INPUTS:

# ------------------------------------------------------------------------------------------------
# TEST 1
# input = Int


def test_DDM_input_int():
    stim = 10
    T = DDM(
        name='DDM',
        function=DriftDiffusionIntegrator(
            noise=0.0,
            rate=1.0,
            time_step_size=1.0
        ),
        time_scale=TimeScale.TIME_STEP
    )
    val = float(T.execute(stim)[0])
    assert val == 10

# ------------------------------------------------------------------------------------------------
# TEST 2
# input = List len 1


def test_DDM_input_list_len_1():
    stim = [10]
    T = DDM(
        name='DDM',
        function=DriftDiffusionIntegrator(
            noise=0.0,
            rate=1.0,
            time_step_size=1.0
        ),
        time_scale=TimeScale.TIME_STEP
    )
    val = float(T.execute(stim)[0])
    assert val == 10

# ------------------------------------------------------------------------------------------------
# TEST 3
# input = Float


def test_DDM_input_float():
    stim = 10.0
    T = DDM(
        name='DDM',
        function=DriftDiffusionIntegrator(
            noise=0.0,
            rate=1.0,
            time_step_size=1.0
        ),
        time_scale=TimeScale.TIME_STEP
    )
    val = float(T.execute(stim)[0])
    assert val == 10.0

# ------------------------------------------------------------------------------------------------

# INVALID INPUTS:

# ------------------------------------------------------------------------------------------------
# TEST 1
# input = List len 2


def test_DDM_input_list_len_2():
    with pytest.raises(DDMError) as error_text:
        stim = [10, 10]
        T = DDM(
            name='DDM',
            default_variable=[0, 0],
            function=DriftDiffusionIntegrator(

                noise=0.0,
                rate=1.0,
                time_step_size=1.0
            ),
            time_scale=TimeScale.TIME_STEP
        )
        float(T.execute(stim)[0])
    assert "must have only a single numeric item" in str(error_text.value)

# ------------------------------------------------------------------------------------------------
# TEST 2
# input = Fn

# ******
# Should functions be caught in validation, rather than with TypeError [just check callable()]?
# So that functions cause the same error as lists (see TEST 1 above)
# ******


def test_DDM_input_fn():
    with pytest.raises(TypeError) as error_text:
        stim = NormalDist().function
        T = DDM(
            name='DDM',
            function=DriftDiffusionIntegrator(

                noise=0.0,
                rate=1.0,
                time_step_size=1.0
            ),
            time_scale=TimeScale.TIME_STEP
        )
        float(T.execute(stim))
    assert "not supported for the input types" in str(error_text.value)


# ======================================= RATE TESTS ============================================

# VALID RATES:

# ------------------------------------------------------------------------------------------------
# TEST 1
# rate = Int

def test_DDM_rate_int():
    stim = 10
    T = DDM(
        name='DDM',
        function=DriftDiffusionIntegrator(
            noise=0.0,
            rate=5,
            time_step_size=1.0
        ),
        time_scale=TimeScale.TIME_STEP
    )
    val = float(T.execute(stim)[0])
    assert val == 50

#  The rate -- ndarray/list bug is fixed on devel but hasn't been pulled into scheduler yet
#  Leaving commented out for now
#
# ------------------------------------------------------------------------------------------------
# TEST 2
# rate = list len 1
#
def test_DDM_rate_list_len_1():
    stim = 10
    T = DDM(
        name='DDM',
        function=DriftDiffusionIntegrator(
            noise=0.0,
            rate=[5],
            time_step_size=1.0
        ),
        time_scale=TimeScale.TIME_STEP
    )
    val = float(T.execute(stim)[0])
    assert val == 50
#
# ------------------------------------------------------------------------------------------------
# TEST 3
# rate = float


def test_DDM_rate_float():
    stim = 10
    T = DDM(
        name='DDM',
        function=DriftDiffusionIntegrator(
            noise=0.0,
            rate=5,
            time_step_size=1.0
        ),
        time_scale=TimeScale.TIME_STEP
    )
    val = float(T.execute(stim)[0])
    assert val == 50

# ------------------------------------------------------------------------------------------------
# TEST 4
# rate = negative

# ******
# Should this pass?
# ******


def test_DDM_input_rate_negative():
    stim = [10]
    T = DDM(
        name='DDM',
        default_variable=[0],
        function=DriftDiffusionIntegrator(
            noise=0.0,
            rate=-5.0,
            time_step_size=1.0
        ),
        time_scale=TimeScale.TIME_STEP
    )
    val = float(T.execute(stim)[0])
    assert val == -50

# ------------------------------------------------------------------------------------------------

# INVALID RATES:

# ------------------------------------------------------------------------------------------------
# TEST 1
# rate = fn

# ******
# Should this pass? (Build in function logic for rate, similar to noise)?
# Should it fail with a DDM error in validate_params()?
# ******


def test_DDM_rate_fn():
    with pytest.raises(typecheck.framework.InputParameterError) as error_text:
        stim = [10]
        T = DDM(
            name='DDM',
            default_variable=[0],
            function=DriftDiffusionIntegrator(

                noise=0.0,
                rate=NormalDist().function,
                time_step_size=1.0
            ),
            time_scale=TimeScale.TIME_STEP
        )
        float(T.execute(stim)[0])
    assert "incompatible value" in str(error_text.value)

# ------------------------------------------------------------------------------------------------


# ======================================= SIZE_INITIALIZATION TESTS ============================================

# VALID INPUTS

# ------------------------------------------------------------------------------------------------
# TEST 1
# size = int, check if variable is an array of zeros


def test_DDM_size_int_check_var():
    T = DDM(
        name='DDM',
        size=1,
        function=DriftDiffusionIntegrator(
            noise=0.0,
            rate=-5.0,
            time_step_size=1.0
        ),
        time_scale=TimeScale.TIME_STEP
    )
    assert len(T.instance_defaults.variable) == 1 and T.instance_defaults.variable[0][0] == 0

# ------------------------------------------------------------------------------------------------
# TEST 2
# size = float, variable = [.4], check output after execution

def test_DDM_size_int_inputs_():
    T = DDM(
        name='DDM',
        size=1.0,
        function=DriftDiffusionIntegrator(
            noise=0.0,
            rate=-5.0,
            time_step_size=1.0
        ),
        time_scale=TimeScale.TIME_STEP
    )
    val = T.execute([.4]).tolist()
    assert val == [[-2.0], [1.0]]

# ------------------------------------------------------------------------------------------------

# INVALID INPUTS

# ------------------------------------------------------------------------------------------------
# TEST 1
# size = 0, check less-than-one error


def test_DDM_mech_size_zero():
    with pytest.raises(ComponentError) as error_text:
        T = DDM(
            name='DDM',
            size=0,
            function=DriftDiffusionIntegrator(
                noise=0.0,
                rate=-5.0,
                time_step_size=1.0
            ),
            time_scale=TimeScale.TIME_STEP
        )
    assert "is not a positive number" in str(error_text.value)

# ------------------------------------------------------------------------------------------------
# TEST 2
# size = -1.0, check less-than-one error


def test_DDM_mech_size_negative_one():
    with pytest.raises(ComponentError) as error_text:
        T = DDM(
            name='DDM',
            size=-1.0,
            function=DriftDiffusionIntegrator(
                noise=0.0,
                rate=-5.0,
                time_step_size=1.0
            ),
            time_scale=TimeScale.TIME_STEP
        )
    assert "is not a positive number" in str(error_text.value)

# ------------------------------------------------------------------------------------------------
# TEST 3
# size = 3.0, check size-too-large error


def test_DDM_size_too_large():
    with pytest.raises(DDMError) as error_text:
        T = DDM(
            name='DDM',
            size=3.0,
            function=DriftDiffusionIntegrator(
                noise=0.0,
                rate=-5.0,
                time_step_size=1.0
            ),
            time_scale=TimeScale.TIME_STEP
        )
    assert "must have only a single numeric item" in str(error_text.value)

# ------------------------------------------------------------------------------------------------
# TEST 4
# size = [1,1], check too-many-input-states error


def test_DDM_size_too_long():
    with pytest.raises(DDMError) as error_text:
        T = DDM(
            name='DDM',
            size=[1, 1],
            function=DriftDiffusionIntegrator(
                noise=0.0,
                rate=-5.0,
                time_step_size=1.0
            ),
            time_scale=TimeScale.TIME_STEP
        )
    assert "is greater than 1, implying there are" in str(error_text.value)


def test_DDM_time():

    D = DDM(
        name='DDM',
        function=DriftDiffusionIntegrator(
            noise=0.0,
            rate=-5.0,
            time_step_size=0.2,
            t0=0.5
        )
    )
    time_0 = D.function_object.previous_time                # t_0  = 0.5
    np.testing.assert_allclose(time_0, [0.5], atol=1e-08)

    time_1 = D.execute(10)[1][0]                            # t_1  = 0.5 + 0.2 = 0.7
    np.testing.assert_allclose(time_1, [0.7], atol=1e-08)

    for i in range(10):                                     # t_11 = 0.7 + 10*0.2 = 2.7
        D.execute(10)
    time_12 = D.execute(10)[1][0]                           # t_12 = 2.7 + 0.2 = 2.9
    np.testing.assert_allclose(time_12, [2.9], atol=1e-08)