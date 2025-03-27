import React, {useEffect, useState} from "react";
import {useAuth, withAuthenticationRequired} from "react-oidc-context";
import {Api, ApiConfig, ListadoPaginadoSistemasDto, RequestParams} from "../openapi/api";
import {Configuration} from '../Configuration'
import {Link} from "react-router-dom";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";

const ListadoSistemas = () => {
    const auth = useAuth();
    const [sistemas, setSistemas] = useState({} as ListadoPaginadoSistemasDto);
    const token = auth.user?.access_token;
    const rp = {headers: {Authorization: `Bearer ${token}`}} as RequestParams
    const api = new Api({
        baseUrl: Configuration.backend.baseUrl,
        baseApiParams: rp
    } as ApiConfig);
    useEffect(() => {
        if (token) {
            api.sistemas.getSistemasInformacion()
                .then(res => res.data)
                .then(data => {
                    setSistemas(data);
                })
                .catch(err => console.error(err));
        }
    }, [token]);

    const listaSistemas = sistemas?.items?.map(s =>
        <li key={s.sistema_id}>
            <Link to={s.sistema_id}>{s.nombre}</Link>
        </li>)
    return (
        <div>
            <p className={"h4 border border-2 rounded p-2"}>Sistemas registrados</p>
            <ul>{listaSistemas}</ul>
            <p hidden={sistemas?.total !== 0}>No se ha encontrado ningún sistema</p>
            <div className={"text-end mt-3"}>
                <Link className={"btn btn-primary"} to={"registro"}><FontAwesomeIcon icon={"plus"}/> Registrar
                    sistema</Link>
            </div>
        </div>
    )
}

export default withAuthenticationRequired(ListadoSistemas, {
    OnRedirecting: () => (<div>Redirecting to the login page...</div>)
});