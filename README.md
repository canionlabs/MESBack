## CanionLabs - Cloud

### Installation

##### DEV Environment

```
make init-dev 
```

##### PROD Environment

```
make init-prod
```

### Decouple Settings

```
SECRET_KEY=super-secret-key
DEBUG=False
DATABASE_URL=postgres://user:password@127.0.0.1:5432/mes_cloud
MONGO_URI=localhost:27017
```

### Generate documentation

Install [doxygen](http://www.stack.nl/~dimitri/doxygen/download.html)

```
# Generate / Update documentation and server 
make gen-doc
```