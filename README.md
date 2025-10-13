# ParkPulse.ai Backend - Flow Blockchain

Complete guide to deploy and run the ParkPulse.ai backend with Flow blockchain integration.

## Quick Start (3 Steps)

### 1. Setup Flow Wallet
```bash
python setup_flow_wallet.py
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Deploy & Run
```bash
# Deploy contract
python deploy_flow_contract.py

# Start backend
python main.py
```

Your backend will be running at `http://localhost:4000`

---

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Deployment](#deployment)
- [Running the Backend](#running-the-backend)
- [API Endpoints](#api-endpoints)
- [Flow CLI Usage](#flow-cli-usage)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software
- **Python 3.8+**
- **PostgreSQL** (for database)
- **Flow CLI** - [Install Guide](https://developers.flow.com/tools/flow-cli/install)

### Install Flow CLI

**macOS:**
```bash
brew install flow-cli
```

**Linux:**
```bash
sh -ci "$(curl -fsSL https://storage.googleapis.com/flow-cli/install.sh)"
```

**Windows:**
```powershell
iex "& { $(irm 'https://storage.googleapis.com/flow-cli/install.ps1') }"
```

Verify installation:
```bash
flow version
```

### Get Flow Account & Tokens

1. **Generate keys:**
   ```bash
   flow keys generate
   ```
   Save the private and public keys securely.

2. **Create testnet account:**
   Visit [Flow Testnet Faucet](https://testnet-faucet.onflow.org/) with your public key to create an account and receive free testnet FLOW tokens.

3. **Save your credentials:**
   - Account address (e.g., `0x1234567890abcdef`)
   - Private key (keep secret!)

---

## Installation

### 1. Clone & Setup

```bash
cd parkpulsebe
pip install -r requirements.txt
```

### 2. Database Setup

Create PostgreSQL database:
```bash
createdb cityroots
```

Configure database connection in `.env` (see Configuration section).

---

## Configuration

### Interactive Setup (Recommended)

Run the setup wizard:
```bash
python setup_flow_wallet.py
```

This will:
- Guide you through wallet configuration
- Validate credentials
- Test Flow connection
- Create `.env` file

### Manual Setup

Create `.env` file:
```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```bash
# Database Configuration
PGHOST=localhost
PGPORT=5432
PGDATABASE=cityroots
PGUSER=your_username
PGPASSWORD=your_password

# API Keys
GEMINI_API_KEY=your_gemini_api_key
GEE_PROJECT_ID=your_google_earth_engine_project

# Server
PORT=4000

# Flow Blockchain
FLOW_NETWORK=testnet
FLOW_ADDRESS=0xYourFlowAddress
FLOW_PRIVATE_KEY=your_private_key_hex
FLOW_CONTRACT_NAME=CommunityVoting
FLOW_CONTRACT_ADDRESS=0xYourFlowAddress
FLOW_ACCESS_NODE=access.devnet.nodes.onflow.org:9000
```

**Important:**
- Replace `0xYourFlowAddress` with your actual Flow address
- Replace `your_private_key_hex` with your private key (without `0x` prefix)
- Never commit `.env` to git

---

## Deployment

### Deploy Contract to Flow Testnet

**Option 1: Python Script (Recommended)**
```bash
python deploy_flow_contract.py
```

The script will:
- ✅ Validate configuration
- ✅ Check account balance
- ✅ Deploy CommunityVoting contract
- ✅ Save deployment info to `cadence/flow_deployment_info.json`
- ✅ Update `.env` automatically

**Option 2: Flow CLI**
```bash
flow project deploy --network testnet
```

### Verify Deployment

Check your contract on Flow Explorer:
```
https://testnet.flowdiver.io/account/0xYourAddress
```

Or use Flow CLI:
```bash
flow accounts get 0xYourAddress --network testnet
```

---

## Running the Backend

### Start the Server

```bash
python main.py
```

The API will be available at:
- **Main URL**: `http://localhost:4000`
- **Docs**: `http://localhost:4000/docs`
- **ReDoc**: `http://localhost:4000/redoc`

### Verify Backend is Running

```bash
# Health check
curl http://localhost:4000/health

# Contract info
curl http://localhost:4000/api/contract-info

# Get proposals
curl http://localhost:4000/api/proposals
```

---

## API Endpoints

### Core Endpoints

#### Health Check
```bash
GET /health
```

#### Contract Information
```bash
GET /api/contract-info
```
Returns Flow contract details and network info.

#### Get All Proposals
```bash
GET /api/proposals
```
Returns all active proposals from Flow blockchain.

#### Get Specific Proposal
```bash
GET /api/proposals/{id}
```
Returns detailed information for a proposal.

### Application Endpoints

#### AI Agent Query
```bash
POST /api/agent
Content-Type: application/json

{
  "query": "Show me parks in Manhattan"
}
```

#### Analyze Park Removal
```bash
POST /api/analyze
Content-Type: application/json

{
  "parkId": "park_123",
  "parkName": "Central Park",
  "location": {
    "lat": 40.7829,
    "lng": -73.9654
  }
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

## Flow CLI Usage

### Query Blockchain (Scripts)

**Get all active proposals:**
```bash
flow scripts execute cadence/scripts/get_all_active_proposals.cdc --network testnet
```

**Get specific proposal:**
```bash
flow scripts execute cadence/scripts/get_proposal.cdc \
  --arg UInt64:1 \
  --network testnet
```

**Get vote counts:**
```bash
flow scripts execute cadence/scripts/get_vote_counts.cdc \
  --arg UInt64:1 \
  --network testnet
```

**Get total proposals:**
```bash
flow scripts execute cadence/scripts/get_total_proposals.cdc --network testnet
```

### Send Transactions

**Create a proposal:**
```bash
flow transactions send cadence/transactions/create_proposal.cdc \
  --arg String:"Central Park" \
  --arg String:"park_001" \
  --arg String:"Protect Central Park from commercial development" \
  --arg UFix64:1735689600.0 \
  --arg UFix64:0.75 \
  --arg UFix64:0.45 \
  --arg UFix64:25.5 \
  --arg UFix64:45.8 \
  --arg UFix64:79.6 \
  --arg UFix64:40.0 \
  --arg UInt64:1500 \
  --arg UInt64:3500 \
  --arg UInt64:800 \
  --arg UInt64:5800 \
  --arg Address:0xYourAddress \
  --network testnet \
  --signer parkpulse
```

**Vote on a proposal:**
```bash
flow transactions send cadence/transactions/vote.cdc \
  --arg UInt64:1 \
  --arg Bool:true \
  --arg Address:0xYourAddress \
  --network testnet \
  --signer parkpulse
```

### Development with Emulator

Start local Flow emulator:
```bash
# Terminal 1: Start emulator
flow emulator start

# Terminal 2: Deploy and test
flow project deploy --network emulator
flow scripts execute cadence/scripts/get_total_proposals.cdc --network emulator
```

Update `.env` for emulator:
```bash
FLOW_NETWORK=emulator
FLOW_ACCESS_NODE=localhost:3569
```

---

## Project Structure

```
parkpulsebe/
├── cadence/                      # Flow Cadence smart contracts
│   ├── contracts/                # Contract definitions
│   │   └── CommunityVoting.cdc  # Main voting contract
│   ├── transactions/             # Write operations
│   │   ├── create_proposal.cdc
│   │   └── vote.cdc
│   ├── scripts/                  # Read operations
│   │   ├── get_proposal.cdc
│   │   ├── get_all_active_proposals.cdc
│   │   ├── get_vote_counts.cdc
│   │   └── get_total_proposals.cdc
│   └── tests/                    # Test files
│
├── flow.json                     # Flow configuration
├── .env                          # Environment variables (gitignored)
├── .env.example                  # Environment template
│
├── main.py                       # FastAPI backend
├── blockchain.py                 # Flow blockchain service
├── deploy_flow_contract.py       # Deployment script
├── setup_flow_wallet.py          # Wallet setup helper
├── database.py                   # Database operations
├── models.py                     # Data models
├── utils.py                      # Utilities
├── agent.py                      # AI agent
│
└── requirements.txt              # Python dependencies
```

---

## Troubleshooting

### "Insufficient balance" Error

**Solution:** Get testnet FLOW tokens from the faucet:
```bash
# Check balance
flow accounts get 0xYourAddress --network testnet
```
Visit: https://testnet-faucet.onflow.org/

### "Flow connection failed"

**Solution:** Verify network configuration:
```bash
# Test connection
flow blocks get latest --network testnet

# Check access node in .env
FLOW_ACCESS_NODE=access.devnet.nodes.onflow.org:9000
```

### "Contract not found"

**Solution:** Verify contract is deployed:
```bash
flow accounts get 0xYourAddress --network testnet
```
Look for `CommunityVoting` in the contracts section.

### "Account not found"

**Solution:** Check your Flow address:
```bash
flow accounts list
```
Verify `FLOW_ADDRESS` in `.env` matches.

### "Invalid private key"

**Solution:**
- Ensure private key is hex format (64 characters)
- Remove `0x` prefix if present
- Verify key matches your account address

### Database Connection Error

**Solution:**
```bash
# Verify PostgreSQL is running
psql -U your_username -d cityroots

# Check .env database credentials
PGHOST=localhost
PGDATABASE=cityroots
PGUSER=your_username
PGPASSWORD=your_password
```

### Import Errors

**Solution:**
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Port Already in Use

**Solution:**
```bash
# Find process using port 4000
lsof -i :4000

# Kill the process
kill -9 <PID>

# Or change port in .env
PORT=8000
```

---

## Network Information

### Testnet (Default)
- **Access Node:** `access.devnet.nodes.onflow.org:9000`
- **Explorer:** https://testnet.flowdiver.io
- **Faucet:** https://testnet-faucet.onflow.org
- **Use Case:** Testing with free FLOW tokens

### Mainnet (Production)
- **Access Node:** `access.mainnet.nodes.onflow.org:9000`
- **Explorer:** https://flowdiver.io
- **Use Case:** Production deployment (costs real FLOW)

### Emulator (Local)
- **Access Node:** `localhost:3569`
- **Use Case:** Local development without internet

---

## Useful Commands

### Flow CLI

```bash
# Project info
flow project info

# List accounts
flow accounts list

# Get account details
flow accounts get 0xYourAddress --network testnet

# Lint Cadence code
flow cadence lint cadence/contracts/CommunityVoting.cdc

# Get latest block
flow blocks get latest --network testnet
```

### Backend

```bash
# Start backend
python main.py

# Start with custom port
PORT=8000 python main.py

# Run in background
nohup python main.py > backend.log 2>&1 &
```

### Development

```bash
# Install dev dependencies
pip install -r requirements.txt

# Run tests
pytest

# Check code style
flake8 *.py
```

---

## Resources

- **Flow Documentation:** https://developers.flow.com/
- **Cadence Language:** https://cadence-lang.org/
- **Flow Python SDK:** https://github.com/janezpodhostnik/flow-py-sdk
- **Flow Discord:** https://discord.gg/flow
- **Testnet Faucet:** https://testnet-faucet.onflow.org/
- **Flow Status:** https://status.onflow.org/

---

## Support

For issues or questions:

1. Check this README's troubleshooting section
2. Review Flow documentation
3. Ask in Flow Discord community
4. Check Flow status page for network issues

---

## Security Notes

⚠️ **Important:**
- Never commit `.env` file to version control
- Keep private keys secure
- Use environment variables for sensitive data
- Test thoroughly on testnet before mainnet
- Validate all user inputs

---

## License

This project is part of ParkPulse.ai. See LICENSE file for details.

---

**You're ready to go!** 🚀

Run `python setup_flow_wallet.py` to get started.
