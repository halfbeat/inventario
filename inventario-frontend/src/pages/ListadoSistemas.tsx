import React, {useEffect, useState} from "react";
import {useAuth} from "react-oidc-context";
import {Api, ApiConfig, ListadoPaginadoSistemasDto, RequestParams} from "../openapi/api";
import {Configuration} from '../Configuration'
import {Link} from "react-router-dom";
import {Button} from "react-bootstrap";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";

export function ListadoSistemas() {
    const auth = useAuth();
    const [sistemas, setSistemas] = useState({} as ListadoPaginadoSistemasDto);
    const token = auth.user?.access_token;
    const rp = {headers: {Authorization: `Bearer ${token}`}} as RequestParams
    const api = new Api({
        baseUrl: Configuration.backend.baseUrl,
        baseApiParams: rp
    } as ApiConfig);
    useEffect(() => {
        api.sistemas.getSistemasInformacion()
            .then(res => res.data)
            .then(data => {
                setSistemas(data);
            })
            .catch(err => console.error(err));
    }, []);

    const listaSistemas = sistemas?.items?.map(s =>
        <li>
            <Link to={s.sistema_id}>{s.nombre}</Link>
        </li>)
    return (
        <div>
            <h1 className={"h5"}>Sistemas registrados</h1>
            <hr/>
            <ul>{listaSistemas}</ul>
            <p hidden={sistemas?.total != 0}>No se ha encontrado ningún sistema</p>
            <Link className={"float-end btn btn-primary btn-sm"} to={"registro"}><FontAwesomeIcon icon={"plus"}/> Registrar
                sistema</Link>
        </div>
    )
}