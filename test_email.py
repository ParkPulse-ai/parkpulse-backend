"""
Test script for email notification service
Run this to verify your email configuration is working
"""

import asyncio
from dotenv import load_dotenv

# Load environment variables FIRST before importing email_service
load_dotenv()

from email_service import send_proposal_notification_email


def test_email():
    """Test sending a proposal notification email"""
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║          ParkPulse.ai - Email Test Script                  ║")
    print("╚══════════════════════════════════════════════════════════════╝\n")

    print("Testing email configuration...\n")

    # Test data
    park_name = "Central Park"
    proposal_id = 999
    end_date = "November 30, 2025"
    description = "Test proposal to verify email notification system is working correctly. NDVI change from 0.750 to 0.250, PM2.5 increase of 45.2%"

    print(f"Park Name: {park_name}")
    print(f"Proposal ID: {proposal_id}")
    print(f"End Date: {end_date}")
    print(f"Recipient: vvdev25@gmail.com")
    print(f"\nSending test email...\n")

    # Send email
    success = send_proposal_notification_email(
        park_name=park_name,
        proposal_id=proposal_id,
        end_date=end_date,
        description=description
    )

    if success:
        print("✅ SUCCESS!")
        print("\nTest email sent successfully to vvdev25@gmail.com")
        print("\nPlease check your inbox (and spam folder) for the email.")
        print("\n" + "="*60)
        print("Email Configuration: WORKING ✓")
        print("="*60)
    else:
        print("❌ FAILED!")
        print("\nEmail sending failed. Please check:")
        print("1. Your .env file has the correct email settings")
        print("2. SENDER_EMAIL and SENDER_PASSWORD are set correctly")
        print("3. You're using an App Password (not your regular password)")
        print("4. Your firewall isn't blocking SMTP connections")
        print("\nSee EMAIL_SETUP.md for detailed setup instructions.")
        print("\n" + "="*60)
        print("Email Configuration: FAILED ✗")
        print("="*60)


if __name__ == "__main__":
    test_email()
