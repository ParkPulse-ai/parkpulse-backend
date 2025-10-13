"""
Flow Blockchain Service for ParkPulse.ai
Handles interactions with Flow blockchain smart contracts
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional, List
import asyncio
try:
    from flow_py_sdk import flow_client, cadence, Tx, ProposalKey, InMemorySigner
    from flow_py_sdk.cadence import Address
    from flow_py_sdk.signer import SignAlgo, HashAlgo
    FLOW_SDK_AVAILABLE = True
except ImportError:
    FLOW_SDK_AVAILABLE = False
    logging.warning("Flow Python SDK not installed. Blockchain features will be limited.")

logger = logging.getLogger(__name__)


class FlowBlockchainService:
    def __init__(self):
        """Initialize Flow blockchain service"""
        self.network = os.getenv('FLOW_NETWORK', 'testnet')
        self.private_key_hex = os.getenv('FLOW_PRIVATE_KEY')
        # Remove 0x prefix from address if present
        self.address = os.getenv('FLOW_ADDRESS', '').replace('0x', '')
        self.contract_name = os.getenv('FLOW_CONTRACT_NAME', 'CommunityVoting')
        self.contract_address = os.getenv('FLOW_CONTRACT_ADDRESS', self.address).replace('0x', '')

        # Network configurations
        self.network_config = {
            'testnet': {
                'host': os.getenv('FLOW_ACCESS_NODE_HOST', 'access.devnet.nodes.onflow.org'),
                'port': os.getenv('FLOW_ACCESS_NODE_PORT', '9000'),
                'explorer': 'https://testnet.flowdiver.io'
            },
            'mainnet': {
                'host': os.getenv('FLOW_ACCESS_NODE_HOST', 'access.mainnet.nodes.onflow.org'),
                'port': os.getenv('FLOW_ACCESS_NODE_PORT', '9000'),
                'explorer': 'https://flowdiver.io'
            },
            'emulator': {
                'host': os.getenv('FLOW_ACCESS_NODE_HOST', 'localhost'),
                'port': os.getenv('FLOW_ACCESS_NODE_PORT', '3569'),
                'explorer': 'http://localhost:8701'
            }
        }

        self.config = self.network_config.get(self.network, self.network_config['testnet'])
        self.access_node_host = self.config['host']
        self.access_node_port = self.config['port']
        self.explorer_base_url = self.config['explorer']

        # Initialize signer if private key is available
        self.signer = None
        if self.private_key_hex and FLOW_SDK_AVAILABLE:
            try:
                logger.info(f"Initializing signer with private key (length: {len(self.private_key_hex)})")
                logger.info(f"Address: {self.address}")
                self.signer = InMemorySigner(
                    hash_algo=HashAlgo.SHA3_256,
                    sign_algo=SignAlgo.ECDSA_P256,
                    private_key_hex=self.private_key_hex
                )
                logger.info("Signer initialized successfully")
            except Exception as e:
                logger.error(f"Could not initialize signer: {e}")
                import traceback
                traceback.print_exc()

    async def is_connected(self) -> bool:
        """Check if connected to Flow blockchain"""
        try:
            async with flow_client(host=self.access_node_host, port=self.access_node_port) as client:
                await client.ping()
                return True
        except Exception as e:
            logger.error(f"Flow connection failed: {e}")
            return False

    async def get_balance(self) -> float:
        """Get account balance in FLOW"""
        if not self.address:
            return 0.0

        try:
            async with flow_client(host=self.access_node_host, port=self.access_node_port) as client:
                account_address = Address.from_hex(self.address)
                account = await client.get_account_at_latest_block(address=account_address.bytes)
                return account.balance / 1e8  # Convert from micro FLOW
        except Exception as e:
            logger.error(f"Failed to get balance: {e}")
            return 0.0

    async def create_proposal_on_blockchain(self, proposal_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a proposal on Flow blockchain"""
        try:
            if not await self.is_connected():
                return {'success': False, 'error': 'Not connected to Flow blockchain'}

            if not self.address or not self.signer:
                return {'success': False, 'error': 'Flow account not configured'}

            # Parse analysis data
            analysis_data = proposal_data['analysisData']

            # Convert datetime to Unix timestamp
            end_date_str = proposal_data['endDate']
            try:
                # Parse date and set time to end of day (23:59:59)
                parsed_date = datetime.strptime(end_date_str, "%B %d, %Y")
                end_of_day = parsed_date.replace(hour=23, minute=59, second=59)
                end_timestamp = end_of_day.timestamp()
            except:
                # Default to 30 days from now
                end_timestamp = datetime.now().timestamp() + 30 * 24 * 3600

            # Ensure end date is in the future with buffer for blockchain clock differences
            current_time = datetime.now().timestamp()
            buffer_time = 3600  # 1 hour buffer

            logger.info(f"Current time: {current_time}")
            logger.info(f"End timestamp: {end_timestamp}")
            logger.info(f"Difference: {end_timestamp - current_time} seconds")

            if end_timestamp <= current_time + buffer_time:
                logger.warning(f"End date {end_timestamp} too close to current time {current_time}, adding 30 days + 1 hour buffer")
                end_timestamp = current_time + (30 * 24 * 3600) + buffer_time

            logger.info(f"Final end timestamp (with buffer): {end_timestamp}")

            # Prepare environmental data
            ndvi_before = float(analysis_data.get('ndviBefore', 0))
            ndvi_after = float(analysis_data.get('ndviAfter', 0))
            pm25_before = float(analysis_data.get('pm25Before', 0))
            pm25_after = float(analysis_data.get('pm25After', 0))
            pm25_increase = float(analysis_data.get('pm25IncreasePercent', 0))
            vegetation_loss = float((ndvi_before - ndvi_after) * 100) if ndvi_before and ndvi_after else 0

            # Prepare demographics
            demographics = analysis_data.get('demographics', {})
            children = int(demographics.get('kids', 0))
            adults = int(demographics.get('adults', 0))
            seniors = int(demographics.get('seniors', 0))
            total_affected = int(analysis_data.get('affectedPopulation10MinWalk', 0))

            # Generate description
            description = await self._generate_blockchain_summary(
                proposal_data['proposalSummary'],
                analysis_data
            )

            # Connect to Flow
            async with flow_client(host=self.access_node_host, port=self.access_node_port) as client:
                account_address = Address.from_hex(self.address)
                account = await client.get_account_at_latest_block(address=account_address.bytes)

                # Check balance
                balance = account.balance / 1e8
                if balance < 0.001:
                    return {'success': False, 'error': f'Insufficient balance: {balance:.4f} FLOW'}

                logger.info(f"Creating proposal with balance: {balance:.4f} FLOW")

                # Get latest block
                latest_block = await client.get_latest_block()

                # Prepare transaction
                contract_addr = self.contract_address if self.contract_address else self.address

                transaction_script = f'''
                    import CommunityVoting from 0x{contract_addr.replace("0x", "")}

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
                    ) {{
                        prepare(signer: &Account) {{}}

                        execute {{
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

                            log(proposalId)
                        }}
                    }}
                '''

                # Build transaction
                logger.info(f"Account address: {account_address.hex()}")
                logger.info(f"Account key sequence number: {account.keys[0].sequence_number}")
                logger.info(f"Account key index: 0")

                proposal_key = ProposalKey(
                    key_address=account_address,
                    key_id=0,
                    key_sequence_number=account.keys[0].sequence_number
                )

                tx = Tx(
                    code=transaction_script,
                    reference_block_id=latest_block.id,
                    payer=account_address,
                    proposal_key=proposal_key
                )

                # Add authorizers
                tx.add_authorizers(account_address)

                # Add arguments
                # IMPORTANT: UFix64 expects values in a special format
                # For timestamps and other large numbers, multiply by 1e8 before passing to UFix64
                tx.add_arguments(
                    cadence.String(proposal_data['parkName']),
                    cadence.String(proposal_data['parkId']),
                    cadence.String(description),
                    cadence.UFix64(int(end_timestamp * 1e8)),  # Convert timestamp to UFix64 format
                    cadence.UFix64(int(ndvi_before * 1e8)),    # Convert to UFix64 format
                    cadence.UFix64(int(ndvi_after * 1e8)),     # Convert to UFix64 format
                    cadence.UFix64(int(pm25_before * 1e8)),    # Convert to UFix64 format
                    cadence.UFix64(int(pm25_after * 1e8)),     # Convert to UFix64 format
                    cadence.UFix64(int(pm25_increase * 1e8)),  # Convert to UFix64 format
                    cadence.UFix64(int(vegetation_loss * 1e8)), # Convert to UFix64 format
                    cadence.UInt64(children),
                    cadence.UInt64(adults),
                    cadence.UInt64(seniors),
                    cadence.UInt64(total_affected),
                    cadence.Address(account_address.bytes)
                )

                # Sign transaction
                tx = tx.with_envelope_signature(
                    account_address,
                    0,
                    self.signer
                )

                # Send transaction
                logger.info("Sending transaction to Flow...")
                tx_grpc = tx.to_signed_grpc()
                tx_result = await client.send_transaction(transaction=tx_grpc)
                tx_id = tx_result.id.hex()

                logger.info(f"Transaction sent: {tx_id}")

                # Wait for transaction to be sealed (poll for result)
                max_attempts = 30
                attempt = 0
                while attempt < max_attempts:
                    await asyncio.sleep(2)  # Wait 2 seconds between checks

                    tx_result_response = await client.get_transaction_result(id=tx_result.id)

                    if tx_result_response.status >= 4:  # 4 = SEALED status
                        if tx_result_response.error_message:
                            return {
                                'success': False,
                                'error': f'Transaction failed: {tx_result_response.error_message}',
                                'transaction_hash': tx_id
                            }

                        # Get proposal ID from events or counter
                        proposal_id = await self.get_total_proposals()

                        return {
                            'success': True,
                            'transaction_hash': tx_id,
                            'proposal_id': proposal_id,
                            'status_code': tx_result_response.status_code,
                            'explorer_url': f"{self.explorer_base_url}/transaction/{tx_id}"
                        }

                    attempt += 1

                # Timeout
                return {
                    'success': False,
                    'error': 'Transaction timeout - please check explorer',
                    'transaction_hash': tx_id,
                    'explorer_url': f"{self.explorer_base_url}/transaction/{tx_id}"
                }

        except Exception as e:
            logger.error(f"Failed to create proposal: {e}")
            import traceback
            traceback.print_exc()
            return {'success': False, 'error': str(e)}

    async def get_proposal(self, proposal_id: int) -> Optional[Dict[str, Any]]:
        """Get proposal from blockchain"""
        max_retries = 3
        retry_delay = 2  # seconds

        for attempt in range(max_retries):
            try:
                async with flow_client(host=self.access_node_host, port=self.access_node_port) as client:
                    contract_addr = self.contract_address if self.contract_address else self.address

                    script_code = f'''
                        import CommunityVoting from 0x{contract_addr.replace("0x", "")}

                        access(all) fun main(proposalId: UInt64): CommunityVoting.Proposal? {{
                            return CommunityVoting.getProposal(proposalId: proposalId)
                        }}
                    '''

                    # Encode arguments
                    from flow_py_sdk.cadence import encode_arguments
                    encoded_args = encode_arguments([cadence.UInt64(proposal_id)])

                    result = await client.execute_script_at_latest_block(
                        script=script_code.encode('utf-8'),
                        arguments=encoded_args
                    )

                    if result:
                        import json
                        from flow_py_sdk.cadence import cadence_object_hook
                        cadence_value = json.loads(result, object_hook=cadence_object_hook)
                        # Parse the result and return proposal data
                        # Pass proposal_id since it's lost in the SDK's struct parsing
                        return self._parse_proposal_result(cadence_value, proposal_id)

                    return None

            except Exception as e:
                error_msg = str(e)
                if "rate limited" in error_msg.lower() and attempt < max_retries - 1:
                    logger.warning(f"Rate limited, retrying in {retry_delay}s (attempt {attempt + 1}/{max_retries})")
                    await asyncio.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                    continue
                else:
                    logger.error(f"Failed to get proposal: {e}")
                    return None

        return None

    async def get_all_active_proposals(self) -> List[int]:
        """Get all active proposal IDs"""
        try:
            async with flow_client(host=self.access_node_host, port=self.access_node_port) as client:
                contract_addr = self.contract_address if self.contract_address else self.address

                script_code = f'''
                    import CommunityVoting from 0x{contract_addr.replace("0x", "")}

                    access(all) fun main(): [UInt64] {{
                        return CommunityVoting.getAllActiveProposals()
                    }}
                '''

                result = await client.execute_script_at_latest_block(
                    script=script_code.encode('utf-8'),
                    arguments=[]
                )

                if result:
                    import json
                    from flow_py_sdk.cadence import cadence_object_hook
                    cadence_value = json.loads(result, object_hook=cadence_object_hook)
                    # cadence_value is an Array object with a 'value' attribute
                    if hasattr(cadence_value, 'value'):
                        return [int(id.value) if hasattr(id, 'value') else int(id) for id in cadence_value.value]
                    return [int(id.value) if hasattr(id, 'value') else int(id) for id in cadence_value] if cadence_value else []
                return []

        except Exception as e:
            logger.error(f"Failed to get active proposals: {e}")
            return []

    async def get_total_proposals(self) -> int:
        """Get total number of proposals"""
        try:
            async with flow_client(host=self.access_node_host, port=self.access_node_port) as client:
                contract_addr = self.contract_address if self.contract_address else self.address

                script_code = f'''
                    import CommunityVoting from 0x{contract_addr.replace("0x", "")}

                    access(all) fun main(): UInt64 {{
                        return CommunityVoting.getTotalProposals()
                    }}
                '''

                # Use execute_script_at_latest_block which expects bytes
                result = await client.execute_script_at_latest_block(
                    script=script_code.encode('utf-8'),
                    arguments=[]
                )

                if result:
                    import json
                    from flow_py_sdk.cadence import cadence_object_hook
                    cadence_value = json.loads(result, object_hook=cadence_object_hook)
                    # cadence_value is a UInt64 object, access its value
                    if hasattr(cadence_value, 'value'):
                        return int(cadence_value.value)
                    return int(cadence_value)
                return 0

        except Exception as e:
            logger.error(f"Failed to get total proposals: {e}")
            return 0

    async def _generate_blockchain_summary(self, full_summary: str, analysis_data: Dict) -> str:
        """Generate a concise summary for blockchain storage"""
        try:
            from google import genai

            client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

            prompt = f"""Create a neutral data summary for a park proposal focusing only on NDVI and PM2.5 metrics.

Key data points to include:
- Park name: {analysis_data.get('parkName', 'Unknown')}
- NDVI change: {analysis_data.get('ndviBefore', 0)} → {analysis_data.get('ndviAfter', 0)}
- PM2.5 increase: {analysis_data.get('pm25IncreasePercent', 0)}%

Requirements:
- Must be between 230-240 characters exactly
- Only include NDVI and PM2.5 data
- Neutral factual tone only
- No emotional words or judgments
- Include exact numerical values

Return only the factual summary."""

            response = client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=prompt
            )

            summary = response.text.strip()

            # Ensure length constraints
            if len(summary) < 230:
                summary += " Environmental impact assessment indicates significant changes."
            elif len(summary) > 240:
                summary = summary[:240]

            return summary

        except Exception as e:
            logger.warning(f"Failed to generate summary: {e}")
            # Fallback summary
            park_name = analysis_data.get('parkName', 'Park')
            ndvi_before = analysis_data.get('ndviBefore', 0)
            ndvi_after = analysis_data.get('ndviAfter', 0)
            pm25_increase = analysis_data.get('pm25IncreasePercent', 0)

            return f"{park_name}: NDVI {ndvi_before}→{ndvi_after}, PM2.5 +{pm25_increase}%"

    def _parse_proposal_result(self, result: Any, proposal_id: int = None) -> Dict[str, Any]:
        """Parse Flow blockchain result into proposal dict"""
        try:
            if not result:
                return None

            # Handle Optional type - check if result has value
            if hasattr(result, 'value') and result.value is None:
                return None

            # Get the actual struct value
            proposal_struct = result.value if hasattr(result, 'value') else result

            if not proposal_struct:
                return None

            # Cadence structs store fields in a dictionary
            # The struct.id returns the type identifier, but struct.fields contains the actual data
            def get_field_value(struct, field_name):
                """Get value from a Cadence struct field"""
                try:
                    # Access the fields dictionary
                    if hasattr(struct, 'fields') and isinstance(struct.fields, dict):
                        field_obj = struct.fields.get(field_name)
                        if field_obj is None:
                            return None

                        # If it's a string (like the struct id), return it
                        if isinstance(field_obj, str):
                            return field_obj

                        # Extract value from Cadence types
                        if hasattr(field_obj, 'value'):
                            return field_obj.value
                        return field_obj
                    return None
                except Exception as e:
                    logger.warning(f"Error getting field {field_name}: {e}")
                    return None

            # Helper to convert UFix64 to float (divide by 1e8)
            def ufix64_to_float(value):
                if value is None:
                    return 0.0
                # UFix64 .value returns the raw integer (already multiplied by 1e8)
                # We need to divide by 1e8 to get the actual float value
                return float(value) / 1e8

            # Helper to convert UInt64 to int
            def uint64_to_int(value):
                if value is None:
                    return 0
                return int(value)

            # Extract fields from the Cadence struct
            # Note: The 'id' field is overridden by Flow SDK with the struct type identifier,
            # so we use the proposal_id parameter passed in
            if proposal_id is None:
                # Fallback: try to get it from fields (will likely fail)
                proposal_id = uint64_to_int(get_field_value(proposal_struct, 'id'))
            park_name = str(get_field_value(proposal_struct, 'parkName') or '')
            park_id = str(get_field_value(proposal_struct, 'parkId') or '')
            description = str(get_field_value(proposal_struct, 'description') or '')
            yes_votes = uint64_to_int(get_field_value(proposal_struct, 'yesVotes'))
            no_votes = uint64_to_int(get_field_value(proposal_struct, 'noVotes'))
            end_date = ufix64_to_float(get_field_value(proposal_struct, 'endDate'))
            creator = str(get_field_value(proposal_struct, 'creator') or '')

            # Get status enum
            status_enum = get_field_value(proposal_struct, 'status')
            # Status enum: 0 = Active, 1 = Accepted, 2 = Declined
            if hasattr(status_enum, 'value'):
                status_value = status_enum.value
            elif hasattr(status_enum, 'rawValue'):
                status_value = get_field_value(status_enum, 'rawValue')
            else:
                status_value = status_enum

            # Map status
            status_map = {0: 'active', 1: 'passed', 2: 'rejected'}
            status = status_map.get(int(status_value) if status_value is not None else 0, 'active')

            # Parse environmental data
            env_data = get_field_value(proposal_struct, 'environmentalData')
            environmental_data = {
                'ndviBefore': ufix64_to_float(get_field_value(env_data, 'ndviBefore')),
                'ndviAfter': ufix64_to_float(get_field_value(env_data, 'ndviAfter')),
                'pm25Before': ufix64_to_float(get_field_value(env_data, 'pm25Before')),
                'pm25After': ufix64_to_float(get_field_value(env_data, 'pm25After')),
                'pm25IncreasePercent': ufix64_to_float(get_field_value(env_data, 'pm25IncreasePercent')),
                'vegetationLossPercent': ufix64_to_float(get_field_value(env_data, 'vegetationLossPercent')),
            }

            # Parse demographics
            demo_data = get_field_value(proposal_struct, 'demographics')
            demographics = {
                'children': uint64_to_int(get_field_value(demo_data, 'children')),
                'adults': uint64_to_int(get_field_value(demo_data, 'adults')),
                'seniors': uint64_to_int(get_field_value(demo_data, 'seniors')),
                'totalAffectedPopulation': uint64_to_int(get_field_value(demo_data, 'totalAffectedPopulation')),
            }

            return {
                'id': proposal_id,
                'parkName': park_name,
                'parkId': park_id,
                'description': description,
                'yesVotes': yes_votes,
                'noVotes': no_votes,
                'endDate': int(end_date),
                'creator': creator,
                'status': status,
                'environmentalData': environmental_data,
                'demographics': demographics,
            }

        except Exception as e:
            logger.error(f"Failed to parse proposal result: {e}")
            logger.error(f"Result type: {type(result)}")
            logger.error(f"Result: {result}")
            import traceback
            traceback.print_exc()
            return None


# Maintain backward compatibility
BlockchainService = FlowBlockchainService
