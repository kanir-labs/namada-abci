from borsh_construct import CStruct, TupleStruct, Enum, U8, U64, String, Option, Vec


AddressHash = TupleStruct(U8[20])

InternalAddress = TupleStruct(Enum(
    'PoS',
    'PosSlashPool',
    'Parameters',
    'Ibc',
    'IbcToken' / AddressHash,
    'Governance',
    'EthBridge',
    'EthBridgePool',
    'Erc20' / AddressHash,
    'Nut' / AddressHash,
    'Multitoken',
    'Pgf',
    'Masp',
    enum_name="InternalAddress"
))

_Address = Enum(
    'Established' / AddressHash,
    'Implicit' / AddressHash,
    'Internal' / InternalAddress,
    enum_name='Address'
)

Address = CStruct(
    'value' / _Address
)

Ed25519 = CStruct(
    'key' / U8[32]
)

Secp256k1 = CStruct(
    'key' / U8[33]
)

PublicKey = Enum(
    'Ed25519' / Ed25519,
    'Secp256k1' / Secp256k1,
    enum_name='PublicKey'
)

Uint = CStruct(
    'raw' / U8[256]
)
Dec = CStruct(
    'raw' / U8[256]
)

SlashType = TupleStruct(Enum(
    'DuplicateVote',
    'LightClientAttack',
    enum_name='SlashType'
))

Slash = CStruct(
    'epoch' / U64,
    'block_height' / U64,
    'r#type' / SlashType,
    'rate' / Dec
)

CommissionPair = CStruct(
    'commission_rate' / Dec,
    'max_commission_change_per_epoch' / Dec
)

ValidatorMetaData = CStruct(
    'email' / String,
    'description' / Option(String),
    'website' / Option(String),
    'discord_handle' / Option(String),
    'avatar' / Option(String)
)

ValidatorState = TupleStruct(Enum(
    'Consensus',
    'BelowCapacity',
    'BelowThreshold',
    'Inactive',
    'Jailed',
    enum_name='ValidatorState'
))

WeightedValidator = CStruct(
    'bonded_stake' / Uint,
    'address' / Address
)

StewardDetail = CStruct(
    'address' / Address,
    'reward_distribution' / Vec(TupleStruct(Address, Dec))
)

PGFInternalTarget = CStruct(
    'target' / Address,
    'amount' / Uint,
)

PGFIbcTarget = CStruct(
    'target' / String,
    'amount' / Uint,
    'port_id' / String,
    'channel_id' / String,
)

PGFTarget = TupleStruct(Enum(
    'Internal' / PGFInternalTarget,
    'Ibc' / PGFIbcTarget,
    enum_name='PGFTarget'
))

StoragePgfFunding = CStruct(
    'detail' / PGFTarget,
    'id' / U64
)

PgfParameters = CStruct(
    'stewards' / Vec(Address),
    'pgf_inflation_rate' / Dec,
    'stewards_inflation_rate' / Dec,
)

AddRemoveAddress = TupleStruct(Enum(
    'Add' / Address,
    'Remove' / Address,
    enum_name='AddRemoveAddress'
))

AddRemovePGFTarget = TupleStruct(Enum(
    'Add' / PGFTarget,
    'Remove' / PGFTarget,
    enum_name='AddRemovePGFAction'
))

PGFAction = TupleStruct(Enum(
    'Continuous' / AddRemovePGFTarget,
    'Retro' / PGFTarget,
    enum_name='PGFAction'
))

OptionHash = CStruct(
    'value' / Option(U8[32])
)

AddRemoveAddresses = CStruct(
    'value' / Vec(AddRemoveAddress)
)

PGFActions = CStruct(
    'value' / Vec(PGFAction)
)

ProposalType = TupleStruct(Enum(
    'Default' / OptionHash,
    'PGFSteward' / AddRemoveAddresses,
    'PGFPayment' / PGFActions,
    enum_name='ProposalType'
))

StorageProposal = CStruct(
    'id' / U64,
    'content' / Vec(TupleStruct(String, String)),
    'author' / Address,
    'r#type' / ProposalType,
    'voting_start_epoch' / U64,
    'voting_end_epoch' / U64,
    'voting_end_epoch' / U64
)

