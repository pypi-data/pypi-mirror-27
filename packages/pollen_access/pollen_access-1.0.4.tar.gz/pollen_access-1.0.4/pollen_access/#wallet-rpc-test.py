#wallet-rpc-test
#12-21-17 Alex Dai

from pollen_access import wallet

w = wallet.Wallet('ADDRESS', 'localhost', '51515')

balance = w.get_available_balance()

payment_id = w.generate_payment_id('Thanks for the fish')

tx_hash = transfer(self, 100, 'SENDADDRESS', payment_id, mixin=4)