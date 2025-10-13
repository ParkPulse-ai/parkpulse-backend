import CommunityVoting from "../../cadence/contracts/CommunityVoting.cdc"

/// Transaction to cast a vote on a proposal
///
/// @param proposalId: ID of the proposal to vote on
/// @param vote: true for Yes, false for No
/// @param voter: Address of the voter

transaction(proposalId: UInt64, vote: Bool, voter: Address) {
    prepare(signer: &Account) {}

    execute {
        CommunityVoting.vote(
            proposalId: proposalId,
            vote: vote,
            voter: voter
        )

        let voteType = vote ? "Yes" : "No"
        log("Vote cast: ".concat(voteType).concat(" for proposal #").concat(proposalId.toString()))
    }
}
