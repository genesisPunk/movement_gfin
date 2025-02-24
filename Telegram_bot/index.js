import { Telegraf, Markup } from 'telegraf';
import fs from 'fs';
import CryptoJS from 'crypto-js';
import { AptosAccount, HexString } from 'aptos';

const bot = new Telegraf('');    // enter your telegram bot key here
const DB_FILE = 'users.json';

// Load or initialize database
const loadDatabase = () => {
    try {
        const data = fs.readFileSync(DB_FILE, 'utf8');
        if (!data) {
            throw new Error('Database file is empty.');
        }
        return JSON.parse(data);
    } catch (error) {
        console.error('Error loading database:', error.message);
        return {};
    }
};

const saveDatabase = (data) => {
    fs.writeFileSync(DB_FILE, JSON.stringify(data, null, 2));
};

let users = loadDatabase();

bot.start((ctx) => {
    const userId = ctx.from.id;
    if (users[userId]) {
        // ctx.reply(`\n<b>Your Address</b><i>(tap to copy)</i>:\n<code>${users[userId].address}</code>\n `, { 
        //     parse_mode: "HTML", 
        //     reply_markup: getWalletKeyboard(userId) 
        // });
        ctx.reply(`\n Your Address:\n${users[userId].address}\n\n `, getWalletKeyboard(userId));
        
    } else {
        ctx.reply('Welcome! Please provide your password and key (separated by a space). \n\n <b>Note:</b>\n <i>We do not store your key or password. Dont forget your passowrd, it will be required in future for txn signing!</i>',  { parse_mode: "HTML" });
    }
});


bot.on('text', (ctx) => {
    const userId = ctx.from.id;
    if (users[userId]) return;

    const [password, key] = ctx.message.text.split(' ');

     // Log the received message to the console
     console.log('Received message:', ctx.message.text); 

    if (!password || !key) {
        return ctx.reply('Invalid format. Please provide both password and key separated by a space.');
    }

    const trimmedKey = key.replace(/^0x/, "");

    // Check if the private key is exactly 64 characters long
    if (trimmedKey.length !== 64) {
        return ctx.reply( key.length.toString() + '  Invalid key length. Please provide a valid 64-character hexadecimal key.');
    }

    // Check if the private key is a valid hexadecimal string
    try {
        HexString.ensure(trimmedKey).toUint8Array();
    } catch (error) {
        console.log(error.toString());
        return ctx.reply('Invalid key. Please provide a valid 64-character hexadecimal key.');
    }

    // Generate Aptos address
    const account = new AptosAccount(Buffer.from(trimmedKey, 'hex'));
    console.log(account.toString());
    const address = account.address().hex();

    // Encrypt the key
    const encryptedKey = CryptoJS.AES.encrypt(trimmedKey, password).toString();

    // Save user data
    users[userId] = { address, encryptedKey };
    saveDatabase(users);

    //ctx.reply(`Your Aptos address: ${address}`, getWalletKeyboard(userId));
    ctx.reply(`Your Address:\n${users[userId].address}\n `, getWalletKeyboard(userId));
    
});

// Generate inline keyboard
const getWalletKeyboard = (userId) => {
    const address = users[userId]?.address;
    return Markup.inlineKeyboard([
        [Markup.button.callback('Wallet  💳', 'wallet'), Markup.button.callback('Test  💎', 'test')],
        [Markup.button.url('Show my Portfolio 💰', `https://movement-poc-ui.vercel.app/address?address=${address || ''}`)],
        [Markup.button.url('Show on Explorer 🔎', `https://explorer.movementlabs.xyz/account/${address || ''}`)]
    ]);
};

// Handle button interactions
bot.action('test', (ctx) => ctx.reply('Test feature coming soon!'));

bot.action('wallet', (ctx) => ctx.reply('Wallet feature coming soon!'));

bot.launch();

console.log('Bot is running...');
