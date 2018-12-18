---
layout: blog
permalink: /posts/:title:output_ext
title: Proposed Extension to WebAuthn
tags: [authentication, standards, webauthn]
---

WebAuthn seems like as powerful a contender to replace passwords as I have seen in my brief experience. I think it is really cool, but suspect that minor rough spots of usability will be huge sticking points with broad adoption. One spot I see is that people often share credentials for very reasonable reasons (shared accounts and needing emergency access to name a couple). This doesn't seem possible in the context of WebAuthn as designed, but luckily it allows extensions!

[Here is my draft extension.](/files/delegation.markdown)

Something else I realized while drafting it- this allows for the creation of backup tokens that can be created at registration time and dumped en-masse with no user overhead.

Disclaimer: I am not a cryptographer, so who knows what evil lurks within. But there isn't moon-math or anything too exotic here. 

The rough cut is as follows: when a client is registering a new key with the server, it also has the key sign a value that is HMAC(restrictions, secretKey). The HMAC and restrictions are shipped off for the server to hold onto. Now anyone that can prove ownership of the secretKey within the restrictions can register a new key with that account. For now these restrictions are how long the token should last, how many uses it gets, and what public keys work with it. Broadly, this is a tool to create trusted tokens that exist off of the Yubikey you may be using day-to-day, bootstrapping trust from registration.
