const fs = require('fs');

const xmlPath = 'c:\\Softly built updates\\MpesaListenerApp\\app\\src\\main\\res\\layout\\activity_main.xml';
let xmlContent = fs.readFileSync(xmlPath, 'utf8');

// 1. Add etSetPin, btnSetPin, btnLogout to mainContainer.
// We can add them right after btnManualLock.
const lockAppBtnStr = `<Button
                android:id="@+id/btnManualLock"
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:text="🔒 Lock App"
                android:backgroundTint="#EF4444"
                android:textColor="#FFFFFF"
                android:layout_marginBottom="16dp"/>`;

const newUiElements = `<Button
                android:id="@+id/btnManualLock"
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:text="🔒 Lock App"
                android:backgroundTint="#EF4444"
                android:textColor="#FFFFFF"
                android:layout_marginBottom="8dp"/>
                
            <LinearLayout
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:orientation="horizontal"
                android:layout_marginBottom="16dp">
                
                <EditText
                    android:id="@+id/etSetPin"
                    android:layout_width="0dp"
                    android:layout_height="wrap_content"
                    android:layout_weight="1"
                    android:hint="Set 4-Digit Lock PIN"
                    android:inputType="numberPassword"
                    android:maxLength="4"
                    android:background="#E5E7EB"
                    android:padding="12dp"
                    android:layout_marginEnd="8dp"/>
                    
                <Button
                    android:id="@+id/btnSetPin"
                    android:layout_width="wrap_content"
                    android:layout_height="wrap_content"
                    android:text="Save PIN"
                    android:backgroundTint="#3B82F6"
                    android:textColor="#FFFFFF"/>
            </LinearLayout>
            
            <Button
                android:id="@+id/btnLogout"
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:text="Logout / Deactivate"
                android:backgroundTint="#6B7280"
                android:textColor="#FFFFFF"
                android:layout_marginBottom="16dp"/>`;

xmlContent = xmlContent.replace(lockAppBtnStr, newUiElements);

// 2. Update etUnlockPin to be 4-digit PIN
const unlockPinRegex = /<EditText\s+android:id="\@\+id\/etUnlockPin"[\s\S]*?\/>/;
const newUnlockPin = `<EditText
            android:id="@+id/etUnlockPin"
            android:layout_width="match_parent"
            android:layout_height="60dp"
            android:hint="4-Digit PIN"
            android:inputType="numberPassword"
            android:maxLength="4"
            android:gravity="center"
            android:textSize="24sp"
            android:background="#F3F4F6"
            android:padding="8dp"
            android:layout_marginBottom="24dp"/>`;

xmlContent = xmlContent.replace(unlockPinRegex, newUnlockPin);

fs.writeFileSync(xmlPath, xmlContent, 'utf8');
console.log("Updated activity_main.xml");
