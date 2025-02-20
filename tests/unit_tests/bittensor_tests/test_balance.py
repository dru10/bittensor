# The MIT License (MIT)
# Copyright © 2022 Yuma Rao

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated 
# documentation files (the “Software”), to deal in the Software without restriction, including without limitation 
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, 
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of 
# the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL 
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION 
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER 
# DEALINGS IN THE SOFTWARE.

import unittest
from typing import Union

from bittensor import Balance
from tests.helpers import CLOSE_IN_VALUE
from hypothesis import given
from hypothesis import strategies as st

"""
TODO: Add tests for the balance class and new number operations
Test the Balance class
"""
valid_tao_numbers_strategy = st.one_of(st.integers(max_value=21_000_000, min_value=-21_000_000), st.floats(allow_infinity=False, allow_nan=False, allow_subnormal=False, max_value=21_000_000.00, min_value=-21_000_000.00))

def remove_zero_filter(x):
    """Remove zero and rounded to zero from the list of valid numbers"""
    return int(x * pow(10, 9)) != 0

class TestBalance(unittest.TestCase):
    @given(balance=valid_tao_numbers_strategy)
    def test_balance_init(self, balance: Union[int, float]):
        balance_ = Balance(balance)
        if isinstance(balance, int):
            assert balance_.rao == balance
        elif isinstance(balance, float):
            assert balance_.tao == CLOSE_IN_VALUE(balance, 0.00001)

    @given(balance=valid_tao_numbers_strategy, balance2=valid_tao_numbers_strategy)
    def test_balance_add(self, balance: Union[int, float], balance2: Union[int, float]):
        balance_ = Balance(balance)
        balance2_ = Balance(balance2)
        rao_: int
        rao2_: int
        if isinstance(balance, int):
            rao_ = balance
        elif isinstance(balance, float):
            rao_ = int(balance * pow(10, 9))
        if isinstance(balance2, int):
            rao2_ = balance2
        elif isinstance(balance2, float):
            rao2_ = int(balance2 * pow(10, 9))

        sum_ = balance_ + balance2_
        assert isinstance(sum_, Balance)
        assert CLOSE_IN_VALUE(sum_.rao, 5) == rao_ + rao2_

    @given(balance=valid_tao_numbers_strategy, balance2=valid_tao_numbers_strategy)
    def test_balance_add_other_not_balance(self, balance: Union[int, float], balance2: Union[int, float]):
        balance_ = Balance(balance)
        balance2_ = balance2
        rao_: int
        rao2_: int
        if isinstance(balance, int):
            rao_ = balance
        elif isinstance(balance, float):
            rao_ = int(balance * pow(10, 9))
        if isinstance(balance2, int):
            rao2_ = balance2
        elif isinstance(balance2, float):
            rao2_ = int(balance2 * pow(10, 9))

        sum_ = balance_ + balance2_
        assert isinstance(sum_, Balance)
        assert CLOSE_IN_VALUE(sum_.rao, 5) == rao_ + rao2_

    @given(balance=valid_tao_numbers_strategy, balance2=valid_tao_numbers_strategy)
    def test_balance_radd_other_not_balance(self, balance: Union[int, float], balance2: Union[int, float]):
        balance_ = Balance(balance)
        balance2_ = balance2
        rao_: int
        rao2_: int
        if isinstance(balance, int):
            rao_ = balance
        elif isinstance(balance, float):
            rao_ = int(balance * pow(10, 9))
        if isinstance(balance2, int):
            rao2_ = balance2
        elif isinstance(balance2, float):
            rao2_ = int(balance2 * pow(10, 9))

        sum_ =  balance2_ + balance_ # This is an radd
        assert isinstance(sum_, Balance)
        assert CLOSE_IN_VALUE(sum_.rao, 5) == rao2_ + rao_

    @given(balance=valid_tao_numbers_strategy, balance2=valid_tao_numbers_strategy)
    def test_balance_sub(self, balance: Union[int, float], balance2: Union[int, float]):
        balance_ = Balance(balance)
        balance2_ = Balance(balance2)
        rao_: int
        rao2_: int
        if isinstance(balance, int):
            rao_ = balance
        elif isinstance(balance, float):
            rao_ = int(balance * pow(10, 9))
        if isinstance(balance2, int):
            rao2_ = balance2
        elif isinstance(balance2, float):
            rao2_ = int(balance2 * pow(10, 9))

        diff_ = balance_ - balance2_
        assert isinstance(diff_, Balance)
        assert CLOSE_IN_VALUE(diff_.rao, 5) == rao_ - rao2_

    @given(balance=valid_tao_numbers_strategy, balance2=valid_tao_numbers_strategy)
    def test_balance_sub_other_not_balance(self, balance: Union[int, float], balance2: Union[int, float]):
        balance_ = Balance(balance)
        balance2_ = balance2
        rao_: int
        rao2_: int
        if isinstance(balance, int):
            rao_ = balance
        elif isinstance(balance, float):
            rao_ = int(balance * pow(10, 9))
        if isinstance(balance2, int):
            rao2_ = balance2
        elif isinstance(balance2, float):
            rao2_ = int(balance2 * pow(10, 9))

        diff_ =  balance_ - balance2_
        assert isinstance(diff_, Balance)
        assert CLOSE_IN_VALUE(diff_.rao, 5) == rao_ - rao2_

    @given(balance=valid_tao_numbers_strategy, balance2=valid_tao_numbers_strategy)
    def test_balance_rsub_other_not_balance(self, balance: Union[int, float], balance2: Union[int, float]):
        balance_ = Balance(balance)
        balance2_ = balance2
        rao_: int
        rao2_: int
        if isinstance(balance, int):
            rao_ = balance
        elif isinstance(balance, float):
            rao_ = int(balance * pow(10, 9))
        if isinstance(balance2, int):
            rao2_ = balance2
        elif isinstance(balance2, float):
            rao2_ = int(balance2 * pow(10, 9))

        diff_ =  balance2_ - balance_ # This is an rsub
        assert isinstance(diff_, Balance)
        assert CLOSE_IN_VALUE(diff_.rao, 5) == rao2_ - rao_

    @given(balance=valid_tao_numbers_strategy, balance2=valid_tao_numbers_strategy)
    def test_balance_mul(self, balance: Union[int, float], balance2: Union[int, float]):
        balance_ = Balance(balance)
        balance2_ = Balance(balance2)
        rao_: int
        rao2_: int
        if isinstance(balance, int):
            rao_ = balance
        elif isinstance(balance, float):
            rao_ = int(balance * pow(10, 9))
        if isinstance(balance2, int):
            rao2_ = balance2
        elif isinstance(balance2, float):
            rao2_ = int(balance2 * pow(10, 9))

        prod_ = balance_ * balance2_
        assert isinstance(prod_, Balance)
        assert CLOSE_IN_VALUE(prod_.rao, 5) == rao_ * rao2_

    @given(balance=valid_tao_numbers_strategy, balance2=valid_tao_numbers_strategy)
    def test_balance_mul_other_not_balance(self, balance: Union[int, float], balance2: Union[int, float]):
        balance_ = Balance(balance)
        balance2_ = balance2
        rao_: int
        rao2_: int
        if isinstance(balance, int):
            rao_ = balance
        elif isinstance(balance, float):
            rao_ = int(balance * pow(10, 9))
        if isinstance(balance2, int):
            rao2_ = balance2
        elif isinstance(balance2, float):
            rao2_ = int(balance2 * pow(10, 9))

        prod_ = balance_ * balance2_
        assert isinstance(prod_, Balance)
        assert CLOSE_IN_VALUE(prod_.rao, 5) == rao_ * rao2_

    @given(balance=valid_tao_numbers_strategy, balance2=valid_tao_numbers_strategy)
    def test_balance_rmul_other_not_balance(self, balance: Union[int, float], balance2: Union[int, float]):
        balance_ = Balance(balance)
        balance2_ = balance2
        rao_: int
        rao2_: int
        if isinstance(balance, int):
            rao_ = balance
        elif isinstance(balance, float):
            rao_ = int(balance * pow(10, 9))
        if isinstance(balance2, int):
            rao2_ = balance2
        elif isinstance(balance2, float):
            rao2_ = int(balance2 * pow(10, 9))

        prod_ =  balance2_ * balance_ # This is an rmul
        assert isinstance(prod_, Balance)
        assert CLOSE_IN_VALUE(prod_.rao, 5) == rao2_ * rao_

    @given(balance=valid_tao_numbers_strategy, balance2=valid_tao_numbers_strategy.filter(remove_zero_filter)) # Avoid zero division
    def test_balance_truediv(self, balance: Union[int, float], balance2: Union[int, float]):
        balance_ = Balance(balance)
        balance2_ = Balance(balance2)
        rao_: int
        rao2_: int
        if isinstance(balance, int):
            rao_ = balance
        elif isinstance(balance, float):
            rao_ = int(balance * pow(10, 9))
        if isinstance(balance2, int):
            rao2_ = balance2
        elif isinstance(balance2, float):
            rao2_ = int(balance2 * pow(10, 9))

        quot_ = balance_ / balance2_
        assert isinstance(quot_, Balance)
        assert CLOSE_IN_VALUE(quot_.rao, 5) == rao_ / rao2_

    @given(balance=valid_tao_numbers_strategy,  balance2=valid_tao_numbers_strategy.filter(remove_zero_filter))
    def test_balance_truediv_other_not_balance(self, balance: Union[int, float], balance2: Union[int, float]):
        balance_ = Balance(balance)
        balance2_ = balance2
        rao_: int
        rao2_: int
        if isinstance(balance, int):
            rao_ = balance
        elif isinstance(balance, float):
            rao_ = int(balance * pow(10, 9))
        if isinstance(balance2, int):
            rao2_ = balance2
        elif isinstance(balance2, float):
            rao2_ = int(balance2 * pow(10, 9))

        quot_ = balance_ / balance2_
        assert isinstance(quot_, Balance)
        assert CLOSE_IN_VALUE(quot_.rao, 5) == rao_ / rao2_

    @given(balance=valid_tao_numbers_strategy.filter(remove_zero_filter), balance2=valid_tao_numbers_strategy) # This is a filter to avoid division by zero
    def test_balance_rtruediv_other_not_balance(self, balance: Union[int, float], balance2: Union[int, float]):
        balance_ = Balance(balance)
        balance2_ = balance2
        rao_: int
        rao2_: int
        if isinstance(balance, int):
            rao_ = balance
        elif isinstance(balance, float):
            rao_ = int(balance * pow(10, 9))
        if isinstance(balance2, int):
            rao2_ = balance2
        elif isinstance(balance2, float):
            rao2_ = int(balance2 * pow(10, 9))

        quot_ =  balance2_ / balance_ # This is an rtruediv
        assert isinstance(quot_, Balance)
        assert CLOSE_IN_VALUE(quot_.rao, 5) == rao2_ / rao_

    @given(balance=valid_tao_numbers_strategy, balance2=valid_tao_numbers_strategy.filter(remove_zero_filter)) # Avoid zero division
    def test_balance_floordiv(self, balance: Union[int, float], balance2: Union[int, float]):
        balance_ = Balance(balance)
        balance2_ = Balance(balance2)
        rao_: int
        rao2_: int
        if isinstance(balance, int):
            rao_ = balance
        elif isinstance(balance, float):
            rao_ = int(balance * pow(10, 9))
        if isinstance(balance2, int):
            rao2_ = balance2
        elif isinstance(balance2, float):
            rao2_ = int(balance2 * pow(10, 9))

        quot_ = balance_ // balance2_
        assert isinstance(quot_, Balance)
        assert CLOSE_IN_VALUE(quot_.rao, 5) == rao_ // rao2_

    @given(balance=valid_tao_numbers_strategy,  balance2=valid_tao_numbers_strategy.filter(remove_zero_filter))
    def test_balance_floordiv_other_not_balance(self, balance: Union[int, float], balance2: Union[int, float]):
        balance_ = Balance(balance)
        balance2_ = balance2
        rao_: int
        rao2_: int
        if isinstance(balance, int):
            rao_ = balance
        elif isinstance(balance, float):
            rao_ = int(balance * pow(10, 9))
        if isinstance(balance2, int):
            rao2_ = balance2
        elif isinstance(balance2, float):
            rao2_ = int(balance2 * pow(10, 9))

        quot_ = balance_ // balance2_
        assert isinstance(quot_, Balance)
        assert CLOSE_IN_VALUE(quot_.rao, 5) == rao_ // rao2_

    @given(balance=valid_tao_numbers_strategy.filter(remove_zero_filter), balance2=valid_tao_numbers_strategy) # This is a filter to avoid division by zero
    def test_balance_rfloordiv_other_not_balance(self, balance: Union[int, float], balance2: Union[int, float]):
        balance_ = Balance(balance)
        balance2_ = balance2
        rao_: int
        rao2_: int
        if isinstance(balance, int):
            rao_ = balance
        elif isinstance(balance, float):
            rao_ = int(balance * pow(10, 9))
        if isinstance(balance2, int):
            rao2_ = balance2
        elif isinstance(balance2, float):
            rao2_ = int(balance2 * pow(10, 9))

        quot_ =  balance2_ // balance_ # This is an rfloordiv
        assert isinstance(quot_, Balance)
        assert CLOSE_IN_VALUE(quot_.rao, 5) == rao2_ // rao_   

    @given(balance=valid_tao_numbers_strategy)
    def test_balance_not_eq_none(self, balance: Union[int, float]):
        balance_ = Balance(balance)
        assert not balance_ == None

    @given(balance=valid_tao_numbers_strategy)
    def test_balance_neq_none(self, balance: Union[int, float]):
        balance_ = Balance(balance)
        assert balance_ != None
