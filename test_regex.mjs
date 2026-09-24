const sms = "UGE2A00EV7 Confirmed.You have received Ksh1.00 from ZIPPORAH MURUNGA 0701***580 on 14/7/26 at 12:24 PM New M-PESA balance is Ksh53.54.";
const txRegex = /\b([A-Z0-9]{10})\b/;
const amtRegex = /Ksh\s*([0-9,]+\.?[0-9]*)/;
const fromRegex = /(?:received from|paid to|from) ([A-Z a-z]+) ([\d*]+)/i;

console.log("Tx:", sms.match(txRegex));
console.log("Amt:", sms.match(amtRegex));
console.log("From:", sms.match(fromRegex));
