# Security

Lungo prioritizes security and employs various measures to minimize the attack surface. The following outlines
implemented security measures:

- HTTPS is enabled by default, and all HTTP requests are redirected to HTTPS.
- CSRF protection is enabled for identity-related endpoints.
- Rate limiting can be configured for identity-related endpoints.
- Cookies are configured to be secure and HTTP-only whenever possible, and the `SameSite` attribute is set to `Lax`.
- Cookies set by different application backend are isolated from each other by the `Path` attribute.
- Security-related headers are set to sensible values, including cross-origin resource policy, frame options, and more.
