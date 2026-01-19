curl -X 'POST' \
  'http://localhost:8000/tpay/backend/transaction' \
  -H 'Authorization: Bearer test-token' \
  -H 'Content-Type: application/json' \
  -d '{
  "amount": "100.00",
  "currency": "USD",
  "purpose": "Test Payment",
  "recipient": "Jane Doe",
  "callbackUrl": "https://example.com/callback",
  "transactionType": "PAYMENT"
}'

