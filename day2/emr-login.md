
Login into EMR from your terminal

open terminal

cd into the directory where you have the pem file

```
cd Downloads
```

make pem file read only

```
chmod 400 azure3-batch.pem
```

On AWS Console/ EMR cluster, go to your cluster name

Copy Primary Node DNS address 

Replace <<primary-node-cns-paste-here>> with primary dns

```
ssh -i azure3-batch.pem hadoop@<<primary-node-cns-paste-here>>
```

if you asked for finger print validation, type yes and enter.. asked only once.

