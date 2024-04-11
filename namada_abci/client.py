import base64
import requests
from borsh_construct.core import Construct
from borsh_construct import U64, Bool, Option, Vec, TupleStruct, U8

from namada_types import Address, PublicKey, Uint, Slash, CommissionPair, ValidatorMetaData, ValidatorState, \
    WeightedValidator, StewardDetail, StoragePgfFunding, PgfParameters, StorageProposal, Vote, GovernanceParameters, \
    ProposalResult, PosParams, BondId, BondsAndUnbondsDetail, LastBlock, PrefixValue, MaspTokenRewardData, \
    Event, Account


class NamadaABCIClient:

    def __init__(self, rpc_url: str):
        self.rpc_url = rpc_url

    def abci_query(self, endpoint: str, result_struct: Construct):
        resp = requests.get(f'{self.rpc_url}/abci_query?path="{endpoint}"')
        resp = resp.json()
        value = base64.b64decode(resp['result']['response']['value'])
        return result_struct.parse(value)

    def epoch(self) -> int:
        return int(self.abci_query("/shell/epoch", U64))

    def native_token(self):
        return self.abci_query("/shell/native_token", Address)

    def epoch_at_height(self, height: int) -> int:
        return int(self.abci_query(f"/shell/epoch_at_height/{height}", U64))

    def last_block(self):
        return self.abci_query(f'/shell/last_block', Option(LastBlock))

    def first_block_height_of_current_epoch(self):
        return self.abci_query(f'/shell/first_block_height_of_current_epoch', Uint)

    def storage_value(self, key: str):
        return self.abci_query(f'/shell/value/{key}', Vec(U8))

    def storage_prefix(self, prefix: str):
        return self.abci_query(f'/shell/prefix/{prefix}', Vec(PrefixValue))

    def has_key(self, key: str) -> bool:
        return bool(self.abci_query(f'/shell/has_key/{key}', Bool))

    def masp_reward_tokens(self):
        return self.abci_query(f'/shell/masp_reward_tokens', Vec(MaspTokenRewardData))

    def is_tx_accepted(self, tx_hash: str):
        return self.abci_query(f'/shell/accepted/{tx_hash}', Option(Event))

    def is_tx_applied(self, tx_hash: str):
        return self.abci_query(f'/shell/applied/{tx_hash}', Option(Event))

    def account(self, owner: str):
        return self.abci_query(f'/shell/account/{owner}', Option(Account))

    def is_public_key_revealed(self, owner: str) -> bool:
        return bool(self.abci_query(f'/shell/revealed/{owner}', Bool))

    def ibc_client_update(self, client_id, consensus_height):
        return self.abci_query(f'/shell/ibc_client_update/{client_id}/{consensus_height}', Option(Event))

    def ibc_packet(self, event_type, source_port, source_channel, dst_port, dst_channel, sequence):
        return self.abci_query(f'/shell/ibc_packet/{event_type}/{source_port}/{source_channel}/'
                               f'{dst_port}/{dst_channel}/{sequence}', Option(Event))

    def is_validator(self, addr: str) -> bool:
        return bool(self.abci_query(f'/vp/pos/validator/is_validator/{addr}', Bool))

    def validator_consensus_key(self, addr: str):
        return self.abci_query(f"/vp/pos/validator/consensus_key/{addr}", Option(PublicKey))

    def validator_addresses(self, addr: str):
        return self.abci_query(f"/vp/pos/validator/addresses/{addr}", Vec(Address))

    def validator_stake(self, addr: str):
        return self.abci_query(f"/vp/pos/validator/stake/{addr}", Option(Uint))

    def validator_slashes(self, addr: str):
        return self.abci_query(f"/vp/pos/validator/slashes/{addr}", Vec(Slash))

    def validator_commission(self, addr: str):
        return self.abci_query(f"/vp/pos/validator/commission/{addr}", Option(CommissionPair))

    def validator_metadata(self, addr: str):
        return self.abci_query(f"/vp/pos/validator/metadata/{addr}", Option(ValidatorMetaData))

    def validator_state(self, addr: str):
        return self.abci_query(f"/vp/pos/validator/state/{addr}", Option(ValidatorState))

    def validator_incoming_redelegation(self, src_validator: str, delegator: str):
        return self.abci_query(f'/vp/pos/validator/incoming_redelegation/{src_validator}/{delegator}', Option(U64))

    def validator_last_infraction_epoch(self, validator: str):
        return self.abci_query(f'/vp/pos/validator/last_infraction_epoch/{validator}', Option(U64))

    def validator_set_consensus(self):
        return self.abci_query(f'/vp/pos/validator_set/consensus', Vec(WeightedValidator))

    def validator_set_below_capacity(self):
        return self.abci_query(f'/vp/pos/validator_set/below_capacity', Vec(WeightedValidator))

    def pos_params(self):
        return self.abci_query(f'/vp/pos/pos_params', PosParams)

    def total_stake(self):
        return self.abci_query(f'/vp/pos/total_stake', Uint)

    def delegations(self, owner: str):
        return self.abci_query(f'/vp/pos/delegations/{owner}', Vec(Address))

    def bond_deltas(self, source: str, validator: str):
        return self.abci_query(f'/vp/pos/bond_deltas/{source}/{validator}', Vec(TupleStruct(U64, Uint)))

    def bond(self, source: str, validator: str):
        return self.abci_query(f'/vp/pos/bond/{source}/{validator}', Uint)

    def rewards(self, validator: str, source: str):
        return self.abci_query(f'/vp/pos/rewards/{validator}/{source}', Uint)

    def bond_with_slashing(self, source: str, validator: str):
        return self.abci_query(f'/vp/pos/bond_with_slashing/{source}/{validator}',
                               Vec(TupleStruct(TupleStruct(U64, U64), Uint)))

    def unbond(self, source: str, validator: str):
        return self.abci_query(f'/vp/pos/unbond/{source}/{validator}', Uint)

    def unbond_with_slashing(self, source: str, validator: str):
        return self.abci_query(f'/vp/pos/unbond_with_slashing/{source}/{validator}',
                               Vec(TupleStruct(TupleStruct(U64, U64), Uint)))

    def withdrawable_tokens(self, source: str, validator: str):
        return self.abci_query(f'/vp/pos/withdrawable_tokens/{source}/{validator}', Uint)

    def bonds_and_unbonds(self, source: str, validator: str):
        return self.abci_query(f'/vp/pos/bonds_and_unbonds/{source}/to/{validator}',
                               Vec(TupleStruct(BondId, BondsAndUnbondsDetail)))

    def enqueued_slashes(self):
        return self.abci_query(f'/vp/pos/enqueued_slashes',
                               Vec(TupleStruct(Address, Vec(TupleStruct(U64, Vec(Slash))))))

    def all_slashes(self):
        return self.abci_query('/vp/pos/all_slashes', Vec(TupleStruct(Address, Vec(Slash))))

    def is_delegator(self, addr: str) -> bool:
        return bool(self.abci_query(f'/vp/pos/is_delegator/{addr}', Bool))

    def validator_by_tm_addr(self, tm_addr: str):
        return self.abci_query(f'/vp/pos/validator_by_tm_addr/{tm_addr}', Option(Address))

    def consensus_keys(self):
        return self.abci_query(f'/vp/pos/consensus_keys', Vec(PublicKey))

    def has_bonds(self, source: str) -> bool:
        return bool(self.abci_query(f'/vp/pos/has_bonds/{source}', Bool))

    def token_denomination(self, addr: str):
        return self.abci_query(f'/vp/token/denomination/{addr}', Option(U8))

    def token_total_supply(self, addr: str):
        return self.abci_query(f'/vp/token/total_supply/{addr}', Uint)

    def is_steward(self, addr: str) -> bool:
        return bool(self.abci_query(f'/vp/pgf/stewards/{addr}', Bool))

    def stewards(self):
        return self.abci_query(f'/vp/pgf/stewards', Vec(StewardDetail))

    def fundings(self):
        return self.abci_query(f'/vp/pgf/fundings', Vec(StoragePgfFunding))

    def pgf_parameters(self):
        return self.abci_query('/vp/pgf/parameters', PgfParameters)

    def proposal(self, proposal_id: int):
        return self.abci_query(f'/vp/governance/proposal/{proposal_id}', Option(StorageProposal))

    def proposal_votes(self, proposal_id: int):
        return self.abci_query(f'/vp/governance/proposal/{proposal_id}/votes', Vec(Vote))

    def governance_parameters(self):
        return self.abci_query(f'/vp/governance/parameters', GovernanceParameters)

    def stored_proposal_result(self, proposal_id: int):
        return self.abci_query(f'/vp/governance/stored_proposal_result/{proposal_id}', Option(ProposalResult))
