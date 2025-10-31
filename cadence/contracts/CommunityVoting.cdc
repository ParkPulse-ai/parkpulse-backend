// CommunityVoting Smart Contract for Flow Blockchain
// A decentralized voting system for park protection proposals

access(all) contract CommunityVoting {

    // Events
    access(all) event ProposalCreated(
        proposalId: UInt64,
        parkName: String,
        parkId: String,
        endDate: UFix64,
        creator: Address
    )

    access(all) event VoteCast(
        proposalId: UInt64,
        voter: Address,
        vote: Bool
    )

    access(all) event ProposalStatusUpdated(
        proposalId: UInt64,
        newStatus: String
    )

    access(all) event ContractInitialized()

    // Enums
    access(all) enum ProposalStatus: UInt8 {
        access(all) case Active
        access(all) case Accepted
        access(all) case Declined
    }

    // Structs
    access(all) struct EnvironmentalData {
        access(all) let ndviBefore: UFix64
        access(all) let ndviAfter: UFix64
        access(all) let pm25Before: UFix64
        access(all) let pm25After: UFix64
        access(all) let pm25IncreasePercent: UFix64
        access(all) let vegetationLossPercent: UFix64

        init(
            ndviBefore: UFix64,
            ndviAfter: UFix64,
            pm25Before: UFix64,
            pm25After: UFix64,
            pm25IncreasePercent: UFix64,
            vegetationLossPercent: UFix64
        ) {
            self.ndviBefore = ndviBefore
            self.ndviAfter = ndviAfter
            self.pm25Before = pm25Before
            self.pm25After = pm25After
            self.pm25IncreasePercent = pm25IncreasePercent
            self.vegetationLossPercent = vegetationLossPercent
        }
    }

    access(all) struct Demographics {
        access(all) let children: UInt64
        access(all) let adults: UInt64
        access(all) let seniors: UInt64
        access(all) let totalAffectedPopulation: UInt64

        init(
            children: UInt64,
            adults: UInt64,
            seniors: UInt64,
            totalAffectedPopulation: UInt64
        ) {
            self.children = children
            self.adults = adults
            self.seniors = seniors
            self.totalAffectedPopulation = totalAffectedPopulation
        }
    }

    access(all) struct Proposal {
        access(all) let id: UInt64
        access(all) let parkName: String
        access(all) let parkId: String
        access(all) let description: String
        access(all) let endDate: UFix64
        access(all) var status: ProposalStatus
        access(all) var yesVotes: UInt64
        access(all) var noVotes: UInt64
        access(all) let environmentalData: EnvironmentalData
        access(all) let demographics: Demographics
        access(all) let creator: Address

        init(
            id: UInt64,
            parkName: String,
            parkId: String,
            description: String,
            endDate: UFix64,
            environmentalData: EnvironmentalData,
            demographics: Demographics,
            creator: Address
        ) {
            self.id = id
            self.parkName = parkName
            self.parkId = parkId
            self.description = description
            self.endDate = endDate
            self.status = ProposalStatus.Active
            self.yesVotes = 0
            self.noVotes = 0
            self.environmentalData = environmentalData
            self.demographics = demographics
            self.creator = creator
        }

        access(contract) fun addYesVote() {
            self.yesVotes = self.yesVotes + 1
        }

        access(contract) fun addNoVote() {
            self.noVotes = self.noVotes + 1
        }

        access(contract) fun updateStatus(newStatus: ProposalStatus) {
            self.status = newStatus
        }
    }

    // Storage paths
    access(all) let AdminStoragePath: StoragePath
    access(all) let AdminPublicPath: PublicPath

    // Contract state
    access(contract) var proposals: {UInt64: Proposal}
    access(contract) var userVotes: {UInt64: {Address: Bool}} // proposalId -> voter -> vote
    access(contract) var hasVoted: {UInt64: {Address: Bool}} // proposalId -> voter -> hasVoted
    access(contract) var proposalCounter: UInt64

    // Admin resource for contract management
    access(all) resource Admin {
        access(all) fun updateProposalStatus(proposalId: UInt64) {
            pre {
                CommunityVoting.proposals[proposalId] != nil: "Proposal does not exist"
            }

            let proposal = CommunityVoting.proposals[proposalId]!
            let currentTime = getCurrentBlock().timestamp

            assert(currentTime > proposal.endDate, message: "Voting period has not ended")
            assert(proposal.status == ProposalStatus.Active, message: "Proposal is not active")

            var newStatus = ProposalStatus.Declined
            if proposal.yesVotes > proposal.noVotes {
                newStatus = ProposalStatus.Accepted
            }

            CommunityVoting.proposals[proposalId]?.updateStatus(newStatus: newStatus)

            var statusString = "Declined"
            if newStatus == ProposalStatus.Accepted {
                statusString = "Accepted"
            }
            emit ProposalStatusUpdated(
                proposalId: proposalId,
                newStatus: statusString
            )
        }

        access(all) fun forceCloseProposal(proposalId: UInt64, newStatus: ProposalStatus) {
            pre {
                CommunityVoting.proposals[proposalId] != nil: "Proposal does not exist"
                CommunityVoting.proposals[proposalId]!.status == ProposalStatus.Active: "Proposal is not active"
            }

            CommunityVoting.proposals[proposalId]?.updateStatus(newStatus: newStatus)

            var statusString = "Declined"
            if newStatus == ProposalStatus.Accepted {
                statusString = "Accepted"
            }
            emit ProposalStatusUpdated(
                proposalId: proposalId,
                newStatus: statusString
            )
        }
    }

    // Public functions
    access(all) fun createProposal(
        parkName: String,
        parkId: String,
        description: String,
        endDate: UFix64,
        environmentalData: EnvironmentalData,
        demographics: Demographics,
        creator: Address
    ): UInt64 {
        pre {
            parkName.length > 0: "Park name cannot be empty"
            parkId.length > 0: "Park ID cannot be empty"
            endDate > getCurrentBlock().timestamp: "End date must be in the future"
        }

        self.proposalCounter = self.proposalCounter + 1
        let proposalId = self.proposalCounter

        let proposal = Proposal(
            id: proposalId,
            parkName: parkName,
            parkId: parkId,
            description: description,
            endDate: endDate,
            environmentalData: environmentalData,
            demographics: demographics,
            creator: creator
        )

        self.proposals[proposalId] = proposal
        self.userVotes[proposalId] = {}
        self.hasVoted[proposalId] = {}

        emit ProposalCreated(
            proposalId: proposalId,
            parkName: parkName,
            parkId: parkId,
            endDate: endDate,
            creator: creator
        )

        return proposalId
    }

    access(all) fun vote(proposalId: UInt64, vote: Bool, voter: Address) {
        pre {
            self.proposals[proposalId] != nil: "Proposal does not exist"
            self.hasVoted[proposalId]![voter] == nil || self.hasVoted[proposalId]![voter] == false: "User has already voted"
        }

        let proposal = self.proposals[proposalId]!
        let currentTime = getCurrentBlock().timestamp

        assert(proposal.status == ProposalStatus.Active, message: "Proposal is not active")
        assert(currentTime <= proposal.endDate, message: "Voting period has ended")

        // Record the vote
        self.userVotes[proposalId]!.insert(key: voter, vote)
        self.hasVoted[proposalId]!.insert(key: voter, true)

        // Update vote count
        if vote {
            self.proposals[proposalId]?.addYesVote()
        } else {
            self.proposals[proposalId]?.addNoVote()
        }

        emit VoteCast(
            proposalId: proposalId,
            voter: voter,
            vote: vote
        )
    }

    // View functions
    access(all) fun getProposal(proposalId: UInt64): Proposal? {
        return self.proposals[proposalId]
    }

    access(all) fun getVoteCounts(proposalId: UInt64): {String: UInt64}? {
        if let proposal = self.proposals[proposalId] {
            return {
                "yesVotes": proposal.yesVotes,
                "noVotes": proposal.noVotes
            }
        }
        return nil
    }

    access(all) fun getUserVote(proposalId: UInt64, user: Address): Bool? {
        if let votes = self.userVotes[proposalId] {
            return votes[user]
        }
        return nil
    }

    access(all) fun hasUserVoted(proposalId: UInt64, user: Address): Bool {
        if let voted = self.hasVoted[proposalId] {
            return voted[user] ?? false
        }
        return false
    }

    access(all) fun isProposalActive(proposalId: UInt64): Bool {
        if let proposal = self.proposals[proposalId] {
            let currentTime = getCurrentBlock().timestamp
            return proposal.status == ProposalStatus.Active && currentTime <= proposal.endDate
        }
        return false
    }

    access(all) fun getAllActiveProposals(): [UInt64] {
        let activeProposals: [UInt64] = []
        let currentTime = getCurrentBlock().timestamp

        for proposalId in self.proposals.keys {
            if let proposal = self.proposals[proposalId] {
                if proposal.status == ProposalStatus.Active {
                    activeProposals.append(proposalId)
                }
            }
        }

        return activeProposals
    }

    access(all) fun getAllClosedProposals(): [UInt64] {
        let closedProposals: [UInt64] = []

        for proposalId in self.proposals.keys {
            if let proposal = self.proposals[proposalId] {
                if proposal.status == ProposalStatus.Accepted || proposal.status == ProposalStatus.Declined {
                    closedProposals.append(proposalId)
                }
            }
        }

        return closedProposals
    }

    access(all) fun getTotalProposals(): UInt64 {
        return self.proposalCounter
    }

    // Contract initialization
    init() {
        self.proposals = {}
        self.userVotes = {}
        self.hasVoted = {}
        self.proposalCounter = 0

        // Set up storage paths
        self.AdminStoragePath = /storage/CommunityVotingAdmin
        self.AdminPublicPath = /public/CommunityVotingAdmin

        // Create and store the admin resource
        let admin <- create Admin()
        self.account.storage.save(<-admin, to: self.AdminStoragePath)

        emit ContractInitialized()
    }
}
