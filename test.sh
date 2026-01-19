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

echo "\n"

curl -X 'GET' \
  'http://localhost:8000/tpay/backend/transaction/148b9947-aad2-4974-8827-4375e7dca844' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer test-token'
