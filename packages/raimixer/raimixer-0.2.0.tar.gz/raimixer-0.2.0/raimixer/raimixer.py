# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Copyright 2017 Juanjo Alvarez

import random
from typing import List, Dict, Optional

import raimixer.rairpc as rairpc

# TODO: precalculate the mixin rounds so I can show a nice progress bar of each round
# TODO: kosher Python package
# TODO: more tests


class RaiMixerException(Exception):
    pass


class WalletLockedException(Exception):
    pass


class RaiMixer:
    # TODO: define better arguments for init and start, or remove start()

    def __init__(self, wallet: str, num_mix_accounts=5, num_rounds=4,
                 rpc: Optional[rairpc.RaiRPC] = None) -> None:

        assert(num_mix_accounts > 1)
        assert(num_rounds > 0)

        self.wallet = wallet
        self.num_mix_accounts = num_mix_accounts
        self.num_rounds = num_rounds

        self.mix_accounts: List[str] = []
        self.balances: Dict[str, int] = {}
        self.tx_counter = 0
        self.rpc: Optional[rairpc.RaiRPC] = rpc

    def start(self, orig_account: str, dest_account: str, real_tosend: int,
              initial_tosend: int, final_send_from_multiple,
              representatives: List[str]) -> None:

        if type(real_tosend) != int or type(initial_tosend) != int:
                raise RaiMixerException('real_tosend and initial_tosend must be integers')

        self.orig_account = orig_account
        self.dest_account = dest_account
        self.initial_tosend = initial_tosend
        self.real_tosend = real_tosend
        self.final_send_from_multiple = final_send_from_multiple
        self.representatives = representatives

        if self.rpc is None:
            self.rpc = rairpc.RaiRPC(self.orig_account, self.wallet)

        if self.rpc.wallet_locked():
            raise WalletLockedException()

        self.mix_accounts = self._generate_accounts(self.num_mix_accounts)

        self._load_balances()

        # Choose the first accounts to receive funds
        num_first_dests = random.randrange(2, len(self.mix_accounts) + 1)
        first_dests = random.choices(self.mix_accounts, k=num_first_dests)

        print('\nStarting sending to initial mixing accounts...')
        self._send_one_to_many(self.orig_account, first_dests)

        # Shake it!
        for i in range(self.num_rounds):
            print('\nStarting mixing round %d...' % (i + 1))
            self._mix()

        self._send_to_dest()

        print('\nDone! Total transactions done: %d' % self.tx_counter)
        assert(self.balances[self.orig_account] == self.initial_tosend - self.real_tosend)
        assert(self.balances[self.dest_account] == self.real_tosend)

        self._delete_accounts()

    def _generate_accounts(self, num: int) -> List[str]:
        print('\nCreating mixing accounts...')
        rep = random.choice(self.representatives)
        return [self.rpc.create_account(rep) for n in range(num)]

    def _delete_accounts(self):
        for acc in self.mix_accounts:
            assert(self.rpc.account_balance(acc)[0] == 0)
            self.rpc.delete_account(acc)

    def _load_balances(self) -> None:
        for acc in self.mix_accounts:
            self.balances[acc] = 0

        self.balances[self.orig_account] = self.initial_tosend
        self.balances[self.dest_account] = 0

    def _send_one_to_many(self, from_: str, dests: List[str],
                          max_send: Optional[int] = None) -> None:
        # from_ could be in dests. This is not a bug but allows for letting some
        # amount in the from_ account if the caller want that to happen (like when mixing)

        split = self._random_amounts_split(self.balances[from_], len(dests))

        for idx, am in enumerate(split):
            if am > 0 and dests[idx] != from_:
                self._send(from_, dests[idx], am)

    def _send_many_to_one(self, froms: List[str], dest: str,
                          max_send: Optional[int] = None) -> None:
        already_sent = 0

        for acc in froms:
            balance = self.balances[acc]

            if acc == dest or balance == 0:
                continue

            tosend: int = 0
            if max_send is not None and (already_sent + balance > max_send):
                tosend = max_send - already_sent
            else:
                tosend = balance

            self._send(acc, dest, tosend)
            already_sent += tosend

            if max_send is not None:
                assert(already_sent <= max_send)
                if already_sent == max_send:
                    return

    def _send(self, orig: str, dest: str, amount: int) -> None:
        initial_tosend = self.balances[orig]
        real_tosend = self.balances[dest]

        assert(amount <= initial_tosend)

        try:
            self.balances[orig] -= amount
            self.balances[dest] += amount
            self.tx_counter += 1
            self.rpc.send_and_receive(orig, dest, amount)
        except:
            self.balances[orig] = initial_tosend
            self.balances[dest] = real_tosend
            self.tx_counter -= 1
            raise

        print("\nSending {} KRAI from [...{}] to [...{}]".format(
            amount // rairpc.KRAI_TO_RAW, orig[-8:], dest[-8:]))

        self._check_balances()
        assert(amount > 0)

    def _check_balances(self):
        total = 0

        for k, v in self.balances.items():
            total += v

        assert(total == self.initial_tosend)

    def _mix(self) -> None:
        mix_plusorig = self.mix_accounts.copy() + [self.orig_account]

        for acc, balance in self.balances.items():
            if balance > 0:
                self._send_one_to_many(acc, mix_plusorig)

    def _send_to_dest(self) -> None:
        # Move any balance in the orig account into one of the mixer accounts
        if self.balances[self.orig_account] > 0:
            print('\nMoving remaining balance in the orig account to mix accounts...')
            self._send_one_to_many(self.orig_account, self.mix_accounts)

        if not self.final_send_from_multiple:
            # Choose a single non-origin account to sent from, collect
            # all the balances to it
            send_from_acc = random.choice(self.mix_accounts)
            print('\nSending to final carrier account [%s]...' % send_from_acc)

            for acc, balance in self.balances.items():
                if acc == send_from_acc:
                    continue

                if balance > 0:
                    self._send(acc, send_from_acc, balance)

        print('\nSending to destination account...')
        self._send_many_to_one(self.mix_accounts + [self.orig_account],
                               self.dest_account, self.real_tosend)

        # Send the rest back to the orig account
        if self.initial_tosend > self.real_tosend:
            print('\nSending remaining balance back to the orig account...')
            self._send_many_to_one(self.mix_accounts, self.orig_account)

    def _random_amounts_split(self, total: int, num_accounts: int) -> List[int]:
        # loop calculating a random amount from 0 to 1/3 of the remainder until
        # the pending amount is 1/10, then send that to a random account
        tosend: Dict[int, int] = {}
        for a in range(num_accounts):
            tosend[a] = 0

        remaining = total

        while True:
            amount = random.randint(1, max(remaining // num_accounts, 1))
            dest = random.randrange(0, num_accounts)
            tosend[dest] += amount
            remaining -= amount

            if remaining == 0:
                break

            if remaining < total / len(self.mix_accounts):
                tosend[dest] += remaining
                break

        return [tosend[i] for i in tosend.keys()]
