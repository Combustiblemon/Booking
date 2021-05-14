# Documentation

## Encryption

To make the server HTTPS a cert and a private key are needed.
The command used to create the  key and cert pairs is:
`openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365`
Any application will only need the cert to verify. Never give out the private key.

After you create the key you'll need to add their paths to the .env file.
Open the `example.env` file and add them

```txt
PATH_TO_CERT=C:\path\to\cert.pem
PATH_TO_KEY=C:\path\to\key.pem
```

## Admin

As of 5/2021 accounts can only be added manually to the DB.
For a client to connect successfully they will need a user and client created for them by the admin by going to the server root address.
The user only needs to know the username and password.

## Filters

list of tuples, each tuple is an operation. eg:

```py
(tuple1) AND (tuple2) AND (tuple3) ...
```

tuples should be:

```py
(parameter_name: str, value: any, operation: str)
```

for the "like" and "or" operations the tuples should be:

```py
([parameter1_name: str, parameter2_name: str], [value1: any, value2: any], operation: str)
```

`value1` and `value2` map to `parameter1_name` and `parameter2_name` respectively.

```txt
        posible operations:
            eq -> ==
            lt -> <
            gt -> >
            ge -> >=
            le -> <=
            nt -> !=
            like
            or
```
