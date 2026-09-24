const fs = require('fs');

const ktPath = 'c:\\Softly built updates\\MpesaListenerApp\\app\\src\\main\\java\\com\\softbuild\\mpesalistener\\MainActivity.kt';
let ktContent = fs.readFileSync(ktPath, 'utf8');

// The file has:
//        try { unregisterReceiver(logReceiver) } catch (_: Exception) {}
//    
//
//    private fun showPinLock() {

ktContent = ktContent.replace(
    'try { unregisterReceiver(logReceiver) } catch (_: Exception) {}',
    'try { unregisterReceiver(logReceiver) } catch (_: Exception) {}\n    }'
);

fs.writeFileSync(ktPath, ktContent, 'utf8');
console.log("Fixed missing closing brace on onDestroy");