ProposalVote = TupleStruct(Enum(
    'Yay',
    'Nay',
    'Abstain',
    enum_name='ProposalVote'
))

Vote = CStruct(
    'validator' / Address,
    'delegator' / Address,
    'data' / ProposalVote
)

GovernanceParameters = CStruct(
    'min_proposal_fund' / Uint,
    'max_proposal_code_size' / U64,
    'min_proposal_voting_period' / U64,
    'max_proposal_period' / U64,
    'max_proposal_content_size' / U64,
    'min_proposal_grace_epochs' / U64,
)

TallyResult = TupleStruct(Enum(
    'Passed',
    'Rejected',
    enum_name='TallyResult'
))

TallyType = TupleStruct(Enum(
    'TwoThirds',
    'OneHalfOverOneThird',
    'LessOneHalfOverOneThirdNay',
    enum_name='TallyType'
))

ProposalResult = CStruct(
    'result' / TallyResult,
    'tally_type' / TallyType,
    'total_voting_power' / Uint,
    'total_yay_power' / Uint,
    'total_nay_power' / Uint,
    'total_abstain_power' / Uint
)

PosParams = CStruct(
    'max_validator_slots' / U64,
    'pipeline_len' / U64,
    'unbonding_len' / U64,
    'tm_votes_per_token' / Dec,
    'block_proposer_reward' / Dec,
    'block_vote_reward' / Dec,
    'max_inflation_rate' / Dec,
    'target_staked_ratio' / Dec,
    'duplicate_vote_min_slash_rate' / Dec,
    'light_client_attack_min_slash_rate' / Dec,
    'cubic_slashing_window_length' / U64,
    'validator_stake_threshold' / Uint,
    'liveness_window_check' / U64,
    'liveness_threshold' / Dec,
    'rewards_gain_p' / Dec,
    'rewards_gain_d' / Dec
)

BondId = CStruct(
    'source' / Address,
    'validator' / Address
)

BondDetails = CStruct(
    'start' / U64,
    'amount' / Uint,
    'slashed_amount' / Option(Uint)
)

UnbondDetails = CStruct(
    'start' / U64,
    'withdraw' / U64,
    'amount' / Uint,
    'slashed_amount' / Option(Uint)
)

BondsAndUnbondsDetail = CStruct(
    'bonds' / Vec(BondDetails),
    'unbonds' / Vec(UnbondDetails),
    'slashes' / Vec(Slash)
)

LastBlock = CStruct(
    'height' / Uint,
    'hash' / U8[32],
    'time' / String
)

EString = CStruct(
    'value' / String
)

DbKeySeg = TupleStruct(Enum(
    'AddressSeg' / Address,
    'StringSeg' / EString,
    enum_name='DbKeySeg'
))

Key = CStruct(
    'segments' / Vec(DbKeySeg)
)

PrefixValue = CStruct(
    'key' / Key,
    'value' / Vec(U8)
)

MaspTokenRewardData = CStruct(
    'name' / String,
    'address' / Address,
    'max_reward_rate' / Dec,
    'kp_gain' / Dec,
    'kd_gain' / Dec,
    'locked_amount_target' / Uint
)

EventType = TupleStruct(Enum(
    'Accepted',
    'Applied',
    'Ibc' / EString,
    'Proposal',
    'PgfPayment',
    'EthereumBridge',
    enum_name='EventType'
))

EventLevel = TupleStruct(Enum(
    'Block',
    'Tx',
    enum_name='EventLevel'
))

Event = CStruct(
    'event_type' / EventType,
    'level' / EventLevel,
    'attributes' / Vec(TupleStruct(String, String))
)

AccountPublicKeysMap = CStruct(
    'pk_to_idx' / Vec(TupleStruct(PublicKey, U8)),
    'idx_to_pk' / Vec(TupleStruct(U8, PublicKey))
)

Account = CStruct(
    'public_keys_map' / AccountPublicKeysMap,
    'threshold' / U8,
    'address' / Address
)
