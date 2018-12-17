### Delegation of Authentication Extension (delegation)

This extension allows one Client to create a token that can be used by a third-party (here called the Delegate) to gain authenticate to the Relying Party. The Delegate is a WebAuthn Client that may be either owned by the same user or may be owned by another trusted party. This allows behavior similar to "password-sharing" for WebAuthn without proceeding through the Registration Flow once for each Relying Party and Client pair. The Client can also place contraints on the Delegate using this extension. The new flexibility also allows for recovery flows that are more efficient.

#### Extension identifier

​	delegation

#### Operation applicability

​	Registration

#### Client extension input

The Boolean value `true` to indicate that this extension is supported by the Relying Party.

```web-idl
partial dictionary AuthenticationExtensionsClientInputs {
  boolean delegation;
};
```

#### Client extension processing

If the client wishes to produce a delegatable credential, perform the following steps:

1. Let `delegation` be a `DelegationExtensionOutputs` with `action = "create"`
2. Let `delegation.use = null`
3. Let `delegation.create` be a non-null  `DelegationCreationOptions`.
   1. Let `delegation.create.options.user` be the `PublicKeyCredentialUserEntity` from the Relying Party's `PublicKeyCredentialCreationOptions
   2. Let `delegation.create.options.expiration` reflect how long to allow the credential to work. A null value signifies no expiration policy.
   3. Let `delegation.create.options.uses` reflect how many times the credential should work. A null value signifies no limit in uses.
   4. Let `delegation.create.options.allowCredentials` reflect any pubkeys that are allowed. If null, then all credentials are allowed.
   5. Let `delegation.create.serializedOptions` be a JSON serialization of `delegation.create.options`.
4. Let `secret` be a random byte array. The `secret` MAY be generated from a cryptographically secure random number generator. The `secret` also MAY be generated as the output of a Key Derivation Function. 
5. Let `delegation.create.challenge` be `SHA-256-HMAC(delegation.create.serializedOptions, secret)`
6. Store or transfer `secret` in a trusted manner. The encoding and means of communication are not specified by this document.
7. Return `delegation`.

If the client wishes to use a delegatable credential, perform the following steps:

1. Let `delegation` be a `DelegationExtensionOutputs` with `action = "use"`.
2. Let `delegation.create = null`.
3. Obtain the `secret` used when processing this extension at registration, and store it in `delegation.use.response`. If this fails, return an error.
4. Return `delegation`.

If the client wishes to do neither, the client should not process this extension. If it is being processed, then return an "`AbortError`" `DOMException`.

#### Client extension output

```web-idl
enum DelegationIdentifier { "create", "use" };

dictionary DelegationCreationOptions {
	PublicKeyCredentialUserEntity user;
	unsigned long long? expiration = null;	
	unsigned long? uses = 1;
    sequence<PublicKeyCredentialDescriptor>? allowCredentials = [];
}

dictionary DelegationCreation {
    BufferSource challenge;
    DelegationCreationOptions options;
    ArrayBuffer serializedOptions;
}

dictionary DelegationUse {
    BufferSource response;
}

dictionary DelegationExtensionOutputs {
    DelegationIdentifier action;
    DelegationCreationOptions? create;
    DelegationUse? use;
}

partial dictionary AuthenticationExtensionsClientOutputs {
  DelegationExtensionOutputs delegation;
};
```



#### Relying Party extension validation

All failed verifications MUST return an error.

If `delegation.action = "create"`:

1. Verify `delegation.create` is non-null.
2. Verify `delegation.create.serializedOptions` when deserialized is equivalent to `delegation.create.options`.
3. Verify that the `delegation.create.options.user` value is equal to the `user` field in the sent `PublicKeyCredentialCreationOptions`.
4. If the authentication suceeds, the Relying Party SHOULD store `delegation.create` until `expiration` milliseconds after the UNIX epoch and with associated data of the number of uses. The Relying Party MUST NOT store `delegation.create`  if authentication fails.
5. Return success.

If `delegation.action = "use"`:

1. Verify `delegation.use` is non-null
2. For all `DelegationCreation` objects associated with the current connection's user handle, `create` (on failed verification continue the loop):
   1. Verify that `create.expiration` is less than the number of milliseconds since the UNIX epoch.
   2. Verify that the associate use counter with this `DelegationCreation` is not equal to or greater than the number of allowed uses.
   3. If `create.allowCredentials` is not null, then verify that the public key of the Delegate's `authenticatorData` is in the sequence.
   4. Verify that `SHA-256-HMAC(create.serializedOptions, create.challenge) = delegation.use.response`
   5. Increment the number of uses for this `DelegationCreation`. 
   6. Return success.
3. Return an error.

#### Authenticator extension input

None.

#### Authenticator extension processing

None.

#### Authenticator extension output

None.

