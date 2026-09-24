const fs = require('fs');

const path = 'c:\\Softly built updates\\MpesaListenerApp\\app\\src\\main\\res\\layout\\activity_main.xml';
let content = fs.readFileSync(path, 'utf8');

// 1. Add manual lock button to mainContainer. Let's put it next to "M-Pesa Auto Verify" title or just below it.
const manualLockBtn = `
            <Button
                android:id="@+id/btnManualLock"
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:text="🔒 Lock App"
                android:backgroundTint="#EF4444"
                android:textColor="#FFFFFF"
                android:layout_marginBottom="16dp"/>
`;
content = content.replace(/<TextView\s+android:layout_width="match_parent"\s+android:layout_height="wrap_content"\s+android:text="POS \/ Web App Settings"[\s\S]*?\/>/, 
`$&
${manualLockBtn}`);

// 2. Add pinContainer at the end of FrameLayout
const pinContainer = `
    <!-- PIN Lock Container -->
    <LinearLayout
        android:id="@+id/pinContainer"
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        android:orientation="vertical"
        android:gravity="center"
        android:padding="32dp"
        android:background="#FFFFFF"
        android:visibility="gone"
        android:elevation="10dp">
        
        <ImageView
            android:layout_width="80dp"
            android:layout_height="80dp"
            android:src="@android:drawable/ic_secure"
            android:tint="#4CAF50"
            android:layout_marginBottom="16dp"/>

        <TextView
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="App Locked"
            android:textSize="28sp"
            android:textStyle="bold"
            android:textColor="#1F2937"
            android:layout_marginBottom="8dp"/>
            
        <TextView
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="Enter your profile password/PIN to unlock."
            android:textSize="14sp"
            android:textColor="#6B7280"
            android:textAlignment="center"
            android:layout_marginBottom="32dp"/>

        <EditText
            android:id="@+id/etUnlockPin"
            android:layout_width="match_parent"
            android:layout_height="60dp"
            android:hint="Password / PIN"
            android:inputType="textPassword"
            android:gravity="center"
            android:textSize="18sp"
            android:background="#F3F4F6"
            android:padding="8dp"
            android:layout_marginBottom="24dp"/>

        <Button
            android:id="@+id/btnUnlockPin"
            android:layout_width="match_parent"
            android:layout_height="60dp"
            android:text="Unlock"
            android:textSize="18sp"
            android:backgroundTint="#4CAF50"
            android:textColor="#FFFFFF"/>
            
    </LinearLayout>
`;

content = content.replace('</FrameLayout>', `${pinContainer}\n</FrameLayout>`);

fs.writeFileSync(path, content, 'utf8');
console.log("activity_main.xml updated");
