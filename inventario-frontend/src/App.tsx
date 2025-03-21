import React from 'react';
import './App.scss';
import {useAuth} from "react-oidc-context";
import {AnonymousApp} from "./AnonymousApp";
import {AutenticatedApp} from "./AutenticatedApp";

function App() {
    const auth = useAuth();

    switch (auth.activeNavigator) {
        case "signinSilent":
            return <div>Signing you in...</div>;
        case "signoutRedirect":
            return <div>Signing you out...</div>;
    }

    if (auth.isLoading) {
        return <div>Loading...</div>;
    }

    if (auth.error) {
        return (<AnonymousApp/>);
    }

    if (auth.isAuthenticated) {
        return (
            <AutenticatedApp/>
        );
    }

    return (<AnonymousApp/>);
}

export default App;
