import ipfshttpclient as ipfs

ipfs_client = ipfs.connect("/ip4/127.0.0.1/tcp/5001")

address = ipfs_client.add("app/photo/1u2cbb88646aa5482487fc0f3884989cb1.png")

print(address)
# print(ipfs_client.cat(address))
