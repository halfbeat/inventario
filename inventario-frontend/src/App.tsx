import React from 'react';
import './App.scss';
import {useAuth} from "react-oidc-context";
import {Layout} from "./layout/Layout";
import {useNavigate} from "react-router-dom";
import {Configuration} from './Configuration'

function App() {
    const auth = useAuth();
    const navigate = useNavigate();

    auth.events.addSilentRenewError(() => console.log('Silent Renew Error'));
    auth.events.addAccessTokenExpiring(() => console.log('Access Token Expiring'));
    auth.events.addSilentRenewError(() => {
        console.log(`Silent Renew Error. Redirecting to sistema ${Configuration.baseUrl}/session-expired`);
        auth.signoutRedirect({
            id_token_hint: auth.user?.id_token,
            post_logout_redirect_uri: `${Configuration.baseUrl}/session-expired`
        })
    });
    auth.events.addUserLoaded(() => console.log('User Loaded'));
    auth.events.addUserSessionChanged(() => console.log('Session Changed'));
    auth.events.addUserUnloaded(() => console.log('User Unloaded'));
    auth.events.addUserSignedIn(() => console.log('User Signed in'));
    auth.events.addUserSignedOut(() => console.log('User Signed Out'));
    auth.events.addAccessTokenExpired(() => console.log('Access Token Expired'));

//    useEffect(() => {
//        if (auth.isAuthenticated) {
//            const handle = setInterval(() => {
//                auth.signinSilent();
//            }, tokenRenewalInterval);
//            return () => clearInterval(handle);
//        }
//    }, [auth, tokenRenewalInterval]);
//    useEffect(() => {
//
//      if (auth.isAuthenticated) {switch (auth.activeNavigator) {
//        case "signinSilent":
//        const handle = setInterval(() => {        return <div>Signing you in...</div>;
//        case "signoutRedirect":
//          auth.signinSilent();        return <div>Signing you out...</div>;
//    }
//        }, tokenRenewalInterval);
//    if (auth.isLoading) {
//        return <div>Loading...</div>;
//        return () => clearInterval(handle);}
//
//      }
//    return (<Layout/>);
//}   }, [auth, tokenRenewalInterval]);

    return (<Layout/>);
}

export default App;
