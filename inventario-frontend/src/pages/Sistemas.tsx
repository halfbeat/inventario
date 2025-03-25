import React, {useEffect, useState} from "react";
import {useAuth} from "react-oidc-context";
import {Api, ApiConfig, ListadoPaginadoSistemasDto, RequestParams} from "../openapi/api";
import {Configuration} from '../Configuration'

export function Sistemas() {
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
    return (
        <div>
            <h1 className={"display-6"}>Sistemas registrados</h1>
            <hr/>
            {sistemas?.items?.length}
        </div>
    )
}