var Configuration = {
    prop1: "abcde",
    prop2: "123",
    oidc: {
        realm: process.env.REACT_APP_OIDC_REALM,
        client_id: process.env.REACT_APP_OIDC_CLIENT_ID,
        redirect_uri: process.env.REACT_APP_OIDC_REDIRECT_URI,
        scope: process.env.REACT_APP_OIDC_SCOPE,
        post_logout_redirect_uri: process.env.REACT_APP_OIDC_REDIRECT_URI,
    },
    backend: {
        baseUrl: process.env.REACT_APP_BACKEND_BASE_URL,
    }
};
exports.Configuration = Configuration;