#import python libraries
import os
from azure.datalake.store import core, lib, multithread
from azure.keyvault import KeyVaultClient
from azure.common.credentials import ServicePrincipalCredentials
from flask import Flask

adls_service_identity_name = os.environ['ADLS']
adls_folder_name = os.environ['ADLS_FOLDER']
adls_service_identity_tenant = os.environ['TENANT_ID']
adls_service_principal_appid = os.environ['SPN_ID']
adls_service_principal_pwd = os.environ['SPN_KEY']
credentials = MSIAuthentication(resource='https://vault.azure.net')
adlCreds = lib.auth(tenant_id = adls_service_identity_tenant, client_id = adls_service_principal_appid, client_secret = adls_service_principal_pwd)
key_vault_client = KeyVaultClient(credentials)
key_vault_uri = "https://pythonwebapp.vault.azure.net/"

#create adls client
adlsFileSystemClient = core.AzureDLFileSystem(adlCreds, store_name=adls_service_identity_name)

app = Flask(__name__)

@app.route('/')

def webapp():

    adlsFileSystemClient.mkdir(adls_folder_name)

    #write to adls
    results = adls_folder_name + '/dummy.txt'
    str_msg = 'This is dummy file'
    with adlsFileSystemClient.open(results, 'wb') as f:
        f.write(str.encode(str_msg))
        f.close()

    client_id = key_vault_client.get_secret(key_vault_uri, "client-id", "7268bdedce754db8a74bc01943cfeccd")
    client_key = key_vault_client.get_secret(key_vault_uri, "client-key", "5c319df69be24b7b8d06ef555e2ca73f")

    return  'client_id:  {} <br/> client_key: {}'.format(client_id.value, client_key.value)

if __name__ == "__main__":
    app.run()