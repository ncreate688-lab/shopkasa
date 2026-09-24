import re

def restore_mpesa():
    with open('src/App_backup.jsx', 'r', encoding='utf-8') as f:
        backup_content = f.read()
    
    with open('src/App.jsx', 'r', encoding='utf-8') as f:
        app_content = f.read()

    # Extract CheckoutModal from backup
    # Find start: const CheckoutModal =
    start_idx_backup = backup_content.find('const CheckoutModal = ({ cart, onConfirm')
    end_idx_backup = backup_content.find('\n    const BulkPriceUpdateModal =', start_idx_backup)
    
    if start_idx_backup == -1 or end_idx_backup == -1:
        print("Could not find CheckoutModal in backup")
        return
        
    checkout_modal_backup = backup_content[start_idx_backup:end_idx_backup]

    # Extract CheckoutModal from app
    start_idx_app = app_content.find('const CheckoutModal = ({ cart, onConfirm')
    end_idx_app = app_content.find('\n    const BulkPriceUpdateModal =', start_idx_app)
    
    if start_idx_app == -1 or end_idx_app == -1:
        print("Could not find CheckoutModal in app")
        return
        
    # Replace in app
    new_app_content = app_content[:start_idx_app] + checkout_modal_backup + app_content[end_idx_app:]
    
    with open('src/App.jsx', 'w', encoding='utf-8') as f:
        f.write(new_app_content)
        
    print("Successfully restored CheckoutModal from backup!")

restore_mpesa()
