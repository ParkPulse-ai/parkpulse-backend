import CommunityVoting from "../../cadence/contracts/CommunityVoting.cdc"

/// Script to retrieve all active proposal IDs
///
/// @return Array of active proposal IDs

access(all) fun main(): [UInt64] {
    return CommunityVoting.getAllActiveProposals()
}
