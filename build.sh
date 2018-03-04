set -xe
rm -f create_address.zip send_email.zip
7z a create_address.zip create_address.py
7z a send_email.zip send_email.py
(cd html && node ./node_modules/webpack-cli/bin/webpack.js --mode development)
