import CommunityVoting from "../../cadence/contracts/CommunityVoting.cdc"

/// Script to retrieve vote counts for a proposal
///
/// @param proposalId: ID of the proposal
/// @return Dictionary with yesVotes and noVotes

access(all) fun main(proposalId: UInt64): {String: UInt64}? {
    return CommunityVoting.getVoteCounts(proposalId: proposalId)
}
