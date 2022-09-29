# Dynamic Client Registration with Software Statements

## Introduction
[Dynamic Client Registration](https://www.rfc-editor.org/rfc/rfc7591.html) is an important feature of OAuth2, where a developer may register their client with an authorization server directly, with no intervention from the server administrator. This allows developers to quickly deploy applications, and eliminates the burden of manually configuring a client for each application. 

## Software Statements
During dynamic client registration, one of the allowed types of client metadata that is sent to the authorization server is the software statement. This is a JSON Web Token that contains information about the client as a bundle, and is issued by an external party. An example of this would be a developer obtaining a software statement from an API publisher for their class of clients. Software statements are generally signed by the issuer, which allows cryptographic validation. A non-normative example of a software statement is as follows:

```json
{
    "software_id": "4NRB1-0XZABZI9E6-5SM3R",
    "client_name": "Example Statement-based Client",
    "client_uri": "https://client.example.net/"
}
```
This is then digitally signed with a cryptographic algorithm, usually RS256, and converted to a base64-encoded string which is then given to the developer. The developer then submits this string to the authorization server alongside the client registration request.

## Gluu Openbanking
An example of this use case would be the [Gluu Open Banking Identity Platform](https://gluu.org/openbanking/), which allows dynamic client registration via software statements. This distribution of Gluu is based on the Janssen Project at the Linux Foundation, which is a fork of Gluu Server 4, a [certified](https://openid.net/certification) OpenID Platform. Gluu Server allows modification of the dynamic client registration flow via interception scripts, which can be used to implement custom business logic. For instance, data could be validated, extra client claims could be populated, scopes could be modified, or APIs could be called to determine whether the client should get registered at all. 

In this flow, the developer obtains a software statement from the Openbanking Directory, then sends the software statement to register their client application. The authorization server runs the [interception script](https://gluu.org/docs/openbanking/scripts/client-registration/) to validate the software statement and provide client credentials. These are then used to obtain access tokens and call APIs. The full flow is as follows:

![openbanking-flow](https://gluu.org/docs/openbanking/img/PKI_Infra.png)

For more information, please refer to the [Gluu Openbanking Documentation](https://gluu.org/docs/openbanking/).