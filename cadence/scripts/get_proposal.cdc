import CommunityVoting from "../../cadence/contracts/CommunityVoting.cdc"

/// Script to retrieve a specific proposal by ID
///
/// @param proposalId: ID of the proposal to retrieve
/// @return The proposal details or nil if not found

access(all) fun main(proposalId: UInt64): CommunityVoting.Proposal? {
    return CommunityVoting.getProposal(proposalId: proposalId)
}
