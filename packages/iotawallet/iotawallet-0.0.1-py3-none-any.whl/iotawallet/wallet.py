import time
from typing import cast, List, Dict, Iterable, Optional

from iota import (
    Iota, ProposedTransaction, Address, Bundle, TransactionHash, Transaction
)

DEPTH = 3


class WalletException(Exception):
    pass


class BundleAlreadyPromoted(WalletException):
    pass


class _Account:
    def __init__(self,
                 addresses: List[Address],
                 balance: int,
                 bundles: List[Bundle]) -> None:
        self.addresses = addresses
        self.balance = balance

        confirmed_bundles = {
            bundle.hash: bundle for bundle in bundles if bundle.is_confirmed
        }

        duplicates: List[Bundle] = []
        unconfirmed: Dict[TransactionHash, Bundle] = {}

        for bundle in bundles:
            if bundle.is_confirmed:
                # Already got these
                pass
            else:
                if bundle.hash in confirmed_bundles:
                    duplicates.append(bundle)
                elif bundle.hash in unconfirmed:
                    # Check timestamps
                    unconfirmed_bundle = unconfirmed[bundle.hash]
                    bundle_timestamp = bundle.tail_transaction.attachment_timestamp
                    unconfirmed_timestamp = unconfirmed_bundle.tail_transaction.attachment_timestamp
                    if bundle_timestamp > unconfirmed_timestamp:
                        duplicates.append(unconfirmed_bundle)
                        unconfirmed[bundle.hash] = bundle
                    else:
                        duplicates.append(bundle)
                else:
                    unconfirmed[bundle.hash] = bundle

        self._confirmed_bundles = confirmed_bundles
        self.duplicate_bundles = duplicates
        self._unconfirmed_bundles = unconfirmed

    @property
    def confirmed_bundles(self) -> Iterable[Bundle]:
        return self._confirmed_bundles.values()

    @property
    def unconfirmed_bundles(self) -> Iterable[Bundle]:
        return self._unconfirmed_bundles.values()


class Wallet:
    """docstring for Wallet"""
    def __init__(self,
                 uri: str,
                 seed: Optional[str] = None) -> None:
        self._iota_api = Iota(uri, seed)
        self.uri = uri
        self.seed = self._iota_api.seed

        self._account = self._get_account()

    @property
    def addresses(self) -> List[Address]:
        return self._account.addresses

    @property
    def balance(self) -> int:
        return self._account.balance

    @property
    def bundles(self) -> Dict[str, Iterable[Bundle]]:
        return {
            'confirmed': self._account.confirmed_bundles,
            'unconfirmed': self._account.unconfirmed_bundles,
            'duplicate': self._account.duplicate_bundles,
        }

    def retry_unconfirmed_bundles(self,
                                  *bundles: Bundle) -> None:
        if len(bundles) == 0:
            bundles = tuple(self.bundles['unconfirmed'])
        for bundle in bundles:
            print(f'Retrying bundle: {bundle.hash}')
            if not self._is_promotable(bundle):
                bundle = self._reattach(bundle)
                while True:
                    time.sleep(2)
                    if self._is_promotable(bundle):
                        break
            for attempt in range(5):
                try:
                    promote_bundle = self._promote(bundle)
                except BundleAlreadyPromoted:
                    break
                else:
                    print(f'Promotion attempt ({attempt}): Bundle {promote_bundle.hash}')

    def _get_account(self) -> _Account:
        response = self._iota_api.get_account_data(inclusion_states=True)
        addresses = response['addresses']
        balance = response['balance']
        bundles = response['bundles']

        return _Account(addresses, balance, bundles)

    def _is_above_max_depth(self,
                            transaction: Transaction) -> bool:
        current_millis = time.time() * 1000
        max_age = 11 * 60 * 1000  # 11 minutes
        diff = current_millis - cast(float, transaction.attachment_timestamp)
        return (0 < diff < max_age)

    def _is_promotable(self,
                       bundle: Bundle) -> bool:
        return (
            self._is_above_max_depth(bundle.tail_transaction) and
            self._iota_api.is_promotable(bundle.tail_transaction.hash)
        )

    def _reattach(self,
                  bundle: Bundle) -> Bundle:
        response = self._iota_api.replay_bundle(
            bundle.tail_transaction.hash,
            DEPTH,
        )
        return Bundle.from_tryte_strings(response['trytes'])

    def _promote(self,
                 bundle: Bundle) -> Bundle:
        tail_hash = bundle.tail_transaction.hash
        response = self._iota_api.get_latest_inclusion([tail_hash])
        if response['states'][tail_hash]:
            raise BundleAlreadyPromoted()

        spam_transfer = ProposedTransaction(
            address=Address(b'9' * 81),
            value=0,
        )
        options = {
            'reference': tail_hash
        }

        response = self._iota_api.send_transfer(
            seed=spam_transfer.address,
            depth=DEPTH,
            transfers=[spam_transfer],
            options=options,
        )
        return response['bundle']

    # def get_new_address(self) -> Address:
    #     return self.get_new_addresses

    def get_addresses(self,
                      index: int = 0,
                      count: int = 1) -> Iterable[Address]:
        response = self._iota_api.get_new_addresses(index, count)
        return cast(Iterable[Address], response['addresses'])

    def get_balances(self,
                     *addresses: Iterable[Address]) -> Iterable[int]:
        response = self._iota_api.get_balances(addresses)
        return cast(Iterable[int], response['balances'])

    def attach_address(self,
                       address: Address) -> None:
        proposed_transaction = ProposedTransaction(address, value=0)
        self._iota_api.send_transfer(depth=DEPTH, transfers=[proposed_transaction])
