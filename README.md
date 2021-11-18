# Github Actions and Lambda Vault secret management demo


Setup steps to be automated

- Fork repository
- Ensure you have a terrform cloud account and get a token
- Create a world facing Vault server with TLS
- Create and AWS programatic user to use to do the terraform things
- Setup kv storage storing your AWS creds

```
vault secrets enable -version=1 -path="pipeline" kv
vault kv put pipeline/aws/creds secret_key=***************** security_token=******************* access_key=ap-southeast-2
vault kv put pipeline/terraform/creds token=*******************
vault kv put pipeline/lambda/data date=null
```

- Setup Vault policy to access the kv data

```
path "pipeline/aws/creds" {
  capabilities = [ "read" ]
}

path "pipeline/terraform/creds" {
  capabilities = [ "read" ]
}

path "pipeline/lambda/data" {
  capabilities = [ "read", "update" ]
}
```

- setup approle authentication

```
vault auth enable approle
vault write auth/approle/role/githubActions secret_id_ttl=86400 token_num_uses=10 token_ttl=14400 token_max_ttl=86400 secret_id_num_uses=0 token_policies="github"
```

- get role and secret id and store then im repo secrets along with the vault address names as:
VAULT_ADDR
VAULT_NAMESPACE
VAULT_ROLE_ID
VAULT_SECRET_ID
VAULTCA (if you created your own)

```
vault read auth/approle/role/githubActions/role-id
vault write -f auth/approle/role/githubActions/secret-id
```
