import os
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient

AZClientID = os.getenv('AZURE_CLIENT_ID')
AZClientSecret = os.getenv('AZURE_CLIENT_SECRET')
AZTenentID = os.getenv('AZURE_TENANT_ID')

akvURI = 'https://akvvault.azure.net'

_azcredential = ClientSecretCredential(
    tenant_id=AZTenentID,
    client_id=AZClientID,
    client_secret=AZClientSecret
)

def getpsqluser():
    _kvClient = SecretClient (
        vault_url=akvURI,
        credential=_azcredential
    )
    psql_user = _kvClient.get_secret("psql-user").value

    return(psql_user)

def getpsqlsecrect():
    _kvClient = SecretClient (
        vault_url=akvURI,
        credential=_azcredential
    )
    psql_pass = _kvClient.get_secret("psql-secrect").value

    return(psql_pass)

def getifbuser():
    _kvClient = SecretClient (
        vault_url=akvURI,
        credential=_azcredential
    )
    ifb_user = _kvClient.get_secret("infoblox-user").value

    return(ifb_user)

def getifbSecret():
    _kvClient = SecretClient (
        vault_url=akvURI,
        credential=_azcredential
    )
    ifb_secrect = _kvClient.get_secret("infoblox-secrect").value

    return(ifb_secrect)
