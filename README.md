# KinTipper

KinTipper is a bot that generates ethereum wallets for Reddit users, and allows them to tip each other with Kin  
**This bot is not live currently, due to the issues that are detailed in the disclaimer**

# Disclaimer
I created this bot in order to  
1. Learn about Reddit bot-making
2. Learn about interacting with the ethereum network from code

Therefore, **this project is not made to be secure and should be treated as such**

When this bot generates a new ethereum wallet, it **SAVES the private keys in PLAIN TEXT**, so access for the new ethereum wallet is not only avilable to the user, but also to the bot creator, and possible Reddit (if they monitor private messages).

For this reaseon, users should not send any large amount of money to their accounts, and this message is added with the creation of a new account:

```
THIS INFO IS ALSO STORED BY KINTIPPER (and Reddit), DO NOT SEND LARGE AMOUNTS OF MONEY TO THIS ADDRESS
```

### Prerequisites

Developed on Python 2.7.12

Needed dependeices are all in the "requirments.txt" file  
Use this to install them
```
pip install -r requirments.txt  
```  


## Built With

* [PRAW](https://github.com/praw-dev/praw) - Used to interact with the reddit API
* [pyEthereum](https://github.com/ethereum/pyethereum) - Used to generate a wallet
* [erc20token-sdk-python](https://github.com/kinfoundation/erc20token-sdk-python) - Used to send/recive data from the ethereum network



## Authors

* **Ron Serruya** - *Initial work* - [Ronserruya](https://github.com/Ronserruya)

## License

The code is currently released under [GPLv2 license](LINK) due to some GPL-licensed packages it uses. (erc20token-sdk-python)


# For the users

## What is this bot?
KinTipper is a bot that allows Reddit users to tip each other with Kin,an ethereum based ERC20 token.


[What is Kin?](https://www.kinecosystem.org/) - Kin is a cryptocurrency token created by Kik Interactive  
[What is Ethereum?](https://en.wikipedia.org/wiki/Ethereum) - Ethereum is the blockchain network Kin is using  
What can I do with my Kin? - You can trade with it, buy things with it, and sell it for fiat currency (regular money)


## How do I use KinTipper?
Every few seconds, the KinTipper bot gets a list of comments, and responds accordingly, so the way to intercat with this bot is to mention his name, and a command

### The !register command:
If you want to register for KinTipper, just submit a comment with the text  
```
KinTipper !register
```
The bot will send you your new wallet details in a private message.  
**IMPORTANT, PLEASE READ THE [DISCLAIMER](#Disclaimer) IN THE TOP OF THIS PAGE, THIS IS NOT DONE IN A SECURE WAY**  
Now you can send Kin and Ether (to pay the fees) to this new wallet

### The tip command  
If you want to tip another Reddit user, you write this in a comment (order of the words is not important)
```
KinTipper /u/<username> <amount>
```
So if for example,I want to thank a user for helping me fix a issue I had, This comment will send 54 Kin from me to the user "CryptoDude"
```
Thank you, it worked! I had trouble with this problem for a week!  
KinTipper /u/CryptoDude 54 :)
```

# Screenshots















