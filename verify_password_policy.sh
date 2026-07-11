#!/bin/bash
echo "=== Password Policy Verification ==="
echo ""

echo "1. Global settings from /etc/login.defs:"
grep -E "^PASS_(MAX|MIN|WARN)" /etc/login.defs 2>/dev/null || echo "  ⚠️  Settings not found in /etc/login.defs"
echo ""

echo "2. All non-system users and their warning days:"
for user in $(awk -F: '$3>=1000 {print $1}' /etc/passwd); do
    warn_days=$(sudo chage -l "$user" 2>/dev/null | grep "warning" | awk -F': ' '{print $2}')
    expiry=$(sudo chage -l "$user" 2>/dev/null | grep "Password expires" | awk -F': ' '{print $2}')
    echo "  $user: Warning days = ${warn_days:-Not set}, Expires = $expiry"
done
echo ""

echo "3. Users expiring within 5 days:"
today=$(date +%s)
for user in $(awk -F: '$3>=1000 {print $1}' /etc/passwd); do
    expiry_date=$(sudo chage -l "$user" 2>/dev/null | grep "Password expires" | cut -d: -f2 | tr -d ' ')
    if [[ "$expiry_date" != "never" && "$expiry_date" != "" ]]; then
        expiry_epoch=$(date -d "$expiry_date" +%s 2>/dev/null)
        days_left=$(( ($expiry_epoch - $today) / 86400 ))
        if [[ $days_left -le 5 && $days_left -ge 0 ]]; then
            echo "  ⚠️  $user: Password expires in $days_left days"
        fi
    fi
done
