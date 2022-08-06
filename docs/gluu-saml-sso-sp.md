# SP initiated SAML flow for Gluu Solo

This article will guide you through the process of a Service Provider (SP) initiated SAML flow for Single Sign On using Gluu as the Identity Provider (IDP). We will be using a locally run Flask application as the SP, which is the [python3-saml](https://github.com/onelogin/python3-saml) library's Flask demo application, modified for our needs. This was tested on Gluu Server 4.4.

## Requirements
- Python3
- Pip3
- Gluu server installation with the [Shibboleth SAML IDP](https://gluu.org/docs/gluu-server/operation/faq/#adding-passportjs-andor-shibboleth-idp-post-installation) and [Passport](https://gluu.org/docs/gluu-server/authn-guide/inbound-saml-passport/#enable-passport) installed and enabled.

## Preparations
1. Create a virtual environment in Python: `python -m venv venv`
2. And activate it: `source venv/bin/activate`
3. Install dependencies: `pip install flask python3-saml`
3. Clone the OneLogin Python3 repository: `git clone https://github.com/onelogin/python3-saml.git`
4. And cd to the Flask demo folder: `cd python3-saml/demo-flask`

## Configuring the Flask application
The `index.py` file in this folder is the Flask application that we will be using to demonstrate the SP initiated flow. Inside the `saml/` folder, there is a file called `settings.json` that will contain the majority of the settings for the application. This file is in the JSON format, with two distinct dictionary objects: `sp` and `idp`. These contain the corresponding settings for the SP and the IDP. For the SP, since we are running Flask on our local machine, we will want to replace the hostname with our localhost. Since Flask runs on port 8000 by default, we replace `<sp_domain>` with `localhost:8000`. Be sure to replace `https` with `http` since we don't have TLS implemented locally. 


For the IDP section, we can use a Metadata XML exchange. Python3-saml contains a class that can parse and update settings dynamically from a remote XML file. The code is as follows, which should be executed in the same directory as the `settings.json` file:

```python
from onelogin.saml2.idp_metadata_parser import OneLogin_Saml2_IdPMetadataParser
import json

HOSTNAME = "http://<your hostname>/idp/shibboleth"

with open("settings.json", "r") as f:
    old = json.loads(f.read())

remote = OneLogin_Saml2_IdPMetadataParser.parse_remote(HOSTNAME, validate_cert=False)
newSettings = OneLogin_Saml2_IdPMetadataParser.merge_settings(old, remote)

with open("settings.json", 'w') as f:
    f.write(json.dumps(newSettings, indent=4))
```
I used `validate_cert=False` because my Gluu server was using a self-signed certificate and so didn't support HTTPS. This **will** overwrite the old `settings.json` file, so be sure to make a backup if you want. Finally, our settings.json looks like this:

```json
{
    "strict": true,
    "debug": true,
    "sp": {
        "entityId": "http://localhost:8000/metadata/",
        "assertionConsumerService": {
            "url": "http://localhost:8000/?acs",
            "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST"
        },
        "singleLogoutService": {
            "url": "http://localhost:8000/?sls",
            "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
        },
        "NameIDFormat": "urn:mace:shibboleth:1.0:nameIdentifier",
        "x509cert": "",
        "privateKey": ""
    },
    "idp": {
        "entityId": "https://<hostname>/idp/shibboleth",
        "singleSignOnService": {
            "url": "https://<hostname>/idp/profile/SAML2/Redirect/SSO",
            "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
        },
        "singleLogoutService": {
            "url": "https://<hostname>/idp/profile/SAML2/Redirect/SLO",
            "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
        },
        "x509certMulti": {
            "signing": [
                "MIID...vg=="
            ],
            "encryption": [
                "MIID...dw=="
            ]
        }
    }
}
```

I didn't need to configure anything additional in `advanced-settings.json`. However, the metadata file expires in 2 days by default. If you don't want to keep regenerating it you can add this key-value pair to this file:

```json
{
    "security": {
        // ...
        // Replace with an appropriate timestamp e.g. "2015-01-01T20:00:00Z"
        "metadataValidUntil": null
        //...
    }
}

```

Next, we need to generate a private key and its corresponding self-signed certificate for our SP application. Navigate to `demo-flask/saml/certs` and run the following command:
```bash
openssl req -new -x509 -days 3652 -nodes -out sp.crt -keyout sp.key
```

## Adding a trust relationship in Gluu Server
For the next step, we will need to obtain the Flask application's metadata XML file. In the `demo-flask` folder, execute `python index.py`. This should load the settings file and start the Flask application. Navigate to `http://localhost:8000` on your web browser and you should see the following screen:

![onelogin homepage]()

Now, navigate to `http://localhost:8000/metadata/` and you should see an XML file. Save it to your local storage. Then, log on to your Gluu server's oxTrust GUI and navigate to `SAML` > `Add Trust Relationships`. Use the following details:

- `Display Name`: choose an appropriate name
- `Description`: any description
- `Entity type`: Single SP
- `Metadata Location`: File
- `Sp Metadata File`: The file you just downloaded from the Flask application
- `SP Logout URL`: leave as blank
- Click on the check mark next to `Configure Relying Party` and click on the button that shows up.
    - Under `Available Profile Configurations`, click on `SAML2SSO` and click Add.
    - A new menu named `SAML2 SSO Profile` will show up. Click on it to expand.
    - `assertionLifetime`: 300000
    - `signResponses`: always
    - `signAssertions`: never
    - `signRequests`: conditional
    - `encryptAssertions`: always
    - `encryptNameIds`: always
    - `Default Authn Methods`: `urn:oasis:names:tc:SAML:2.0:ac:classes:Password`
    - `IncludeAttributeStatement`: Yes
    - `Support Unspecified NameIdFormat?`: Yes
    - Under Available NameID Formats, select `SAML:2.0:nameid-format:transient` and click add
    - Click Save
- Now you need to release additional attributes from the right hand side pane. Click on an attribute to release it to the SP. For this example we will release Username, Email and TransientID. 
- Finally, click `Add` and then `Activate`. It will take a few minutes for Shibboleth to load your new trust relationship, so please wait.


## Testing SP initiated flow
With everything set up, start the Flask application and navigate to `http://localhost:8000`. You should see the login screen as mentioned before. Click on `Login` and you should be redirected to your Gluu server's oxAuth login page.

![gluu-login]()

Now you can log in with your Gluu server user credentials. If everything runs okay, you will be redirected back to the Flask application which will display the attributes you released.

![flask-attributes]()

## References
- [Gluu 4.4 Documentation](https://gluu.org/docs/gluu-server/4.4/)
- [SP initiated SAML flow tutorial](https://github.com/GluuFederation/tutorials/blob/master/oidc-sso-tutorials/tutorials/SAML-SSO-with-Gluu-Shibboleth-SP-Initiated-Flow.md) by [kdhttps](https://github.com/kdhttps)
- [Securing the Perimeter](https://www.amazon.com/Securing-Perimeter-Deploying-Identity-Management/dp/1484226003) by Michael Schwartz