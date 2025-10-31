# ParkPulse.ai

**A decentralized community-driven platform for Urban City Planning on Flow Blockchain**

![Flow Blockchain](https://img.shields.io/badge/Built%20on-Flow%20Blockchain-00EF8B?style=for-the-badge&logo=flow)
![Network](https://img.shields.io/badge/Network-Testnet-blue?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

---

## 🚀 Deployed on Flow Blockchain Testnet

### Contract Details

| Contract Name | Contract Address | Explorer Link |
|--------------|------------------|---------------|
| **CommunityVoting** | `0xd63bdc807b56f6a5` | [View on FlowScan](https://testnet.flowscan.io/contract/A.d63bdc807b56f6a5.CommunityVoting) |

**Network:** Flow Testnet
**Contract Address:** `0xd63bdc807b56f6a5`
**View on Explorer:** https://testnet.flowscan.io/contract/A.d63bdc807b56f6a5.CommunityVoting

### Contract Capabilities
- Create park protection proposals with environmental data
- Cast votes (yes/no) on active proposals
- Track voting results with demographic impact analysis
- Automatic proposal status management
- Event emission for transparency

---

## 🌊 Why Flow Blockchain?

ParkPulse is built on **Flow Blockchain (Testnet)** for several compelling reasons:

### 1. **Resource-Oriented Programming with Cadence**
Flow's Cadence language provides unique safety guarantees perfect for voting systems:
- **No reentrancy attacks** - Built-in protection against common smart contract vulnerabilities
- **Static typing** - Catches errors at compile time, critical for governance contracts
- **Resource safety** - Prevents double-voting and ensures vote integrity

### 2. **User Experience First**
- **Human-readable transactions** - Voters can see exactly what they're signing
- **Low transaction costs** - Makes community voting accessible to everyone
- **Fast finality** - Quick vote confirmations without waiting

### 3. **Scalability**
- **Multi-node architecture** - Separates consensus, execution, and verification
- **No gas wars** - Predictable costs for community proposals
- **Future-proof** - Can scale as the platform grows to multiple cities

### 4. **Developer Experience**
- **Excellent tooling** - Flow CLI, emulator, and comprehensive documentation
- **Python & JavaScript SDKs** - Easy integration with web applications
- **Active community** - Strong support and growing ecosystem

### 5. **Environmental Mission Alignment**
- **Energy efficient** - Proof-of-Stake consensus aligns with environmental values
- **Sustainable infrastructure** - Lower carbon footprint than alternatives

---

## 📖 Overview

**ParkPulse.ai** is a decentralized platform that empowers communities to protect public parks through transparent, blockchain-based voting. When a park faces threats like commercial development or removal, ParkPulse enables citizens to create proposals, analyze environmental impact, and vote on protective measures.

The platform combines:
- **AI-powered environmental analysis** (NDVI vegetation indices, PM2.5 air quality)
- **Demographic impact assessment** (affected populations)
- **Decentralized governance** via Flow blockchain smart contracts
- **Transparent voting** with immutable on-chain records

### Key Use Cases
- Protect parks from commercial development
- Community-driven conservation decisions
- Evidence-based environmental advocacy
- Transparent democratic processes for urban planning

---

## Table of Contents
- [Deployed on Flow Blockchain Testnet](#-deployed-on-flow-blockchain-testnet)
- [Why Flow Blockchain?](#-why-flow-blockchain)
- [Overview](#-overview)
- [Features](#features)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Demo & Resources](#demo--resources)
- [Contributing](#contributing)
- [License](#license)

---

## Features

### For Citizens
- **Create Proposals** - Submit park protection proposals with AI-generated impact analysis
- **Vote on Issues** - Cast votes on proposals affecting your community
- **View Impact Data** - See environmental and demographic impact before voting
- **Track Results** - Real-time voting results stored immutably on-chain

### Environmental Analysis
- **NDVI Analysis** - Vegetation health tracking using satellite imagery
- **Air Quality Monitoring** - PM2.5 levels before/after park removal scenarios
- **Impact Prediction** - AI-powered analysis of park removal consequences

### Blockchain Features
- **Decentralized Voting** - No central authority can manipulate results
- **Immutable Records** - All votes permanently recorded on Flow blockchain
- **Transparent Process** - Anyone can verify voting integrity
- **Smart Contract Automation** - Automatic proposal status updates

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     ParkPulse.ai Platform                    │
└─────────────────────────────────────────────────────────────┘
                              │
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────┐    ┌──────────────────┐    ┌─────────────┐
│   Frontend   │    │     Backend      │    │Flow Testnet │
│  (Next.js)   │◄───┤  (Python/FastAPI)│◄───┤  Blockchain │
│              │    │                  │    │             │
│ - React UI   │    │ - Flow SDK       │    │ Community   │
│ - Flow SDK   │    │ - AI Analysis    │    │ Voting      │
│ - Mapbox     │    │ - GEE API        │    │ Contract    │
│ - Voting     │    │ - PostgreSQL     │    │ 0xd63b...   │
└──────────────┘    └──────────────────┘    └─────────────┘
```

### Data Flow
1. **User Action** - Citizen interacts with frontend (create proposal/vote)
2. **Backend Processing** - AI analyzes environmental impact via Google Earth Engine
3. **Blockchain Transaction** - Data submitted to Flow smart contract
4. **On-Chain Storage** - Proposal/vote recorded immutably
5. **Event Emission** - Contract emits events for transparency
6. **Frontend Update** - UI reflects new blockchain state

---

## Technology Stack

### Frontend (`parkpulsefe/`)
- **Next.js 15** - React framework with server-side rendering
- **TypeScript** - Type-safe development
- **@onflow/react-sdk** - Flow blockchain integration
- **Mapbox GL** - Interactive park mapping
- **Tailwind CSS** - Modern styling

### Backend (`parkpulsebe/`)
- **Python 3.8+** - Core backend language
- **FastAPI** - High-performance REST API
- **Flow Python SDK** - Blockchain interaction
- **Google Earth Engine API** - Satellite imagery analysis
- **PostgreSQL** - Relational database
- **Gemini AI** - Environmental impact analysis

### Blockchain
- **Flow Blockchain** - Layer 1 blockchain (Testnet)
- **Cadence** - Resource-oriented smart contract language
- **Flow CLI** - Development and deployment tooling

---

## Getting Started

### Prerequisites
- **Node.js 18+** (for frontend)
- **Python 3.8+** (for backend)
- **PostgreSQL** (for database)
- **Flow CLI** ([Installation Guide](https://developers.flow.com/tools/flow-cli/install))

### Quick Start

#### 1. Clone Repository
```bash
git clone https://github.com/yourusername/ParkPulseAi.git
cd ParkPulseAi
```

#### 2. Setup Backend
```bash
cd parkpulsebe

# Install dependencies
pip install -r requirements.txt

# Setup Flow wallet (interactive)
python setup_flow_wallet.py

# Create database
createdb cityroots

# Configure environment
cp .env.example .env
# Edit .env with your credentials

# Start backend
python main.py
```

Backend runs at: `http://localhost:4000`

#### 3. Setup Frontend
```bash
cd parkpulsefe

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend runs at: `http://localhost:3000`

### Detailed Setup

For complete setup instructions including:
- Flow wallet creation
- Contract deployment
- API key configuration
- Troubleshooting

See:
- **Backend README**: [parkpulsebe/README.md](parkpulsebe/README.md)
- **Contract Deployment**: [parkpulsebe/deploy_flow_contract.py](parkpulsebe/deploy_flow_contract.py)

---

## Project Structure

```
ParkPulseAi/
├── README.md                          # This file
│
├── parkpulsefe/                       # Frontend (Next.js)
│   ├── src/
│   │   ├── app/                       # Next.js app router
│   │   ├── components/                # React components
│   │   └── lib/                       # Utilities & Flow config
│   ├── package.json
│   └── tsconfig.json
│
├── parkpulsebe/                       # Backend (Python)
│   ├── cadence/                       # Flow Cadence contracts
│   │   ├── contracts/
│   │   │   └── CommunityVoting.cdc    # Main voting contract
│   │   ├── transactions/              # Write operations
│   │   │   ├── create_proposal.cdc
│   │   │   └── vote.cdc
│   │   └── scripts/                   # Read operations
│   │       ├── get_all_active_proposals.cdc
│   │       ├── get_proposal.cdc
│   │       └── get_vote_counts.cdc
│   │
│   ├── main.py                        # FastAPI application
│   ├── blockchain.py                  # Flow blockchain service
│   ├── agent.py                       # AI analysis
│   ├── database.py                    # PostgreSQL operations
│   ├── deploy_flow_contract.py        # Deployment script
│   ├── setup_flow_wallet.py           # Wallet setup wizard
│   ├── requirements.txt               # Python dependencies
│   ├── flow.json                      # Flow configuration
│   ├── .env.example                   # Environment template
│   └── README.md                      # Backend documentation
│
└── .gitignore
```

---

## Demo & Resources

### Video Demo
[Coming Soon - Link to demo video]

### Live Demo
[Coming Soon - Link to deployed application]

### GitHub Repository
[https://github.com/yourusername/ParkPulseAi](https://github.com/yourusername/ParkPulseAi)

### Flow Resources
- **Contract on FlowScan**: [View Contract](https://testnet.flowscan.io/contract/A.d63bdc807b56f6a5.CommunityVoting)
- **Flow Documentation**: [https://developers.flow.com/](https://developers.flow.com/)
- **Cadence Language**: [https://cadence-lang.org/](https://cadence-lang.org/)

### API Documentation
- **Backend API Docs**: `http://localhost:4000/docs` (when running)
- **Interactive API**: `http://localhost:4000/redoc`

---

## API Endpoints

### Blockchain Endpoints

#### Get Contract Information
```bash
GET /api/contract-info
```
Returns Flow contract details and network information.

#### Get All Proposals
```bash
GET /api/proposals
```
Returns all active proposals from Flow blockchain.

#### Get Specific Proposal
```bash
GET /api/proposals/{id}
```
Returns detailed proposal information including votes and impact data.

### Application Endpoints

#### Create Proposal with AI Analysis
```bash
POST /api/analyze
Content-Type: application/json

{
  "parkId": "park_001",
  "parkName": "Central Park",
  "location": {
    "lat": 40.7829,
    "lng": -73.9654
  }
}
```

#### Query AI Agent
```bash
POST /api/agent
Content-Type: application/json

{
  "query": "Show me parks in Manhattan"
}
```

#### Calculate NDVI
```bash
POST /api/ndvi
Content-Type: application/json

{
  "location": {
    "lat": 40.7829,
    "lng": -73.9654
  },
  "startDate": "2024-01-01",
  "endDate": "2024-12-31"
}
```

---

## Smart Contract Functions

### Transactions (Write Operations)

#### Create Proposal
```cadence
createProposal(
    parkName: String,
    parkId: String,
    description: String,
    endDate: UFix64,
    environmentalData: EnvironmentalData,
    demographics: Demographics,
    creator: Address
)
```

#### Vote on Proposal
```cadence
vote(
    proposalId: UInt64,
    vote: Bool,
    voter: Address
)
```

### Scripts (Read Operations)

#### Get All Active Proposals
```cadence
getActiveProposals(): [Proposal]
```

#### Get Proposal by ID
```cadence
getProposal(proposalId: UInt64): Proposal?
```

#### Get Vote Counts
```cadence
getVoteCounts(proposalId: UInt64): {String: UInt64}
```

---

## Contributing

We welcome contributions to ParkPulse.ai! Here's how you can help:

### Areas for Contribution
- Frontend UI/UX improvements
- Additional Cadence smart contract features
- Environmental analysis enhancements
- Documentation improvements
- Bug fixes and testing

### Development Process
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly (testnet deployment)
5. Commit with clear messages
6. Push to your fork
7. Open a Pull Request

### Testing
```bash
# Backend tests
cd parkpulsebe
pytest

# Frontend tests
cd parkpulsefe
npm test

# Flow contract tests
flow test parkpulsebe/cadence/tests/
```

---

## Roadmap

### Phase 1: MVP (Current)
- [x] Flow testnet deployment
- [x] Basic voting functionality
- [x] Environmental impact analysis
- [x] Web interface

### Phase 2: Enhanced Features
- [ ] Mobile app (iOS/Android)
- [ ] Multi-language support
- [ ] Advanced AI predictions
- [ ] Integration with city APIs

### Phase 3: Mainnet & Scale
- [ ] Flow mainnet deployment
- [ ] Multi-city expansion
- [ ] DAO governance features
- [ ] Token rewards for participation

### Phase 4: Ecosystem
- [ ] Partner with environmental NGOs
- [ ] Government integration
- [ ] Open data platform
- [ ] Research partnerships

---

## Security

### Auditing
- Smart contract code is open-source for community review
- Currently deployed on testnet for testing
- Will undergo professional audit before mainnet deployment

### Reporting Vulnerabilities
If you discover a security issue, please email: security@parkpulse.ai

### Best Practices
- Never commit private keys
- Use environment variables for sensitive data
- Test thoroughly on testnet before mainnet
- Validate all user inputs

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Made with ❤️ for parks, communities, and the environment.

**#BuildOnFlow #FlowBlockchain #Web3ForGood**
