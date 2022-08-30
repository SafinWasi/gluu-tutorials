# Integrating Gluu Server with Tru ID

## Introduction

It's a modern axiom that passwords are bad. But there are still many deployment challenges for organizations to rollout two-factor authentication, such as requiring end users to purchase hardware or install a special app on their smart phone. [tru.ID](https://tru.id/) has developed a technology that enables organizations to verify that a data connection associated with a SIM card is associated with the person's phone number. The advantage of this strategy is that nothing special is needed by the end user. They can use their mobile web browser and any QR scanner, now built-in to most camera apps. In order for this to work, the end user may have to switch-off their WiFi--tru.ID needs a data connection from the telco.

This article will demonstrate how to use [tru.ID](https://github.com/tru-ID/oidc-bridge) with [Gluu Server CE 4.4.1](https://gluu.org/), your favorite open source digital identity platform. In our sample flow, the first factor (something you know) is username/password. The second factor (something you have) is obtained via tru.ID's PhoneCheck API, which verifies possession of the SIM card associated with the phone number.

In our demo setup, we are using a sample `oidc-bridge` provided by tru.ID, which runs as a separate service/container.

The sequence diagram for the flow is as follows:

![service-diagram](https://raw.githubusercontent.com/tru-ID/oidc-bridge/main/integration-gluu/gluu-truid-authentication-flow.png)

## Authentication Flow

1. The user navigates to the sample application and clicks `Login`.

![tru-login.png](../assets/tru-id/tru-login.png)

2. Then user's browser is redirected to the Gluu Server `/authorize` endpoint as you'd expect in an OpenID Connect code flow

![gluu-login.png](../assets/tru-id/gluu-login.png)

3. After authentication, they are redirected back to the application, where the call to the PhoneCheck API is made. Another option is to call the PhoneCheck API in step 2 of the Gluu Server interception script. We may provide this later...stay tuned.

4. The end user scans a QR code displayed by the demo application:

![qr-code.png](../assets/tru-id/qr-code.png)

5. On the phone, the QR code resolves to a URL. The end user may be asked to turn off WiFi for network verification.

![wifi.png](../assets/tru-id/wifi.png)

6. Then they are shown a consent screen to allow verification for the web application.

![request.png](../assets/tru-id/request.png)

7. Upon allowing access on the phone, the browser logs in to the application.

![logged-in.png](../assets/tru-id/logged-in.png)

## How to setup

tru.ID already has a detailed guide on [how to set up integration with Gluu Server](https://github.com/tru-ID/oidc-bridge/tree/main/integration-gluu#readme), with their `oidc-bridge` sample application as the example.
