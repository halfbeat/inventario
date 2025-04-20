import {withAuthenticationRequired} from "react-oidc-context";
import React from "react";
import {Link, useParams} from "react-router-dom";
import {SistemaHeader} from "./SistemaHeader";
import {ComponenteSistema} from "../componentes/ComponenteSistema";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";


const EdicionComponenteSistemaPage = () => {
    let params = useParams();
    return (
        <>
            <SistemaHeader/>
            <div className={"text-end mb-1"}>
                <Link className={"btn btn-primary btn-sm"} to={`/sistemas/${params.sistema_id}/componentes`}><FontAwesomeIcon icon={"arrow-left"}/> Volver</Link>
            </div>
            <ComponenteSistema sistemaId={params.sistema_id} componenteId={params.componente_id}/>
        </>

    )
}


export default withAuthenticationRequired(EdicionComponenteSistemaPage, {
    OnRedirecting: () => (<div>Redirecting to the login page...</div>)
});