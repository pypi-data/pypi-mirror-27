# Parameter Encoder

## TL;DR Version:
In case you need a refresher on what we're using the Parameter Encoder for:
* encode_data - Accepts a dictionary and a key and encodes the data - returning a url safe string
* decode_data - Accepts an encoded data string and a key used to decode it - returns a dict

## What it does:
The Parameter Encoder contains two functions - one encodes a dict data and the other decodes a string from the encode function.
The key required by both methods is the secret we use to encrypt and decrypt the data.

Any data needed can be added to the `parameters` dictionary

## encode_data
The encode_data method accepts a dictionary and key.
The dictionary can contain but is not limited to:
* email_id
* url_id
* contact_id
* link_type
* redirect_url

It then uses the key to encode the dictionary using the DES algorithm and then uses base64 to make it short and urlsafe.

## decode_data
The decode_url function accepts an encoded string and a decryption key and returns
a decoded dict usin the key to decrypt the DES algorithm.

## Testing
In order to run the tests - `python url_helper_test.py`
