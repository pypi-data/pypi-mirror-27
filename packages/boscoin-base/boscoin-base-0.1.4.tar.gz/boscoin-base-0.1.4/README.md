[![Build Status](https://travis-ci.org/StellarCN/py-stellar-base.svg)](https://travis-ci.org/StellarCN/py-stellar-base)

# Note
Python libraries that allow you to interface with the Boscoin horizon interface.
Boscoin-base library consists of classes to read, write, hash, and sign the xdr structures that are used in boscoin-core.
Currently testnet is connected to that of stellar, but it will be fixed once
Boscoin starts to run thier own.


# Installation
    `pip install boscoin-base`
# Quick Start

## 1. Create a Stellar key pair
There are 2 methods for generating a key pair in `py-boscoin-base`.

### 1.1 Random generation
```python
    from boscoin_base.keypair import Keypair
    kp = Keypair.random()
```    

### 1.2 Deterministic generation
Or we may generate from a Unicode mnemonic string:
```python
    from boscoin_base.utils import StellarMnemonic
    sm = StellarMnemonic("chinese") # here we use chinese, but default language is 'english'
    m = sm.generate() 
    # or m = u'域 监 惜 国 期 碱 珍 继 造 监 剥 电' (must add u'' before the string if using Python 2)
    kp = Keypair.deterministic(m, lang='chinese')
```
After the key pair generation, we can get a public key/seed from it:
 ```python
    publickey = kp.address().decode()
    seed = kp.seed().decode()
```    
The public key is also your account address. If someone needs to send you a transaction, you should share with them this key.
The seed is your secret. For safety, please keep it local and never send it through the Internet.

Whenever we forget/lose your public key, we can regenerate the key pair from the seed:
```python
    from boscoin_base.keypair import Keypair
    kp = Keypair.from_seed(seed)
```   
This is my favorite key pair in TESTNET, let's use them in the following steps.
```python
    publickey = 'GDVDKQFP665JAO7A2LSHNLQIUNYNAAIGJ6FYJVMG4DT3YJQQJSRBLQDG'
    seed = 'SCVLSUGYEAUC4MVWJORB63JBMY2CEX6ATTJ5MXTENGD3IELUQF4F6HUB'
```   

## 2.Create Account
After the key pair generation, you have already got the address, but it is not activated until someone transfers at least 20 lumen into it. 

### 2.1 Testnet
If you want to play in the Stellar test network, you can ask our Friendbot to create an account for you as shown below:
```python
    import requests
    publickey=kp.address().decode()
    r=requests.get('https://horizon-testnet.stellar.org/friendbot?addr='+publickey)
```
### 2.2 Livenet
On the other hand, if you would like to create an account in the livenet, you should buy some BOS from an exchange.
When you withdraw the BOS into your new account, the exchange will automatically create the account for you.
However, if you want to create an account from another account of your own, you may run the following code:
```python
    from boscoin_base.keypair import Keypair
    from boscoin_base.asset import Asset
    from boscoin_base.operation import Payment
    from boscoin_base.operation import CreateAccount
    from boscoin_base.transaction import Transaction
    from boscoin_base.transaction_envelope import TransactionEnvelope as Te
    from boscoin_base.memo import TextMemo
    from boscoin_base.horizon import horizon_testnet, horizon_livenet
    
    oldAccountSeed = "SCVLSUGYEAUC4MVWJORB63JBMY2CEX6ATTJ5MXTENGD3IELUQF4F6HUB"
    newAccountAddress = "XXX"
    amount = '25' # Any amount higher than 0.1
    kp = Keypair.from_seed(oldAccountSeed)
    horizon = horizon_livenet()
    asset = Asset("BOS")
    # create op 
    op = CreateAccount({
        'destination': newAccountAddress,
        'starting_balance': amount
    })
    # create a memo
    msg = TextMemo('')
    # get sequence of new account address
    sequence = horizon.account(kp.address()).get('sequence')
    # construct the transaction
    tx = Transaction(
        source=kp.address().decode(),
        opts={
            'sequence': sequence,
            #'timeBounds': [],
            'memo': msg,
            #'fee': 10000,
            'operations': [
                op,
            ],
         },
    )
    # build envelope
    envelope = Te(tx=tx, opts={"network_id": "PUBLIC"})
    # sign 
    envelope.sign(kp)
    # submit
    xdr = envelope.xdr()
    response = horizon.submit(xdr)
    
```
Then, you can check the status of this operation with the response.

## 3. Check account
### 3.1 Basic info
After creating the account, we may check the basic information of the account.
```python
    from boscoin_base.address import Address
    publickey = 'GDVDKQFP665JAO7A2LSHNLQIUNYNAAIGJ6FYJVMG4DT3YJQQJSRBLQDG'
    address = Address(address=publickey) # address = Address(address=publickey,network='public') for livenet
    address.get() # get the updated information
```
Now you can check the address `balance`, `sequence`, `flags`, `signers`, `data` etc.
```python
    print "balances: " + address.balances
    print "sequence: " + address.sequence
    print "flags: " + address.flags
    print "signers: " + address.signers
    print "data: " + address.data
```

### 3.2 Check payments
We can check the most recent payments by:
`address.payments()`

We can use three parameters to customize the query: `limit`, `order`, and `cursor` (`paging_token`), and the default value for them are respectively: `limit=10, order="asc", cursor=0`.

So if you need to check payments after a specific cursor, try:
`address.payments(cursor='4225135422738433', limit=20, order='asc')`

Horizon has SSE support for push data, if you really want to, use it like this: `address.payments(sse=True, cursor='4225135422738433')`

### 3.3 Check others
Just like payments, we can check `transactions`, `effects`, `offers`, and `operations` by:
```python
     address.transactions()
     address.effects()
     address.offers()
     address.operations()
```
By the way, offers do not have SSE support.

## 4. Building transaction
We can build a transaction with a wrapper or from scratch.

### 4.1 Build with a wrapper
```python
    from boscoin_base.builder import Builder
    seed = "SCVLSUGYEAUC4MVWJORB63JBMY2CEX6ATTJ5MXTENGD3IELUQF4F6HUB"
    builder = Builder(secret=seed) # builder = Builder(secret=seed, network='public') for LIVENET
```
How about sending Bob a payment?
```python
    bob_address = 'XXX'
    builder.append_payment_op(bob_address,'100','BOS')
```
Or if you want to pay him with CNY:
```python
    CNY_ISSUER = 'GDVDKQFP665JAO7A2LSHNLQIUNYNAAIGJ6FYJVMG4DT3YJQQJSRBLQDG'# Just a Stellar address which issues asset CNY
    builder.append_payment_op(bob_address, '100', 'CNY', CNY_ISSUER)
```
And maybe you need to carry a message:
```python
    builder.add_text_memo('Buy yourself a beer!') # string length <= 28 bytes
```    
At last, sign & submit
 ```python   
    builder.sign()
    builder.submit()
```
Done.

Sometimes, we need to deal with multi-signature transactions. Especially when you get a xdr string (or transaction envelope xdr) from a friend or partner, which describes a multi-sig transaction. They may need you to sign on it too. 
```python
    builder = Builder(secret=seed) # or builder = Builder(secret=secret, network='public') for LIVENET.
    builder.import_from_xdr(xdr_string) # the xdr_string come from your friend
    builder.sign()
    builder.to_xdr() # generate new xdr string 
    # or builder.submit() # submit to Stellar network
```

### 4.2 Build from scratch
```python   
    from boscoin_base.keypair import Keypair
    from boscoin_base.asset import Asset
    from boscoin_base.operation import Payment
    from boscoin_base.transaction import Transaction
    from boscoin_base.transaction_envelope import TransactionEnvelope as Te
    from boscoin_base.memo import TextMemo
    from boscoin_base.horizon import horizon_testnet, horizon_pubic
    
    alice_seed = 'SAZJ3EDATROKTNNN4WZBZPRC34AN5WR43VEHAFKT5D66UEZTKDNKUHOK'
    bob_address = 'GDLP3SP4WP72L4BAJWZUDZ6SAYE4NAWILT5WQDS7RWC4XCUNUQDRB2A4'
    CNY_ISSUER = 'GDVDKQFP665JAO7A2LSHNLQIUNYNAAIGJ6FYJVMG4DT3YJQQJSRBLQDG'
    amount = '100'
    
    Alice = Keypair.from_seed(alice_seed)
    horizon = horizon_testnet()# horizon = horizon_pubic() for LIVENET
    
    asset = Asset('CNY', CNY_ISSUER) 
    # create op 
    op = Payment({
        # 'source' : Alice.address().decode(),
        'destination': bob_address,
        'asset': asset,
        'amount': amount
    })
    # create a memo
    msg = TextMemo('Buy yourself a beer !')
    
    # get sequence of Alice
    sequence = horizon.account(Alice.address()).get('sequence') 
    
    # construct Tx
    tx = Transaction(
        source=Alice.address().decode(),
        opts={
            'sequence': sequence,
            # 'timeBounds': [],
            'memo': msg,
            # 'fee': 10000,
            'operations': [
                op,
            ],
        },
    )
    
    
    # build envelope
    envelope = Te(tx=tx, opts={"network_id": "TESTNET"}) # envelope = Te(tx=tx, opts={"network_id": "PUBLIC"}) for LIVENET
    # sign 
    envelope.sign(Alice)
    # submit
    xdr = envelope.xdr()
    response=horizon.submit(xdr)
```

