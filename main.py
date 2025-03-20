import asyncio
import os
from pathlib import Path
import core
import core.captcha
import modules.faucet
import settings
from utils import utils
from core.process_wallets import process_wallets


def configure_settings():
    print("\n=== SAHARA AI Configuration Menu ===")
    print("1. Configure sleep times")
    print("2. Configure thread settings")
    print("3. Configure API key")
    print("4. Configure actions")
    print("5. Start the process")
    print("6. Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-6): ")
            
            if choice == "1":
                print("\n=== Sleep Times Configuration ===")
                min_wallet = int(input("Enter minimum sleep time between wallets (in seconds): "))
                max_wallet = int(input("Enter maximum sleep time between wallets (in seconds): "))
                min_action = int(input("Enter minimum sleep time between actions (in seconds): "))
                max_action = int(input("Enter maximum sleep time between actions (in seconds): "))
                
                settings.sleep_wallets = [min_wallet, max_wallet]
                settings.sleep_actions = [min_action, max_action]
                print("Sleep times configured successfully!")
                
            elif choice == "2":
                print("\n=== Thread Settings Configuration ===")
                threads = int(input("Enter number of threads (1-10): "))
                skip = int(input("Enter number of wallets to skip (0 or more): "))
                
                settings.threads = max(1, min(10, threads))
                settings.skip_wallets = max(0, skip)
                print("Thread settings configured successfully!")
                
            elif choice == "3":
                print("\n=== API Key Configuration ===")
                api_key = input("Enter your 2captcha API key: ")
                settings.api_key = api_key
                print("API key configured successfully!")
                
            elif choice == "4":
                print("\n=== Actions Configuration ===")
                settings.Faucet = input("Enable Faucet? (y/n): ").lower() == 'y'
                settings.Transaction = input("Enable Transaction? (y/n): ").lower() == 'y'
                settings.Claim = input("Enable Claim? (y/n): ").lower() == 'y'
                print("Actions configured successfully!")
                
            elif choice == "5":
                print("\nCurrent Configuration:")
                print(f"Sleep between wallets: {settings.sleep_wallets[0]}-{settings.sleep_wallets[1]} seconds")
                print(f"Sleep between actions: {settings.sleep_actions[0]}-{settings.sleep_actions[1]} seconds")
                print(f"Threads: {settings.threads}")
                print(f"Skip wallets: {settings.skip_wallets}")
                print(f"API Key: {'Configured' if settings.api_key else 'Not configured'}")
                print(f"Faucet: {'Enabled' if settings.Faucet else 'Disabled'}")
                print(f"Transaction: {'Enabled' if settings.Transaction else 'Disabled'}")
                print(f"Claim: {'Enabled' if settings.Claim else 'Disabled'}")

                
                if input("\nStart the process? (y/n): ").lower() == 'y':
                    return True
                else:
                    print("Process cancelled.")
                    
            elif choice == "6":
                print("Exiting...")
                return False
                
            else:
                print("Invalid choice. Please try again.")
                
        except ValueError:
            print("Invalid input. Please enter a valid number.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")


async def main():
    if len(private_keys) != len(proxies):
        raise Exception('Private keys do not match the number of proxies')
    elif len(private_keys)  == 0 or len(proxies) == 0:
        raise Exception('No proxies and private keys found')
    
    start_index = settings.skip_wallets

    tasks = []
    for count, (private_key, proxy) in enumerate(zip(private_keys[start_index:], proxies[start_index:]), start=start_index + 1):
        tasks.append(process_wallets(private_keys, count, private_key, proxy))

    await asyncio.gather(*tasks)


if __name__ == '__main__':
    BASE_DIR = Path(__file__).resolve().parent
    private_keys = utils.read_file(os.path.join(BASE_DIR, "data", "private_keys.txt"))
    proxies = utils.read_file(os.path.join(BASE_DIR, "data", "proxies.txt"))
    
    if configure_settings():
        asyncio.run(main())
