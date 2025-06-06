import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.scss';
import App from './App';
import reportWebVitals from './reportWebVitals';

import {AuthProvider, AuthProviderProps} from "react-oidc-context";
import {library} from '@fortawesome/fontawesome-svg-core'
import {fas} from '@fortawesome/free-solid-svg-icons'
import {Log, User} from 'oidc-client-ts';

import {BrowserRouter} from "react-router-dom";

library.add(fas);
Log.setLogger(console);


const oidcConfig: AuthProviderProps = {
    authority: window.REACT_APP_OIDC_REALM,
    client_id: window.REACT_APP_OIDC_CLIENT_ID,
    redirect_uri: window.REACT_APP_OIDC_REDIRECT_URI,
    scope: window.REACT_APP_OIDC_SCOPE,
    post_logout_redirect_uri: window.REACT_APP_OIDC_REDIRECT_URI,
    automaticSilentRenew: true,
    onSigninCallback: async (user: User | undefined) => {
        if (user) {
            window.history.replaceState({}, document.title, window.location.pathname);
        }
    },
};

const root = ReactDOM.createRoot(
    document.getElementById('root') as HTMLElement
);
root.render(
    <React.StrictMode>
        <AuthProvider {...oidcConfig}>
            <BrowserRouter basename={window.PUBLIC_URL}>
            <App/>
            </BrowserRouter>
        </AuthProvider>
    </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
