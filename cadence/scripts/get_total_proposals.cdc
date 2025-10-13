import CommunityVoting from "../contracts/CommunityVoting.cdc"

/// Script to retrieve the total number of proposals
///
/// @return Total proposal count

access(all) fun main(): UInt64 {
    return CommunityVoting.getTotalProposals()
}
