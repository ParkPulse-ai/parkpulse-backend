import CommunityVoting from "../../cadence/contracts/CommunityVoting.cdc"

/// Transaction to create a new park protection proposal
///
/// @param parkName: Name of the park
/// @param parkId: Unique identifier for the park
/// @param description: Detailed description of the proposal
/// @param endDate: Voting end date (Unix timestamp as UFix64)
/// @param ndviBefore: NDVI value before park removal
/// @param ndviAfter: NDVI value after park removal
/// @param pm25Before: PM2.5 level before removal
/// @param pm25After: PM2.5 level after removal
/// @param pm25IncreasePercent: Percentage increase in PM2.5
/// @param vegetationLossPercent: Percentage of vegetation loss
/// @param children: Number of children affected
/// @param adults: Number of adults affected
/// @param seniors: Number of seniors affected
/// @param totalAffectedPopulation: Total population affected
/// @param creator: Address of the proposal creator

transaction(
    parkName: String,
    parkId: String,
    description: String,
    endDate: UFix64,
    ndviBefore: UFix64,
    ndviAfter: UFix64,
    pm25Before: UFix64,
    pm25After: UFix64,
    pm25IncreasePercent: UFix64,
    vegetationLossPercent: UFix64,
    children: UInt64,
    adults: UInt64,
    seniors: UInt64,
    totalAffectedPopulation: UInt64,
    creator: Address
) {
    prepare(signer: &Account) {}

    execute {
        let environmentalData = CommunityVoting.EnvironmentalData(
            ndviBefore: ndviBefore,
            ndviAfter: ndviAfter,
            pm25Before: pm25Before,
            pm25After: pm25After,
            pm25IncreasePercent: pm25IncreasePercent,
            vegetationLossPercent: vegetationLossPercent
        )

        let demographics = CommunityVoting.Demographics(
            children: children,
            adults: adults,
            seniors: seniors,
            totalAffectedPopulation: totalAffectedPopulation
        )

        let proposalId = CommunityVoting.createProposal(
            parkName: parkName,
            parkId: parkId,
            description: description,
            endDate: endDate,
            environmentalData: environmentalData,
            demographics: demographics,
            creator: creator
        )

        log("Proposal created with ID: ".concat(proposalId.toString()))
    }
}
