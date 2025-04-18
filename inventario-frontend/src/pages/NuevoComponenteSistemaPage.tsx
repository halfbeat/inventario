import {withAuthenticationRequired} from "react-oidc-context";
import React from "react";
import {useParams} from "react-router-dom";
import {SistemaHeader} from "./SistemaHeader";
import {ComponenteSistema} from "../componentes/ComponenteSistema";


const NuevoComponenteSistemaPage = () => {
    let params = useParams();
    return (
        <>
            <SistemaHeader/>
            <ComponenteSistema sistemaId={params.sistema_id} componenteId={undefined}/>
        </>

    )
}


export default withAuthenticationRequired(NuevoComponenteSistemaPage, {
    OnRedirecting: () => (<div>Redirecting to the login page...</div>)
});