# IDP initiated SAML flow for Gluu Solo

This article will guide you through the process of an Identity Provider (IDP) initiated SAML flow for Single Sign On using Gluu as the Identity Provider (IDP). This is a niche use case, and unless you explicitly need support for this, you should use an [SP initiated flow](https://github.com/SafinWasi/gluu-tutorials/blob/master/docs/gluu-saml-sso-sp.md).

## Introduction
In an IDP initiated SAML flow, the IDP sends an unsolicited SAML response to the SP, without the SP having to request anything. In this sort of flow, the URL usually contains the `unsoliticed` keyword. There are some use cases for this, primarily for compatibility with legacy systems. A banking site may use an external service to handle foreign currencies. The customer clicks on a link that takes them to an external website to buy foreign currencies. In this case, an unsolicited SAML response is created by the IDP (banking site) and sent to the third party SP (foreign currency site) which can validate the assertion and provide the service.

However, there are drawbacks to this. When an SP receives an unsolicited SAML response, it has no idea where to redirect the user after validation. This would require manual configuration for every incoming unsolicited SAML response, which reduces interoperability. IDP initiated flow has been depracated in OAuth and OpenID connect using the state parameter.

## Requirements
- Completion of the [SP initiated flow tutorial](https://github.com/SafinWasi/gluu-tutorials/blob/master/docs/gluu-saml-sso-sp.md) 
**OR**
- Completion of the [AWS integration tutorial](https://gluu.org/docs/gluu-server/4.4/integration/saas/aws/).

## Procedure

If you are using the SP initiated flow tutorial:
1. Open the `metadata.xml` from the SP initiated flow tutorial
2. Replacing `<sp entity ID>` with the `<entityId>` value from the file, visit `https://<hostname>/idp/profile/SAML2/Unsolicited/SSO?providerId=<sp entity ID>`. For us, the URL turned out to be `https://<hostname>/idp/profile/SAML2/Unsolicited/SSO?providerId=https://localhost:5000/metadata/`.
3. Log in to oxTrust with your Gluu credentials
4. That's it. You should be able to see the released attributes.

If you are using AWS integration:
1. Visit `https://<hostname>/idp/profile/SAML2/Unsolicited/SSO?providerId=urn:amazon:webservices`. In this case, the Gluu server sends an unsolicited SAML response to AWS releasing the custom attributes that we already configured, allowing you to use single sign on. 

## References
- [Gluu 4.4 Documentation](https://gluu.org/docs/gluu-server/4.4/)
- [IDP initiated SAML flow tutorial](https://github.com/GluuFederation/tutorials/blob/master/oidc-sso-tutorials/tutorials/SAML-SSO-with-Gluu-Shibboleth-IDP-Initiated-Flow.md) by [kdhttps](https://github.com/kdhttps)
- [Securing the Perimeter](https://www.amazon.com/Securing-Perimeter-Deploying-Identity-Management/dp/1484226003) by Michael Schwartz